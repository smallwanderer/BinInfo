"""Layer 3: Relevance Screen. See agent-docs/planner-v2.md §3.

Reuses snippet/02_result.json (Fast Search candidate pool): flattens and
dedups candidates by uid across all sub-topics/sources, then tags each
candidate against every topic in a single LLM call.

Usage: python 03_relevance_screen.py
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from agent.planning.relevance_screen import finalize_pool, relevance_screen  # noqa: E402

RESULT_2_PATH = Path(__file__).resolve().parent / "02_result.json"


def _flatten_pool(fast_search: list[dict]) -> dict[str, dict]:
    """uid -> candidate dict, deduped across topics/sources."""
    pool: dict[str, dict] = {}
    for item in fast_search:
        for c in item["kci"] + item["pubmed"]:
            pool.setdefault(c["uid"], c)
    return pool


async def run() -> dict:
    layer2 = json.loads(RESULT_2_PATH.read_text(encoding="utf-8"))
    topics = [sq["topic"] for sq in layer2["query_builder"]["sub_queries"]]
    constraints = layer2.get("entry_agent", {}).get("fillable_constraints") or []
    pool = _flatten_pool(layer2["fast_search"])

    result, usage = await relevance_screen(topics, list(pool.values()), constraints)
    tags_by_uid = {t.uid: t for t in result.tags}

    screened = [
        {
            **pool[uid],
            "relevant_to": tags_by_uid[uid].relevant_to if uid in tags_by_uid else [],
            "unmet_constraints": tags_by_uid[uid].unmet_constraints if uid in tags_by_uid else [],
        }
        for uid in pool
    ]
    pool_out = finalize_pool(screened)
    return {
        "topics": topics,
        "constraints": constraints,
        "candidate_count": len(pool),
        "screened": screened,
        "pool": pool_out,
        "usage": usage,
    }


async def main() -> None:
    result = await run()

    out_path = Path(__file__).resolve().parent / "03_result.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    sys.stdout.reconfigure(errors="replace")
    print(f"candidates: {result['candidate_count']}, final pool (Screened Pool): {len(result['pool'])}")
    print(f"token usage: {result['usage']}")
    print(f"saved to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
