# Inventario vivo de fuentes — TerraAlerta Chile

**Responsable de mantenimiento:** quien integre o modifique un conector debe actualizar esta tabla en el mismo PR.
Este documento es el entregable 1 del gate de confiabilidad (ver [AUDITORIA_MVP_2026-10-14.md](AUDITORIA_MVP_2026-10-14.md)).
El código fuente de verdad sobre qué conectores están habilitados vive en
[`services/api/app/sources.py`](../services/api/app/sources.py); esta tabla documenta el estado en prosa y el historial de verificación.

| Fuente | `license_status` | Última verificación | Evidencia de consulta de prueba | Responsable |
|---|---|---|---|---|
| Open-Meteo Forecast API | `approved` (no comercial) | 2026-10-14 | `curl https://api.open-meteo.com/v1/forecast?latitude=-33.6378&longitude=-70.3539&hourly=precipitation&forecast_days=3&timezone=America/Santiago` → 200 OK con serie horaria | equipo TerraAlerta |
| Open-Meteo Elevation API | `approved` (no comercial) | 2026-10-14 | `curl https://api.open-meteo.com/v1/elevation?latitude=-33.6378&longitude=-70.3539` → 200 OK (`elevation: [957.0]`). **Nota:** durante pruebas de integración se observó un 503 transitorio; el backend degrada a `quality_flag=unavailable` sin inventar valores. | equipo TerraAlerta |
| NASA GPM IMERG | `research_only` | 2026-10-14 (solo revisión documental) | No se ha probado ingesta real: requiere cuenta NASA Earthdata. Pendiente antes de activar (gate G0/G1). | pendiente de asignar |
| NASA LHASA | `research_only` | 2026-10-14 (solo revisión documental) | Repositorio de referencia; sin ingesta ni reentrenamiento realizado. | pendiente de asignar |
| Copernicus DEM GLO-30/GLO-90 | `pending` | 2026-10-14 (solo revisión documental) | GLO-30 exige registro CCM desde julio 2026; no se ha completado el registro. | pendiente de asignar |
| DGA (estaciones hidrométricas) | `pending` | 2026-10-14 (solo revisión documental) | No se ha verificado API/descarga ni cobertura por estación cercana a San José de Maipo. | pendiente de asignar |
| DMC (observaciones meteorológicas) | `pending` | 2026-10-14 (solo revisión documental) | No se ha verificado API disponible ni derechos de reutilización. | pendiente de asignar |
| SERNAGEOMIN (remociones en masa) | `pending` | 2026-10-14 (solo revisión documental) | No se ha verificado WMS/WFS/descarga, escala ni vigencia. | pendiente de asignar |
| SENAPRED (contenido de preparación) | `pending` | 2026-10-14 | Checklist en `/v1/preparedness` es un **borrador editorial propio**, no una cita literal verificada contra el sitio oficial vigente. | pendiente de asignar |
| Copernicus GloFAS | `blocked` | 2026-10-14 | No es dependencia del MVP. | — |
| Google Flood Hub | `blocked` | 2026-10-14 | API requiere autorización no obtenida. | — |
| SERNAGEOMIN, Informe Registrado RM-2017-23 (evento puntual, no API) | `approved` para cita en `/v1/events` | 2026-10-14 (ver nota de dominio caído abajo) | PDF oficial citado en https://portalgeo.sernageomin.cl/Informes_PDF_Nac/RM-2017-23.pdf; usado como fuente del único evento `verified` cargado (`sjm-2017-02-quebrada-san-jose`). El enlace dejó de responder (ver fila siguiente), pero la cita bibliográfica se conserva. No es un conector ni una API — es una cita documental puntual, ver `services/api/app/events_data.py`. | equipo TerraAlerta |
| Catastro de remociones en masa (compilación de terceros, Universidad Andrés Bello, vía ArcGIS Online) | `pending` | 2026-10-14 | API REST pública sin autenticación: `https://services3.arcgis.com/uZrwedu11XCCdHk1/arcgis/rest/services/Catastro_de_remociones_en_masa_Sernageomin/FeatureServer` — probada en vivo, 2.880 registros nacionales, 218 dentro del bbox piloto, 113 con localidad de San José de Maipo/Cajón del Maipo confirmada por nombre (excluidos los 17 sub-eventos del informe RM-2017-23 ya cubierto a mano). **No es un canal oficial de SERNAGEOMIN** y el ítem de ArcGIS no declara licencia explícita. Todos sus eventos se exponen con `verification_status="pending_review"`, nunca `"verified"` (test `test_only_hand_curated_events_are_marked_verified`). | equipo TerraAlerta |

## Nota de infraestructura: dominio de informes PDF de SERNAGEOMIN caído (14-10-2026)

El antiguo "Portal Geomin" de SERNAGEOMIN, donde se alojaban los informes técnicos PDF citados
por el catastro de remociones en masa (`portalgeomin.sernageomin.cl` y `portalgeo.sernageomin.cl`,
dos subdominios distintos), **ya no resuelve por DNS**. Verificado dos veces de forma
independiente: desde el entorno de este agente y desde la red/navegador del usuario (ambos con
`ERR_NAME_NOT_RESOLVED` / timeout). El sitio actual de SERNAGEOMIN
(`sernageomin.cl/visores-mineros/`) tampoco lista ya un visor de remociones en masa. Esto afecta
a toda cita que use ese dominio (incluida la del evento `verified` de 2017): la cita bibliográfica
se conserva como referencia, pero el enlace no es clicable hoy.

**Antes de integrar nuevas citas de informes SERNAGEOMIN:** confirmar si el archivo se movió a
otra dirección (p. ej. contactando a SERNAGEOMIN directamente) en vez de asumir que el dominio
antiguo sigue vigente.

## Reglas de actualización

1. Un conector solo pasa a `approved` cuando existe evidencia documentada de licencia de uso (o términos públicos verificados) **y** una consulta de prueba real registrada aquí con fecha.
2. Si una fuente deja de responder o cambia sus términos, degradar su estado inmediatamente y registrar la fecha del cambio.
3. Ninguna fuente en `pending`, `research_only` o `blocked` puede exponerse como `quality_flag="real"` en la API (ver pruebas en `services/api/tests/test_sources.py` y `test_locations.py`).
