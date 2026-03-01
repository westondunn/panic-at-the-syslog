/**
 * ProfileDropdown – Avatar circle with a dropdown menu.
 * Static placeholder – no real auth wiring yet.
 */
import { useEffect, useRef, useState } from "react";

const MENU_ITEMS = [
  { label: "Profile", href: "#" },
  { label: "Settings", href: "#" },
];

export default function ProfileDropdown() {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  // Close on outside click
  useEffect(() => {
    if (!open) return;
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [open]);

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex h-9 w-9 items-center justify-center rounded-full bg-primary-500 text-sm font-bold text-text-inverse transition-shadow hover:shadow-md"
        aria-label="User menu"
        aria-expanded={open}
        aria-haspopup="true"
      >
        A
      </button>

      {open && (
        <div className="absolute right-0 top-12 z-50 min-w-[160px] rounded-card bg-surface py-1 shadow-card-hover ring-1 ring-primary-100">
          <div className="border-b border-primary-50 px-4 py-2">
            <p className="text-sm font-semibold text-text-primary">Admin</p>
            <p className="text-xs text-text-secondary">admin@localhost</p>
          </div>
          {MENU_ITEMS.map(({ label, href }) => (
            <a
              key={label}
              href={href}
              className="block px-4 py-2 text-sm text-text-secondary transition-colors hover:bg-background hover:text-text-primary"
            >
              {label}
            </a>
          ))}
          <hr className="my-1 border-primary-50" />
          <a
            href="/sign-in"
            className="block px-4 py-2 text-sm text-error transition-colors hover:bg-error/5"
          >
            Sign Out
          </a>
        </div>
      )}
    </div>
  );
}
