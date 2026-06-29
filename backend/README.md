# Backend

FastAPI service for uploads, detection, topology normalization, STRIDE analysis, and report generation.

## Local Run

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment

Use Gemini with the free tier by setting:

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
LLM_ENABLED=true
```

The app falls back to local STRIDE rules when Gemini is unavailable.

## Main Endpoints

- `GET /health`
- `POST /detect`
- `POST /analyze`
- `POST /reports`
