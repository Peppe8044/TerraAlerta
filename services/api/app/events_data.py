"""Catálogo estático de eventos históricos (seed curado, no un scraper).

Cada entrada exige una fuente oficial citable y verificable, no solo
cobertura de prensa (ver docs/ALUVIONES_Y_PREVENCION.md punto D y
docs/AUDITORIA_MVP_2026-10-14.md entregable 5). Este archivo se edita a
mano tras investigación documentada; no hay ingesta automática.

Regla explícita (ver docs/ALUVIONES_Y_PREVENCION.md): el evento de Las
Condes de octubre de 2026 permanece como "candidato por verificar" y NO se
incorpora aquí hasta contar con fuente oficial y localización verificada.
Tampoco se incorporan antecedentes de 1980/1991/2012 encontrados en
cobertura secundaria hasta confirmar que ocurrieron dentro de la comuna de
San José de Maipo y contar con una cita primaria (ver docs/DECISIONES.md).
"""
from __future__ import annotations

from app.schemas import EventRecord

# Ubicación aproximada a nivel de localidad (centro de San José de Maipo),
# NO la coordenada exacta de la quebrada San José — no se verificó esa
# coordenada puntual, por eso location_certainty="approximate".
_SAN_JOSE_DE_MAIPO_LOCALITY = {"lat": -33.6378, "lon": -70.3539, "place": "San José de Maipo (centro urbano)", "radius_km": 10}

EVENTS: list[EventRecord] = [
    EventRecord(
        id="sjm-2017-02-quebrada-san-jose",
        date="2017-02-25",
        approx_location=_SAN_JOSE_DE_MAIPO_LOCALITY,
        hazard_type="aluvion",
        source=(
            "SERNAGEOMIN, Informe Registrado RM-2017-23, "
            "https://portalgeo.sernageomin.cl/Informes_PDF_Nac/RM-2017-23.pdf"
        ),
        location_certainty="approximate",
        verification_status="verified",
        notes=(
            "Flujos de detritos y barro en la cuenca alta del río Maipo tras un sistema de lluvias "
            "intensas; el estero/quebrada San José canalizó uno de los flujos de mayor impacto, "
            "afectando campings turísticos y cortando la ruta G-25. Documentado en informe técnico "
            "oficial de SERNAGEOMIN. No se incluye cifra de víctimas: las cifras de prensa difieren "
            "entre fuentes y no es el objeto de este registro de amenaza geológica."
        ),
    ),
]
