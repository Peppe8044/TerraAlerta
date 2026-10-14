"""Esquemas Pydantic compartidos por los routers.

Estructura de indicador alineada con docs/ARQUITECTURA.md y
docs/AUDITORIA_MVP_2026-10-14.md: toda cifra real debe exhibir fuente,
fecha, unidad, resolución y limitaciones. `value=None` es explícito ante
ausencia de dato; nunca se rellena con valores inventados.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

LicenseStatus = Literal["approved", "pending", "research_only", "blocked"]
DataStatus = Literal["sufficient_data", "partial_data", "unavailable"]


class SourceInfo(BaseModel):
    dataset: str
    owner: str
    url: str
    license_status: LicenseStatus
    retrieval_mode: str = Field(description="Cómo se obtiene el dato (API, descarga manual, pendiente).")
    last_verified: str = Field(description="Fecha ISO de última verificación documental, no de ingesta de datos.")
    notes: str


class Indicator(BaseModel):
    name: str
    value: float | None
    unit: str | None
    source_id: str
    observed_at: str | None = None
    issued_at: str | None = None
    retrieved_at: str
    spatial_resolution: str
    coverage: str
    quality_flag: Literal["real", "synthetic", "unavailable"]
    limitations: list[str] = Field(default_factory=list)


class LocationSummary(BaseModel):
    location: dict
    experimental: bool = True
    status: DataStatus
    indicators: list[Indicator]
    limitations: list[str]
    official_alerts_url: str = "https://www.senapred.cl/"


class EventRecord(BaseModel):
    id: str
    date: str
    approx_location: dict
    hazard_type: Literal["aluvion", "remocion_en_masa", "inundacion"]
    source: str
    location_certainty: Literal["verified", "approximate", "unverified_candidate"]
    verification_status: Literal["verified", "pending_review"]
    notes: str


class EventsResponse(BaseModel):
    events: list[EventRecord]
    message: str


class PreparednessItem(BaseModel):
    text: str
    source: str


class PreparednessChecklist(BaseModel):
    hazard: str
    version: str
    last_reviewed: str
    source_attribution: str
    official_url: str
    items: list[PreparednessItem]
    disclaimer: str
