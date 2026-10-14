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
        # No asumir que todo el listado está "verificado": EventRecord admite
        # verification_status="pending_review", así que se cuenta cada estado
        # por separado en vez de describir el conjunto completo como verificado
        # (hallazgo de revisión en PR #2).
        verified_count = sum(1 for e in EVENTS if e.verification_status == "verified")
        pending_count = len(EVENTS) - verified_count
        parts = []
        if verified_count:
            parts.append(f"{verified_count} evento(s) verificado(s)")
        if pending_count:
            parts.append(f"{pending_count} evento(s) pendiente(s) de revisión")
        message = (
            f"{', '.join(parts)} con fuente citable para esta zona. "
            "Esta lista es un punto de partida, no un inventario completo ni auditado de todos "
            "los eventos ocurridos en la zona."
        )

    return EventsResponse(events=EVENTS, message=message)
