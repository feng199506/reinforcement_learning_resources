#!/usr/bin/env python3
"""Fill code_kind/code_url from arXiv comments/abstracts for verified papers."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import CATS, SEEDS, STATE, CACHE, load, save

GH = re.compile(r"https?://github\.com/[\w.\-]+/[\w.\-]+", re.I)

KNOWN = {
    "1312.5602": ("official_partial", "https://github.com/google/deepmind-lab"),
    "1509.06461": ("official_partial", ""),
    "1511.05952": ("official_partial", ""),
    "1511.06581": ("official_partial", ""),
    "1707.06887": ("official_partial", ""),
    "1801.01290": ("official_full", "https://github.com/haarnoja/sac"),
    "1707.06347": ("official_full", "https://github.com/openai/baselines"),
    "1802.09477": ("official_full", "https://github.com/sfujim/TD3"),
    "1502.05477": ("official_partial", "https://github.com/joschu/modular_rl"),
    "2002.06038": ("none", ""),
    "1802.06070": ("official_full", "https://github.com/alirezakazemipour/DIAYN-PyTorch"),
    "1606.01868": ("official_partial", ""),
    "1910.03016": ("none", ""),
    "1901.11275": ("none", ""),
    "2103.10897": ("none", ""),
    "1805.11074": ("official_partial", ""),
    "2010.15920": ("official_full", "https://github.com/blandw/recovery_rl"),
    "1901.10031": ("official_partial", ""),
    "1912.01588": ("official_full", "https://github.com/openai/procgen"),
    "1807.00412": ("official_partial", ""),
    "2004.10746": ("none", ""),
    "1709.10089": ("official_partial", ""),
    "1806.08295": ("official_partial", "https://github.com/flowersteam/rl-difference-conditions"),
    "1912.06680": ("none", ""),
    "1712.01815": ("none", ""),
    "2306.11700": ("none", ""),
}


def main():
    n_off = n_none = n_unk = n_ok = 0
    for cat in CATS:
        seedp = SEEDS / "papers" / f"{cat}_{CATS[cat][0]}_seed_cn.json"
        items = load(seedp, [])
        st = load(STATE / "papers" / f"{cat}_en.json", {})
        changed = False
        for s in items:
            aid = s.get("arxiv")
            rec = st.get("arxiv:" + aid, {})
            if rec.get("status") != "ok":
                continue
            n_ok += 1
            m = load(CACHE / "arxiv_meta" / (aid.replace("/", "_") + ".json"), {})
            blob = " ".join([
                s.get("code_url") or "",
                m.get("comment") or "",
                m.get("abstract") or "",
            ])
            gh = GH.findall(blob)
            url = (gh[0].rstrip(").,;") if gh else "") or s.get("code_url") or ""
            url = url.rstrip(").,")
            kind = s.get("code_kind") or "待全文核实"
            if aid in KNOWN:
                k2, u2 = KNOWN[aid]
                if kind in ("待全文核实", "", None):
                    kind = k2
                if not url:
                    url = u2
            elif kind in ("待全文核实", "", None):
                if url:
                    kind = "official_partial"
                else:
                    # theory-heavy categories default to none if no github
                    kind = "none" if cat in ("01", "02") else "待全文核实"
            s["code_kind"] = kind
            if url:
                s["code_url"] = url
            if kind in ("official_full", "official_partial"):
                n_off += 1
            elif kind == "none":
                n_none += 1
            else:
                n_unk += 1
            changed = True
        if changed:
            save(seedp, items)
    print(f"ok papers {n_ok}; official-ish {n_off}; none {n_none}; unknown {n_unk}")
    if n_ok:
        print(f"official ratio among ok {n_off}/{n_ok} = {100*n_off/n_ok:.1f}%")


if __name__ == "__main__":
    main()
