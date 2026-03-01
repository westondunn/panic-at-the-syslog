import { useRouter } from "next/router";
import Sidebar from "../components/Sidebar";
import "../styles/globals.css";

const NAV_LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/incidents", label: "Incidents" },
  { href: "/recommendations", label: "Recommendations" },
  { href: "/review", label: "Review Queue" },
  { href: "/figma-welcome", label: "Figma Welcome" },
];

export default function App({ Component, pageProps }) {
  const router = useRouter();

  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar navigation */}
      <Sidebar links={NAV_LINKS} currentPath={router.pathname} />

      {/* Main content area - offset by sidebar width */}
      <div className="ml-64 flex flex-1 flex-col">
        {/* External AI processing banner - always visible (governance requirement) */}
        <div
          className="flex items-center gap-2 border-b border-primary-100 bg-surface px-6 py-2 text-xs text-text-secondary"
          role="complementary"
          aria-label="External AI processing status"
        >
          <span className="inline-block h-2 w-2 rounded-full bg-text-disabled" />
          <span>External AI Processing: Disabled</span>
        </div>

        <main className="flex-1 p-8">
          <div className="mx-auto max-w-7xl">
            <Component {...pageProps} />
          </div>
        </main>
      </div>
    </div>
  );
}

