"""Week 9 — Hosting, Deployment & Scale: Customer Service Swarm.

Demonstrates the production runtime concerns:

* **Fast path vs. durable path** — FAQ-style messages answer inline; refunds are
  **long-running** and run as a background task with a pollable status (Durable
  Functions / Durable Tasks in prod).
* **Status polling** — every durable task is addressable by id.
* **Scale knobs** — concurrency settings exposed for the autoscaling story.

Fully runnable offline; the Dockerfile + Container Apps notes (README) cover deploy.
"""

from __future__ import annotations

import re
import uuid
from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ── settings ────────────────────────────────────────────────────────────
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    max_concurrent_sessions: int = 1000
    worker_count: int = 4

    @property
    def use_foundry(self) -> bool:
        return False


@lru_cache
def get_settings() -> Settings:
    return Settings()


# ── schemas ─────────────────────────────────────────────────────────────
class SupportRequest(BaseModel):
    customer_message: str = Field(..., min_length=1, description="Incoming customer-service message.")
    order_id: str | None = None


class SupportResponse(BaseModel):
    kind: str  # "answer" (fast path) | "task" (durable path)
    answer: str | None = None
    task_id: str | None = None
    state: str | None = None  # processing | completed | failed


class TaskRecord(BaseModel):
    task_id: str
    state: str
    kind: str
    result: dict | None = None
    message: str


# ── durable task store (Durable Tasks / Cosmos in prod) ─────────────────
_TASKS: dict[str, TaskRecord] = {}


def get_task(task_id: str) -> TaskRecord | None:
    return _TASKS.get(task_id)


_ORDER_RE = re.compile(r"#?\b(\d{4,8})\b")
_FAQ = {
    "hours": "Our support team is available 24/7 during the holiday season.",
    "track": "You can track your order from the 'My Orders' page using your order number.",
    "return": "Items can be returned within 30 days in original packaging.",
}


def answer_faq(message: str) -> str:
    low = message.lower()
    for key, val in _FAQ.items():
        if key in low:
            return val
    return "Thanks for reaching out — a customer-service agent will follow up shortly."


def process_refund(task_id: str, message: str, order_id: str | None) -> None:
    """The durable unit of work. In prod this is a Durable Functions activity."""
    rec = _TASKS[task_id]
    order = order_id
    if not order:
        m = _ORDER_RE.search(message)
        order = m.group(1) if m else None
    if not order:
        rec.state = "failed"
        rec.result = {"reason": "no_order_id"}
        return
    rec.state = "completed"
    rec.result = {"order_id": order, "status": "refunded", "amount_estimate": "full"}


def is_refund(message: str) -> bool:
    return any(w in message.lower() for w in ("refund", "money back", "chargeback"))


def start_refund_task(message: str, order_id: str | None) -> TaskRecord:
    task_id = f"TASK-{uuid.uuid4().hex[:8].upper()}"
    rec = TaskRecord(task_id=task_id, state="processing", kind="refund", message=message)
    _TASKS[task_id] = rec
    return rec
