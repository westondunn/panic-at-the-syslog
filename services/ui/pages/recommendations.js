import { useState } from "react";

const API_BASE = process.env.API_BASE_URL || "http://localhost:8000";

export async function getServerSideProps() {
  const token = process.env.API_INTERNAL_TOKEN || "";
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  try {
    const res = await fetch(`${API_BASE}/api/v1/insights`, { headers });
    if (!res.ok) return { props: { insights: [] } };
    const data = await res.json();
    return { props: { insights: Array.isArray(data.items) ? data.items : [] } };
  } catch {
    return { props: { insights: [] } };
  }
}

const styles = {
  heading: { fontSize: "1.5rem", fontWeight: "700", marginBottom: "0.25rem" },
  sub: { color: "#64748b", marginBottom: "1.25rem", fontSize: "0.95rem" },
  filterRow: { display: "flex", gap: "0.75rem", marginBottom: "1.25rem" },
  input: {
    flex: "1",
    maxWidth: "400px",
    padding: "0.5rem 0.75rem",
    border: "1px solid #cbd5e1",
    borderRadius: "0.375rem",
    fontSize: "0.875rem",
    outline: "none",
  },
  list: { listStyle: "none", padding: 0, margin: 0 },
  card: {
    backgroundColor: "#ffffff",
    border: "1px solid #e2e8f0",
    borderRadius: "0.5rem",
    padding: "1rem 1.25rem",
    marginBottom: "0.75rem",
    boxShadow: "0 1px 2px rgba(0,0,0,0.04)",
  },
  cardTitle: { fontWeight: "600", marginBottom: "0.25rem" },
  cardBody: { color: "#475569", fontSize: "0.875rem", lineHeight: "1.5" },
  badge: {
    display: "inline-block",
    fontSize: "0.7rem",
    padding: "0.15rem 0.4rem",
    borderRadius: "0.25rem",
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
    marginBottom: "0.4rem",
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: "0.03em",
  },
  empty: { color: "#94a3b8", marginTop: "2rem", textAlign: "center" },
  count: { fontSize: "0.8rem", color: "#64748b", marginLeft: "0.5rem" },
};

export default function RecommendationsPage({ insights }) {
  const [query, setQuery] = useState("");

  const q = query.trim().toLowerCase();
  const filtered = q
    ? insights.filter((item) =>
        [item.id, item.title, item.summary, item.recommendation, item.type, item.detail, item.description]
          .filter(Boolean)
          .some((v) => String(v).toLowerCase().includes(q))
      )
    : insights;

  return (
    <>
      <h1 style={styles.heading}>
        Recommendations
        <span style={styles.count}>({filtered.length})</span>
      </h1>
      <p style={styles.sub}>AI-generated insights and remediation recommendations.</p>

      <div style={styles.filterRow}>
        <input
          type="search"
          placeholder="Filter recommendations…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
          aria-label="Filter recommendations"
        />
      </div>

      {filtered.length === 0 ? (
        <p style={styles.empty}>
          {insights.length === 0
            ? "No recommendations available yet."
            : "No recommendations match your filter."}
        </p>
      ) : (
        <ul style={styles.list}>
          {filtered.map((item, i) => (
            <li key={item.id ?? i} style={styles.card}>
              {item.type && <span style={styles.badge}>{item.type}</span>}
              <div style={styles.cardTitle}>
                {item.title ?? item.summary ?? item.recommendation ?? item.id ?? "Untitled Insight"}
              </div>
              {item.detail && <div style={styles.cardBody}>{item.detail}</div>}
              {item.description && <div style={styles.cardBody}>{item.description}</div>}
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
