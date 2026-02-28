/**
 * DataTable – Material Dashboard–style table with header, search filter, and
 * optional empty-state message.
 *
 * Props:
 *  - title       : string (page heading)
 *  - subtitle    : string
 *  - columns     : [{ key, label, render? }]
 *  - rows        : array of objects
 *  - filterKeys  : array of keys to search against
 *  - emptyText   : string shown when no rows exist
 *  - noMatchText : string shown when filter yields nothing
 */
import { useState } from "react";

export default function DataTable({
  title,
  subtitle,
  columns,
  rows,
  filterKeys = [],
  emptyText = "No data.",
  noMatchText = "No items match your filter.",
}) {
  const [query, setQuery] = useState("");

  const q = query.trim().toLowerCase();
  const filtered = q
    ? rows.filter((row) =>
        filterKeys.some(
          (k) => row[k] != null && String(row[k]).toLowerCase().includes(q),
        ),
      )
    : rows;

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-text-primary">
          {title}
          <span className="ml-2 text-sm font-normal text-text-secondary">
            ({filtered.length})
          </span>
        </h1>
        {subtitle && (
          <p className="mt-1 text-sm text-text-secondary">{subtitle}</p>
        )}
      </div>

      {/* Search */}
      <div className="mb-4">
        <input
          type="search"
          placeholder={`Filter ${title.toLowerCase()}…`}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label={`Filter ${title.toLowerCase()}`}
          className="w-full max-w-md rounded-lg border border-primary-100 bg-surface px-4 py-2.5 text-sm text-text-primary placeholder:text-text-disabled outline-none transition focus:border-info focus:ring-2 focus:ring-info/20"
        />
      </div>

      {/* Table */}
      {filtered.length === 0 ? (
        <p className="mt-8 text-center text-text-secondary">
          {rows.length === 0 ? emptyText : noMatchText}
        </p>
      ) : (
        <div className="overflow-hidden rounded-card bg-surface shadow-card">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-primary-100 bg-background">
                {columns.map((col) => (
                  <th
                    key={col.key}
                    className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-text-secondary"
                  >
                    {col.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((row, i) => (
                <tr
                  key={row.id ?? i}
                  className="border-b border-primary-50 last:border-0 transition-colors hover:bg-background/60"
                >
                  {columns.map((col) => (
                    <td key={col.key} className="px-4 py-3 text-text-primary">
                      {col.render ? col.render(row) : (row[col.key] ?? "—")}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
