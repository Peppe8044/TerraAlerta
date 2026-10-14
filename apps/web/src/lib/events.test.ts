import { describe, expect, it } from "vitest";
import { extractYear, sortEvents } from "./events";
import type { EventRecord } from "./types";

function makeEvent(overrides: Partial<EventRecord>): EventRecord {
  return {
    id: "test",
    date: "2020-01-01",
    approx_location: { lat: -33.6, lon: -70.3, place: "test", radius_km: 5 },
    hazard_type: "aluvion",
    source: "SERNAGEOMIN, test",
    location_certainty: "approximate",
    verification_status: "pending_review",
    notes: "",
    ...overrides,
  };
}

describe("extractYear", () => {
  it("extrae el año de una fecha ISO", () => {
    expect(extractYear("2017-02-25")).toBe(2017);
  });

  it("extrae el año de una fecha parcial en texto", () => {
    expect(extractYear("1987, Junio")).toBe(1987);
  });

  it("devuelve 0 cuando no hay año en el texto", () => {
    expect(extractYear("Año no especificado en la fuente")).toBe(0);
  });
});

describe("sortEvents", () => {
  it("ordena del más reciente al más antiguo", () => {
    const events = [
      makeEvent({ id: "old", date: "1991-01-01" }),
      makeEvent({ id: "new", date: "2017-01-01" }),
    ];
    expect(sortEvents(events).map((e) => e.id)).toEqual(["new", "old"]);
  });

  it("dentro del mismo año, pone los verificados antes que los pendientes de revisión", () => {
    const events = [
      makeEvent({ id: "pending", date: "2017-01-01", verification_status: "pending_review" }),
      makeEvent({ id: "verified", date: "2017-06-01", verification_status: "verified" }),
    ];
    // Mismo año (2017) en ambos a propósito de la prueba de desempate.
    const sameYear = events.map((e) => ({ ...e, date: "2017-01-01" }));
    expect(sortEvents(sameYear).map((e) => e.id)).toEqual(["verified", "pending"]);
  });

  it("no muta el arreglo original", () => {
    const events = [makeEvent({ id: "a", date: "1991-01-01" }), makeEvent({ id: "b", date: "2017-01-01" })];
    const copy = [...events];
    sortEvents(events);
    expect(events).toEqual(copy);
  });
});
