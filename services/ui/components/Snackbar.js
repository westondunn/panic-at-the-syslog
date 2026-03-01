/**
 * Snackbar – Material Dashboard–style toast notification.
 *
 * Props:
 *  - open       : boolean
 *  - message    : string
 *  - variant    : "success" | "error" | "warning" | "info" (default "info")
 *  - onClose    : callback
 *  - duration   : auto-dismiss ms (default 4000, 0 = no auto-dismiss)
 */
import { useEffect } from "react";

const VARIANT_STYLES = {
  success: "gradient-success",
  error: "gradient-error",
  warning: "gradient-warning",
  info: "gradient-info",
};

const VARIANT_ICONS = {
  success: "✓",
  error: "✕",
  warning: "⚠",
  info: "ℹ",
};

export default function Snackbar({
  open,
  message,
  variant = "info",
  onClose,
  duration = 4000,
}) {
  useEffect(() => {
    if (!open || duration <= 0) return;
    const timer = setTimeout(() => onClose?.(), duration);
    return () => clearTimeout(timer);
  }, [open, duration, onClose]);

  if (!open) return null;

  return (
    <div className="fixed bottom-6 right-6 z-[70] animate-[slideUp_0.3s_ease-out]">
      <div
        role="alert"
        className={`flex items-center gap-3 rounded-card px-5 py-3 text-sm font-medium text-text-inverse shadow-stat ${VARIANT_STYLES[variant] ?? VARIANT_STYLES.info}`}
      >
        <span className="text-lg">{VARIANT_ICONS[variant]}</span>
        <span className="flex-1">{message}</span>
        <button
          onClick={onClose}
          className="ml-2 rounded p-0.5 text-text-inverse/70 transition-colors hover:text-text-inverse"
          aria-label="Dismiss notification"
        >
          <svg
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}
