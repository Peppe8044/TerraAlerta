"use client";

import { useEffect, useState } from "react";
import { getSources } from "@/lib/api";
import type { LicenseStatus, SourceInfo } from "@/lib/types";

// Exigido por la auditoría de confiabilidad (docs/AUDITORIA_MVP_2026-10-14.md,
// entregable 2): un panel "¿De dónde viene este dato?" antes de mostrar
// cualquier evaluación. Lista TODAS las fuentes registradas, incluidas las
// que están pending/research_only/blocked — la transparencia incluye decir
// qué NO está habilitado todavía y por qué.
const LICENSE_LABELS: Record<LicenseStatus, string> = {
  approved: "Aprobada (no comercial)",
  pending: "Pendiente de verificar",
  research_only: "Solo investigación",
  blocked: "Bloqueada",
};

const LICENSE_COLORS: Record<LicenseStatus, string> = {
  approved: "#1b5e20",
  pending: "#8a6d00",
  research_only: "#5b21b6",
  blocked: "#6b7280",
};

export function SourcesPanel() {
  const [sources, setSources] = useState<SourceInfo[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getSources()
      .then((data) => {
        if (!cancelled) setSources(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : String(err));
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section aria-label="De dónde vienen estos datos" style={{ marginTop: 16 }}>
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
        {open ? "Ocultar «¿De dónde viene este dato?»" : "¿De dónde viene este dato?"}
      </button>

      {open && (
        <div style={{ marginTop: 8 }}>
          {error && <p role="alert">No se pudo cargar el inventario de fuentes: {error}</p>}
          {!sources && !error && <p role="status">Cargando inventario de fuentes…</p>}
          {sources && (
            <ul style={{ listStyle: "none", padding: 0, fontSize: 12 }}>
              {sources.map((source) => (
                <li
                  key={source.dataset}
                  style={{ marginBottom: 10, borderBottom: "1px solid #e5e7eb", paddingBottom: 8 }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                    <strong>{source.dataset}</strong>
                    <span
                      style={{
                        color: "white",
                        backgroundColor: LICENSE_COLORS[source.license_status],
                        borderRadius: 999,
                        padding: "1px 8px",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {LICENSE_LABELS[source.license_status]}
                    </span>
                  </div>
                  <div style={{ color: "#4b5563" }}>{source.owner}</div>
                  <div style={{ color: "#6b7280" }}>
                    {source.retrieval_mode} · última verificación: {source.last_verified}
                  </div>
                  <div style={{ color: "#6b7280" }}>{source.notes}</div>
                  <a href={source.url} target="_blank" rel="noreferrer">
                    {source.url}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}
