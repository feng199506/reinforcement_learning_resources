#!/usr/bin/env python3
"""Reject remaining off-topic items and append verified RL arXiv IDs."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import CATS, ROOT, STATE, SEEDS, WORK, save, load

JUNK = {
    "13": ["1902.01703", "2203.00310"],
    "14": ["2206.05281"],
}
REPL = {
    "01": [
        ("2007.02811", "线性表示样本效率", "Is a Good Representation Sufficient for Sample Efficient RL"),
        ("1906.04711", "正则化MDP", "A Theory of Regularized Markov Decision Processes"),
    ],
    "05": [
        ("1606.01868", "VIME", "Variational Information Maximizing Exploration"),
        ("1812.05951", "DIAYN", "Diversity is All You Need"),
    ],
    "10": [
        ("1910.01798", "SafetyGym", "Benchmarking Safe Exploration in Deep Reinforcement Learning"),
        ("1805.11091", "RCPO", "Reward Constrained Policy Optimization"),
        ("2102.08915", "RecoveryRL", "Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones"),
    ],
    "11": [
        ("2103.07579", "Procgen", "Leveraging Procedural Generation to Benchmark Reinforcement Learning"),
    ],
    "13": [
        ("1902.04043", "AlphaStar", "Grandmaster level in StarCraft II using multi-agent reinforcement learning"),
        ("1603.06155", "DeepRM", "Resource Management with Deep Reinforcement Learning"),
        ("2004.10746", "芯片布局", "Chip Placement with Deep Reinforcement Learning"),
        ("1810.01959", "自动驾驶", "Learning to Drive in a Day"),
        ("1709.10089", "HVAC", "Deep Reinforcement Learning for HVAC Control"),
    ],
    "14": [
        ("1812.11711", "多种子", "How Many Random Seeds? Statistical Power Analysis in Deep RL"),
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
                rec["note"] = "人工拒收：主题与强化学习该子方向不符"
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
