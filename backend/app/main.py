from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import analyze, detect, health, reports
from app.config import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(detect.router)
app.include_router(analyze.router)
app.include_router(reports.router)

if settings.frontend_dist_dir.exists():
    app.mount("/", StaticFiles(directory=settings.frontend_dist_dir, html=True), name="frontend")
