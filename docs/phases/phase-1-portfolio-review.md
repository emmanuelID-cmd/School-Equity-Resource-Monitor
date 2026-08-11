# Phase 1 — Portfolio Review

## Objective

Turn the Phase 0 normalized records into an operational portfolio review screen for NYC high schools.

## Scope

- School year, borough, and review-signal filters.
- Priority review queue based on transparent attendance/graduation observations.
- Selected-school evidence panel with matched pairs, denominators, and warnings.
- Loading, insufficient-data, and API-error states.
- Cursor-paginated `/api/portfolio` route that returns complete school-year records in pages of 100.

## Non-goals

- Budget context, persistent action plans, or elementary/middle-school records.
- Causal claims or opaque risk scores.
- Client-side direct fetching of raw NYC metric rows in production.

## Acceptance criteria

- [x] Filters update the queue and selected-school evidence.
- [x] Every review signal is traceable to matched attendance and graduation records.
- [x] Small denominators and missing matches are visible.
- [x] The screen remains usable on narrow layouts.

## Planned copy refinement

- Approved: add explanatory text above the School Year filter: “Reviewable school records currently run through 2022; later records do not yet have sufficient matched attendance and graduation data.” Keep this as planned copy until the next UI refinement pass.

## Exit criteria

Phase 1 is complete. The live Portfolio Review screen was tested against loading, filtering, empty, error, cursor, disparity-threshold, and responsive states. The implementation is in commit `19ec683`.
