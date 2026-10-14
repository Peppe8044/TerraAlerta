"use client";

import { useCallback, useState } from "react";
import { LocationPanel } from "@/components/LocationPanel";
import { MapView } from "@/components/MapView";
import { PreparednessChecklist } from "@/components/PreparednessChecklist";
import { getLocationSummary } from "@/lib/api";
import { isInsidePilotCoverage } from "@/lib/coverage";
import type { LocationSummary } from "@/lib/types";

export default function HomePage() {
  const [summary, setSummary] = useState<LocationSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSelectPoint = useCallback(async (lat: number, lon: number) => {
    if (!isInsidePilotCoverage(lat, lon)) {
      setSummary(null);
      setError("Punto fuera de la zona piloto (San José de Maipo).");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await getLocationSummary(lat, lon);
      setSummary(data);
    } catch (err) {
      setSummary(null);
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <main>
      <div style={{ flex: "1 1 60%" }}>
        <MapView onSelectPoint={handleSelectPoint} />
      </div>
      <aside
        style={{
          flex: "1 1 40%",
          padding: 16,
          overflowY: "auto",
          background: "white",
          borderLeft: "1px solid #e5e7eb",
        }}
      >
        <h1 style={{ fontSize: 18 }}>TerraAlerta Chile (piloto San José de Maipo)</h1>
        <p style={{ fontSize: 13, color: "#4b5563" }}>
          Prototipo experimental. No predice inundaciones a nivel de vivienda, no emite alertas
          oficiales y no sustituye a{" "}
          <a href="https://www.senapred.cl/" target="_blank" rel="noreferrer">
            SENAPRED
          </a>
          .
        </p>
        <LocationPanel loading={loading} error={error} summary={summary} />
        <PreparednessChecklist />
      </aside>
    </main>
  );
}
