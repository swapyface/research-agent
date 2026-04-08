"""Researcher agent — runs parallel web searches for each research question."""
from __future__ import annotations
import concurrent.futures
from typing import Any
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage
from src.utils.logger import get_logger

logger = get_logger(__name__)
_search_tool = TavilySearchResults(max_results=5)

def _search_one(question: str) -> dict[str, Any]:
    logger.debug("Searching: %s", question)
    try:
        results = _search_tool.invoke({"query": question})
        return {"question": question, "results": results, "error": None}
    except Exception as exc:
        logger.warning("Search failed for '%s': %s", question, exc)
        return {"question": question, "results": [], "error": str(exc)}

def researcher_node(state: dict) -> dict:
    questions = state.get("research_questions", [])
    logger.info("Researcher: running %d searches in parallel", len(questions))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        all_results = list(pool.map(_search_one, questions))
    return {
        "search_results": all_results,
        "messages": [AIMessage(content=f"Completed {len(all_results)} research searches.", name="researcher")],
    }
