#!/usr/bin/env python3
"""Look up arXiv IDs by title via the Atom API."""
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from papers_en import API, parse_entries, http

TITLES = [
    'Is a Good Representation Sufficient for Sample Efficient Reinforcement Learning',
    'A Theory of Regularized Markov Decision Processes',
    'Diversity is All You Need: Learning Skills without a Reward Function',
    'Benchmarking Safe Exploration in Deep Reinforcement Learning',
    'Reward Constrained Policy Optimization',
    'Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones',
    'Leveraging Procedural Generation to Benchmark Reinforcement Learning',
    'Resource Management with Deep Reinforcement Learning',
    'Learning to Drive in a Day',
    'How Many Random Seeds? Statistical Power Analysis in Deep Reinforcement Learning Experiments',
    'A Comprehensive Survey of Safe Reinforcement Learning',
    'Safe Reinforcement Learning: A Survey',
    'Constrained Policy Optimization',
    'Lyapunov-based Safe Policy Optimization for Continuous Control',
    'A Review of Safe Reinforcement Learning: Methods, Theory and Applications',
    'Procgen Benchmark',
    'The Distracting Control Suite',
    'Quantifying Generalization in Reinforcement Learning',
    'A Survey on Transfer Learning in Reinforcement Learning',
    'Empirical Design in Reinforcement Learning',
    'Reproducibility of Benchmarked Deep Reinforcement Learning Tasks',
    'Deep Reinforcement Learning that Matters',
    'Statistical Power Analysis in Deep Reinforcement Learning',
    'How many random seeds should you use',
    'AlphaStar: Grandmaster level in StarCraft II',
    'Chip Placement with Deep Reinforcement Learning',
    'A Lyapunov-based Approach to Safe Reinforcement Learning',
    'Conservative Safety Critics for Exploration',
]


def main():
    for t in TITLES:
        q = API + urllib.parse.urlencode({
            "search_query": f'ti:"{t}"',
            "start": 0, "max_results": 3,
        })
        code, body, _, _ = http(q, accept="application/atom+xml")
        entries = parse_entries(body or b"") if code == 200 else {}
        if not entries:
            q2 = API + urllib.parse.urlencode({
                "search_query": f"all:{t}",
                "start": 0, "max_results": 3,
            })
            code, body, _, _ = http(q2, accept="application/atom+xml")
            entries = parse_entries(body or b"") if code == 200 else {}
        print("Q:", t[:70])
        if not entries:
            print("  NONE", code)
        for aid, e in list(entries.items())[:3]:
            print(f"  {aid}  {e.get('title','')[:90]}")
        print()


if __name__ == "__main__":
    main()
