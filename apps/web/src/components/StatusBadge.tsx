import { statusLabel } from "@/lib/status";
import type { DataStatus } from "@/lib/types";

const COLORS: Record<DataStatus, string> = {
  sufficient_data: "#1b5e20",
  partial_data: "#8a6d00",
  unavailable: "#6b7280",
};

export function StatusBadge({ status }: { status: DataStatus }) {
  return (
    <span
      style={{
        display: "inline-block",
        padding: "2px 10px",
        borderRadius: 999,
        fontSize: 13,
        fontWeight: 600,
        color: "white",
        backgroundColor: COLORS[status] ?? COLORS.unavailable,
      }}
    >
      {statusLabel(status)}
    </span>
  );
}
