/**
 * 500 – Material Dashboard–style server error page.
 */
import Link from "next/link";

export default function ServerError() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center text-center">
      <h1 className="text-8xl font-bold text-error/40">500</h1>
      <h2 className="mt-4 text-2xl font-bold text-text-primary">
        Server Error
      </h2>
      <p className="mt-2 max-w-md text-sm text-text-secondary">
        Something went wrong on our end. The team has been notified. Please try
        again in a moment.
      </p>
      <Link
        href="/"
        className="mt-8 inline-flex items-center gap-2 rounded-lg gradient-error px-6 py-2.5 text-sm font-semibold text-text-inverse shadow-stat transition-shadow hover:shadow-card-hover"
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
