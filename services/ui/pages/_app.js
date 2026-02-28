import Head from "next/head";
import Link from "next/link";
import { useRouter } from "next/router";

const NAV_LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/incidents", label: "Incidents" },
  { href: "/recommendations", label: "Recommendations" },
  { href: "/review", label: "Review Queue" },
];

const styles = {
  wrapper: {
    fontFamily: "ui-sans-serif, system-ui, sans-serif",
    minHeight: "100vh",
    backgroundColor: "#f8fafc",
    color: "#0f172a",
  },
  banner: {
    backgroundColor: "#f1f5f9",
    borderBottom: "1px solid #e2e8f0",
    padding: "0.35rem 1.5rem",
    fontSize: "0.75rem",
    color: "#64748b",
    display: "flex",
    alignItems: "center",
    gap: "0.4rem",
  },
  bannerDot: {
    display: "inline-block",
    width: "0.5rem",
    height: "0.5rem",
    borderRadius: "50%",
    backgroundColor: "#94a3b8",
  },
  nav: {
    backgroundColor: "#1e293b",
    padding: "0 1.5rem",
    display: "flex",
    alignItems: "center",
    gap: "0",
  },
  brand: {
    color: "#f8fafc",
    fontWeight: "700",
    fontSize: "1rem",
    padding: "1rem 1.5rem 1rem 0",
    marginRight: "1rem",
    borderRight: "1px solid #334155",
    textDecoration: "none",
  },
  navLink: {
    color: "#94a3b8",
    textDecoration: "none",
    padding: "1rem 0.75rem",
    fontSize: "0.875rem",
    display: "inline-block",
  },
  navLinkActive: {
    color: "#f8fafc",
    borderBottom: "2px solid #3b82f6",
  },
  main: {
    padding: "2rem 1.5rem",
    maxWidth: "1200px",
    margin: "0 auto",
  },
};

export default function App({ Component, pageProps }) {
  const router = useRouter();

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

      <nav style={styles.nav} aria-label="Main navigation">
        <Link href="/" style={styles.brand}>
          Panic! At The Syslog
        </Link>
        {NAV_LINKS.map(({ href, label }) => {
          const isActive = router.pathname === href;
          return (
            <Link
              key={href}
              href={href}
              style={{
                ...styles.navLink,
                ...(isActive ? styles.navLinkActive : {}),
              }}
              aria-current={isActive ? "page" : undefined}
            >
              {label}
            </Link>
          );
        })}
      </nav>

      <main style={styles.main}>
        <Component {...pageProps} />
      </main>
    </div>
  );
}
