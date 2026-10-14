"""Registro de fuentes (ver docs/DATOS.md y docs/FUENTES_ESTADO.md).

Este módulo es la única fuente de verdad en código sobre qué conectores
están habilitados (`approved`) frente a los que permanecen `pending`,
`research_only` o `blocked`. Un router NUNCA debe exponer datos de una
fuente que no figure aquí como `approved`.
"""
from __future__ import annotations

from app.schemas import SourceInfo

SOURCES: dict[str, SourceInfo] = {
    "open_meteo_forecast": SourceInfo(
        dataset="Open-Meteo Forecast API (modelo numérico, no estación DMC)",
        owner="Open-Meteo.com",
        url="https://open-meteo.com/en/terms",
        license_status="approved",
        retrieval_mode="API HTTP pública, sin clave, uso no comercial",
        last_verified="2026-10-14",
        notes=(
            "Datos de modelo numérico (reanálisis/NWP), no observación directa de "
            "pluviómetro. Verificar términos antes de cualquier uso comercial. "
            "Resolución de modelo (~p. ej. ERA5/ICON, variable por celda), no "
            "equivale a lluvia exacta sobre una parcela."
        ),
    ),
    "open_meteo_elevation": SourceInfo(
        dataset="Open-Meteo Elevation API (derivado de Copernicus DEM GLO-90)",
        owner="Open-Meteo.com",
        url="https://open-meteo.com/en/docs/elevation-api",
        license_status="approved",
        retrieval_mode="API HTTP pública, sin clave, uso no comercial",
        last_verified="2026-10-14",
        notes="Entrega solo elevación puntual; no calcula pendiente. Resolución ~90 m.",
    ),
    "nasa_imerg": SourceInfo(
        dataset="NASA GPM IMERG",
        owner="NASA",
        url="https://gpm.nasa.gov/data/imerg",
        license_status="research_only",
        retrieval_mode="Requiere cuenta NASA Earthdata; sin ingesta automatizada en este MVP",
        last_verified="2026-10-14",
        notes="Resolución ~0.1°; producto Early es diferido. Pendiente validar latencia/cobertura (gate G1/G2).",
    ),
    "nasa_lhasa": SourceInfo(
        dataset="NASA LHASA",
        owner="NASA",
        url="https://github.com/nasa/lhasa",
        license_status="research_only",
        retrieval_mode="Repositorio de referencia; sin proceso de reentrenamiento local",
        last_verified="2026-10-14",
        notes="Solo como referencia comparativa en investigación; no es veredicto operativo (ver docs/VALIDACION.md).",
    ),
    "copernicus_dem": SourceInfo(
        dataset="Copernicus DEM GLO-30/GLO-90",
        owner="Copernicus / ESA",
        url="https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/DEM.html",
        license_status="pending",
        retrieval_mode="GLO-30 requiere registro CCM (desde julio 2026); sin integración directa aún",
        last_verified="2026-10-14",
        notes="Modelo de superficie, no levantamiento detallado del terreno. Pendiente de verificar licencia de redistribución.",
    ),
    "dga": SourceInfo(
        dataset="DGA — estaciones hidrométricas",
        owner="Dirección General de Aguas, MOP",
        url="https://dga.mop.gob.cl/",
        license_status="pending",
        retrieval_mode="Pendiente verificar API/descarga, cobertura por estación y condiciones de reutilización",
        last_verified="2026-10-14",
        notes="No habilitado en este MVP. Ver docs/ROADMAP_VALOR_CIUDADANO.md capacidad 2.",
    ),
    "dmc": SourceInfo(
        dataset="DMC — observaciones meteorológicas",
        owner="Dirección Meteorológica de Chile",
        url="https://www.meteochile.gob.cl/",
        license_status="pending",
        retrieval_mode="Pendiente verificar API disponible y derechos de reutilización",
        last_verified="2026-10-14",
        notes="No habilitado en este MVP.",
    ),
    "sernageomin": SourceInfo(
        dataset="SERNAGEOMIN — inventario de remociones en masa / cartografía de amenazas",
        owner="Servicio Nacional de Geología y Minería",
        url="https://portalgeomin.sernageomin.cl/",
        license_status="pending",
        retrieval_mode="Pendiente verificar WMS/WFS/descarga, escala y vigencia",
        last_verified="2026-10-14",
        notes="No habilitado en este MVP. Mostrar como referencia, nunca como clasificación automática de viviendas.",
    ),
    "sernageomin_unab_catalog": SourceInfo(
        dataset=(
            "Catastro de remociones en masa (compilación de terceros, Universidad Andrés Bello, "
            "vía ArcGIS Online, citando informes SERNAGEOMIN)"
        ),
        owner="Investigadora independiente (Universidad Andrés Bello), citando informes de SERNAGEOMIN",
        url=(
            "https://services3.arcgis.com/uZrwedu11XCCdHk1/arcgis/rest/services/"
            "Catastro_de_remociones_en_masa_Sernageomin/FeatureServer"
        ),
        license_status="pending",
        retrieval_mode=(
            "API REST pública de ArcGIS Online, sin autenticación, consultada vía "
            "pipelines/sernageomin_unab_catalog/fetch_and_filter.py (ejecución manual, no en vivo)"
        ),
        last_verified="2026-10-14",
        notes=(
            "NO es un canal oficial de SERNAGEOMIN: el ítem de ArcGIS no declara licencia explícita "
            "de reuso ('no se han proporcionado restricciones'), y cada registro cita un informe "
            "original en portalgeo.sernageomin.cl, dominio actualmente dado de baja (no resuelve "
            "DNS; el antiguo 'Portal Geomin' ya no aparece en sernageomin.cl/visores-mineros/). "
            "Por eso todos los eventos importados de esta fuente llevan "
            "verification_status='pending_review', nunca 'verified'. Pendiente: contactar a la "
            "autora o a SERNAGEOMIN para confirmar licencia y ubicación actual de los informes PDF."
        ),
    ),
    "senapred_preparedness": SourceInfo(
        dataset="SENAPRED — orientación de preparación ante aluviones/lluvias intensas",
        owner="Servicio Nacional de Prevención y Respuesta ante Desastres",
        url="https://www.senapred.cl/",
        license_status="pending",
        retrieval_mode="Contenido editorial propio, pendiente de revisión/cita literal contra el texto oficial vigente",
        last_verified="2026-10-14",
        notes=(
            "El checklist incluido en /v1/preparedness es un borrador genérico marcado como "
            "pendiente de revisión editorial (gate G4). No reemplaza al sitio oficial."
        ),
    ),
    "google_flood_hub": SourceInfo(
        dataset="Google Flood Hub",
        owner="Google Research",
        url="https://sites.research.google/gr/floodforecasting/",
        license_status="blocked",
        retrieval_mode="API requiere autorización no obtenida",
        last_verified="2026-10-14",
        notes="No es dependencia del MVP (ver docs/AUDITORIA_MVP_2026-10-14.md).",
    ),
    "copernicus_glofas": SourceInfo(
        dataset="Copernicus GloFAS",
        owner="Copernicus Emergency Management Service",
        url="https://global-flood.emergency.copernicus.eu/",
        license_status="blocked",
        retrieval_mode="No integrado en este MVP",
        last_verified="2026-10-14",
        notes="Referencia de crecidas a gran escala; no equivale a mapa de inundación de parcela.",
    ),
}


def list_sources() -> list[SourceInfo]:
    return list(SOURCES.values())
