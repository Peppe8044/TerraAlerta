from __future__ import annotations

from fastapi import APIRouter

from app.schemas import SourceInfo
from app.sources import list_sources

router = APIRouter()


@router.get("/v1/sources", response_model=list[SourceInfo])
def get_sources() -> list[SourceInfo]:
    return list_sources()
