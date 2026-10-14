# Producto y casos de uso

## Problema

Pronósticos y mapas geográficos existen, pero la población necesita una explicación entendible de qué factores del entorno conviene vigilar. No confundir esta necesidad con tener capacidad probada de pronosticar pérdidas concretas.

## Usuarios del MVP

Residentes de la Región Metropolitana interesados en lluvias intensas y condiciones de su entorno; investigadores que quieran inspeccionar las fuentes y su trazabilidad.

## Flujo principal

1. Usuario entra sin cuenta y acepta o rechaza geolocalización.
2. Si no acepta, escribe comuna o mueve el mapa.
3. Toca un punto en San José de Maipo.
4. App carga información observada y pronosticada y muestra hora, unidad, procedencia y cobertura espacial.
5. App muestra pendientes, datos hidrográficos y factores relevantes **solo donde exista suficiente calidad**.
6. App comunica: `datos suficientes / datos parciales / información no disponible`, sin usar etiquetas de seguridad engañosas.
7. Usuario abre «Por qué veo esto» y encuentra evidencias, limitaciones y links a SENAPRED/DMC.

## Fuera del MVP

Alertas push de evacuación, clasificación de seguridad de viviendas, daños económicos, modelos GAN/LLM que inventen valores, identificación de especies de pastos, gestión de ganado, inteligencia de parcela y pagos; posibles fases posteriores sujetas a investigación de datos y demanda.

## Aceptación

Interfaz móvil legible, no exige cuenta, capa de mapa funcional, timestamps visibles, trazabilidad por indicador, tratamiento explícito de fallos/latencia, accesibilidad, español chileno, aviso de carácter experimental.

## Extensión de prevención ante aluviones (14-10-2026)

El MVP incorpora consulta de precipitaciones observadas/previstas, capas de susceptibilidad geográfica donde sean legítimas y fiables, historial documentado de eventos y orientación preventiva oficial. Las notificaciones, reportes ciudadanos y fichas de predios quedan para fases posteriores. Ver [ALUVIONES_Y_PREVENCION.md](ALUVIONES_Y_PREVENCION.md). La lista inicial de «Fuera del MVP» sigue aplicando a notificaciones automáticas, alertas de evacuación y predicción puntual.

## Nuevos casos de uso ciudadanos

Se incorporan planificación familiar sin cuenta, observaciones hidrológicas por estación, comparación histórica de precipitación, preparación contextual, y como fases de investigación radar de inundaciones y asistente de IA. La extensión detallada, dependencias y criterios de aceptación están en [ROADMAP_VALOR_CIUDADANO.md](ROADMAP_VALOR_CIUDADANO.md). El registro persistente de predios sigue fuera del MVP para proteger datos personales.
