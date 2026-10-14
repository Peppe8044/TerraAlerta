# Decisiones, bloqueos y próximos pasos — 14-10-2026

Este documento es el entregable 7 de `docs/CLAUDE_CODE.md`. Registra lo implementado en este sprint, lo bloqueado y la investigación pendiente. No reemplaza los gates de `docs/AUDITORIA_MVP_2026-10-14.md`.

## Qué se implementó

- Monorepo: `apps/web` (Next.js 15 + TypeScript + MapLibre), `services/api` (FastAPI), `infra` (Docker Compose), `pipelines` (stubs), `tests` (puntero), `docs`.
- Backend con cobertura geográfica restringida a San José de Maipo (bounding box aproximado, ver `services/api/app/config.py`), endpoints `/health`, `/v1/sources`, `/v1/locations/summary`, `/v1/precipitation/forecast`, `/v1/rain/observed`, `/v1/terrain/profile`, `/v1/events` (vacío, auditado), `/v1/preparedness` (borrador editorial).
- Único proveedor de datos **real** integrado: Open-Meteo (pronóstico + elevación), no comercial, sin clave. Verificado con consultas reales durante el desarrollo (ver `docs/FUENTES_ESTADO.md`), incluyendo un caso real de fallo (503 transitorio en el endpoint de elevación) que el sistema manejó devolviendo `quality_flag="unavailable"` en vez de inventar un valor.
- Frontend con mapa navegable (MapLibre + tiles OSM de demostración), selección de punto restringida a la zona piloto, panel de trazabilidad por indicador (fuente, unidad, fecha, resolución, limitaciones), panel «Por qué veo esto» con enlace a SENAPRED, y checklist de preparación.
- 20 tests backend (pytest, sin red real — usan fixtures sintéticas marcadas explícitamente) y 5 tests frontend (vitest) sobre lógica pura (estado de datos, cobertura geográfica). Lint limpio (`ruff`, `next lint`, `tsc --noEmit`). Build de producción de Next.js verificado.
- CI (GitHub Actions) para backend y frontend.

## Bloqueado / no implementado (y por qué)

- **NASA IMERG**: requiere cuenta NASA Earthdata; no se gestionó en este sprint. Queda en `research_only` en `services/api/app/sources.py`.
- **Copernicus DEM GLO-30/GLO-90** (para pendiente real del terreno): GLO-30 exige registro CCM desde julio 2026. El endpoint `/v1/terrain/profile` expone `slope` como `unavailable` explícito — nunca inventado.
- **DGA / DMC** (estaciones hidrométricas y observación local): sin verificación de API/licencia. No implementado (ver `docs/ROADMAP_VALOR_CIUDADANO.md` capacidad 2).
- **SERNAGEOMIN** (inventario de remociones en masa): sin verificación de acceso WMS/WFS. No implementado.
- **Eventos históricos**: el endpoint existe pero deliberadamente vacío — no hay aún un conjunto de eventos corroborados y geolocalizados.
- **ML de aluviones, puntajes de riesgo, rutas de evacuación, notificaciones push**: fuera de alcance por decisión explícita de los documentos de producto; no se tocó este sprint.
- **Contenido SENAPRED**: el checklist de `/v1/preparedness` es un borrador editorial propio pendiente de revisión/cita literal contra el texto oficial vigente (gate G4). No usar en producción sin esa revisión.

## Deuda técnica conocida

- El bounding box de cobertura es una aproximación operativa, no la geometría administrativa oficial de la comuna. Reemplazar por la capa oficial (INE/BCN) antes de ampliar cobertura.
- Vulnerabilidades residuales de `npm audit` en herramientas de desarrollo (ESLint/lint tooling vía `fast-glob`/`braces`/`micromatch`, y `postcss` transitivo vía Next.js 15) sin parche estable disponible sin saltar a Next.js 16 (cambio mayor). No afectan el bundle servido a usuarios. Revisar al planificar la migración a Next 16.
- No hay base de datos poblada: PostGIS está en `docker-compose.yml` como scaffolding para capas futuras (quebradas, eventos, DEM), pero el MVP actual no depende de ella para servir indicadores.
- Tiles de mapa: se usan tiles de demostración de OpenStreetMap (`tile.openstreetmap.org`), válidos solo para bajo tráfico según su [política de uso](https://operations.osmfoundation.org/policies/tiles/). Antes de tráfico real, migrar a un proveedor de tiles propio o con licencia.

## Próximos pasos de investigación (no implementar sin pasar gates)

1. Gestionar cuenta NASA Earthdata y medir latencia/cobertura real de IMERG para Chile central (gate G1/G2).
2. Verificar condiciones de reutilización y API de DGA/DMC para al menos una estación cercana a San José de Maipo.
3. Completar registro Copernicus CCM para DEM GLO-30 y evaluar si la resolución basta para pendiente a escala de ladera (no de vivienda).
4. Revisión editorial línea a línea del checklist de preparación contra el texto vigente de SENAPRED, con fecha de versión.
5. Definir el esquema y la fuente auditada para el primer lote de eventos históricos documentados (SERNAGEOMIN/SENAPRED), sin incorporar aún el caso de Las Condes (octubre 2026) marcado como candidato por verificar en `docs/ALUVIONES_Y_PREVENCION.md`.
