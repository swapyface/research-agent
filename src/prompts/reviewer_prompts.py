REVIEWER_SYSTEM = """You are a senior editor reviewing a blog post draft. Evaluate on:
1. Accuracy & depth — are claims well-supported?
2. Structure & flow — logical progression?
3. Clarity — is technical content accessible?
4. Completeness — does it fully address the topic?
5. Engagement — compelling title, hook, and conclusion?

If the draft meets all criteria, respond starting with: APPROVED
Otherwise, provide specific, actionable feedback as a numbered list.
Be concise — max 200 words."""

def reviewer_human(topic: str, draft: str) -> str:
    return f"## Topic\n{topic}\n\n## Draft\n{draft}"
