---
title: ThreatGraph AI
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# ThreatGraph AI

## Equipe

Joalisson Borges, Luis Gustavo Santini, Marina Souza Lucas, Diego Santos.

ThreatGraph AI is a hackathon MVP for automated STRIDE threat modeling from software architecture diagrams.

The system accepts an architecture image, detects architecture components with a supervised YOLO model, normalizes detections into a structured architecture graph, and runs a LangGraph-style multi-agent workflow to generate a technical and executive security report.

## Main Modules

- `backend/`: FastAPI API, detection services, topology normalization, agents, prompts, rules, and report generation.
- `frontend/`: Vite + React interface for upload, component review, report viewing, and history.
- `notebooks/`: Colab notebook for training the architecture component detector.
- `datasets/`: Dataset documentation and YOLO data config examples.
- `models/`: Local model artifact location and metadata.
- `docs/`: Architecture, training, dataset, STRIDE methodology, and demo notes.
- `examples/`: Sample inputs and generated outputs for demos.

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Backend API:

```text
http://localhost:8000
```

Frontend:

```text
http://localhost:5173
```

## MVP Flow

1. Upload an architecture diagram.
2. Detect components with the trained YOLO model.
3. Review detections and confidence levels.
4. Normalize components into a topology graph.
5. Generate STRIDE threats, probable vulnerabilities, countermeasures, and a report.

## Gemini Free Tier

The backend uses Gemini through `GEMINI_API_KEY` when available. If the key is missing, the dependency is not installed, or the free-tier quota is exhausted, the app falls back to local rule-based threat generation so the demo still works.

Recommended local `.env` values:

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
LLM_ENABLED=true
```

The frontend also has a session-only Gemini key field. For safer handling, the key is kept only in React memory, is not stored in localStorage, and is sent only to `/analyze` through request headers. In production, prefer a backend-managed secret over entering API keys in the browser.

The trained detector artifact is expected at:

```text
models/best.pt
```

## Notes

`training_results/` keeps raw notebook outputs. `models/` contains the artifact used by the backend.
