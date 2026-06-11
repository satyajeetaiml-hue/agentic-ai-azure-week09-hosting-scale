"""Smoke tests for Week 9 — Hosting, Deployment & Scale."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_endpoint_accepts_input():
    r = client.post("/api/v1/support", json={"customer_message": "I want a refund for order #88231, it arrived damaged."})
    assert r.status_code == 200


def test_endpoint_rejects_empty():
    r = client.post("/api/v1/support", json={"customer_message": ""})
    assert r.status_code == 422
