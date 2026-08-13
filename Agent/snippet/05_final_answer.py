"""Layer 5: Final Answer. Combines snippet/04_result.json's per-topic
PaperQA2 answers into one answer to the original user question
(snippet/01_result.json's "query"), with a deterministic disclaimer for
any unfillable constraints (e.g. Impact Factor).

Usage: python 05_final_answer.py
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from agent.planning.final_answer import synthesize_final_answer  # noqa: E402

RESULT_1_PATH = Path(__file__).resolve().parent / "01_result.json"
RESULT_4_PATH = Path(__file__).resolve().parent / "04_result.json"


async def run() -> dict:
    layer1 = json.loads(RESULT_1_PATH.read_text(encoding="utf-8"))
    layer4 = json.loads(RESULT_4_PATH.read_text(encoding="utf-8"))

    question = layer1["query"]
    unfillable = layer1["entry_agent"].get("unfillable_constraints") or []
    topic_answers = {topic: a["answer"] for topic, a in layer4["answers"].items()}

    answer, usage = await synthesize_final_answer(question, topic_answers, unfillable)
    return {"question": question, "final_answer": answer, "usage": usage}


async def main() -> None:
    result = await run()

    out_path = Path(__file__).resolve().parent / "05_result.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    sys.stdout.reconfigure(errors="replace")
    print(result["final_answer"])
    print(f"\ntoken usage: {result['usage']}")
    print(f"saved to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
