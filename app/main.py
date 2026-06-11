"""Week 9 — Hosting, Deployment & Scale.

Customer Service Swarm: fast-path FAQ answers + durable long-running refund tasks
with status polling. Run:  uvicorn app.main:app --reload
"""

from fastapi import BackgroundTasks, FastAPI, HTTPException

from app.service import (
    SupportRequest,
    SupportResponse,
    TaskRecord,
    answer_faq,
    get_settings,
    get_task,
    is_refund,
    process_refund,
    start_refund_task,
)

settings = get_settings()
app = FastAPI(title="Week 9 — Hosting & Scale (CS Swarm)", version="0.2.0")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "week": "9", "backend": "mock"}


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "service": "agentic-ai-azure-week09-hosting-scale",
        "endpoint": "/api/v1/support",
        "docs": "/docs",
    }


@app.get("/api/v1/scale", tags=["week09"])
def scale_config() -> dict[str, int]:
    """Expose the concurrency knobs that drive KEDA autoscaling decisions."""
    return {
        "max_concurrent_sessions": settings.max_concurrent_sessions,
        "worker_count": settings.worker_count,
    }


@app.post("/api/v1/support", response_model=SupportResponse, tags=["week09"])
def support(payload: SupportRequest, background: BackgroundTasks) -> SupportResponse:
    """Fast path answers inline; refunds spawn a durable background task."""
    if is_refund(payload.customer_message):
        rec = start_refund_task(payload.customer_message, payload.order_id)
        background.add_task(process_refund, rec.task_id, payload.customer_message, payload.order_id)
        return SupportResponse(kind="task", task_id=rec.task_id, state=rec.state)
    return SupportResponse(kind="answer", answer=answer_faq(payload.customer_message))


@app.get("/api/v1/tasks/{task_id}", response_model=TaskRecord, tags=["week09"])
def task_status(task_id: str) -> TaskRecord:
    rec = get_task(task_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return rec
