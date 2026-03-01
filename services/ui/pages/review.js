import Badge, { severityVariant } from "../components/Badge";
import DataTable from "../components/DataTable";

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

const COLUMNS = [
  { key: "id", label: "ID" },
  {
    key: "description",
    label: "Description",
    render: (row) =>
      row.description ?? row.summary ?? row.title ?? row.message ?? "—",
  },
  {
    key: "priority",
    label: "Priority",
    render: (row) => {
      const val = row.priority ?? row.severity;
      return val ? <Badge variant={severityVariant(val)}>{val}</Badge> : "—";
    },
  },
  {
    key: "state",
    label: "State",
    render: (row) => row.state ?? row.status ?? "—",
  },
];

const FILTER_KEYS = [
  "id",
  "description",
  "summary",
  "title",
  "message",
  "priority",
  "severity",
  "state",
  "status",
];

export default function ReviewPage({ items }) {
  return (
    <DataTable
      title="Review Queue"
      subtitle="Items awaiting human review before action is taken."
      columns={COLUMNS}
      rows={items}
      filterKeys={FILTER_KEYS}
      emptyText="Review queue is empty. Nothing awaiting action."
      noMatchText="No items match your filter."
    />
  );
}
