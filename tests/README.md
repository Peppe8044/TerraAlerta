# Tests

Las suites de pruebas viven junto a cada paquete, no en este directorio:

- Backend: [`services/api/tests`](../services/api/tests) (pytest). Ejecutar con:
  ```
  cd services/api
  pip install -r requirements-dev.txt
  pytest -q
  ```
- Frontend: [`apps/web/src/**/*.test.ts`](../apps/web/src) (vitest). Ejecutar con:
  ```
  cd apps/web
  npm install
  npm test
  ```

Este directorio raíz queda como punto de entrada documental para quien busque "tests" desde la
raíz del monorepo (ver `docs/CLAUDE_CODE.md`, paso 2 de estructura). El pipeline de CI
(`.github/workflows/ci.yml`) ejecuta ambas suites en cada push/PR.
