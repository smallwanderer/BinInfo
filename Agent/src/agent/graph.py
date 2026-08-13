"""LangGraph ReAct agent tool-calling into KCI (via paperModule's MCP
server, stdio) and PubMed (direct E-utilities tool). Domestic-only scope
is deprecated (see paperModule/pc-docs/domestic-imple-spec.md banner);
this is the current KCI+PubMed design.
"""
from __future__ import annotations

import sys
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .capabilities import mentions_unsupported_constraint
from .tools.pubmed import search_pubmed

_PAPER_MODULE_DIR = Path(__file__).resolve().parents[1] / "paperModule"

MCP_SERVERS = {
    "kmed_kci": {
        "command": sys.executable,
        "args": [str(_PAPER_MODULE_DIR / "adapters" / "mcp_server.py")],
        "transport": "stdio",
    }
}

SYSTEM_PROMPT = (
    "You are a literature search agent assisting Korean medicine / drug discovery research.\n"
    "- Domestic literature: use kmed_kci's search_literature/research_literature/get_paper/"
    "get_fulltext tools, passing the Korean query as-is.\n"
    "- International literature: use the search_pubmed tool, and always translate the query "
    "into English keywords before calling it.\n"
    "\n"
    "**ABSOLUTE RULE about Impact Factor (IF)**: none of this system's tools (kmed_kci, "
    "search_pubmed) provide journal IF/citation-index data at all. Paper results only have a "
    "journal name field, never an IF number.\n"
    "If the user requests an IF condition (e.g. 'IF 5 or higher'):\n"
    "1. Do NOT filter or sort search results by IF (impossible -- the value doesn't exist here).\n"
    "2. NEVER claim a specific paper does or doesn't meet the IF condition -- you don't know the "
    "actual IF value.\n"
    "3. The first line of your answer MUST state, verbatim: "
    "'⚠️ This system does not have journal Impact Factor data, so results were not filtered or "
    "verified by IF. The list below is unrelated to IF.'\n"
    "Breaking this rule by guessing or fabricating IF-related facts is considered the most "
    "serious kind of error."
)


async def build_agent(model: str = "gpt-4o-mini"):
    mcp_client = MultiServerMCPClient(MCP_SERVERS)
    kci_tools = await mcp_client.get_tools()
    tools = [*kci_tools, search_pubmed]
    llm = ChatOpenAI(model=model)
    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


# The prompt asks the LLM to self-disclose the missing-IF-data limitation,
# but instruction-following isn't guaranteed (verified: gpt-4o-mini silently
# drops the disclaimer under load). Enforce it deterministically instead of
# trusting the model, via the shared registry in capabilities.py.
_IF_DISCLAIMER = (
    "⚠️ 이 시스템은 저널 Impact Factor 데이터를 보유하고 있지 않아 IF 기준으로 "
    "필터링/확인하지 않았습니다. 아래는 IF와 무관하게 검색된 결과입니다.\n\n"
)


async def ask(agent, question: str) -> str:
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    answer = result["messages"][-1].content
    if mentions_unsupported_constraint(question) and "⚠️" not in answer:
        answer = _IF_DISCLAIMER + answer
    return answer
