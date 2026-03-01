import Badge, { severityVariant } from "../components/Badge";
import DataTable from "../components/DataTable";

const API_BASE = process.env.API_BASE_URL || "http://localhost:8000";

export async function getServerSideProps() {
  const token = process.env.API_INTERNAL_TOKEN || "";
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  try {
    const res = await fetch(`${API_BASE}/api/v1/incidents`, { headers });
    if (!res.ok) return { props: { incidents: [] } };
    const data = await res.json();
    return {
      props: { incidents: Array.isArray(data.items) ? data.items : [] },
    };
  } catch {
    return { props: { incidents: [] } };
  }
}

const COLUMNS = [
  { key: "id", label: "ID" },
  {
    key: "summary",
    label: "Summary",
    render: (row) => row.summary ?? row.title ?? row.message ?? "—",
  },
  {
    key: "severity",
    label: "Severity",
    render: (row) =>
      row.severity ? (
        <Badge variant={severityVariant(row.severity)}>{row.severity}</Badge>
      ) : (
        "—"
      ),
  },
  { key: "status", label: "Status" },
];

const FILTER_KEYS = ["id", "summary", "title", "message", "severity", "status"];

export default function IncidentsPage({ incidents }) {
  return (
    <DataTable
      title="Incidents"
      subtitle="Active and resolved incidents."
      columns={COLUMNS}
      rows={incidents}
      filterKeys={FILTER_KEYS}
      emptyText="No incidents found. The system is quiet."
      noMatchText="No incidents match your filter."
    />
  );
}
