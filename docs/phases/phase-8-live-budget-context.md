# Phase 8 — Live Partial Budget/Resource Context Planning

## Objective

Plan a separate **Budget / Resources** navigation area that can present live, clearly labeled partial budget context without treating it as complete or definitive financial data.

## Placement

- New top-level navigation item: **Budget / Resources**.
- Do not embed budget data directly into Portfolio Review, Schools, or Action Plans.
- A future contextual link from a School Equity Profile may open the selected school in Budget / Resources.

## Scope

- Define school and fiscal-year selection.
- Define live Galaxy context retrieval through an approved controlled retrieval method.
- Label source, fiscal year, retrieval date, metric type, available fields, and missing fields.
- Define partial, unavailable, invalid, suppressed, stale, and not-comparable states.
- Preserve observational language and source limitations.
- Define responsive and accessible behavior.
- Define security, retry, timeout, response validation, and recovery requirements for a future implementation.

## Partial-data rules

- Show available fields only with a visible **Partial budget context** warning when the record is incomplete.
- Identify which fields, years, or categories are missing.
- Never fill missing values from district, citywide, or unrelated sources.
- Never calculate unsupported totals, rankings, or per-student comparisons.
- Never represent budgeted inputs as actual spending.
- Distinguish missing, unavailable, invalid, suppressed, stale, and not-comparable states.
- Preserve source URL, source owner, fiscal year, reporting period, and retrieval date.
- Allow the user to open or verify the originating source when possible.

## Proposed user flow

1. User opens **Budget / Resources** from the main navigation.
2. User selects or searches for a school.
3. User selects a fiscal year.
4. The system retrieves the approved live source record.
5. The page displays available context, source metadata, and limitations.
6. If the record is incomplete or unavailable, the page explains what could not be retrieved and does not substitute another value.

## Future display requirements

- School identity and DBN/BN/source-code mapping.
- Fiscal year displayed separately from school year.
- Exact reporting period and source publication date when available.
- Metric type clearly labeled as allocation, projection, estimate, budgeted position, or actual spending.
- Enrollment basis and calculation notes when a per-student value is present.
- Source owner, source URL, retrieval date, and freshness warning.
- Field-level missing-data indicators.
- Readable warnings that do not rely on color alone.
- Responsive layout for desktop, tablet, and mobile.
- Keyboard navigation, visible focus, semantic labels, and screen-reader announcements.

## Future retrieval and validation contract

The implementation must use an approved controlled retrieval method. Direct Galaxy HTML parsing is not authorized by this planning document.

Before displaying a record, the future backend must validate:

- HTTP response status and timeout behavior.
- Response schema and required fields.
- Data types, numeric validity, and allowed metric types.
- DBN, BN, or school-code mapping.
- Fiscal year and reporting-period format.
- Source-specific availability and suppression status.
- Duplicate and unexpected-record behavior.

Failed validation must produce an explicit user-facing recovery state and must not silently drop, substitute, or reinterpret the record.

## Required implementation gate

Before Builder implements this feature, the user must separately approve:

- The controlled live retrieval method.
- The exact Galaxy fields permitted for display.
- Partial-data warning language.
- Missing, suppressed, unavailable, stale, and not-comparable behavior.
- Fiscal-year handling.
- Source and retrieval-date presentation.
- Security, retry, timeout, and validation behavior.

## Non-goals

- No UI implementation in this planning phase.
- No navigation changes in this planning phase.
- No production API changes.
- No Supabase or database changes.
- No snapshot creation.
- No complete budget ledger.
- No blended metrics or rankings.
- No causal claims.
- No Action Plan automation.

## Acceptance criteria

- Separate Budget / Resources navigation placement is documented.
- Live partial-data behavior and warnings are documented.
- Source, fiscal-year, reporting-period, and retrieval metadata requirements are documented.
- Missing, invalid, suppressed, stale, unavailable, and not-comparable states are defined.
- Retrieval validation and recovery requirements are documented.
- Accessibility and responsive requirements are documented.
- The implementation gate is explicit.
- No production UI, API, database, Supabase, snapshot, or retrieval implementation is created.
- `.env` remains ignored and outside all artifacts.

## Exit criteria

Phase 8 planning is complete when this document is Reviewer-approved. Planning completion does not mean the Budget / Resources UI or backend has been built or that implementation is authorized.

## Status

Phase 8 Builder documentation complete; Reviewer approval is pending. This phase remains read-only.
