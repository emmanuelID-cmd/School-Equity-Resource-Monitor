# Phase 7 — Budget/Resource Context Implementation Readiness

## Objective

Define a safe future product layer for budget/resource context without authorizing production implementation before an approved stable source exists.

## Scope

- Define the proposed budget/resource UI and its user purpose.
- Define the backend integration contract required by a future UI.
- Keep allocations, projections, estimated expenditures, budgeted positions, and actual spending separate.
- Define fiscal-year display and school-year comparison rules.
- Define DBN, BN, or school-code mapping requirements.
- Define missing-data, unavailable-data, suppressed-record, and source-warning states.
- Define how budget context could appear beside observational attendance/graduation patterns.
- Define responsive and accessible UI requirements for a future implementation.
- Specify the source-readiness gate before implementation begins.

## Non-goals

- No budget UI implementation.
- No Galaxy HTML parser.
- No production API changes.
- No Supabase or database changes.
- No snapshot creation.
- No blended funding metric.
- No rankings.
- No causal conclusions.
- No Action Plan automation based on budget values.

## Proposed product purpose

If a stable source is approved later, budget/resource context may help users review whether school-level allocation, projection, estimated expenditure, or budgeted-position information should be considered alongside observed attendance and graduation patterns. It must remain contextual and observational. The product must not state or imply that spending causes attendance, graduation, or demographic outcomes.

## Future UI requirements

- Clearly label the source and metric type on every budget-context view.
- Display fiscal year separately from school year.
- Show school identity, DBN/BN mapping, reporting period, and source publication date.
- Keep allocation, projection, estimate, budgeted position, and actual spending in separate sections or views.
- Show enrollment basis and calculation notes where a per-student value is displayed.
- Show source warnings when data is unavailable, incomplete, suppressed, stale, or not comparable.
- Never substitute a district, citywide, projection, or estimate value for a missing school record without explicit labeling.
- Preserve responsive behavior across desktop, tablet, and mobile.
- Preserve keyboard navigation, visible focus, semantic labels, and screen-reader announcements for warnings and errors.

## Future backend contract

A future implementation must expose source-separated records with at least:

- `dbn` or validated source identifier mapping.
- `school_code` or `bn` when supplied by the source.
- `school_year` only when explicitly supported by the source.
- `fiscal_year` and exact reporting period.
- `metric_type` such as allocation, projection, estimate, budgeted_position, or actual_spending.
- Metric value and unit.
- Enrollment count and enrollment basis when applicable.
- Source name, owner, URL, publication date, and retrieval date.
- Availability status distinguishing valid, missing, unavailable, suppressed, invalid, and not comparable.
- Source-specific notes and warnings.

The backend must validate response status, schema, required fields, types, identifier mapping, and source-specific period rules. It must not blend records from different sources into an unlabeled metric.

## Source-readiness gate

Phase 7 implementation cannot begin until a source satisfies all applicable requirements:

- Stable API, download, or explicitly approved controlled retrieval.
- School-level identifier mapping.
- Fiscal-year compatibility with the product's school-year context documented without assuming equivalence.
- Metric definitions and enrollment basis documented.
- Missing, unavailable, invalid, and suppressed-record behavior documented.
- High-school and population coverage tested.
- Source ownership, publication cadence, and source-transition behavior documented.
- Separate implementation plan approved by the user.

Galaxy HTML parsing is not an approved source contract. A controlled snapshot remains a separately approved fallback and is not authorized by this planning document.

## Acceptance criteria

- Proposed UI purpose and boundaries are documented.
- Future backend fields and validation requirements are documented.
- Source-separated metric behavior is explicit.
- Fiscal-year and school-year handling is explicit.
- Error, warning, accessibility, and responsive requirements are documented.
- The source-readiness gate is explicit.
- No production UI, API, database, or snapshot is created.
- `.env` remains ignored and outside all artifacts.

## Exit criteria

Phase 7 planning is complete when this document is Reviewer-approved. Planning completion does not mean budget integration has been built or that implementation is authorized.

## Status

Phase 7 Builder documentation complete; Reviewer approval is pending. No UI or backend implementation has begun.
