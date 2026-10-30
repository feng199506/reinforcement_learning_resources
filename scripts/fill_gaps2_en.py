#!/usr/bin/env python3
"""Reject off-topic IDs from fill_gaps_en.py and queue title-verified replacements."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import CATS, ROOT, STATE, SEEDS, WORK, save, load

JUNK = {
    "01": ["2007.02811", "1906.04711"],
    "05": ["1812.05951"],
    "10": ["1910.01798", "1805.11091", "2102.08915"],
    "11": ["2103.07579"],
    "13": ["1603.06155", "1810.01959"],
    "14": ["1812.11711"],
}
REPL = {
    "01": [
        ("1910.03016", "线性表示样本效率", "Is a Good Representation Sufficient for Sample Efficient RL"),
        ("1901.11275", "正则化MDP", "A Theory of Regularized Markov Decision Processes"),
    ],
    "05": [
        ("1802.06070", "DIAYN", "Diversity is All You Need"),
    ],
    "10": [
        ("1805.11074", "RCPO", "Reward Constrained Policy Optimization"),
        ("2010.15920", "RecoveryRL", "Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones"),
        ("1901.10031", "Lyapunov安全策略", "Lyapunov-based Safe Policy Optimization for Continuous Control"),
    ],
    "11": [
        ("1912.01588", "Procgen", "Leveraging Procedural Generation to Benchmark Reinforcement Learning"),
    ],
    "13": [
        ("1807.00412", "自动驾驶", "Learning to Drive in a Day"),
    ],
    "14": [
        ("1806.08295", "多种子", "How Many Random Seeds? Statistical Power Analysis in Deep RL"),
    ],
}


def main():
    rej = WORK / "rejected"
    rej.mkdir(parents=True, exist_ok=True)
    for cat, ids in JUNK.items():
        st_path = STATE / "papers" / f"{cat}_en.json"
        st = load(st_path, {})
        seedp = list((SEEDS / "papers").glob(f"{cat}_*_seed_cn.json"))[0]
        items = json.loads(seedp.read_text())
        keep = []
        for s in items:
            aid = s.get("arxiv")
            k = "arxiv:" + aid
            if aid in ids:
                rec = st.get(k, {})
                rec["status"] = "rejected"
                rec["note"] = "人工拒收：arXiv 编号对应论文与拟收强化学习主题不符（标题检索已核对）"
                p = rec.get("path") or ""
                if p and (ROOT / p).exists():
                    shutil.move(str(ROOT / p), str(rej / Path(p).name))
                    rec["path"] = ""
                st[k] = rec
                print("rejected", cat, aid)
            else:
                keep.append(s)
        seedp.write_text(json.dumps(keep, ensure_ascii=False, indent=1))
        save(st_path, st)

    for cat, rows in REPL.items():
        seedp = list((SEEDS / "papers").glob(f"{cat}_*_seed_cn.json"))[0]
        items = json.loads(seedp.read_text())
        have = {x.get("arxiv") for x in items}
        for aid, sub, reason in rows:
            if aid in have:
                continue
            items.append({
                "arxiv": aid, "subtopic": sub, "type": "原始研究论文",
                "level": "硕士/博士", "difficulty": "中级",
                "reason": reason,
                "summary": "", "summary_basis": "arXiv 摘要（下载后登记）",
                "code_kind": "待全文核实", "task": CATS[cat][1],
            })
            print("queued", cat, aid, sub)
        seedp.write_text(json.dumps(items, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
