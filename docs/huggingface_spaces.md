# Hugging Face Spaces Deployment

This project is prepared to run as a Docker Space.

## Space Settings

Use:

```yaml
sdk: docker
app_port: 7860
```

The root `Dockerfile` builds the React frontend, copies it into the FastAPI image, and starts Uvicorn on port `7860`.

## Secrets

No secret is required for the default deterministic fallback. For server-side Gemini use, add this Space secret:

```text
GEMINI_API_KEY
```

The frontend can also send a session-only Gemini key from the browser settings panel.

## Local Docker Test

```bash
docker build -t threatgraph-ai .
docker run --rm -p 7860:7860 threatgraph-ai
```

Open:

```text
http://localhost:7860
```
