import { useState } from "react";

const API_BASE = process.env.API_BASE_URL || "http://localhost:8000";

export async function getServerSideProps() {
  const token = process.env.API_INTERNAL_TOKEN || "";
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  try {
    const res = await fetch(`${API_BASE}/api/v1/review-queue`, { headers });
    if (!res.ok) return { props: { items: [] } };
    const data = await res.json();
    return { props: { items: Array.isArray(data.items) ? data.items : [] } };
  } catch {
    return { props: { items: [] } };
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
  priorityHigh: {
    display: "inline-block",
    padding: "0.1rem 0.4rem",
    borderRadius: "0.25rem",
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    fontWeight: "600",
    fontSize: "0.75rem",
  },
  priorityMed: {
    display: "inline-block",
    padding: "0.1rem 0.4rem",
    borderRadius: "0.25rem",
    backgroundColor: "#fef3c7",
    color: "#92400e",
    fontWeight: "600",
    fontSize: "0.75rem",
  },
  priorityLow: {
    display: "inline-block",
    padding: "0.1rem 0.4rem",
    borderRadius: "0.25rem",
    backgroundColor: "#f0fdf4",
    color: "#166534",
    fontWeight: "600",
    fontSize: "0.75rem",
  },
  empty: { color: "#94a3b8", marginTop: "2rem", textAlign: "center" },
  count: { fontSize: "0.8rem", color: "#64748b", marginLeft: "0.5rem" },
};

function PriorityBadge({ value }) {
  if (!value) return <span>—</span>;
  const normalized = String(value).toLowerCase();
  let badgeStyle = styles.priorityLow;
  if (normalized === "high" || normalized === "critical") badgeStyle = styles.priorityHigh;
  else if (normalized === "medium" || normalized === "med") badgeStyle = styles.priorityMed;
  return <span style={badgeStyle}>{value}</span>;
}

export default function ReviewPage({ items }) {
  const [query, setQuery] = useState("");

  const q = query.trim().toLowerCase();
  const filtered = q
    ? items.filter((item) =>
        [item.id, item.description, item.summary, item.title, item.message, item.priority, item.severity, item.state, item.status]
          .filter(Boolean)
          .some((v) => String(v).toLowerCase().includes(q))
      )
    : items;

  return (
    <>
      <h1 style={styles.heading}>
        Review Queue
        <span style={styles.count}>({filtered.length})</span>
      </h1>
      <p style={styles.sub}>Items awaiting human review before action is taken.</p>

      <div style={styles.filterRow}>
        <input
          type="search"
          placeholder="Filter review items…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
          aria-label="Filter review items"
        />
      </div>

      {filtered.length === 0 ? (
        <p style={styles.empty}>
          {items.length === 0
            ? "Review queue is empty. Nothing awaiting action."
            : "No items match your filter."}
        </p>
      ) : (
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>ID</th>
              <th style={styles.th}>Description</th>
              <th style={styles.th}>Priority</th>
              <th style={styles.th}>State</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((item, i) => (
              <tr key={item.id ?? i}>
                <td style={styles.td}>{item.id ?? "—"}</td>
                <td style={styles.td}>
                  {item.description ?? item.summary ?? item.title ?? item.message ?? "—"}
                </td>
                <td style={styles.td}>
                  <PriorityBadge value={item.priority ?? item.severity} />
                </td>
                <td style={styles.td}>{item.state ?? item.status ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
