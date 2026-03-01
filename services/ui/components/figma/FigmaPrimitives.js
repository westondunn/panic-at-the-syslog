export function FigmaPageFrame({ children, nodeId }) {
  return (
    <section
      className="min-h-[850px] overflow-hidden rounded-card border border-primary-100 bg-surface shadow-card"
      data-node-id={nodeId}
    >
      {children}
    </section>
  );
}

export function FigmaSplitLayout({ children, nodeId }) {
  return (
    <div className="flex min-h-[850px] flex-col xl:flex-row" data-node-id={nodeId}>
      {children}
    </div>
  );
}

export function FigmaLeftPanel({ children, nodeId }) {
  return (
    <aside
      className="flex w-full flex-col justify-between bg-[#e4e4e4] p-8 xl:w-[600px] xl:p-16"
      data-node-id={nodeId}
    >
      {children}
    </aside>
  );
}

export function FigmaRightPanel({ children, nodeId }) {
  return (
    <div className="flex flex-1 flex-col gap-12 p-8 xl:p-16" data-node-id={nodeId}>
      {children}
    </div>
  );
}

export function FigmaSection({ children, nodeId, className = "" }) {
  return (
    <section className={className} data-node-id={nodeId}>
      {children}
    </section>
  );
}

export function FigmaH4({ children, nodeId }) {
  return (
    <h2
      className="text-[32px] leading-[1.235] tracking-[0.25px] text-[#212121]"
      data-node-id={nodeId}
    >
      {children}
    </h2>
  );
}

export function FigmaBody({ children, nodeId }) {
  return (
    <p className="text-base leading-[1.5] tracking-[0.15px]" data-node-id={nodeId}>
      {children}
    </p>
  );
}

export function FigmaCtaRow({ children, nodeId }) {
  return (
    <div className="rounded border border-primary-100 bg-surface p-6" data-node-id={nodeId}>
      <div className="flex flex-col gap-4 sm:flex-row">{children}</div>
    </div>
  );
}

export function FigmaOutlinedLinkCta({ children, href, nodeId, tone = "primary" }) {
  const toneClass =
    tone === "secondary"
      ? "border-[#ce93d8] text-[#9c27b0]"
      : "border-[#90caf9] text-[#1976d2]";

  return (
    <a
      className={`inline-flex items-center justify-center rounded border px-[22px] py-2 text-[15px] font-medium uppercase leading-[26px] tracking-[0.46px] ${toneClass} underline`}
      href={href}
      target="_blank"
      rel="noreferrer"
      data-node-id={nodeId}
    >
      {children}
    </a>
  );
}

export function FigmaOutlinedLabelCta({ children, nodeId, tone = "secondary" }) {
  const toneClass = tone === "primary" ? "border-[#90caf9] text-[#1976d2]" : "border-[#ce93d8] text-[#9c27b0]";

  return (
    <p
      className={`inline-flex items-center justify-center rounded border px-[22px] py-2 text-[15px] font-medium uppercase leading-[26px] tracking-[0.46px] ${toneClass}`}
      data-node-id={nodeId}
    >
      {children}
    </p>
  );
}

export function FigmaPanelFooter({
  left,
  right,
  nodeId,
  leftNodeId,
  rightNodeId,
}) {
  return (
    <div
      className="mt-12 flex items-center justify-between text-xs leading-[1.66] tracking-[0.4px] text-text-secondary"
      data-node-id={nodeId}
    >
      <span data-node-id={leftNodeId}>{left}</span>
      <span data-node-id={rightNodeId}>{right}</span>
    </div>
  );
}

export function FigmaInfoList({
  title,
  items,
  nodeId,
  className = "text-base leading-[1.5] tracking-[0.15px]",
}) {
  return (
    <div className={className} data-node-id={nodeId}>
      <p>{title}</p>
      <ul className="list-disc pl-6">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export function FigmaRichTextBlock({
  nodeId,
  paragraphs,
  className = "space-y-4 text-base leading-[1.5] tracking-[0.15px]",
}) {
  return (
    <div className={className} data-node-id={nodeId}>
      {paragraphs.map((paragraph) => (
        <p key={paragraph.id} data-node-id={paragraph.id}>
          {paragraph.parts.map((part, index) =>
            part.type === "link" ? (
              <a
                key={`${paragraph.id}-${index}`}
                className="underline"
                href={part.href}
                target="_blank"
                rel="noreferrer"
              >
                {part.text}
              </a>
            ) : (
              <span key={`${paragraph.id}-${index}`}>{part.text}</span>
            ),
          )}
        </p>
      ))}
    </div>
  );
}
