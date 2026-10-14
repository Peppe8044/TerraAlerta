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

## Segunda ronda: panel de fuentes, visor de eventos y primer evento verificado

Tras el merge del MVP inicial (PR #1), se cerraron dos brechas detectadas al revisar el cumplimiento contra la auditoría:

1. **Panel "¿De dónde viene este dato?" en el frontend** (`apps/web/src/components/SourcesPanel.tsx`): el backend `/v1/sources` existía desde el PR #1, pero ninguna pantalla lo mostraba. Es el entregable 2 explícito de `docs/AUDITORIA_MVP_2026-10-14.md`. Ahora lista las 11 fuentes registradas (incluidas las `pending`/`research_only`/`blocked`), con su estado de licencia, dueño y notas.
2. **Visor de eventos históricos en el frontend** (`apps/web/src/components/EventsViewer.tsx`): el endpoint `/v1/events` existía pero ningún componente lo consumía.
3. **Primer evento histórico verificado** (`services/api/app/events_data.py`): se investigó con fuentes abiertas y se incorporó el aluvión del 25 de febrero de 2017 en la quebrada/estero San José (San José de Maipo), documentado oficialmente en el informe técnico SERNAGEOMIN RM-2017-23 (https://portalgeo.sernageomin.cl/Informes_PDF_Nac/RM-2017-23.pdf). Es un catálogo **curado a mano, no un scraper**: cada entrada exige una fuente oficial citable.
   - Se marcó `location_certainty="approximate"` (coordenada a nivel de localidad, no la coordenada exacta de la quebrada, que no se verificó) y `verification_status="verified"` (respaldado por informe técnico oficial, no solo prensa).
   - Deliberadamente **no** se incluyó el conteo de víctimas: las cifras de prensa consultadas (The Clinic, Meganoticias, agencias) difieren entre sí, y ese dato no es necesario para un registro de amenaza geológica.
   - Deliberadamente **no** se incorporaron otros antecedentes encontrados en cobertura secundaria (aluviones de 1980 en ríos Mapocho/Maipo/Yeso/Colorado, aluvión de Las Amarillas 1991, remociones de Avenida El Carmen 2012): no se pudo confirmar con una fuente primaria que hayan ocurrido dentro de los límites de la comuna de San José de Maipo. Queda como investigación pendiente.
   - Se respetó explícitamente la instrucción de `docs/ALUVIONES_Y_PREVENCION.md`: el evento de Las Condes de octubre de 2026 sigue **excluido** por no tener localización verificada; hay un test (`test_events_does_not_include_unverified_las_condes_2026_candidate`) que falla si alguien lo agrega sin pasar por esa verificación.

Backend: 27 tests (antes 26). Frontend: 5 tests (sin cambio; los dos componentes nuevos son de solo lectura y se probaron manualmente contra la API real, ver más abajo). Lint y build verificados tras los cambios.

## Correcciones tras revisión automatizada (PR #1, Codex)

El bot de revisión de código del repositorio (`chatgpt-codex-connector`) señaló 6 hallazgos reales sobre el primer commit del MVP. Todos se corrigieron antes de mergear:

1. **Ventana de pronóstico mal alineada**: `forecast_days` alinea a medianoche, no a la hora actual — una consulta de "24 h" hecha a media tarde sumaba sobre todo horas ya transcurridas del día en curso. Se cambió a `forecast_hours` (alineado a la hora en curso). Verificado contra la API real: una consulta a las 10:35 local ahora cubre 10:00 de hoy → 09:00 de mañana (24 h exactas desde ahora).
2. **Ventana de "lluvia reciente" mal alineada**: mismo problema con `past_days`. Se cambió a `past_hours` + `forecast_hours=0`. Verificado: una consulta de 6 h a las 10:35 ahora cubre 04:00–09:00 (las 6 horas inmediatamente anteriores), no medianoche–06:00.
3. **Series incompletas/ausentes tratadas como 0 mm `real`**: se añadió `_validate_hourly_series()` en `open_meteo.py`, que lanza `ProviderError` (→ `quality_flag="unavailable"`) si el arreglo de precipitación viene vacío, más corto que el horizonte pedido, o con todos los valores `null`. Antes, cualquiera de esos casos se reportaba silenciosamente como `0 mm` con `quality_flag="real"`.
4. **Guard de cobertura geográfica faltante en 3 endpoints**: `/v1/precipitation/forecast`, `/v1/rain/observed` y `/v1/terrain/profile` no aplicaban `check_coverage()` (solo `/v1/locations/summary` lo hacía), permitiendo consultar cualquier coordenada válida globalmente bajo una app que se presenta como piloto de San José de Maipo. Ahora los tres devuelven 422 fuera de la zona piloto, igual que `/v1/locations/summary`.
5. **`apps/web/Dockerfile` roto**: copiaba `/app/public` pero el proyecto no tenía directorio `public/`, por lo que `docker compose up --build` fallaría en el paso `COPY`. Se agregó `apps/web/public/robots.txt`.
6. **Condición de carrera en el frontend**: si el usuario tocaba el punto A y luego el B antes de que A respondiera, una respuesta tardía de A podía sobrescribir el panel que ya mostraba B. Se agregó un contador de "selección más reciente" (`useRef`) en `src/app/page.tsx` que descarta respuestas de selecciones obsoletas.

Se añadieron 6 tests nuevos en el backend (26 en total) cubriendo los puntos 3 y 4; los puntos 1, 2, 5 y 6 se verificaron manualmente contra la API real de Open-Meteo y con `npm run build` (ver salida de verificación en el historial de este sprint). El build de la imagen Docker del frontend no se ejecutó de extremo a extremo en este entorno (sin Docker Desktop activo), pero se confirmó que las tres rutas que copia el Dockerfile (`.next/standalone`, `.next/static`, `public/`) existen tras `npm run build`.

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
