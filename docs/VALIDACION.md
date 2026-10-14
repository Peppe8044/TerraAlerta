# Plan de investigación y validación

## Preguntas

1. ¿Cubre cada fuente la zona seleccionada y con qué latencia/calidad?
2. ¿Los indicadores de lluvia observada concuerdan razonablemente con estaciones locales? Comparar períodos coincidentes, escala y sesgos.
3. ¿Las capas de relieve tienen suficiente resolución para una inferencia territorial, sin afirmar seguridad puntual?
4. ¿Existe un conjunto confiable de **eventos y no eventos** de deslizamientos para evaluar un modelo en Chile?

## Diseño

- Identificar períodos históricos de 5–10 episodios para un **smoke test**, y ampliar muestra con eventos/no eventos para evaluación estadística.
- Nunca usar datos posteriores al evento como variables de entrada en una predicción retrospectiva.
- Separación temporal (train/validation/test) y, cuando sea posible, geográfica por cuencas.
- Línea base 1: umbrales de lluvia basados en literatura/locales; línea base 2: pronóstico convencional; LHASA como referencia, no verdad absoluta.
- Métricas según tarea: MAE/RMSE/sesgo (lluvia); precisión-recall, sensibilidad, tasa de falsas alertas y calibración (eventos); cobertura de datos y latencia.
- Publicar limitaciones, intervalos de confianza y protocolo de actualización.

## Puertas de decisión

G0: licencias y permisos trazables. G1: ingesta reproducible y calidad aceptable. G2: comparación retrospectiva honesta con línea base. G3: prueba con usuarios de comprensión. G4: análisis de costos y demanda. **No afirmar que existe un modelo de prevención validado antes de G2/G3.**

## Definición de éxito del MVP

App funciona con datos auténticos de una zona y aporta explicación/trazabilidad útil; NO se exige ni se declara mejora predictiva no demostrada. La expansión a alertas automáticas queda condicionada a validación independiente y revisión de seguridad.
