"""FastAPI server — exposes the research agent as a REST API."""
from __future__ import annotations
import asyncio, uuid
from datetime import datetime
from typing import Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from src.graph import research_graph
from src.utils.logger import get_logger

logger = get_logger("api")
app = FastAPI(title="Research Agent API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
_jobs: dict[str, dict[str, Any]] = {}

class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=5, max_length=300)

class ResearchResponse(BaseModel):
    job_id: str; status: str; topic: str; created_at: str

class JobStatusResponse(BaseModel):
    job_id: str; status: str; topic: str
    draft: str | None = None; outline: dict | None = None
    metadata: dict | None = None; error: str | None = None
    created_at: str; completed_at: str | None = None

async def _run_pipeline(job_id: str, topic: str) -> None:
    _jobs[job_id]["status"] = "running"
    try:
        initial_state = {"topic": topic, "research_questions": [], "outline": {},
            "search_results": [], "draft": "", "review_feedback": "",
            "revised_draft": "", "metadata": {}, "messages": []}
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(None, research_graph.invoke, initial_state)
        _jobs[job_id].update({"status": "completed",
            "draft": final_state.get("revised_draft") or final_state.get("draft", ""),
            "outline": final_state.get("outline"), "metadata": final_state.get("metadata"),
            "completed_at": datetime.utcnow().isoformat()})
    except Exception as exc:
        _jobs[job_id].update({"status": "failed", "error": str(exc),
            "completed_at": datetime.utcnow().isoformat()})

@app.get("/health")
def health(): return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/research", response_model=ResearchResponse, status_code=202)
async def start_research(req: ResearchRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    _jobs[job_id] = {"job_id": job_id, "topic": req.topic, "status": "pending", "created_at": created_at}
    background_tasks.add_task(_run_pipeline, job_id, req.topic)
    return ResearchResponse(job_id=job_id, status="pending", topic=req.topic, created_at=created_at)

@app.get("/research/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str):
    job = _jobs.get(job_id)
    if not job: raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(**job)

@app.get("/research")
def list_jobs():
    return [{"job_id": j["job_id"], "topic": j["topic"], "status": j["status"]} for j in _jobs.values()]
