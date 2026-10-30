#!/usr/bin/env python3
import sys
import urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from papers_en import API, parse_entries, http

QUERIES = [
    'ti:"Resource Management with Deep Reinforcement Learning"',
    'ti:DeepRM AND all:reinforcement',
    'au:Mao AND ti:"Resource Management"',
    'ti:"Deep Reinforcement Learning based HVAC"',
    'ti:"HVAC" AND all:"reinforcement learning" AND au:Wei',
    'ti:"Safety Gym"',
    'ti:"OpenAI Safety Gym"',
    'ti:"Benchmarking Safe Exploration"',
    'ti:"CityLearn"',
    'ti:"job shop" AND all:"reinforcement learning"',
    'ti:"traffic signal" AND all:"reinforcement learning"',
    'ti:"inventory" AND all:"reinforcement learning" AND ti:deep',
]

def main():
    for t in QUERIES:
        q = API + urllib.parse.urlencode({"search_query": t, "start": 0, "max_results": 3})
        code, body, _, _ = http(q, accept="application/atom+xml")
        entries = parse_entries(body or b"") if code == 200 else {}
        print("Q:", t[:80])
        if not entries:
            print("  NONE", code)
        for aid, e in list(entries.items())[:3]:
            print(f"  {aid}  {e.get('title','')[:90]}")
        print()

if __name__ == "__main__":
    main()
