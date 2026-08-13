"""LangGraph agent CLI. Usage: python main.py "질문" """
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from agent.graph import ask, build_agent  # noqa: E402


async def main() -> None:
    question = " ".join(sys.argv[1:]) or "황금의 항염 효과에 대한 국내외 연구를 찾아줘"
    agent = await build_agent()
    print(await ask(agent, question))


if __name__ == "__main__":
    asyncio.run(main())
