# Phase 9 — Budget/Resource Context Implementation

## Objective

Implement a separate Budget / Resources feature that presents live Galaxy budget context as partial, observational information rather than a complete or definitive financial record.

## Scope completed

- Added a separate Budget / Resources navigation destination.
- Added school discovery by DBN, school code, and school name.
- Added debounced school search with internally scrollable results.
- Added fiscal-year selection from 2006 through 2026.
- Added controlled server-side Galaxy retrieval.
- Added school-code and fiscal-year validation.
- Added year-mismatch protection.
- Added source metadata, retrieval date, and partial-data warnings.
- Added missing, invalid, unavailable, timeout, not-found, and not-comparable handling.
- Added internal scrolling for search results and budget records.
- Preserved responsive and keyboard-accessible controls.
- Preserved existing Portfolio Review, Schools, and Action Plans behavior.

## Data boundary

Galaxy values are budgeted context and are not presented as definitive actual spending. Missing values are not substituted with district, citywide, projection, estimate, or unrelated records. No budget rankings, blended metrics, causal claims, or Action Plan automation were added.

## Implementation files

- `api/budget.py`
- `budget.html`
- `budget.js`
- `server.py`
- `shared-header.js`
- `styles.css`

## Verification evidence

- Existing automated test suite: 15 tests passed.
- Valid `M292` + FY2025 request returned FY2025 data and source date.
- Valid `M292` + FY2026 request returned FY2026 data and source date.
- School search returned `M292` / Orchard Collegiate Academy.
- Invalid school codes and fiscal years returned explicit validation errors.
- Clearing the school input preserved displayed data and prevented unintended year requests.
- Load Budget Context remained disabled until a school result and fiscal year were selected.
- Manual browser verification confirmed loading, search, year switching, error handling, responsive behavior, and keyboard interaction.

## Known non-blocking issue

The school-search dropdown may retain a blue browser-rendered aesthetic in Safari. This does not affect search behavior, data retrieval, validation, accessibility operation, or existing product functionality. It is intentionally deferred as a minor visual refinement.

## Non-goals

- No Supabase or database persistence.
- No complete budget ledger.
- No actual-spending claim.
- No budget ranking or blended metric.
- No causal interpretation.
- No Action Plan automation based on budget context.

## Risks and limitations

- Galaxy remains an HTML-form source rather than a stable machine-readable API.
- Returned records may be partial or unavailable.
- Fiscal year must remain distinct from school year.
- Source changes may require adapter maintenance.

## Status

Phase 9 implementation complete. Budget / Resources is live partial context only; future source improvements or visual refinements require separate approved work.
