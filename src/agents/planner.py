"""Planner agent — decomposes a research topic into questions and an outline."""
from __future__ import annotations
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from src.prompts.planner_prompts import PLANNER_SYSTEM, planner_human
from src.utils.logger import get_logger
from src.utils.parsers import parse_json_block

logger = get_logger(__name__)

def planner_node(state: dict) -> dict:
    topic = state["topic"]
    logger.info("Planner: decomposing topic '%s'", topic)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    response = llm.invoke([
        {"role": "system", "content": PLANNER_SYSTEM},
        {"role": "user", "content": planner_human(topic)},
    ])
    parsed = parse_json_block(response.content)
    return {
        "research_questions": parsed.get("research_questions", []),
        "outline": parsed.get("outline", {}),
        "messages": [AIMessage(content=response.content, name="planner")],
    }
