"use client";

import { useEffect, useState } from "react";
import { getEvents } from "@/lib/api";
import type { EventsResponse, LocationCertainty } from "@/lib/types";

const CERTAINTY_LABELS: Record<LocationCertainty, string> = {
  verified: "Localización verificada",
  approximate: "Localización aproximada",
  unverified_candidate: "Candidato sin verificar",
};

const HAZARD_LABELS: Record<string, string> = {
  aluvion: "Aluvión",
  remocion_en_masa: "Remoción en masa",
  inundacion: "Inundación",
};

const VERIFICATION_LABELS: Record<string, string> = {
  verified: "Verificado",
  pending_review: "Pendiente de revisión",
};

function formatApproxLocation(location: Record<string, unknown>): string {
  const place = typeof location.place === "string" ? location.place : null;
  const radiusKm = typeof location.radius_km === "number" ? location.radius_km : null;
  if (place && radiusKm != null) return `${place} (±${radiusKm} km)`;
  if (place) return place;
  return "Ubicación aproximada sin descripción";
}

export function EventsViewer() {
  const [data, setData] = useState<EventsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getEvents()
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : String(err));
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section aria-label="Eventos históricos documentados" style={{ marginTop: 16 }}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        style={{
          background: "none",
          border: "1px solid #6b7280",
          color: "#374151",
          borderRadius: 6,
          padding: "6px 10px",
          cursor: "pointer",
          fontSize: 13,
        }}
      >
        {open ? "Ocultar eventos históricos" : "Eventos históricos documentados"}
      </button>

      {open && (
        <div style={{ marginTop: 8, fontSize: 12 }}>
          {error && <p role="alert">No se pudo cargar el historial de eventos: {error}</p>}
          {!data && !error && <p role="status">Cargando eventos históricos…</p>}
          {data && (
            <>
              <p style={{ color: "#4b5563" }}>{data.message}</p>
              {data.events.length > 0 && (
                <ul style={{ listStyle: "none", padding: 0 }}>
                  {data.events.map((event) => (
                    <li
                      key={event.id}
                      style={{ marginBottom: 10, borderBottom: "1px solid #e5e7eb", paddingBottom: 8 }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                        <strong>
                          {event.date} · {HAZARD_LABELS[event.hazard_type] ?? event.hazard_type}
                        </strong>
                        <span
                          style={{
                            color: event.verification_status === "verified" ? "#1b5e20" : "#8a6d00",
                            fontWeight: 600,
                          }}
                        >
                          {VERIFICATION_LABELS[event.verification_status]}
                        </span>
                      </div>
                      <div style={{ color: "#6b7280" }}>
                        {formatApproxLocation(event.approx_location)} ·{" "}
                        {CERTAINTY_LABELS[event.location_certainty]}
                      </div>
                      <div>{event.notes}</div>
                      <div style={{ color: "#6b7280" }}>Fuente: {event.source}</div>
                    </li>
                  ))}
                </ul>
              )}
            </>
          )}
        </div>
      )}
    </section>
  );
}
