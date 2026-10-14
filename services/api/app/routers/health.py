from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict:
    """Estado del servicio. No afirma frescura de fuentes externas."""
    return {"status": "ok", "service": "terraalerta-api"}
