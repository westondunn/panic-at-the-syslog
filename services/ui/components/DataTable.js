/**
 * DataTable – Material Dashboard–style table with header, search filter,
 * sortable columns, pagination, and optional empty-state message.
 *
 * Props:
 *  - title       : string (page heading)
 *  - subtitle    : string
 *  - columns     : [{ key, label, render?, sortable? }]
 *  - rows        : array of objects
 *  - filterKeys  : array of keys to search against
 *  - emptyText   : string shown when no rows exist
 *  - noMatchText : string shown when filter yields nothing
 *  - pageSize    : rows per page (default 10)
 */
import { useMemo, useState } from "react";

function ChevronUp({ className = "" }) {
  return (
    <svg
      className={className}
      viewBox="0 0 20 20"
      fill="currentColor"
      width="14"
      height="14"
    >
      <path
        fillRule="evenodd"
        d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function ChevronDown({ className = "" }) {
  return (
    <svg
      className={className}
      viewBox="0 0 20 20"
      fill="currentColor"
      width="14"
      height="14"
    >
      <path
        fillRule="evenodd"
        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
        clipRule="evenodd"
      />
    </svg>
  );
}

export default function DataTable({
  title,
  subtitle,
  columns,
  rows,
  filterKeys = [],
  emptyText = "No data.",
  noMatchText = "No items match your filter.",
  pageSize = 10,
}) {
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState(null);
  const [sortDir, setSortDir] = useState("asc"); // "asc" | "desc"
  const [page, setPage] = useState(0);

  const q = query.trim().toLowerCase();

  // Filter
  const filtered = useMemo(() => {
    const base = q
      ? rows.filter((row) =>
          filterKeys.some(
            (k) => row[k] != null && String(row[k]).toLowerCase().includes(q),
          ),
        )
      : rows;

    // Sort
    if (!sortKey) return base;
    return [...base].sort((a, b) => {
      const aVal = a[sortKey] ?? "";
      const bVal = b[sortKey] ?? "";
      const cmp = String(aVal).localeCompare(String(bVal), undefined, {
        numeric: true,
        sensitivity: "base",
      });
      return sortDir === "asc" ? cmp : -cmp;
    });
  }, [rows, q, filterKeys, sortKey, sortDir]);

  // Pagination
  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
  const safePage = Math.min(page, totalPages - 1);
  const paged = filtered.slice(safePage * pageSize, (safePage + 1) * pageSize);

  // Reset page on filter change
  const handleQueryChange = (e) => {
    setQuery(e.target.value);
    setPage(0);
  };

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
    setPage(0);
  };

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
          onChange={handleQueryChange}
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
        <>
          <div className="overflow-hidden rounded-card bg-surface shadow-card">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-primary-100 bg-background">
                  {columns.map((col) => {
                    const isSorted = sortKey === col.key;
                    const sortable = col.sortable !== false;
                    return (
                      <th
                        key={col.key}
                        className={`px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-text-secondary ${sortable ? "cursor-pointer select-none hover:text-text-primary" : ""}`}
                        onClick={
                          sortable ? () => handleSort(col.key) : undefined
                        }
                        aria-sort={
                          isSorted
                            ? sortDir === "asc"
                              ? "ascending"
                              : "descending"
                            : undefined
                        }
                      >
                        <span className="inline-flex items-center gap-1">
                          {col.label}
                          {sortable &&
                            isSorted &&
                            (sortDir === "asc" ? (
                              <ChevronUp className="text-info" />
                            ) : (
                              <ChevronDown className="text-info" />
                            ))}
                        </span>
                      </th>
                    );
                  })}
                </tr>
              </thead>
              <tbody>
                {paged.map((row, i) => (
                  <tr
                    key={row.id ?? safePage * pageSize + i}
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

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="mt-4 flex items-center justify-between text-xs text-text-secondary">
              <span>
                Showing {safePage * pageSize + 1}–
                {Math.min((safePage + 1) * pageSize, filtered.length)} of{" "}
                {filtered.length}
              </span>
              <div className="flex gap-1">
                <button
                  onClick={() => setPage((p) => Math.max(0, p - 1))}
                  disabled={safePage === 0}
                  className="rounded-lg px-3 py-1.5 transition-colors hover:bg-primary-100 disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                {Array.from({ length: totalPages }, (_, i) => (
                  <button
                    key={i}
                    onClick={() => setPage(i)}
                    className={`rounded-lg px-3 py-1.5 transition-colors ${
                      i === safePage
                        ? "bg-info text-text-inverse font-semibold"
                        : "hover:bg-primary-100"
                    }`}
                  >
                    {i + 1}
                  </button>
                ))}
                <button
                  onClick={() =>
                    setPage((p) => Math.min(totalPages - 1, p + 1))
                  }
                  disabled={safePage >= totalPages - 1}
                  className="rounded-lg px-3 py-1.5 transition-colors hover:bg-primary-100 disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
