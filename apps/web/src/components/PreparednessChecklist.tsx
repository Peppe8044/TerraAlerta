"use client";

import { useEffect, useState } from "react";
import { getPreparedness } from "@/lib/api";
import type { PreparednessChecklist as PreparednessChecklistType } from "@/lib/types";

export function PreparednessChecklist() {
  const [checklist, setChecklist] = useState<PreparednessChecklistType | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    getPreparedness("landslide")
      .then((data) => {
        if (!cancelled) setChecklist(data);
      })
      .catch((err) => {
        if (!cancelled) setError(String(err));
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (error) return null; // Degradación silenciosa: no es crítico para el flujo principal.
  if (!checklist) return null;

  return (
    <section aria-label="Preparación ante aluviones" style={{ marginTop: 16 }}>
      <h3 style={{ fontSize: 14, marginBottom: 4 }}>Preparación (borrador v{checklist.version})</h3>
      <ul style={{ fontSize: 13, paddingLeft: 18 }}>
        {checklist.items.map((item) => (
          <li key={item.text}>{item.text}</li>
        ))}
      </ul>
      <p style={{ fontSize: 11, color: "#6b7280" }}>{checklist.disclaimer}</p>
      <a href={checklist.official_url} target="_blank" rel="noreferrer">
        Orientación oficial SENAPRED
      </a>
    </section>
  );
}
