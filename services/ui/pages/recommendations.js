import Badge from "../components/Badge";
import CardList from "../components/CardList";

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

const FILTER_KEYS = [
  "id",
  "title",
  "summary",
  "recommendation",
  "type",
  "detail",
  "description",
];

function InsightCard({ item }) {
  return (
    <div className="rounded-card bg-surface p-5 shadow-card transition-shadow hover:shadow-card-hover">
      {item.type && <Badge variant="info">{item.type}</Badge>}
      <h3 className="mt-2 text-base font-semibold text-text-primary">
        {item.title ??
          item.summary ??
          item.recommendation ??
          item.id ??
          "Untitled Insight"}
      </h3>
      {item.detail && (
        <p className="mt-1 text-sm leading-relaxed text-text-secondary">
          {item.detail}
        </p>
      )}
      {item.description && (
        <p className="mt-1 text-sm leading-relaxed text-text-secondary">
          {item.description}
        </p>
      )}
    </div>
  );
}

export default function RecommendationsPage({ insights }) {
  return (
    <CardList
      title="Recommendations"
      subtitle="AI-generated insights and remediation recommendations."
      items={insights}
      filterKeys={FILTER_KEYS}
      renderCard={(item) => <InsightCard item={item} />}
      emptyText="No recommendations available yet."
      noMatchText="No recommendations match your filter."
    />
  );
}
