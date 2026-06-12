# Week 9 — Hosting, Deployment & Scale

[![CI](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week09-hosting-scale/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week09-hosting-scale/actions/workflows/ci.yml)

> ▶️ **Run in VS Code — no Azure needed.** `pip install -r requirements.txt`, then `uvicorn app.main:app --reload` and open http://127.0.0.1:8000/docs. Runs in **mock mode** by default — no `az login`, keys, or `.env` required. Wiring real Azure (below) is optional.

> **Standalone lab** from the *Agentic AI on Azure — Enterprise Master Class*.
> Course hub: [azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass).

---

## 🎯 Learning goal
Package and deploy agents for production scale, with **durable long-running tasks** and **status polling**.

## 🏢 Enterprise use case — "Black-Friday Customer Service Swarm" (Retail / E-commerce)
A fleet of CS agents scales from 10 to 10,000 sessions, scales to zero overnight, and runs durable
**refund** tasks without blocking the request path.

## ✅ What this repo implements
- **Fast path** — FAQ-style messages answer inline.
- **Durable path** — refunds spawn a background task (FastAPI `BackgroundTasks`; **Durable Functions /
  Durable Tasks** in prod) with a pollable status at `GET /api/v1/tasks/{id}`.
- **Scale knobs** at `GET /api/v1/scale` (the signals KEDA uses).
- **Dockerfile + Gunicorn/Uvicorn** for the Container Apps deploy story.

## 🚀 Quick start
```bash
python -m venv .venv && .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
```bash
curl -X POST http://127.0.0.1:8000/api/v1/support \
  -H "Content-Type: application/json" \
  -d '{"customer_message": "I want a refund for order #88231, it arrived damaged."}'
# -> {"kind":"task","task_id":"TASK-...","state":"processing"}  then poll:
curl http://127.0.0.1:8000/api/v1/tasks/<task_id>
```
Run tests: `pytest -q`

## 🐳 Deploy (Container Apps)
```bash
docker build -t cs-swarm .
docker run -p 8000:8000 cs-swarm        # CMD uses gunicorn + uvicorn workers
```
Then push to ACR and deploy to **Azure Container Apps** with KEDA (scale-to-zero). Compare targets:

| | Container Apps | AKS | Functions |
|--|----------------|-----|-----------|
| Best for | most agent APIs | platform control | bursty/short |
| Scaling | KEDA, scale-to-zero | HPA/KEDA (you manage) | per-execution |
| Ops burden | low | high | lowest |

## 🏗️ Architect's lens
- Decision matrix above — **Container Apps is the course default**.
- Async FastAPI + Gunicorn/Uvicorn workers; connection pooling to models.
- Cost: token budgets, model routing (small for triage, large for hard cases), caching.

## 🧰 Tech stack
Docker, Azure Container Apps (+KEDA), AKS, Azure Functions, ACR, FastAPI + Gunicorn/Uvicorn, Bicep/Terraform.

## 🗺️ Series
Prev: [Week 8](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week08-rag-grounding) ·
Next: [Week 10 — Observability](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week10-observability) ·
[All labs](https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure)

## 📄 License
MIT — see [`LICENSE`](LICENSE).

## 📊 Teaching slides

Download the **7-slide deck** for classroom use: [`agentic-ai-azure-week09-hosting-scale.pptx`](slides/agentic-ai-azure-week09-hosting-scale.pptx)

Prefer PDF? Download the **handout (slides + speaker notes)**: [`agentic-ai-azure-week09-hosting-scale-handout.pdf`](slides/agentic-ai-azure-week09-hosting-scale-handout.pdf)

> Slides: Title · Learning goal · Enterprise use case · Architecture/flow · Key concepts · Run it · Architect's takeaways.

