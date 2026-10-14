"""Catálogo de eventos históricos: lista curada a mano + un lote importado.

Dos fuentes, con rigor distinto:

1. Eventos verificados a mano (`_HAND_CURATED`): cada uno fue investigado
   individualmente contra una fuente oficial primaria y citable. Pueden
   llevar `verification_status="verified"`.

2. Lote importado (`app/data/sernageomin_unab_catalog_sjm.json`, generado
   por `pipelines/sernageomin_unab_catalog/fetch_and_filter.py`): proviene
   de una compilación de terceros (Universidad Andrés Bello, vía ArcGIS
   Online) que cita informes SERNAGEOMIN cuyo dominio original
   (portalgeo.sernageomin.cl) está dado de baja, y cuya licencia de reuso
   no está declarada explícitamente (ver docs/FUENTES_ESTADO.md). Por eso
   TODO el lote lleva `verification_status="pending_review"` — nunca
   `"verified"` — sin excepción. Ver docs/DECISIONES.md para el detalle de
   la investigación.

Regla explícita (ver docs/ALUVIONES_Y_PREVENCION.md): el evento de Las
Condes de octubre de 2026 permanece como "candidato por verificar" y NO se
incorpora aquí hasta contar con fuente oficial y localización verificada.
"""
from __future__ import annotations

import json
from pathlib import Path

from app.schemas import EventRecord

_DATA_DIR = Path(__file__).parent / "data"

# Ubicación aproximada a nivel de localidad (centro de San José de Maipo),
# NO la coordenada exacta de la quebrada San José — no se verificó esa
# coordenada puntual, por eso location_certainty="approximate".
_SAN_JOSE_DE_MAIPO_LOCALITY = {"lat": -33.6378, "lon": -70.3539, "place": "San José de Maipo (centro urbano)", "radius_km": 10}

_HAND_CURATED: list[EventRecord] = [
    EventRecord(
        id="sjm-2017-02-quebrada-san-jose",
        date="2017-02-25",
        approx_location=_SAN_JOSE_DE_MAIPO_LOCALITY,
        hazard_type="aluvion",
        source=(
            "SERNAGEOMIN, Informe Registrado RM-2017-23, "
            "https://portalgeo.sernageomin.cl/Informes_PDF_Nac/RM-2017-23.pdf "
            "(enlace actualmente inaccesible: el dominio portalgeo.sernageomin.cl está dado de "
            "baja, verificado el 14-10-2026; cita bibliográfica conservada como referencia)."
        ),
        location_certainty="approximate",
        verification_status="verified",
        notes=(
            "Flujos de detritos y barro en la cuenca alta del río Maipo tras un sistema de lluvias "
            "intensas; el estero/quebrada San José canalizó uno de los flujos de mayor impacto, "
            "afectando campings turísticos y cortando la ruta G-25. Documentado en informe técnico "
            "oficial de SERNAGEOMIN. No se incluye cifra de víctimas: las cifras de prensa difieren "
            "entre fuentes y no es el objeto de este registro de amenaza geológica. El catálogo de "
            "terceros usado para el lote 'pending_review' de este mismo archivo excluye los 17 "
            "sub-eventos de este mismo informe (código RM-2017-23-*) para no duplicar."
        ),
    ),
]


def _load_imported_batch() -> list[EventRecord]:
    path = _DATA_DIR / "sernageomin_unab_catalog_sjm.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as fh:
        raw_records = json.load(fh)
    return [EventRecord(**record) for record in raw_records]


EVENTS: list[EventRecord] = [*_HAND_CURATED, *_load_imported_batch()]
