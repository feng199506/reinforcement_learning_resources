#!/usr/bin/env python3
"""Reject off-topic downloads whose arXiv IDs did not match the intended RL papers."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import CATS, ROOT, STATE, SEEDS, WORK, save, load

JUNK = {
    "01": ["2106.08005", "2205.10821", "2301.08252"],
    "02": ["1703.05426"],
    "05": ["2004.12277", "2303.11103"],
    "08": ["2301.00704"],
    "10": ["1910.12708", "2102.09079", "2303.03231", "2404.04710"],
    "11": ["2312.05253", "2402.19402"],
    "13": ["1902.01714", "2103.11972", "2509.23791"],
}
REPL = {
    "01": ["2103.10897"],
    "02": ["1703.05449"],
    "05": ["2002.06038"],
    "08": ["1910.09508"],
    "10": ["2310.12567"],
    "11": ["1806.10729"],
    "13": ["1902.01703"],
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
                rec["note"] = "人工拒收：arXiv 编号与拟收强化学习论文不符"
                p = rec.get("path") or ""
                if p and (ROOT / p).exists():
                    shutil.move(str(ROOT / p), str(rej / Path(p).name))
                    rec["path"] = ""
                st[k] = rec
                print("rejected", cat, aid)
            else:
                keep.append(s)
        have = {x.get("arxiv") for x in keep}
        for aid in REPL.get(cat, []):
            if aid not in have:
                keep.append({
                    "arxiv": aid, "subtopic": "补缺", "type": "原始研究论文",
                    "level": "硕士/博士", "difficulty": "中级",
                    "reason": "替换无关条目后的主题匹配补缺。",
                    "summary": "", "summary_basis": "arXiv 摘要（下载后登记）",
                    "code_kind": "待全文核实", "task": CATS[cat][1],
                })
                print("queued", cat, aid)
        seedp.write_text(json.dumps(keep, ensure_ascii=False, indent=1))
        save(st_path, st)


if __name__ == "__main__":
    main()
