// Tipos espejo de services/api/app/schemas.py.
// Mantener sincronizados manualmente hasta que se genere un cliente OpenAPI.

export type LicenseStatus = "approved" | "pending" | "research_only" | "blocked";
export type DataStatus = "sufficient_data" | "partial_data" | "unavailable";
export type QualityFlag = "real" | "synthetic" | "unavailable";

export interface SourceInfo {
  dataset: string;
  owner: string;
  url: string;
  license_status: LicenseStatus;
  retrieval_mode: string;
  last_verified: string;
  notes: string;
}

export interface Indicator {
  name: string;
  value: number | null;
  unit: string | null;
  source_id: string;
  observed_at: string | null;
  issued_at: string | null;
  retrieved_at: string;
  spatial_resolution: string;
  coverage: string;
  quality_flag: QualityFlag;
  limitations: string[];
}

export interface LocationSummary {
  location: { lat: number; lon: number };
  experimental: boolean;
  status: DataStatus;
  indicators: Indicator[];
  limitations: string[];
  official_alerts_url: string;
}

export type LocationCertainty = "verified" | "approximate" | "unverified_candidate";
export type VerificationStatus = "verified" | "pending_review";
export type HazardType = "aluvion" | "remocion_en_masa" | "inundacion";

export interface EventRecord {
  id: string;
  date: string;
  approx_location: Record<string, unknown>;
  hazard_type: HazardType;
  source: string;
  location_certainty: LocationCertainty;
  verification_status: VerificationStatus;
  notes: string;
}

export interface EventsResponse {
  events: EventRecord[];
  message: string;
}

export interface PreparednessItem {
  text: string;
  source: string;
}

export interface PreparednessChecklist {
  hazard: string;
  version: string;
  last_reviewed: string;
  source_attribution: string;
  official_url: string;
  items: PreparednessItem[];
  disclaimer: string;
}
