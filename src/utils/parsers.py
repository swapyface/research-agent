"""Utility helpers for parsing LLM outputs."""
from __future__ import annotations
import json, re

def parse_json_block(text: str) -> dict:
    """Extract and parse a JSON object from an LLM response."""
    cleaned = re.sub(r"```(?:json)?\s*", "", text).replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not parse JSON from LLM response:\n{text[:500]}")
