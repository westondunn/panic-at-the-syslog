/**
 * CardList – Material Dashboard–style card list for Recommendations / Insights.
 *
 * Props:
 *  - title       : string
 *  - subtitle    : string
 *  - items       : array
 *  - filterKeys  : keys to search
 *  - renderCard  : (item, index) => React node
 *  - emptyText   : string
 *  - noMatchText : string
 */
import { useState } from "react";

export default function CardList({
  title,
  subtitle,
  items,
  filterKeys = [],
  renderCard,
  emptyText = "No items.",
  noMatchText = "No items match your filter.",
}) {
  const [query, setQuery] = useState("");

  const q = query.trim().toLowerCase();
  const filtered = q
    ? items.filter((item) =>
        filterKeys.some(
          (k) => item[k] != null && String(item[k]).toLowerCase().includes(q),
        ),
      )
    : items;

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

      {/* Items */}
      {filtered.length === 0 ? (
        <p className="mt-8 text-center text-text-secondary">
          {items.length === 0 ? emptyText : noMatchText}
        </p>
      ) : (
        <ul className="space-y-3">
          {filtered.map((item, i) => (
            <li key={item.id ?? i}>{renderCard(item, i)}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
