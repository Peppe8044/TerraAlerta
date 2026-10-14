"""Configuración centralizada de la API.

No se definen aquí credenciales reales: todo valor sensible debe llegar por
variable de entorno (ver `.env.example`). Ningún valor por defecto habilita
una fuente de pago.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "TerraAlerta Chile API"
    environment: str = "development"
    timezone: str = "America/Santiago"

    # Proveedor de pronóstico no comercial (ver docs/DATOS.md y
    # docs/AUDITORIA_MVP_2026-10-14.md). Sin clave de API.
    open_meteo_base_url: str = "https://api.open-meteo.com/v1"
    open_meteo_timeout_seconds: float = 10.0

    # Zona piloto: San José de Maipo. Bounding box aproximado (no es límite
    # administrativo oficial); ver docs/DECISIONES.md.
    pilot_bbox_min_lat: float = -34.30
    pilot_bbox_max_lat: float = -33.55
    pilot_bbox_min_lon: float = -70.45
    pilot_bbox_max_lon: float = -69.75

    cache_ttl_seconds: int = 1800


@lru_cache
def get_settings() -> Settings:
    return Settings()
