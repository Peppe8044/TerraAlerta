from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.schemas import PreparednessChecklist, PreparednessItem

router = APIRouter()

# Contenido editorial propio. BORRADOR pendiente de revisión/cita literal
# contra el texto oficial vigente de SENAPRED (gate G4, ver
# docs/AUDITORIA_MVP_2026-10-14.md y docs/ROADMAP_VALOR_CIUDADANO.md).
# No contiene rutas de evacuación ni veredictos de seguridad.
_CHECKLISTS: dict[str, PreparednessChecklist] = {
    "landslide": PreparednessChecklist(
        hazard="landslide",
        version="0.1.0-borrador",
        last_reviewed="2026-10-14",
        source_attribution=(
            "Checklist genérico elaborado a partir de principios públicos de protección civil; "
            "pendiente de contraste línea a línea con el contenido oficial vigente de SENAPRED."
        ),
        official_url="https://www.senapred.cl/",
        items=[
            PreparednessItem(
                text=(
                    "Identificar junto a tu familia las vías de evacuación oficiales definidas "
                    "por la autoridad local, no generadas por esta app."
                ),
                source="SENAPRED (pendiente de cita literal)",
            ),
            PreparednessItem(
                text="Mantener un kit básico de emergencia (agua, linterna, radio a pilas, medicamentos, documentos).",
                source="SENAPRED (pendiente de cita literal)",
            ),
            PreparednessItem(
                text=(
                    "Seguir los canales oficiales de SENAPRED y la autoridad local ante lluvias "
                    "intensas, no solo esta aplicación experimental."
                ),
                source="SENAPRED (pendiente de cita literal)",
            ),
            PreparednessItem(
                text="Evitar acercarse a quebradas o cauces durante y después de lluvias intensas.",
                source="SENAPRED (pendiente de cita literal)",
            ),
        ],
        disclaimer=(
            "Esta lista es orientativa y experimental. No reemplaza las instrucciones oficiales "
            "de SENAPRED ni constituye una alerta vigente."
        ),
    ),
}


@router.get("/v1/preparedness", response_model=PreparednessChecklist)
def preparedness(hazard: str = Query("landslide")) -> PreparednessChecklist:
    checklist = _CHECKLISTS.get(hazard)
    if checklist is None:
        raise HTTPException(status_code=404, detail=f"No hay checklist para hazard='{hazard}' todavía.")
    return checklist
