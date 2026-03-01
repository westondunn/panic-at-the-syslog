/**
 * Footer – Material Dashboard–style footer inside main content area.
 */

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="mx-auto mt-auto w-full max-w-7xl px-8 pb-6 pt-4">
      <div className="flex flex-col items-center justify-between gap-2 border-t border-primary-100 pt-4 sm:flex-row">
        <p className="text-xs text-text-secondary">
          &copy; {year}{" "}
          <span className="font-semibold text-text-primary">
            Panic! At The Syslog
          </span>
          . Open source under MIT license.
        </p>
        <nav className="flex gap-4 text-xs" aria-label="Footer links">
          <a
            href="/docs"
            className="text-text-secondary transition-colors hover:text-text-primary"
          >
            Docs
          </a>
          <a
            href="https://github.com/westondunn/panic-at-the-syslog"
            target="_blank"
            rel="noopener noreferrer"
            className="text-text-secondary transition-colors hover:text-text-primary"
          >
            GitHub
          </a>
          <a
            href="/LICENSE"
            className="text-text-secondary transition-colors hover:text-text-primary"
          >
            License
          </a>
        </nav>
      </div>
    </footer>
  );
}
