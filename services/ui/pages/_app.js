import Head from "next/head";
import { useRouter } from "next/router";
import { useCallback, useState } from "react";
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
    <div style={styles.wrapper}>
      <Head>
        <link rel="icon" href="/favicon.png" type="image/png" />
        <title>Panic! At The Syslog</title>
      </Head>

      {/* External AI processing banner — always visible */}
      <div
        style={styles.banner}
        role="complementary"
        aria-label="External AI processing status"
      >
        <span style={styles.bannerDot} />
        <span>External AI Processing: Disabled</span>
      </div>
    </div>
  );
}
