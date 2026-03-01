/**
 * Skeleton – animated placeholder for loading states.
 *
 * Props:
 *  - className : additional classes for sizing
 *  - variant   : "text" | "circular" | "rectangular" (default: "text")
 *  - lines     : number of text lines to render (variant=text)
 *  - height    : explicit height (variant=rectangular)
 */

export default function Skeleton({
  className = "",
  variant = "text",
  lines = 1,
  height,
}) {
  const base = "animate-pulse rounded bg-primary-100/60";

  if (variant === "circular") {
    return (
      <div
        className={`${base} rounded-full ${className}`}
        style={{ height, width: height }}
        aria-hidden="true"
      />
    );
  }

  if (variant === "rectangular") {
    return (
      <div
        className={`${base} w-full ${className}`}
        style={{ height: height ?? "8rem" }}
        aria-hidden="true"
      />
    );
  }

  // Text variant – renders multiple lines with varying widths
  const widths = ["w-full", "w-5/6", "w-4/6", "w-3/4", "w-2/3", "w-5/6"];

  return (
    <div className={`space-y-2 ${className}`} aria-hidden="true">
      {Array.from({ length: lines }, (_, i) => (
        <div key={i} className={`${base} h-3 ${widths[i % widths.length]}`} />
      ))}
    </div>
  );
}
