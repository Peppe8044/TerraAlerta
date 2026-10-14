"use client";

import { useState } from "react";
import type { Indicator, LocationSummary } from "@/lib/types";
import { StatusBadge } from "./StatusBadge";

function IndicatorRow({ indicator }: { indicator: Indicator }) {
  return (
    <li style={{ marginBottom: 12, borderBottom: "1px solid #e5e7eb", paddingBottom: 8 }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
        <strong>{indicator.name}</strong>
        <span>
          {indicator.value !== null ? `${indicator.value} ${indicator.unit ?? ""}` : "Sin dato"}
        </span>
      </div>
      <div style={{ fontSize: 12, color: "#4b5563" }}>
        Fuente: {indicator.source_id} · Resolución: {indicator.spatial_resolution} · Cobertura:{" "}
        {indicator.coverage}
        {indicator.observed_at ? ` · Observado: ${indicator.observed_at}` : ""}
        {indicator.issued_at ? ` · Emitido: ${indicator.issued_at}` : ""}
        {` · Consultado: ${indicator.retrieved_at}`}
      </div>
      {indicator.limitations.length > 0 && (
        <ul style={{ fontSize: 12, color: "#9a3412", marginTop: 4, paddingLeft: 18 }}>
          {indicator.limitations.map((limitation) => (
            <li key={limitation}>{limitation}</li>
          ))}
        </ul>
      )}
    </li>
  );
}

interface LocationPanelProps {
  loading: boolean;
  error: string | null;
  summary: LocationSummary | null;
}

export function LocationPanel({ loading, error, summary }: LocationPanelProps) {
  const [showWhy, setShowWhy] = useState(false);

  if (loading) {
    return <p role="status">Cargando condiciones observadas y previstas…</p>;
  }

  if (error) {
    return (
      <p role="alert" style={{ color: "#b91c1c" }}>
        No hay datos recientes para este punto: {error}
      </p>
    );
  }

  if (!summary) {
    return (
      <p>
        Toque un punto dentro de San José de Maipo en el mapa para ver pronóstico, elevación y
        trazabilidad de cada dato.
      </p>
    );
  }

  return (
    <section aria-label="Resumen de la ubicación seleccionada">
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2 style={{ fontSize: 16, margin: 0 }}>
          Lat {summary.location.lat.toFixed(4)}, Lon {summary.location.lon.toFixed(4)}
        </h2>
        <StatusBadge status={summary.status} />
      </header>

      <p style={{ fontSize: 13, fontStyle: "italic", marginTop: 8 }}>
        Información experimental. No predice daños en una propiedad específica ni sustituye a
        SENAPRED.
      </p>

      <ul style={{ listStyle: "none", padding: 0, marginTop: 12 }}>
        {summary.indicators.map((indicator) => (
          <IndicatorRow key={indicator.name} indicator={indicator} />
        ))}
      </ul>

      <button
        type="button"
        onClick={() => setShowWhy((value) => !value)}
        aria-expanded={showWhy}
        style={{
          background: "none",
          border: "1px solid #2563eb",
          color: "#2563eb",
          borderRadius: 6,
          padding: "6px 10px",
          cursor: "pointer",
        }}
      >
        {showWhy ? "Ocultar «Por qué veo esto»" : "Por qué veo esto"}
      </button>

      {showWhy && (
        <div style={{ marginTop: 10, fontSize: 13 }}>
          <ul>
            {summary.limitations.map((limitation) => (
              <li key={limitation}>{limitation}</li>
            ))}
          </ul>
          <a href={summary.official_alerts_url} target="_blank" rel="noreferrer">
            Ver alertas oficiales en SENAPRED
          </a>
        </div>
      )}
    </section>
  );
}
