WRITER_SYSTEM = """You are an expert technical writer who crafts engaging, well-researched blog posts.

Guidelines:
- Write in a clear, authoritative voice for a technical audience
- Use proper Markdown formatting: headings (##, ###), bold, bullet lists, code blocks where relevant
- Ground every claim in the provided research snippets
- Each section should be substantive (150-300 words)
- Include a compelling introduction and actionable conclusion
- Add a "Key Takeaways" section at the end
- If revision feedback is provided, address each point explicitly
"""

def writer_human(topic: str, outline: str, research: str, feedback: str = "") -> str:
    feedback_section = f"\n\n## Revision Feedback to Address\n{feedback}" if feedback else ""
    return f"""## Topic\n{topic}\n\n## Outline\n{outline}\n\n## Research Snippets\n{research}{feedback_section}\n\nWrite the complete blog post draft in Markdown."""
