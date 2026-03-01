/**
 * Breadcrumb – Material Dashboard–style breadcrumb trail.
 *
 * Props:
 *  - currentPath : router.pathname
 *  - links       : [{ href, label }] – the NAV_LINKS array from _app
 */
import Link from "next/link";

export default function Breadcrumb({ currentPath, links }) {
  const current = links.find((l) => l.href === currentPath);
  const label = current?.label ?? "Page";

  return (
    <nav aria-label="Breadcrumb" className="flex items-center gap-1 text-sm">
      <Link
        href="/"
        className="text-text-secondary transition-colors hover:text-text-primary"
      >
        Pages
      </Link>
      <span className="text-text-disabled">/</span>
      <span className="font-medium text-text-primary">{label}</span>
    </nav>
  );
}
