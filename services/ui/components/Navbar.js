/**
 * Navbar – Material Dashboard–style top bar with breadcrumbs, search,
 * notification bell, AI-status chip, theme toggle, and profile dropdown.
 *
 * Props:
 *  - currentPath : router.pathname
 *  - links       : NAV_LINKS array
 *  - onMenuToggle: callback to toggle mobile sidebar
 *  - themeToggle : optional ReactNode for the dark/light toggle button
 */
import Breadcrumb from "./Breadcrumb";
import ProfileDropdown from "./ProfileDropdown";

/* Bell icon (Heroicon outline) */
function BellIcon() {
  return (
    <svg
      className="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={1.5}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"
      />
    </svg>
  );
}

/* Hamburger icon */
function MenuIcon() {
  return (
    <svg
      className="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
      />
    </svg>
  );
}

/* Search icon */
function SearchIcon() {
  return (
    <svg
      className="h-4 w-4 text-text-disabled"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
      />
    </svg>
  );
}

export default function Navbar({
  currentPath,
  links,
  onMenuToggle,
  themeToggle,
}) {
  const current = links.find((l) => l.href === currentPath);
  const pageTitle = current?.label ?? "Page";

  return (
    <header className="sticky top-0 z-30 w-full bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-3">
        {/* Left: hamburger (mobile) + breadcrumb + page title */}
        <div className="flex items-center gap-4">
          <button
            onClick={onMenuToggle}
            className="rounded-lg p-1.5 text-text-secondary transition-colors hover:bg-primary-100 hover:text-text-primary lg:hidden"
            aria-label="Toggle sidebar"
          >
            <MenuIcon />
          </button>

          <div>
            <Breadcrumb currentPath={currentPath} links={links} />
            <h2 className="text-lg font-bold text-text-primary">{pageTitle}</h2>
          </div>
        </div>

        {/* Right: search + AI chip + bell + theme + profile */}
        <div className="flex items-center gap-3">
          {/* Search — hidden on small screens */}
          <div className="relative hidden md:block">
            <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2">
              <SearchIcon />
            </span>
            <input
              type="search"
              placeholder="Search…"
              aria-label="Global search"
              className="w-48 rounded-lg border border-primary-100 bg-surface py-1.5 pl-9 pr-3 text-sm text-text-primary placeholder:text-text-disabled outline-none transition focus:w-64 focus:border-info focus:ring-2 focus:ring-info/20"
            />
          </div>

          {/* External AI processing status chip */}
          <div
            className="hidden items-center gap-1.5 rounded-full border border-primary-100 bg-surface px-3 py-1 text-[0.7rem] text-text-secondary sm:flex"
            role="status"
            aria-label="External AI processing status"
          >
            <span className="inline-block h-1.5 w-1.5 rounded-full bg-text-disabled" />
            AI: Off
          </div>

          {/* Notification bell */}
          <button
            className="relative rounded-lg p-2 text-text-secondary transition-colors hover:bg-primary-100 hover:text-text-primary"
            aria-label="Notifications"
          >
            <BellIcon />
            {/* Badge dot – visible when there are unread notifications */}
            <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-error ring-2 ring-background" />
          </button>

          {/* Theme toggle slot */}
          {themeToggle}

          {/* Profile */}
          <ProfileDropdown />
        </div>
      </div>
    </header>
  );
}
