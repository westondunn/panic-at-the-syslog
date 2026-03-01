/**
 * 404 – Material Dashboard–style "page not found" error page.
 */
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center text-center">
      <h1 className="text-8xl font-bold text-text-disabled">404</h1>
      <h2 className="mt-4 text-2xl font-bold text-text-primary">
        Page Not Found
      </h2>
      <p className="mt-2 max-w-md text-sm text-text-secondary">
        The page you&apos;re looking for doesn&apos;t exist or has been moved.
        Check the URL or head back to the dashboard.
      </p>
      <Link
        href="/"
        className="mt-8 inline-flex items-center gap-2 rounded-lg gradient-info px-6 py-2.5 text-sm font-semibold text-text-inverse shadow-stat transition-shadow hover:shadow-card-hover"
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
            d="M10 19l-7-7m0 0l7-7m-7 7h18"
          />
        </svg>
        Back to Dashboard
      </Link>
    </div>
  );
}
