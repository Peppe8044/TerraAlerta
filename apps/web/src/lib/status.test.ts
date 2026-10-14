import { describe, expect, it } from "vitest";
import { statusLabel } from "./status";

describe("statusLabel", () => {
  it("nunca devuelve una etiqueta de seguridad no validada", () => {
    const labels = [
      statusLabel("sufficient_data"),
      statusLabel("partial_data"),
      statusLabel("unavailable"),
    ];
    for (const label of labels) {
      expect(label.toLowerCase()).not.toContain("seguro");
      expect(label.toLowerCase()).not.toContain("riesgo");
      expect(label.toLowerCase()).not.toContain("peligro");
    }
  });

  it("mapea cada estado de datos a un texto legible", () => {
    expect(statusLabel("sufficient_data")).toBe("Datos suficientes");
    expect(statusLabel("partial_data")).toBe("Datos parciales");
    expect(statusLabel("unavailable")).toBe("Información no disponible");
  });

  it("usa un valor por defecto seguro ante un estado desconocido", () => {
    // @ts-expect-error -- probamos una entrada inválida a propósito
    expect(statusLabel("algo_no_definido")).toBe("Información no disponible");
  });
});
