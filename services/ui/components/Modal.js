/**
 * Modal – centered overlay dialog with backdrop.
 *
 * Props:
 *  - open      : boolean
 *  - onClose   : callback
 *  - title     : string
 *  - children  : ReactNode (body content)
 *  - footer    : optional ReactNode (action buttons)
 *  - size      : "sm" | "md" | "lg" (default "md")
 */
import { useEffect, useRef } from "react";

const SIZE_MAP = {
  sm: "max-w-sm",
  md: "max-w-lg",
  lg: "max-w-2xl",
};

export default function Modal({
  open,
  onClose,
  title,
  children,
  footer,
  size = "md",
}) {
  const dialogRef = useRef(null);

  // Trap focus inside the modal and handle Escape
  useEffect(() => {
    if (!open) return;

    const handleKey = (e) => {
      if (e.key === "Escape") onClose?.();
    };
    document.addEventListener("keydown", handleKey);

    // Prevent body scroll
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.removeEventListener("keydown", handleKey);
      document.body.style.overflow = prevOverflow;
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Dialog */}
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className={`relative w-full ${SIZE_MAP[size] ?? SIZE_MAP.md} rounded-card bg-surface shadow-card-hover transition-transform`}
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-primary-100 px-6 py-4">
          <h3 className="text-lg font-semibold text-text-primary">{title}</h3>
          <button
            onClick={onClose}
            className="rounded-lg p-1 text-text-secondary transition-colors hover:bg-primary-100 hover:text-text-primary"
            aria-label="Close dialog"
          >
            <svg
              className="h-5 w-5"
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

        {/* Body */}
        <div className="px-6 py-4 text-sm text-text-primary">{children}</div>

        {/* Footer */}
        {footer && (
          <div className="flex items-center justify-end gap-3 border-t border-primary-100 px-6 py-4">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
