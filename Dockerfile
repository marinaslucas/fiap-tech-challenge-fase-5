FROM node:20-alpine AS frontend

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend ./
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=7860
ENV MODEL_PATH=/app/models/best.pt
ENV MODEL_METADATA_PATH=/app/models/model_metadata.json
ENV STORAGE_DIR=/app/backend/storage
ENV FRONTEND_DIST_DIR=/app/frontend/dist
ENV CORS_ORIGINS=http://localhost:7860,http://127.0.0.1:7860

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY backend ./backend
COPY models ./models
COPY --from=frontend /app/frontend/dist ./frontend/dist

EXPOSE 7860

WORKDIR /app/backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
