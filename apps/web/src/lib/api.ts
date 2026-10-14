import type { EventsResponse, LocationSummary, PreparednessChecklist, SourceInfo } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`API ${response.status} en ${path}: ${body}`);
  }
  return response.json() as Promise<T>;
}

export function getLocationSummary(lat: number, lon: number): Promise<LocationSummary> {
  return getJson<LocationSummary>(`/v1/locations/summary?lat=${lat}&lon=${lon}`);
}

export function getSources(): Promise<SourceInfo[]> {
  return getJson<SourceInfo[]>("/v1/sources");
}

export function getEvents(): Promise<EventsResponse> {
  return getJson<EventsResponse>("/v1/events");
}

export function getPreparedness(hazard = "landslide"): Promise<PreparednessChecklist> {
  return getJson<PreparednessChecklist>(`/v1/preparedness?hazard=${hazard}`);
}
