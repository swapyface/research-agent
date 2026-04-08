# 🔬 Research Agent

A **production-grade agentic AI application** built with LangGraph and OpenAI GPT-4o that automatically transforms any research topic into a structured blog post draft.

## Architecture

```
User Topic → Planner → Researcher (parallel Tavily searches) → Writer → Reviewer
                                                                      ↑______↓ (revision loop, max 2x)
                                                                            ↓
                                                                  Final Blog Draft
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| **Planner** | Decomposes topic into 4–6 research questions + outline | GPT-4o |
| **Researcher** | Parallel web searches via Tavily | Tavily API |
| **Writer** | Synthesizes research → Markdown blog post | GPT-4o |
| **Reviewer** | Quality gate with revision loop (max 2 cycles) | GPT-4o |

## Quickstart

```bash
git clone https://github.com/swapyface/research-agent.git
cd research-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add OPENAI_API_KEY + TAVILY_API_KEY
python main.py --topic "The impact of LLMs on software engineering"
```

## REST API

```bash
uvicorn api:app --reload
curl -X POST http://localhost:8000/research -H "Content-Type: application/json" -d '"'"'{"topic": "Quantum computing in finance"}'"'"'
```

## Project Structure

```
research-agent/
├── main.py              # CLI entrypoint
├── api.py               # FastAPI async REST server
├── requirements.txt
├── .env.example
├── src/
│   ├── graph.py         # LangGraph StateGraph orchestrator
│   ├── agents/          # planner, researcher, writer, reviewer
│   ├── prompts/         # All LLM prompts
│   └── utils/           # logger, parsers
└── tests/
```

## License

MIT