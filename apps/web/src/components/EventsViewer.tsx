"use client";

import { useEffect, useMemo, useState } from "react";
import { getEvents } from "@/lib/api";
import { sortEvents } from "@/lib/events";
import type { EventRecord, EventsResponse, LocationCertainty } from "@/lib/types";

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

const INITIAL_VISIBLE_COUNT = 20;

function formatApproxLocation(location: Record<string, unknown>): string {
  const place = typeof location.place === "string" ? location.place : null;
  const radiusKm = typeof location.radius_km === "number" ? location.radius_km : null;
  if (place && radiusKm != null) return `${place} (±${radiusKm} km)`;
  if (place) return place;
  return "Ubicación aproximada sin descripción";
}

function EventItem({ event }: { event: EventRecord }) {
  const [showFullSource, setShowFullSource] = useState(false);
  const shortSource = event.source.split(".")[0] + ".";

  return (
    <li style={{ marginBottom: 10, borderBottom: "1px solid #e5e7eb", paddingBottom: 8 }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
        <strong>
          {event.date} · {HAZARD_LABELS[event.hazard_type] ?? event.hazard_type}
        </strong>
        <span
          style={{
            color: event.verification_status === "verified" ? "#1b5e20" : "#8a6d00",
            fontWeight: 600,
            whiteSpace: "nowrap",
          }}
        >
          {VERIFICATION_LABELS[event.verification_status]}
        </span>
      </div>
      <div style={{ color: "#6b7280" }}>
        {formatApproxLocation(event.approx_location)} · {CERTAINTY_LABELS[event.location_certainty]}
      </div>
      <div>{event.notes}</div>
      <div style={{ color: "#6b7280" }}>
        Fuente: {showFullSource ? event.source : shortSource}{" "}
        {event.source.length > shortSource.length && (
          <button
            type="button"
            onClick={() => setShowFullSource((v) => !v)}
            style={{
              background: "none",
              border: "none",
              color: "#2563eb",
              cursor: "pointer",
              padding: 0,
              font: "inherit",
            }}
          >
            {showFullSource ? "ver menos" : "ver fuente completa"}
          </button>
        )}
      </div>
    </li>
  );
}

export function EventsViewer() {
  const [data, setData] = useState<EventsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);
  const [showAll, setShowAll] = useState(false);

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

  const sortedEvents = useMemo(() => (data ? sortEvents(data.events) : []), [data]);
  const visibleEvents = showAll ? sortedEvents : sortedEvents.slice(0, INITIAL_VISIBLE_COUNT);

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
              {sortedEvents.length > 0 && (
                <>
                  <ul style={{ listStyle: "none", padding: 0 }}>
                    {visibleEvents.map((event) => (
                      <EventItem key={event.id} event={event} />
                    ))}
                  </ul>
                  {sortedEvents.length > INITIAL_VISIBLE_COUNT && (
                    <button
                      type="button"
                      onClick={() => setShowAll((v) => !v)}
                      style={{
                        background: "none",
                        border: "1px solid #6b7280",
                        color: "#374151",
                        borderRadius: 6,
                        padding: "4px 8px",
                        cursor: "pointer",
                        fontSize: 12,
                      }}
                    >
                      {showAll ? "Mostrar menos" : `Mostrar los ${sortedEvents.length} eventos`}
                    </button>
                  )}
                </>
              )}
            </>
          )}
        </div>
      )}
    </section>
  );
}
