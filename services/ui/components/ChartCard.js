/**
 * ChartCard – Material Dashboard–style card wrapping a recharts chart.
 *
 * Props:
 *  - title    : string
 *  - subtitle : optional string
 *  - gradient : "dark" | "info" | "success" | "warning" | "error"
 *  - children : recharts chart element(s)
 *  - footer   : optional ReactNode
 */

const GRADIENT_COLORS = {
  dark: { start: "#42424a", end: "#191919" },
  info: { start: "#66bb6a", end: "#43a047" },
  success: { start: "#66bb6a", end: "#43a047" },
  warning: { start: "#ffa726", end: "#fb8c00" },
  error: { start: "#ef5350", end: "#e53935" },
};

export default function ChartCard({
  title,
  subtitle,
  gradient = "dark",
  children,
  footer,
}) {
  return (
    <div className="rounded-card bg-surface shadow-card">
      {/* Chart area with gradient background */}
      <div className="relative mx-4 -mt-6 overflow-hidden rounded-stat shadow-stat">
        <div
          className="h-48 p-4"
          style={{
            background: `linear-gradient(195deg, ${(GRADIENT_COLORS[gradient] ?? GRADIENT_COLORS.dark).start}, ${(GRADIENT_COLORS[gradient] ?? GRADIENT_COLORS.dark).end})`,
          }}
        >
          {children}
        </div>
      </div>

      {/* Title + subtitle */}
      <div className="px-4 pt-4 pb-2">
        <h3 className="text-base font-semibold text-text-primary">{title}</h3>
        {subtitle && (
          <p className="mt-0.5 text-xs text-text-secondary">{subtitle}</p>
        )}
      </div>

      {/* Optional footer */}
      {footer && (
        <div className="border-t border-primary-50 px-4 py-3 text-xs text-text-secondary">
          {footer}
        </div>
      )}
    </div>
  );
}
