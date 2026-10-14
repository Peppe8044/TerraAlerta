// Debe reflejar el bounding box piloto de services/api/app/config.py.
// Es una aproximación operativa, no un límite administrativo oficial
// (ver docs/DECISIONES.md).
export const PILOT_BBOX = {
  minLat: -34.3,
  maxLat: -33.55,
  minLon: -70.45,
  maxLon: -69.75,
};

export const PILOT_CENTER: [number, number] = [-70.3539, -33.6378]; // [lon, lat]

export function isInsidePilotCoverage(lat: number, lon: number): boolean {
  return (
    lat >= PILOT_BBOX.minLat &&
    lat <= PILOT_BBOX.maxLat &&
    lon >= PILOT_BBOX.minLon &&
    lon <= PILOT_BBOX.maxLon
  );
}
