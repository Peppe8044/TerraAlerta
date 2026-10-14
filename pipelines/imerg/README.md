# Importador IMERG (investigación, no activado)

**Estado:** `research_only` / `blocked` para ingesta automática (ver `docs/FUENTES_ESTADO.md`).

NASA GPM IMERG requiere una cuenta NASA Earthdata para descarga programática. No se ha
gestionado esa cuenta en este sprint, por lo que no existe aquí ningún script de ingesta real.

Antes de escribir código de ingesta:

1. Registrar cuenta Earthdata y documentar el proceso de autenticación (nunca credenciales en
   el repositorio — usar variables de entorno, ver `.env.example`).
2. Confirmar el producto exacto (`Early`/`Late`/`Final`), su latencia real y su licencia de
   redistribución para uso no comercial.
3. Diseñar la ingesta como **reproducible** sobre un intervalo histórico fijo primero (no "en
   vivo"), con datos de prueba marcados `synthetic` separados de cualquier dato real descargado.
4. Solo entonces habilitar el conector en `services/api/app/sources.py` como `approved`.
