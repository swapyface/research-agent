#!/usr/bin/env python3
"""
Research Agent CLI

Usage:
    python main.py --topic "The impact of LLMs on software engineering"
    python main.py --topic "Quantum computing in finance" --output draft.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from datetime import datetime

from src.graph import research_graph
from src.utils.logger import get_logger

logger = get_logger("research_agent")


def run(topic: str, output_path: str | None = None) -> str:
    logger.info("=" * 60)
    logger.info("Starting Research Agent for topic: %s", topic)
    logger.info("=" * 60)

    initial_state = {
        "topic": topic,
        "research_questions": [],
        "outline": {},
        "search_results": [],
        "draft": "",
        "review_feedback": "",
        "revised_draft": "",
        "metadata": {},
        "messages": [],
    }

    final_state = research_graph.invoke(initial_state)
    final_draft = final_state.get("revised_draft") or final_state.get("draft", "")
    metadata = final_state.get("metadata", {})

    logger.info("Pipeline complete. Revision cycles: %s", metadata.get("revision_cycles", 0))

    if output_path:
        path = Path(output_path)
    else:
        slug = topic[:50].lower().replace(" ", "-").replace("/", "-")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path(f"outputs/{slug}_{timestamp}.md")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(final_draft, encoding="utf-8")
    logger.info("Draft saved to: %s", path)
    return final_draft


def main() -> None:
    parser = argparse.ArgumentParser(description="Research Agent: auto-generate blog post drafts.")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--output", default=None, help="Output file path (optional)")
    args = parser.parse_args()

    try:
        draft = run(topic=args.topic, output_path=args.output)
        print("\n" + "=" * 60)
        print("GENERATED DRAFT")
        print("=" * 60)
        print(draft)
    except Exception as exc:
        logger.error("Pipeline failed: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
