"""Reviewer agent — critiques the draft and decides approve vs. revise."""
from __future__ import annotations
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from src.prompts.reviewer_prompts import REVIEWER_SYSTEM, reviewer_human
from src.utils.logger import get_logger

logger = get_logger(__name__)
_MAX_REVISION_CYCLES = 2

def reviewer_node(state: dict) -> dict:
    draft = state.get("draft", "")
    topic = state["topic"]
    cycle = len([m for m in state.get("messages", []) if getattr(m, "name", "") == "reviewer"])
    logger.info("Reviewer: reviewing draft (cycle %d)", cycle + 1)
    if cycle >= _MAX_REVISION_CYCLES:
        logger.info("Max revision cycles reached — auto-approving.")
        return {
            "review_feedback": "APPROVED (max cycles reached)",
            "revised_draft": draft,
            "metadata": {"revision_cycles": cycle},
            "messages": [AIMessage(content="APPROVED (max cycles reached)", name="reviewer")],
        }
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    response = llm.invoke([
        {"role": "system", "content": REVIEWER_SYSTEM},
        {"role": "user", "content": reviewer_human(topic=topic, draft=draft)},
    ])
    feedback = response.content
    approved = "APPROVED" in feedback.upper()
    return {
        "review_feedback": feedback,
        "revised_draft": draft if approved else "",
        "metadata": {"revision_cycles": cycle + 1, "approved": approved},
        "messages": [AIMessage(content=feedback, name="reviewer")],
    }
