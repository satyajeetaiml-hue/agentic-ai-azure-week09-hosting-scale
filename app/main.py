"""Week 9 — Hosting, Deployment & Scale — starter FastAPI service.

Use case: Black-Friday Customer Service Swarm (Retail / E-commerce).
See README.md for the full lab brief. Run:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Week 9 — Hosting, Deployment & Scale", version="0.1.0")


class LabRequest(BaseModel):
    customer_message: str = Field(..., min_length=1, description="An incoming customer-service message.")


@app.get("/health")
def health():
    return {"status": "ok", "week": "9", "use_case": "Black-Friday Customer Service Swarm"}


@app.get("/")
def root():
    return {
        "service": "agentic-ai-azure-week09-hosting-scale",
        "week": "9",
        "endpoint": "/api/v1/support",
        "docs": "/docs",
    }


@app.post("/api/v1/support")
def handler(payload: LabRequest):
    """Mock handler for the Black-Friday Customer Service Swarm.

    TODO (lab): replace this stub with the real implementation described in
    README.md (the Azure services for this week are listed in the Tech Stack).
    """
    return {
        "week": "9",
        "use_case": "Black-Friday Customer Service Swarm",
        "received": payload.customer_message,
        "status": "accepted",
        "note": "Mock response — implement the real agent per README.md.",
    }
