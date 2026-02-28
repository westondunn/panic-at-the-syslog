import Link from "next/link";

const API_BASE = process.env.API_BASE_URL || "http://localhost:8000";

/** Fetch a collection from the backend. Returns [] on any error or non-2xx. */
async function fetchCollection(collection, token) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  try {
    const res = await fetch(`${API_BASE}/api/v1/${collection}`, { headers });
    if (!res.ok) return [];
    const data = await res.json();
    return Array.isArray(data.items) ? data.items : [];
  } catch {
    return [];
  }
}

export async function getServerSideProps() {
  // API_INTERNAL_TOKEN is a server-only env var — never sent to the browser.
  const token = process.env.API_INTERNAL_TOKEN || "";
  const [incidents, findings, insights, reviewQueue] = await Promise.all([
    fetchCollection("incidents", token),
    fetchCollection("findings", token),
    fetchCollection("insights", token),
    fetchCollection("review-queue", token),
  ]);
  return {
    props: {
      counts: {
        incidents: incidents.length,
        findings: findings.length,
        insights: insights.length,
        reviewQueue: reviewQueue.length,
      },
    },
  };
}

const LINKED_CARDS = [
  { label: "Incidents", key: "incidents", href: "/incidents", color: "#ef4444" },
  { label: "Recommendations", key: "insights", href: "/recommendations", color: "#3b82f6" },
  { label: "Review Queue", key: "reviewQueue", href: "/review", color: "#8b5cf6" },
];

// Findings are surfaced as a count-only stat (no dedicated page yet).
const STAT_CARDS = [
  { label: "Findings", key: "findings", color: "#f97316" },
];

const styles = {
  heading: { fontSize: "1.5rem", fontWeight: "700", marginBottom: "0.25rem" },
  sub: { color: "#64748b", marginBottom: "2rem", fontSize: "0.95rem" },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
    gap: "1rem",
  },
  card: {
    borderRadius: "0.5rem",
    border: "1px solid #e2e8f0",
    backgroundColor: "#ffffff",
    padding: "1.25rem 1.5rem",
    textDecoration: "none",
    color: "inherit",
    display: "block",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
  },
  cardCount: { fontSize: "2.5rem", fontWeight: "800", lineHeight: "1" },
  cardLabel: { fontSize: "0.875rem", color: "#64748b", marginTop: "0.4rem" },
};

export default function Dashboard({ counts }) {
  return (
    <>
      <h1 style={styles.heading}>Dashboard</h1>
      <p style={styles.sub}>Summary of current system state.</p>
      <div style={styles.grid}>
        {LINKED_CARDS.map(({ label, key, href, color }) => (
          <Link key={key} href={href} style={styles.card}>
            <div style={{ ...styles.cardCount, color }}>{counts[key]}</div>
            <div style={styles.cardLabel}>{label}</div>
          </Link>
        ))}
        {STAT_CARDS.map(({ label, key, color }) => (
          <div key={key} style={{ ...styles.card, cursor: "default" }}>
            <div style={{ ...styles.cardCount, color }}>{counts[key]}</div>
            <div style={styles.cardLabel}>{label}</div>
          </div>
        ))}
      </div>
    </>
  );
}