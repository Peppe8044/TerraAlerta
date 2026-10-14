from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import events, health, locations, precipitation, preparedness, sources, terrain

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Prototipo experimental de inteligencia territorial para San José de Maipo. "
        "No predice inundaciones a nivel de vivienda, no emite alertas oficiales y no "
        "sustituye a SENAPRED."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "development" else [],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sources.router)
app.include_router(locations.router)
app.include_router(precipitation.router)
app.include_router(terrain.router)
app.include_router(events.router)
app.include_router(preparedness.router)
