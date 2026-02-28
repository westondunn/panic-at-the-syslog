/**
 * Badge – Material Dashboard–style colored badge for severity / priority / type.
 *
 * Props:
 *  - children : text content
 *  - variant  : "success" | "warning" | "error" | "info" | "neutral" (default)
 */

const VARIANTS = {
  success: "bg-success/10 text-success",
  warning: "bg-warning/10 text-warning",
  error: "bg-error/10 text-error",
  info: "bg-info/10 text-info",
  neutral: "bg-primary-100 text-primary-500",
};

export default function Badge({ children, variant = "neutral" }) {
  return (
    <span
      className={`inline-block rounded-badge px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wide ${VARIANTS[variant] ?? VARIANTS.neutral}`}
    >
      {children}
    </span>
  );
}

/** Helper: map raw priority/severity strings to badge variants. */
export function severityVariant(value) {
  if (!value) return "neutral";
  const v = String(value).toLowerCase();
  if (v === "critical" || v === "high") return "error";
  if (v === "medium" || v === "med") return "warning";
  if (v === "low") return "success";
  return "info";
}
