"""Unit tests for utility functions (no API calls required)."""
import pytest
from src.utils.parsers import parse_json_block

def test_parse_clean_json():
    text = '{"research_questions": ["q1", "q2"], "outline": {"title": "Test"}}'
    result = parse_json_block(text)
    assert result["research_questions"] == ["q1", "q2"]
    assert result["outline"]["title"] == "Test"

def test_parse_fenced_json():
    text = '```json\n{"key": "value"}\n```'
    result = parse_json_block(text)
    assert result["key"] == "value"

def test_parse_json_with_preamble():
    text = 'Here is the JSON:\n{"foo": 42}'
    result = parse_json_block(text)
    assert result["foo"] == 42

def test_parse_invalid_json_raises():
    with pytest.raises(ValueError):
        parse_json_block("this is not json at all")

def test_graph_nodes_importable():
    from src.agents import planner, researcher, writer, reviewer
    from src.prompts import planner_prompts, writer_prompts, reviewer_prompts
    assert True
