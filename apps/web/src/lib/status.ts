import type { DataStatus } from "./types";

// Textos visibles al usuario para cada estado de datos. Deliberadamente NO
// se usan etiquetas de seguridad ("seguro"/"peligro"): ver docs/PRODUCTO.md
// y docs/AUDITORIA_MVP_2026-10-14.md.
export const STATUS_LABELS: Record<DataStatus, string> = {
  sufficient_data: "Datos suficientes",
  partial_data: "Datos parciales",
  unavailable: "Información no disponible",
};

export function statusLabel(status: DataStatus): string {
  return STATUS_LABELS[status] ?? "Información no disponible";
}
