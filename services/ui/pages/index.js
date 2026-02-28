import StatCard from "../components/StatCard";

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

const STAT_CARDS = [
  {
    label: "Incidents",
    key: "incidents",
    gradient: "error",
    icon: "🔴",
    href: "/incidents",
  },
  { label: "Findings", key: "findings", gradient: "warning", icon: "🔍" },
  {
    label: "Recommendations",
    key: "insights",
    gradient: "info",
    icon: "💡",
    href: "/recommendations",
  },
  {
    label: "Review Queue",
    key: "reviewQueue",
    gradient: "dark",
    icon: "📋",
    href: "/review",
  },
];

export default function Dashboard({ counts }) {
  return (
    <>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-text-primary">Dashboard</h1>
        <p className="mt-1 text-sm text-text-secondary">
          Summary of current system state.
        </p>
      </div>

      {/* Stat cards grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-4">
        {STAT_CARDS.map(({ label, key, gradient, icon, href }) => (
          <StatCard
            key={key}
            label={label}
            value={counts[key]}
            gradient={gradient}
            icon={icon}
            href={href}
          />
        ))}
      </div>

      {/* Placeholder for future chart / activity panels */}
      <div className="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-card bg-surface p-6 shadow-card">
          <h3 className="mb-2 text-base font-semibold text-text-primary">
            Recent Activity
          </h3>
          <p className="text-sm text-text-secondary">
            Activity timeline will appear here once events are flowing.
          </p>
        </div>
        <div className="rounded-card bg-surface p-6 shadow-card">
          <h3 className="mb-2 text-base font-semibold text-text-primary">
            Pipeline Health
          </h3>
          <p className="text-sm text-text-secondary">
            Pipeline metrics and throughput charts will appear here.
          </p>
        </div>
      </div>
    </>
  );
}
