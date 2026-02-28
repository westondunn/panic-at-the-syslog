/**
 * StatCard – Material Dashboard–style stat card with a gradient icon area.
 *
 * Props:
 *  - label       : string  – short descriptor ("Incidents", "Findings", …)
 *  - value       : number | string
 *  - gradient    : "dark" | "info" | "success" | "warning" | "error"
 *  - icon        : React node (optional, SVG or emoji)
 *  - href        : optional link destination
 *  - footer      : optional footer text
 */
import Link from "next/link";

const GRADIENT_MAP = {
  dark: "gradient-dark",
  info: "gradient-info",
  success: "gradient-success",
  warning: "gradient-warning",
  error: "gradient-error",
};

export default function StatCard({
  label,
  value,
  gradient = "info",
  icon,
  href,
  footer,
}) {
  const inner = (
    <div className="relative flex items-center justify-between rounded-xl bg-surface p-4 shadow-card transition-shadow hover:shadow-card-hover">
      {/* Gradient icon box – offset above the card like Material Dashboard */}
      <div
        className={`${GRADIENT_MAP[gradient] ?? GRADIENT_MAP.info} absolute -top-4 left-4 flex h-16 w-16 items-center justify-center rounded-stat text-2xl text-text-inverse shadow-stat`}
      >
        {icon ?? "📊"}
      </div>

      {/* Value + label right-aligned */}
      <div className="ml-auto text-right">
        <p className="text-sm font-light text-text-secondary">{label}</p>
        <h4 className="text-2xl font-bold text-text-primary">{value}</h4>
      </div>
    </div>
  );

  const card = (
    <div className="pt-4">
      {href ? (
        <Link href={href} className="block no-underline">
          {inner}
          {footer && (
            <p className="mt-2 px-4 text-xs text-text-secondary">{footer}</p>
          )}
        </Link>
      ) : (
        <>
          {inner}
          {footer && (
            <p className="mt-2 px-4 text-xs text-text-secondary">{footer}</p>
          )}
        </>
      )}
    </div>
  );

  return card;
}
