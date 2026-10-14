import { describe, expect, it } from "vitest";
import { isInsidePilotCoverage, PILOT_CENTER } from "./coverage";

describe("isInsidePilotCoverage", () => {
  it("acepta el centro de la zona piloto", () => {
    const [lon, lat] = PILOT_CENTER;
    expect(isInsidePilotCoverage(lat, lon)).toBe(true);
  });

  it("rechaza un punto claramente fuera de Chile central", () => {
    expect(isInsidePilotCoverage(-53.16, -70.91)).toBe(false);
  });
});
