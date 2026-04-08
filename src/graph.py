"""Research Agent Graph — LangGraph-powered multi-agent pipeline.

Flow: plan_research → web_search (parallel) → synthesize → write_draft → review → END
"""
from __future__ import annotations
import operator
from typing import Annotated, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from src.agents.planner import planner_node
from src.agents.researcher import researcher_node
from src.agents.writer import writer_node
from src.agents.reviewer import reviewer_node
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ResearchState(TypedDict):
    topic: str
    research_questions: list[str]
    outline: dict[str, Any]
    search_results: Annotated[list[dict], operator.add]
    draft: str
    review_feedback: str
    revised_draft: str
    metadata: dict[str, Any]
    messages: Annotated[list[BaseMessage], operator.add]

def should_revise(state: ResearchState) -> str:
    feedback = state.get("review_feedback", "")
    if feedback and "APPROVED" not in feedback.upper():
        logger.info("Reviewer requested revisions — looping back to writer.")
        return "revise"
    logger.info("Draft approved — finishing.")
    return "finish"

def build_graph() -> StateGraph:
    graph = StateGraph(ResearchState)
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("reviewer", reviewer_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "reviewer")
    graph.add_conditional_edges("reviewer", should_revise, {"revise": "writer", "finish": END})
    return graph.compile()

research_graph = build_graph()
