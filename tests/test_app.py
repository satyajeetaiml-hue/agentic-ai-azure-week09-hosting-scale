"""Hermetic tests for the Week 9 CS swarm (fast path + durable tasks)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_scale_config():
    body = client.get("/api/v1/scale").json()
    assert body["worker_count"] >= 1
    assert body["max_concurrent_sessions"] >= 1


def test_fast_path_answers_inline():
    r = client.post("/api/v1/support", json={"customer_message": "How do I track my order?"})
    assert r.status_code == 200
    body = r.json()
    assert body["kind"] == "answer"
    assert body["answer"]


def test_refund_spawns_durable_task_and_completes():
    r = client.post(
        "/api/v1/support",
        json={"customer_message": "I want a refund for order #88231, it arrived damaged."},
    )
    body = r.json()
    assert body["kind"] == "task"
    task_id = body["task_id"]
    # BackgroundTasks run during the request lifecycle; status should be terminal.
    status = client.get(f"/api/v1/tasks/{task_id}").json()
    assert status["state"] == "completed"
    assert status["result"]["order_id"] == "88231"
    assert status["result"]["status"] == "refunded"


def test_refund_without_order_fails_gracefully():
    r = client.post("/api/v1/support", json={"customer_message": "I demand a refund now"})
    task_id = r.json()["task_id"]
    status = client.get(f"/api/v1/tasks/{task_id}").json()
    assert status["state"] == "failed"


def test_task_404():
    assert client.get("/api/v1/tasks/TASK-NOPE").status_code == 404


def test_validation_rejects_empty():
    assert client.post("/api/v1/support", json={"customer_message": ""}).status_code == 422
