# Figma Import Spec (Repo-Local)

This document defines the default process and acceptance criteria for importing
Figma designs into the UI codebase.

## Purpose

- Keep imports reviewable and deterministic.
- Preserve product shell identity (logo, nav, governance banner).
- Maintain semantic, accessible markup while staying pixel-close to source.

## Non-negotiables

- Keep existing sidebar logo and brand treatment unchanged unless explicitly
  requested.
- Do not introduce proprietary integrations by default.
- Do not add new UI dependencies unless approved.
- Keep imports within existing Next.js + Tailwind approach used in `services/ui`.

## Handoff workflow (required)

Use the following handoff sequence for each import task:

1. Planner (Panic)
2. Implementer (Panic)
3. Security Review (Panic)

### Planner output requirements

- Source Figma URL/file key/node IDs.
- Route mapping (new page vs existing page update).
- Fidelity target (`pixel-close`, `adapted`, or `exact`).
- Explicit in-scope vs out-of-scope list.
- Risks and validation checklist.

### Implementer output requirements

- Minimal diff summary with changed files.
- Reusable primitive usage and new primitives added.
- Semantic corrections made (links/buttons/headings/lists).
- Verification command results.

### Security Review output requirements

- External link hardening (`target`, `rel`) checks.
- No secret or sensitive data leakage in UI code.
- Dependency and supply-chain impact statement.
- Required fixes vs recommendations.

## Route and shell rules

- Imported content lives in page body only.
- App shell remains in `_app.js` + `Sidebar`.
- Sidebar logo and core navigation remain stable unless task says otherwise.

## Primitive-first implementation

Before importing multiple screens, create/extend reusable primitives under:

- `services/ui/components/figma/`

Current starter primitives:

- `FigmaPageFrame`
- `FigmaSplitLayout`
- `FigmaLeftPanel`
- `FigmaRightPanel`
- `FigmaSection`
- `FigmaH4`
- `FigmaBody`
- `FigmaCtaRow`
- `FigmaOutlinedLinkCta`
- `FigmaOutlinedLabelCta`
- `FigmaPanelFooter`
- `FigmaInfoList`
- `FigmaRichTextBlock`
- `FigmaCenteredCanvas`

## Fidelity and semantics policy

- Preserve layout geometry, typography scale, spacing rhythm, and visual intent.
- Keep source text accurate (including symbols).
- Render anchors only when source contains an actionable URL.
- Render non-linked CTAs as non-anchor elements.
- Include `data-node-id` on key wrappers for traceability.

## Acceptance checklist per imported screen

- Route renders with no runtime errors.
- Visual structure matches Figma at desktop and mobile breakpoints.
- Headings and body text use correct hierarchy.
- CTA semantics are correct (link vs label).
- External URLs are safe (`target="_blank"` and `rel="noreferrer"`).
- `npm run build` passes for `services/ui`.

## Suggested implementation cadence

1. Import one screen.
2. Extract/adjust primitives.
3. Validate and review.
4. Import next screen using primitives.
