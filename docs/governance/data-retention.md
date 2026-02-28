# Panic! At The Syslog — Data Retention

## Goal
Balance forensic usefulness with privacy and storage discipline:
- Keep raw logs only as long as needed for processing and review.
- Keep critical evidence indefinitely when necessary.
- Keep analysis artifacts (insights) as the long-term record.

## Data classes
1. **Raw syslog**
   - Unstructured line data
   - Potentially sensitive (hostnames, internal IPs, identifiers)
2. **Normalized events**
   - Structured canonical representation
   - Typically less verbose but still sensitive
3. **Findings**
   - Rule-derived detections with evidence pointers
4. **Insights**
   - Recommendations and rationale (LLM or deterministic)
   - Stored long-term for operational memory

## Default policy
- Raw syslog spool: short TTL (e.g., 7–14 days) with extension by review hold.
- Normalized events: TTL (e.g., 30–90 days) unless marked critical/pinned.
- Findings: retained long-term (configurable).
- Insights: retained indefinitely by default.

## Review-driven retention
A review workflow exists to decide what to keep:
- **Confirm incident:** pin relevant evidence (raw excerpt hash + normalized event IDs).
- **False positive:** keep insight/finding but allow raw to expire.
- **Ignore:** keep insight only (or delete, depending on org policy).

## Critical retention criteria (suggested)
Retain indefinitely when:
- Severity is critical, OR
- Security category with high confidence, OR
- Manually pinned by an admin, OR
- Policy mandates retention (compliance environment)

## Deletion & verification
- Purge jobs must be deterministic and logged.
- Provide periodic verification reports (e.g., “raw spool size”, “expired vs pinned counts”).