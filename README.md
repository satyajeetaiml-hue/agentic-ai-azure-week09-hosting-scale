# Week 9 — Hosting, Deployment & Scale

[![CI](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week09-hosting-scale/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week09-hosting-scale/actions/workflows/ci.yml)

> **Standalone lab** from the *Agentic AI on Azure — Enterprise Master Class* (12 weeks).
> Each lab is an independent, runnable FastAPI starter. Part of the
> [course series](https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure).

---

## 🎯 Learning goal
Package and deploy agents for production scale on Azure compute substrates.

## 🏢 Enterprise use case — "Black-Friday Customer Service Swarm" (Retail / E-commerce)
A fleet of customer-service agents must scale from 10 to 10,000 concurrent sessions, scale to zero overnight, and stay within cost guardrails — with durable long-running tasks for refunds.

---

## 🧪 What you'll build (lab)
1. Containerize the FastAPI agent app with **Docker**.
2. Deploy to **Azure Container Apps** with autoscaling (KEDA, scale-to-zero).
3. Add **Durable Tasks** for long-running operations (refunds).
4. Compare deploy targets: Container Apps vs. **AKS** vs. **Azure Functions**.

> This starter ships with a **runnable mock** of the endpoint so you can run and test
> immediately, then progressively replace the mock with the real Azure implementation.

## 🏗️ Architect's lens
- Decision matrix: Container Apps (managed, event-driven, scale-to-zero) vs. AKS (max control) vs. Functions (bursty).
- Concurrency model: async FastAPI + uvicorn/gunicorn workers; connection pooling to models.
- Cost: token budgets, model routing (small model for triage, large for hard cases), caching.

## 🧰 Tech stack
Docker, Azure Container Apps (+ KEDA), AKS, Azure Functions, Azure Container Registry, FastAPI + Gunicorn/Uvicorn, Bicep/Terraform.

---

## 🚀 Quick start

```bash
# 1. Create & activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) copy the env template — runs in MOCK mode without it
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux

# 4. Run the API
uvicorn app.main:app --reload
```

Open the interactive docs at **http://127.0.0.1:8000/docs**.

### Try the endpoint
```bash
curl -X POST http://127.0.0.1:8000/api/v1/support \
  -H "Content-Type: application/json" \
  -d '{"customer_message": "I want a refund for order #88231, it arrived damaged."}'
```

### Run the tests
```bash
pytest -q
```

### Run with Docker
```bash
docker build -t agentic-ai-azure-week09-hosting-scale .
docker run -p 8000:8000 agentic-ai-azure-week09-hosting-scale
```

---

## 📁 Project structure
```
agentic-ai-azure-week09-hosting-scale/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI app + the /api/v1/support endpoint
├── tests/
│   └── test_smoke.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

---

## 🗺️ Where this fits
This repo covers **Week 9 — Hosting, Deployment & Scale**. The full 12-week path and reference architecture
live in the master-class companion repo:
**[azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass)**.

## 📄 License
MIT — see [`LICENSE`](LICENSE).
