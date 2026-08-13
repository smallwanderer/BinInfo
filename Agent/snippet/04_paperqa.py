"""Layer 4: PaperQA2 over the Screened Pool. See agent-docs/planner-v2.md §3.

Reuses snippet/03_result.json's "pool" (Screened Pool, already filtered +
sorted): ingests it once into a persistent PaperQASession, then asks one
question per topic against the shared corpus (not one compound question).

Usage: python 04_paperqa.py
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "paperModule" / "src"))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from kmed_domestic_lit.deep.paperqa_adapter import PaperQASession  # noqa: E402
from kmed_domestic_lit.models import Paper  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agent.planning.usage import sum_usage  # noqa: E402

RESULT_3_PATH = Path(__file__).resolve().parent / "03_result.json"


async def run() -> dict:
    layer3 = json.loads(RESULT_3_PATH.read_text(encoding="utf-8"))
    topics = layer3["topics"]
    pool = [Paper.model_validate(c) for c in layer3["pool"]]

    async with PaperQASession(model="gpt-4o-mini") as session:
        added = await session.ingest(pool)
        answers = {}
        usages = []
        for topic in topics:
            answer, evidence, usage = await session.ask(topic)
            usages.append(usage)
            answers[topic] = {
                "answer": answer,
                "evidence": [e.model_dump() for e in evidence],
            }

    return {
        "pool_size": len(pool),
        "ingested": added,
        "answers": answers,
        "usage": sum_usage(*usages),
    }


async def main() -> None:
    result = await run()

    out_path = Path(__file__).resolve().parent / "04_result.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    sys.stdout.reconfigure(errors="replace")
    print(f"pool_size={result['pool_size']}, ingested={result['ingested']}")
    print(f"token usage: {result['usage']}")
    for topic, a in result["answers"].items():
        print(f"\n=== {topic} ===")
        print(a["answer"][:300])
    print(f"\nsaved to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
