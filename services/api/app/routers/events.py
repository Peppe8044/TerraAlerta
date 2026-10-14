from __future__ import annotations

from fastapi import APIRouter

from app.events_data import EVENTS
from app.schemas import EventsResponse

router = APIRouter()


@router.get("/v1/events", response_model=EventsResponse)
def list_events() -> EventsResponse:
    """Visor de eventos históricos.

    Lista curada a mano (ver `app/events_data.py`), no un scraper: cada
    entrada exige una fuente oficial citable. Deliberadamente corta en este
    MVP — aún no existe un inventario completo auditado para San José de
    Maipo (ver docs/ALUVIONES_Y_PREVENCION.md punto D y
    docs/AUDITORIA_MVP_2026-10-14.md entregable 5). No se simulan aluviones
    reales ni se usan noticias no corroboradas como si fueran observación
    instrumental.
    """
    if not EVENTS:
        message = (
            "Aún no hay eventos históricos verificados cargados para esta zona. "
            "Este visor se completará solo con registros corroborados y geolocalizados "
            "(SERNAGEOMIN, SENAPRED u otra fuente oficial citable)."
        )
    else:
        message = (
            f"{len(EVENTS)} evento(s) histórico(s) verificado(s) con fuente oficial citable. "
            "Esta lista es un punto de partida, no un inventario completo ni auditado de todos "
            "los eventos ocurridos en la zona."
        )

    return EventsResponse(events=EVENTS, message=message)
