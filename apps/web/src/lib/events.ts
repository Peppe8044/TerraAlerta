import type { EventRecord } from "./types";

export function extractYear(dateText: string): number {
  const match = dateText.match(/\d{4}/);
  return match ? Number(match[0]) : 0;
}

// Más recientes primero; dentro de un mismo año, verificados antes que
// pendientes de revisión, para que lo más confiable aparezca arriba.
export function sortEvents(events: EventRecord[]): EventRecord[] {
  return [...events].sort((a, b) => {
    const yearDiff = extractYear(b.date) - extractYear(a.date);
    if (yearDiff !== 0) return yearDiff;
    if (a.verification_status === b.verification_status) return 0;
    return a.verification_status === "verified" ? -1 : 1;
  });
}
