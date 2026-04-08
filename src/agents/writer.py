"""Writer agent — synthesizes research into a structured blog post draft."""
from __future__ import annotations
import json
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from src.prompts.writer_prompts import WRITER_SYSTEM, writer_human
from src.utils.logger import get_logger

logger = get_logger(__name__)

def writer_node(state: dict) -> dict:
    topic = state["topic"]
    outline = state.get("outline", {})
    search_results = state.get("search_results", [])
    feedback = state.get("review_feedback", "")
    logger.info("Writer: drafting blog post for '%s'", topic)
    condensed = []
    for item in search_results:
        snippets = [r.get("content", "")[:400] for r in item.get("results", [])[:3]]
        condensed.append({"question": item["question"], "snippets": snippets})
    llm = ChatOpenAI(model="gpt-4o", temperature=0.6)
    response = llm.invoke([
        {"role": "system", "content": WRITER_SYSTEM},
        {"role": "user", "content": writer_human(
            topic=topic, outline=json.dumps(outline, indent=2),
            research=json.dumps(condensed, indent=2), feedback=feedback)},
    ])
    return {
        "draft": response.content,
        "messages": [AIMessage(content="Draft complete.", name="writer")],
    }
