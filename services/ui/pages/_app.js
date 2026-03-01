import { useRouter } from "next/router";
import { useCallback, useState } from "react";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ThemeToggle from "../components/ThemeToggle";
import "../styles/globals.css";

const NAV_LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/incidents", label: "Incidents" },
  { href: "/recommendations", label: "Recommendations" },
  { href: "/review", label: "Review Queue" },
];

/** Routes that use the auth layout (no sidebar/navbar/footer). */
const AUTH_ROUTES = ["/sign-in", "/sign-up"];

export default function App({ Component, pageProps }) {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = useCallback(() => setSidebarOpen((o) => !o), []);
  const closeSidebar = useCallback(() => setSidebarOpen(false), []);

  // Auth pages render without the shell
  if (AUTH_ROUTES.includes(router.pathname)) {
    return <Component {...pageProps} />;
  }

  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar navigation */}
      <Sidebar
        links={NAV_LINKS}
        currentPath={router.pathname}
        open={sidebarOpen}
        onClose={closeSidebar}
      />

      {/* Main content area – responsive sidebar offset */}
      <div className="flex flex-1 flex-col lg:ml-64">
        <Navbar
          currentPath={router.pathname}
          links={NAV_LINKS}
          onMenuToggle={toggleSidebar}
          themeToggle={<ThemeToggle />}
        />

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl">
            <Component {...pageProps} />
          </div>
        </main>

        <Footer />
      </div>
    </div>
  );
}
