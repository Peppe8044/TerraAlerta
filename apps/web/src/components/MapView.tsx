"use client";

import { Map as MaplibreMap, Marker, NavigationControl } from "maplibre-gl";
import type { MapMouseEvent, StyleSpecification } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef } from "react";
import { PILOT_CENTER } from "@/lib/coverage";

// Estilo de demostración con tiles OSM. Para tráfico real, reemplazar por
// un proveedor de tiles con licencia propia (ver política de OSM:
// https://operations.osmfoundation.org/policies/tiles/ y docs/ARQUITECTURA.md).
const DEMO_STYLE: StyleSpecification = {
  version: 8,
  sources: {
    osm: {
      type: "raster",
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "© OpenStreetMap contributors",
    },
  },
  layers: [{ id: "osm", type: "raster", source: "osm" }],
};

interface MapViewProps {
  onSelectPoint: (lat: number, lon: number) => void;
}

export function MapView({ onSelectPoint }: MapViewProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<MaplibreMap | null>(null);
  const markerRef = useRef<Marker | null>(null);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = new MaplibreMap({
      container: containerRef.current,
      style: DEMO_STYLE,
      center: PILOT_CENTER,
      zoom: 11,
    });
    map.addControl(new NavigationControl(), "top-right");

    map.on("click", (event: MapMouseEvent) => {
      const { lat, lng } = event.lngLat;

      if (markerRef.current) {
        markerRef.current.remove();
      }
      markerRef.current = new Marker().setLngLat([lng, lat]).addTo(map);

      onSelectPoint(lat, lng);
    });

    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [onSelectPoint]);

  return (
    <div
      ref={containerRef}
      data-testid="map-container"
      style={{ width: "100%", height: "100%", minHeight: 360 }}
      aria-label="Mapa de San José de Maipo, toque un punto para consultar condiciones"
      role="application"
    />
  );
}
