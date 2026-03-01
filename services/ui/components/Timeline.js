/**
 * Timeline – Material Dashboard–style vertical timeline list.
 *
 * Props:
 *  - items : [{ id, icon?, color?, title, description?, time }]
 */

const DOT_COLORS = {
  error: "bg-error",
  warning: "bg-warning",
  success: "bg-success",
  info: "bg-info",
  default: "bg-text-disabled",
};

export default function Timeline({ items = [] }) {
  if (items.length === 0) {
    return (
      <p className="text-sm text-text-secondary">
        No recent activity to display.
      </p>
    );
  }

  return (
    <ul className="relative space-y-6 pl-6">
      {/* Vertical line */}
      <span
        className="absolute left-[7px] top-2 bottom-2 w-0.5 bg-primary-100"
        aria-hidden="true"
      />

      {items.map((item, idx) => (
        <li key={item.id ?? idx} className="relative flex gap-4">
          {/* Dot */}
          <span
            className={`absolute -left-6 top-1 h-3.5 w-3.5 rounded-full ring-2 ring-surface ${DOT_COLORS[item.color] ?? DOT_COLORS.default}`}
            aria-hidden="true"
          />

          <div className="min-w-0 flex-1">
            <div className="flex items-baseline justify-between gap-2">
              <p className="text-sm font-medium text-text-primary truncate">
                {item.icon && <span className="mr-1.5">{item.icon}</span>}
                {item.title}
              </p>
              {item.time && (
                <time className="shrink-0 text-[0.65rem] text-text-disabled">
                  {item.time}
                </time>
              )}
            </div>
            {item.description && (
              <p className="mt-0.5 text-xs text-text-secondary truncate">
                {item.description}
              </p>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}
