import {
    Area,
    AreaChart,
    Bar,
    BarChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";
import ChartCard from "../components/ChartCard";
import StatCard from "../components/StatCard";
import Timeline from "../components/Timeline";

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
  // Demo chart data — will be replaced by real API data later
  const CHART_DATA = [
    { day: "Mon", incidents: counts.incidents > 0 ? 3 : 0 },
    { day: "Tue", incidents: counts.incidents > 0 ? 5 : 0 },
    { day: "Wed", incidents: counts.incidents > 0 ? 2 : 0 },
    { day: "Thu", incidents: counts.incidents > 0 ? 7 : 0 },
    { day: "Fri", incidents: counts.incidents > 0 ? 4 : 0 },
    { day: "Sat", incidents: counts.incidents > 0 ? 1 : 0 },
    { day: "Sun", incidents: counts.incidents > 0 ? 6 : 0 },
  ];

  const THROUGHPUT_DATA = Array.from({ length: 24 }, (_, i) => ({
    hour: `${String(i).padStart(2, "0")}:00`,
    events: Math.floor(Math.random() * 500 + 200),
  }));

  const ACTIVITY_ITEMS = [
    {
      id: 1,
      title: "New critical incident detected",
      description: "auth-server: brute-force login pattern",
      time: "2 min ago",
      color: "error",
      icon: "🔴",
    },
    {
      id: 2,
      title: "Recommendation generated",
      description: "Block IP range 203.0.113.0/24",
      time: "15 min ago",
      color: "info",
      icon: "💡",
    },
    {
      id: 3,
      title: "Finding promoted to incident",
      description: "Unusual outbound traffic on port 4444",
      time: "1 hr ago",
      color: "warning",
      icon: "⚠️",
    },
    {
      id: 4,
      title: "Pipeline health check passed",
      description: "All services reporting nominal",
      time: "2 hr ago",
      color: "success",
      icon: "✅",
    },
  ];
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

      {/* Charts + timeline */}
      <div className="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Incidents over time – bar chart */}
        <div className="pt-6">
          <ChartCard
            title="Incidents This Week"
            subtitle="Daily incident count"
            gradient="dark"
            footer="Updated just now"
          >
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={CHART_DATA}
                margin={{ top: 8, right: 8, bottom: 0, left: -20 }}
              >
                <XAxis
                  dataKey="day"
                  tick={{ fill: "#fff", fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: "#fff9", fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={{
                    background: "#1a2035",
                    border: "none",
                    borderRadius: 8,
                    color: "#fff",
                    fontSize: 12,
                  }}
                  itemStyle={{ color: "#fff" }}
                  cursor={{ fill: "rgba(255,255,255,0.05)" }}
                />
                <Bar
                  dataKey="incidents"
                  fill="rgba(255,255,255,0.8)"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Pipeline throughput – area chart */}
        <div className="pt-6">
          <ChartCard
            title="Pipeline Throughput"
            subtitle="Events processed per hour"
            gradient="info"
            footer="Last 24 hours"
          >
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={THROUGHPUT_DATA}
                margin={{ top: 8, right: 8, bottom: 0, left: -20 }}
              >
                <XAxis
                  dataKey="hour"
                  tick={{ fill: "#fff", fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: "#fff9", fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={{
                    background: "#1a2035",
                    border: "none",
                    borderRadius: 8,
                    color: "#fff",
                    fontSize: 12,
                  }}
                  itemStyle={{ color: "#fff" }}
                  cursor={{ stroke: "rgba(255,255,255,0.3)" }}
                />
                <Area
                  type="monotone"
                  dataKey="events"
                  stroke="#fff"
                  fill="rgba(255,255,255,0.2)"
                  strokeWidth={2}
                />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>
      </div>

      {/* Recent activity timeline */}
      <div className="mt-8">
        <div className="rounded-card bg-surface p-6 shadow-card">
          <h3 className="mb-4 text-base font-semibold text-text-primary">
            Recent Activity
          </h3>
          <Timeline items={ACTIVITY_ITEMS} />
        </div>
      </div>
    </>
  );
}
