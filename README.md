# TerraAlerta Chile

**Estado:** MVP experimental implementado (prototipo auditable). **Fecha:** 14 de octubre de 2026.

TerraAlerta Chile es una plataforma experimental de inteligencia territorial que combina lluvia observada, pronóstico y características geográficas para explicar **condiciones que pueden aumentar la vulnerabilidad frente a lluvias extremas y deslizamientos**. No predice inundaciones a nivel de vivienda, no emite alertas oficiales y no sustituye a SENAPRED.

## Alcance MVP

Piloto: **San José de Maipo, Región Metropolitana**. Aplicación web adaptada a móviles. Seleccionar punto en mapa y ver: pronóstico de lluvia a 24/48/72 h, lluvia reciente (cuando haya fuente válida), pendiente y proximidad a drenajes/cursos de agua, procedencia/actualización de cada dato, y ficha de condiciones observadas con incertidumbres. La evaluación inicial será **descriptiva**, no una probabilidad calibrada de desastre. Un módulo experimental de deslizamientos podrá incorporarse solo después de validar cobertura y resultados.

## Estructura del monorepo

```
apps/web/        Next.js 15 + TypeScript + MapLibre (frontend)
services/api/    FastAPI + Pydantic (backend)
infra/           docker-compose.yml (Postgres/PostGIS + api + web)
pipelines/       Stubs de ingesta (ninguno activado — ver pipelines/README.md)
tests/           Puntero a las suites de cada paquete
docs/            Especificación, gobernanza de datos y decisiones
```

## Cómo correrlo

**Backend:**
```
cd services/api
python -m venv .venv && source .venv/Scripts/activate   # o .venv/bin/activate en Linux/Mac
pip install -r requirements-dev.txt
pytest -q                 # 20 tests, sin red real
uvicorn app.main:app --reload
```

**Frontend:**
```
cd apps/web
npm install
npm test                  # vitest, lógica pura
npm run dev               # http://localhost:3000, requiere la API en :8000
```

**Con Docker Compose:**
```
cp .env.example .env
docker compose -f infra/docker-compose.yml up --build
```

Solo **Open-Meteo** (pronóstico y elevación) está integrado como fuente real y aprobada para este
MVP no comercial; el resto de fuentes (IMERG, DEM, DGA, DMC, SERNAGEOMIN) permanece deshabilitado
hasta verificar licencia y cobertura — ver [docs/FUENTES_ESTADO.md](docs/FUENTES_ESTADO.md) y
[docs/DECISIONES.md](docs/DECISIONES.md).

## Primeros pasos con Claude Code

1. Leer `docs/PRODUCTO.md`, `docs/DATOS.md`, `docs/ARQUITECTURA.md`, `docs/VALIDACION.md` y `docs/CLAUDE_CODE.md`.
2. Monorepo creado con `/apps/web`, `/services/api`, `/pipelines`, `/infra`, `/tests`, `/docs`.
3. El demo reproducible actual usa un único conector real (Open-Meteo); fixtures sintéticas solo en tests, nunca en la UI.
4. En ningún entorno mostrar una puntuación de riesgo numérica no validada.
5. Usar secretos mediante variables de entorno; nunca incluir credenciales o coordenadas de predios privados en el repositorio.

## Licencia

No se ha elegido aún licencia para el código original. No asumir que las licencias de terceros se extienden automáticamente al código o a productos derivados. Consultar `docs/DATOS.md`.

## Extensión preventiva: aluviones

El roadmap de lluvia intensa, cartografía de quebradas, eventos históricos, preparación ciudadana, futuras notificaciones y reportes se documenta en [docs/ALUVIONES_Y_PREVENCION.md](docs/ALUVIONES_Y_PREVENCION.md). Los niveles P0/P1/P2 separan funciones implementables de hipótesis que exigen evaluación adicional.

## Auditoría de confiabilidad

Antes de implementar o publicar nuevas capacidades, consultar [Auditoría MVP y matriz de implementabilidad](docs/AUDITORIA_MVP_2026-10-14.md). Distingue componentes implementables ahora, condicionados a disponibilidad/licencia y funciones de investigación no aptas para alertas operativas.

## Nuevos módulos ciudadanos

Consultar [Roadmap de valor ciudadano](docs/ROADMAP_VALOR_CIUDADANO.md): plan familiar/terreno, monitoreo hidrológico DGA, comparaciones históricas, radar Sentinel-1, preparación contextual y asistente explicativo. Las fases y restricciones de confiabilidad se documentan allí.
