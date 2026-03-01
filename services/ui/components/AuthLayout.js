/**
 * AuthLayout – full-screen centered layout for sign-in / sign-up pages.
 * Material Dashboard–style: gradient background with a centered white card.
 */

export default function AuthLayout({ children }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      {/* Background gradient accent */}
      <div
        className="fixed inset-x-0 top-0 h-72 gradient-dark"
        aria-hidden="true"
      />
      {/* Floating brand */}
      <div className="fixed left-6 top-6 z-10 flex items-center gap-2">
        <span className="text-2xl">🚨</span>
        <span className="text-sm font-bold text-text-inverse">
          Panic! At The Syslog
        </span>
      </div>

      {/* Auth card */}
      <div className="relative z-10 w-full max-w-md rounded-card bg-surface p-8 shadow-card-hover">
        {children}
      </div>
    </div>
  );
}
