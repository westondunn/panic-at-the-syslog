import { useState } from "react";

const API_BASE = process.env.API_BASE_URL || "http://localhost:8000";

export async function getServerSideProps() {
  const token = process.env.API_INTERNAL_TOKEN || "";
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  try {
    const res = await fetch(`${API_BASE}/api/v1/incidents`, { headers });
    if (!res.ok) return { props: { incidents: [] } };
    const data = await res.json();
    return { props: { incidents: Array.isArray(data.items) ? data.items : [] } };
  } catch {
    return { props: { incidents: [] } };
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
  table: { width: "100%", borderCollapse: "collapse", fontSize: "0.875rem" },
  th: {
    textAlign: "left",
    padding: "0.5rem 0.75rem",
    borderBottom: "2px solid #e2e8f0",
    color: "#475569",
    fontWeight: "600",
    backgroundColor: "#f8fafc",
  },
  td: {
    padding: "0.6rem 0.75rem",
    borderBottom: "1px solid #f1f5f9",
    verticalAlign: "top",
  },
  empty: { color: "#94a3b8", marginTop: "2rem", textAlign: "center" },
  count: { fontSize: "0.8rem", color: "#64748b", marginLeft: "0.5rem" },
};

export default function IncidentsPage({ incidents }) {
  const [query, setQuery] = useState("");

  const q = query.trim().toLowerCase();
  const filtered = q
    ? incidents.filter((item) =>
        [item.id, item.summary, item.title, item.message, item.severity, item.status]
          .filter(Boolean)
          .some((v) => String(v).toLowerCase().includes(q))
      )
    : incidents;

  return (
    <>
      <h1 style={styles.heading}>
        Incidents
        <span style={styles.count}>({filtered.length})</span>
      </h1>
      <p style={styles.sub}>Active and resolved incidents.</p>

      <div style={styles.filterRow}>
        <input
          type="search"
          placeholder="Filter incidents…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
          aria-label="Filter incidents"
        />
      </div>

      {filtered.length === 0 ? (
        <p style={styles.empty}>
          {incidents.length === 0
            ? "No incidents found. The system is quiet."
            : "No incidents match your filter."}
        </p>
      ) : (
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>ID</th>
              <th style={styles.th}>Summary</th>
              <th style={styles.th}>Severity</th>
              <th style={styles.th}>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((item, i) => (
              <tr key={item.id ?? i}>
                <td style={styles.td}>{item.id ?? "—"}</td>
                <td style={styles.td}>{item.summary ?? item.title ?? item.message ?? "—"}</td>
                <td style={styles.td}>{item.severity ?? "—"}</td>
                <td style={styles.td}>{item.status ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
