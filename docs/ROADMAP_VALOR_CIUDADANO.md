# Roadmap de valor ciudadano y nuevas capacidades

**Fecha:** 14-10-2026. **Estado:** especificación, no implementación.

El objetivo sigue siendo prevención climática y territorial ante precipitaciones, crecidas, inundaciones y remociones en masa en Chile; la primera zona piloto es San José de Maipo. Estos módulos **complementan**, no reemplazan, `ALUVIONES_Y_PREVENCION.md` ni la auditoría del MVP. Reutilizar componentes existentes.

## Priorización y seis capacidades

| Capacidad | Fase | Dependencia | Resultado observable |
|---|---|---|---|
| 1. Mi familia y mi terreno | MVP: checklist local sin cuenta; P1: predio/familia privados | Recomendaciones SENAPRED, privacidad | Plan descargable/editable local; no almacenarlo en servidor por defecto |
| 2. Ríos y esteros | MVP si DGA tiene estación accesible; si no, vista «sin cobertura» | Catálogo DGA, frecuencia y permisos API | Gráfico con caudal/nivel, unidad, estación, fecha, rezago y distancia; sin extrapolar a la casa |
| 3. Comparador histórico de lluvias | MVP de investigación si hay serie comparable; sin datos, se omite | Históricos DGA/DMC/CR2/IMERG y homogeneidad | Percentiles/anomalías descriptivas con período de referencia, cobertura e incertidumbre |
| 4. Inundación observada por radar | P2 investigación | Sentinel-1, disponibilidad de escenas, licencias, validación | Mapas retrospectivos identificados como observaciones satelitales probables, no «ahora» |
| 5. Preparación contextual | MVP usando SENAPRED, sin consejos inventados | Contenido oficial versionado y revisado | Checklist según amenaza, señales, enlaces oficiales, accesible sin conexión si descargado |
| 6. Asistente explicativo con IA | P1/P2 tras validación | Corpus versionado, citas, filtros de respuestas y pruebas | Preguntas como «qué significa isoterma cero», citas y negativa a predecir daños individuales |

## Recorridos de usuarios

**Plan familiar:** entra sin cuenta → elige amenaza (aluvión, lluvia intensa, inundación) → revisa preparación SENAPRED → marca checklist → exporta PDF o almacena localmente. Si se incorporan miembros de familia o coordenadas exactas, consentimiento separado y controles de borrado.

**Monitoreo DGA:** selecciona ubicación → aplicación muestra estaciones con posición conocida y distancias → elige estación → ve serie observada en su unidad original (m³/s para caudal o m para nivel según sensor), timestamp y rezago → advertencia visible: una estación no predice por sí sola la inundación de su propiedad. Evitar semáforos de seguridad basados en umbrales inventados.

**Comparador histórico:** elige comuna/estación y ventana temporal → verifica continuidad y homogeneidad de serie → muestra acumulado, referencia histórica de misma estación/fuente y percentil solo con tamaño de muestra suficiente → etiqueta «comparación descriptiva, no pronóstico de aluvión». No mezclar escalas de IMERG y pluviómetros como si fueran equivalentes.

**Radar de inundaciones (investigación):** elige evento fechado → busca escenas aptas antes/después → segmenta señal posible de agua → muestra máscara y zonas de incertidumbre, sombras radar, vegetación y falsos positivos → contraste con productos o evidencias independientes antes de publicar. Nunca inferir afectación exacta de una vivienda.

**Asistente IA:** pregunta → recupera únicamente material autorizado/versionado → responde en lenguaje claro y cita fuente/fecha → distingue observación, pronóstico e hipótesis → ante emergencias deriva a fuentes oficiales y a servicios de emergencia, no genera rutas de evacuación propias.

## Contratos de datos candidatos

- `GET /v1/hydro/stations?bbox=`: id, nombre, coordenadas, variable, unidad, autoridad, actualización.
- `GET /v1/hydro/stations/{id}/observations?from=&to=`: serie, valor, unidad, timestamp, flags y calidad.
- `GET /v1/rain/climatology?location=&period=`: base temporal, tamaño muestral, estadísticas, fuentes y advertencias.
- `GET /v1/preparedness/checklists?hazard=`: contenido SENAPRED versionado, fuente y fecha de revisión.
- `POST /v1/assistant/explain` **solo P1**: consulta contextual sin datos privados no consentidos, respuestas con referencias; diseñar y aprobar antes de activar.
- Registro predial y perfiles de familia solo en P1, evitando almacenar datos personales en MVP.

## Puertas y pruebas obligatorias

- DGA: comprobar acceso legal a cada endpoint o descarga, variable, frecuencia, latencia, continuidad, calidad y cobertura; si no hay datos recientes, mostrar «sin observaciones recientes».
- Comparador histórico: reportar fecha de referencia, años efectivos de muestra, discontinuidades y sesgo; abstenerse ante series insuficientes.
- Familia: accesibilidad, persistencia local y privacidad; recomendaciones oficiales no equivalen a evacuación.
- IA: referencias obligatorias, respuestas ante preguntas adversariales, alucinaciones y seguridad; no entregar certeza donde faltan mediciones.
- Radar: evaluar falsos positivos y negativos contra observaciones y escenas terrestres independientes.
- Si una capacidad no supera requisitos, deshabilitarla sin datos sintéticos visibles al público.

## Restricciones de lanzamiento

No declarar riesgo «bajo/seguro» en una casa, emitir alarmas oficiales, confirmar afectación por satélite sin corroboración, ni prometer modelos ML validados. Priorizar la claridad para ciudadanos sobre complejidad analítica.

## Referencias iniciales a verificar por conjunto antes de integración

DGA: https://dga.mop.gob.cl/ ; SENAPRED: https://www.senapred.cl/ ; Sentinel-1 / Copernicus: https://dataspace.copernicus.eu/ ; DMC: https://www.meteochile.gob.cl/ ; CR2: https://explorador.cr2.cl/

Estas direcciones son puntos de partida, no autorizaciones automáticas para extracción o redistribución.
