"""Fast Search CLI. spec Phase 1 완료 기준.

Usage: python cli.py "황금 항염" [--k 10]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from kmed_domestic_lit.fast.search import fast_search


async def main() -> None:
    parser = argparse.ArgumentParser(description="국내 한의학 논문 Fast Search")
    parser.add_argument("query")
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--year-from", type=int, default=None)
    parser.add_argument("--year-to", type=int, default=None)
    parser.add_argument("--journal", default=None)
    args = parser.parse_args()

    cards = await fast_search(
        args.query, k=args.k, year_from=args.year_from, year_to=args.year_to, journal=args.journal
    )
    print(json.dumps([c.model_dump() for c in cards], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
