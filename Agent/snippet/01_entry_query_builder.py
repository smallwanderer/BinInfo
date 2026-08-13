"""Layer 1: Entry Agent + Query Builder (Fast planning stage).
See agent-docs/planner-v2.md §3. Saves result next to this file.

Usage: python 01_entry_query_builder.py "질문"
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from agent.capabilities import classify_constraints  # noqa: E402
from agent.planning.fast_planner import entry_agent, query_builder  # noqa: E402
from agent.planning.usage import sum_usage  # noqa: E402

DEFAULT_QUERY = "뇌혈관질환후유증에 대한 침치료의 효과를 IF 5이상 저널 기준으로 찾아줘"


async def run(query: str) -> dict:
    entry, entry_usage = await entry_agent(query)
    # Fillable/unfillable is a deterministic capability check (capabilities.py),
    # not something the Entry Agent LLM call classifies -- see its docstring.
    fillable, unfillable = classify_constraints(entry.constraints)
    built, builder_usage = await query_builder(entry.goal, fillable)
    return {
        "query": query,
        "entry_agent": {
            "goal": entry.goal,
            "constraints": entry.constraints,
            "fillable_constraints": fillable,
            "unfillable_constraints": unfillable,
        },
        "query_builder": built.model_dump(),
        "usage": {
            "entry_agent": entry_usage,
            "query_builder": builder_usage,
            "total": sum_usage(entry_usage, builder_usage),
        },
    }


async def main() -> None:
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    result = await run(query)

    out_path = Path(__file__).resolve().parent / "01_result.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    sys.stdout.reconfigure(errors="replace")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\ntoken usage: {result['usage']['total']}")
    print(f"saved to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
