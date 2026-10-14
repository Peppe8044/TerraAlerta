"""Importador reproducible: catastro de remociones en masa (compilación de
terceros, Universidad Andrés Bello, hospedado en ArcGIS Online) filtrado a
localidades de San José de Maipo / Cajón del Maipo.

Estado de la fuente (ver docs/FUENTES_ESTADO.md): `pending` — no es un canal
oficial de SERNAGEOMIN (lo administra una investigadora de la UNAB), el
ítem de ArcGIS no declara licencia explícita, y cada registro enlaza al PDF
original en `portalgeo.sernageomin.cl`, dominio actualmente dado de baja
(no resuelve DNS, verificado el 14-10-2026 — el antiguo "Portal Geomin" ya
no aparece en sernageomin.cl/visores-mineros/). Por eso TODO lo que genera
este script se marca `verification_status="pending_review"`, nunca
`"verified"`.

Este script NO corre automáticamente: es una herramienta manual, ejecutada
a mano cuando se quiera refrescar `services/api/app/data/sernageomin_unab_catalog_sjm.json`.
No hay ingesta en vivo de esta fuente.

Uso:
    python pipelines/sernageomin_unab_catalog/fetch_and_filter.py

Requiere `requests` (no está en requirements.txt de la API porque esto no
corre en producción; instalar con `pip install requests` para ejecutarlo).
"""
from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import requests

SERVICE_URL = (
    "https://services3.arcgis.com/uZrwedu11XCCdHk1/arcgis/rest/services/"
    "Catastro_de_remociones_en_masa_Sernageomin/FeatureServer/0/query"
)

# Bounding box piloto (debe coincidir con services/api/app/config.py).
PILOT_BBOX = {"min_lat": -34.30, "max_lat": -33.55, "min_lon": -70.45, "max_lon": -69.75}

# Palabras clave de localidades inequívocamente dentro de la comuna de San
# José de Maipo / Cajón del Maipo. Deliberadamente NO se incluyen nombres
# genéricos que podrían repetirse en otras comunas de Chile.
KEYWORDS: dict[str, str] = {
    "san jose de maipo": "San José de Maipo",
    "cajon del maipo": "Cajón del Maipo",
    "banos morales": "Baños Morales",
    "san alfonso": "San Alfonso",
    "san gabriel": "San Gabriel (Cajón del Maipo)",
    "el volcan": "El Volcán",
    "lo valdes": "Lo Valdés",
    "melocoton": "Melocotón",
    "los maitenes": "Los Maitenes (Cajón del Maipo)",
    "guayacan": "Guayacán (Cajón del Maipo)",
    "queltehues": "Queltehues",
    "estero yeso": "Estero/Río Yeso",
    "rio volcan": "Río Volcán",
    "rio yeso": "Río Yeso",
    "rio colorado": "Río Colorado (afluente del Maipo)",
}

MONTH_NUMBERS = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12",
}

HAZARD_MAP = {
    "Flujo": "aluvion",
    "Deslizamiento": "remocion_en_masa",
    "Caída": "remocion_en_masa",
    "Caida": "remocion_en_masa",
    "Propagación": "remocion_en_masa",
    "Propagacion": "remocion_en_masa",
    "Deformaciones de ladera": "remocion_en_masa",
}


def _strip_accents(value: str) -> str:
    if not value:
        return ""
    return "".join(c for c in unicodedata.normalize("NFD", value) if unicodedata.category(c) != "Mn").lower()


def _format_date(attrs: dict) -> str:
    year = attrs.get("Año_del_evento") or 0
    month_raw = (attrs.get("Mes_de_inicio_del_evento") or "").strip()
    day_raw = (attrs.get("Dia_del_evento") or "").strip()

    if not year:
        return "Año no especificado en la fuente"

    year_str = str(int(year))
    month_key = _strip_accents(month_raw)
    month_num = MONTH_NUMBERS.get(month_key)
    day_is_clean_number = day_raw.isdigit()

    if month_num and day_is_clean_number:
        return f"{year_str}-{month_num}-{int(day_raw):02d}"
    if month_raw and month_raw.lower() != "sin información":
        return f"{year_str}, {month_raw}" + (f" {day_raw}" if day_raw and day_raw.lower() != "sin información" else "")
    return f"{year_str} (mes/día no especificados en la fuente)"


def _match_keyword(attrs: dict) -> str | None:
    haystack = _strip_accents(" ".join(str(attrs.get(k) or "") for k in (
        "Fuente_de_la_informacion", "Nota", "Estacion_de_ocurrencia_del_even",
    )))
    for key, label in KEYWORDS.items():
        if key in haystack:
            return label
    return None


def fetch_raw() -> list[dict]:
    where = (
        f"Latitud >= {PILOT_BBOX['min_lat']} AND Latitud <= {PILOT_BBOX['max_lat']} "
        f"AND Longitud >= {PILOT_BBOX['min_lon']} AND Longitud <= {PILOT_BBOX['max_lon']}"
    )
    response = requests.get(
        SERVICE_URL,
        params={"where": where, "outFields": "*", "f": "json", "resultRecordCount": 1000},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return [f["attributes"] for f in payload.get("features", [])]


def transform(attrs: dict, locality_label: str) -> dict:
    precision = (attrs.get("Precision_de_coordenadas") or "").strip()
    location_certainty = "approximate" if precision == "Coordenadas exactas" else "unverified_candidate"
    radius_km = 2 if precision == "Coordenadas exactas" else 6

    hazard_raw = (attrs.get("Tipo_de_remocion_en_masa") or "").strip()
    hazard_type = HAZARD_MAP.get(hazard_raw, "remocion_en_masa")

    enlace = attrs.get("Enlace_de_documento_asociado") or ""
    fuente = attrs.get("Fuente_de_la_informacion") or "(sin cita registrada)"
    detonante = attrs.get("Detonante") or "no especificado"
    tipo_material = attrs.get("Tipo_de_material") or "no especificado"

    return {
        "id": f"unab-sernageomin-{attrs.get('Codigo_de_la_remocion_en_masa')}",
        "date": _format_date(attrs),
        "approx_location": {
            "lat": attrs.get("Latitud"),
            "lon": attrs.get("Longitud"),
            "place": locality_label,
            "radius_km": radius_km,
        },
        "hazard_type": hazard_type,
        "source": (
            f"Catálogo de remociones en masa (compilación de terceros, Universidad Andrés "
            f"Bello, vía ArcGIS Online, no es un canal oficial de SERNAGEOMIN): {fuente}. "
            f"Informe original citado: {enlace} — enlace actualmente inaccesible (el dominio "
            f"portalgeo.sernageomin.cl está dado de baja; verificado 14-10-2026)."
        ),
        "location_certainty": location_certainty,
        "verification_status": "pending_review",
        "notes": (
            f"Tipo original SERNAGEOMIN: '{hazard_raw}'. Detonante registrado: {detonante}. "
            f"Material: {tipo_material}. Código SERNAGEOMIN: {attrs.get('Codigo_de_la_remocion_en_masa')}. "
            "Pendiente de confirmación directa: la licencia de reuso de este catálogo no está "
            "declarada y el informe original no es verificable mientras el dominio esté caído."
        ),
    }


# Informes ya cubiertos a mano con mayor rigor en app/events_data.py (evitar
# duplicar el mismo informe como entrada "pending_review" granular y como
# entrada "verified" resumida). Ver docs/DECISIONES.md.
EXCLUDED_REPORT_PREFIXES = (
    "RM-2017-23",  # ya cubierto por sjm-2017-02-quebrada-san-jose (verified)
)


def main() -> None:
    raw = fetch_raw()
    print(f"Registros en bbox piloto: {len(raw)}")

    records = []
    skipped_duplicates = 0
    for attrs in raw:
        locality = _match_keyword(attrs)
        if not locality:
            continue
        code = str(attrs.get("Codigo_de_la_remocion_en_masa") or "")
        if code.startswith(EXCLUDED_REPORT_PREFIXES):
            skipped_duplicates += 1
            continue
        records.append(transform(attrs, locality))

    print(f"Omitidos por duplicar un informe ya cubierto a mano: {skipped_duplicates}")

    print(f"Registros con localidad de San José de Maipo/Cajón del Maipo confirmada: {len(records)}")

    out_path = Path(__file__).resolve().parents[2] / "services" / "api" / "app" / "data" / "sernageomin_unab_catalog_sjm.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)
    print(f"Escrito: {out_path}")


if __name__ == "__main__":
    main()
