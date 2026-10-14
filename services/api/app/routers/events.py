from __future__ import annotations

from fastapi import APIRouter

from app.schemas import EventsResponse

router = APIRouter()


@router.get("/v1/events", response_model=EventsResponse)
def list_events() -> EventsResponse:
    """Visor de eventos históricos.

    Deliberadamente vacío en este MVP: aún no existe un conjunto de eventos
    corroborados y geolocalizados con calidad indicada (ver
    docs/ALUVIONES_Y_PREVENCION.md punto D y
    docs/AUDITORIA_MVP_2026-10-14.md entregable 5). No se simulan aluviones
    reales ni se usan noticias no corroboradas como si fueran observación
    instrumental.
    """
    return EventsResponse(
        events=[],
        message=(
            "Aún no hay eventos históricos verificados cargados para esta zona. "
            "Este visor se completará solo con registros corroborados y geolocalizados "
            "(SERNAGEOMIN, SENAPRED u otra fuente oficial citable)."
        ),
    )
