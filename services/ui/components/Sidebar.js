/**
 * Sidebar – Material Dashboard–style dark sidebar with navigation links.
 * Responsive: hidden off-screen on mobile, slides in when `open` is true.
 */
import Link from "next/link";

// Simple SVG icons matching Material Dashboard's icon style
const DEFAULT_ICONS = {
  "/": (
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
        d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2z"
      />
    </svg>
  ),
  "/incidents": (
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
        d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
  ),
  "/recommendations": (
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
        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
      />
    </svg>
  ),
  "/review": (
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
        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
      />
    </svg>
  ),
};

/**
 * Props:
 *  - links       : [{ href, label, icon? }]
 *  - currentPath : current router.pathname for active state
 *  - open        : boolean – mobile sidebar visible (controlled)
 *  - onClose     : callback – close sidebar on mobile
 */
export default function Sidebar({ links, currentPath, open, onClose }) {
  return (
    <>
      {/* Backdrop overlay – mobile only */}
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed left-0 top-0 z-50 flex h-screen w-64 flex-col bg-sidebar shadow-sidebar transition-transform duration-300 ease-in-out ${
          open ? "translate-x-0" : "-translate-x-full"
        } lg:translate-x-0`}
      >
        {/* Brand */}
        <div className="flex items-center gap-3 px-6 py-6">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-surface/10 text-lg">
            🚨
          </div>
          <div>
            <h1 className="text-sm font-bold text-text-inverse leading-tight">
              Panic!
            </h1>
            <p className="text-xs text-text-inverse/50">At The Syslog</p>
          </div>

          {/* Close button – mobile only */}
          <button
            onClick={onClose}
            className="ml-auto rounded-lg p-1 text-text-inverse/50 transition-colors hover:text-text-inverse lg:hidden"
            aria-label="Close sidebar"
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

        <hr className="mx-4 border-text-inverse/10" />

        {/* Navigation links */}
        <nav
          className="mt-2 flex-1 space-y-1 px-3"
          aria-label="Main navigation"
        >
          {links.map(({ href, label, icon }) => {
            const isActive = currentPath === href;
            return (
              <Link
                key={href}
                href={href}
                onClick={onClose}
                aria-current={isActive ? "page" : undefined}
                className={`flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-sidebar-active text-text-inverse shadow-md"
                    : "text-text-inverse/70 hover:bg-text-inverse/5 hover:text-text-inverse"
                }`}
              >
                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-text-inverse/10">
                  {icon ?? DEFAULT_ICONS[href] ?? DEFAULT_ICONS["/"]}
                </span>
                {label}
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="px-6 pb-6 pt-2">
          <p className="text-[0.65rem] text-text-inverse/30">
            Panic! At The Syslog v0.1.0
          </p>
        </div>
      </aside>
    </>
  );
}
