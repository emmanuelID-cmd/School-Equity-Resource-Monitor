# Phase 3 — Equity Comparison Chart

## Objective

Add an accessible visual comparison of demographic 90%+ attendance and four-year graduation outcomes to the School Equity Profile.

## Scope

- Plot available standalone demographic groups by attendance and graduation rates.
- Synchronize the chart with the selected School Year.
- Provide hover and keyboard-focus point details.
- Preserve the demographic table as the complete data representation.
- Provide accessible text and insufficient-data equivalents.
- Preserve observational interpretation.

## Non-goals

- Causal trendlines or regression claims.
- New risk scores or review-signal definitions.
- Gender-by-race intersections.
- Budget/resource context.
- Action-plan persistence.
- Elementary or middle schools.

## Inputs

- Phase 2 baseline at commit `c79d801`.
- Existing `/api/profile` response.
- Existing School Equity Profile table and year selector.

## Deliverables

- Accessible attendance-versus-graduation chart in the School Equity Profile.
- Chart styling for desktop, tablet, and mobile layouts.
- Chart-specific verification and final review evidence.

## Acceptance criteria

- Matched demographic records render as chart points.
- X-axis represents 90%+ attendance and Y-axis represents four-year graduation.
- Point details include demographic, rates, gap, and denominators.
- Hover and keyboard focus expose equivalent details.
- Missing/suppressed values are not plotted as zero.
- The existing table remains unchanged as the complete detail view.
- School Year changes update the chart with the profile.
- Insufficient data has a clear explanation.
- Accessible text equivalent is available.
- Existing Phase 2 navigation, filters, states, and table behavior are preserved.
- Existing tests and chart verification pass with no console errors.

## Risks

- Small or missing denominators may make plotted points misleading without context.
- Mobile chart sizing must not reduce table usability.
- Chart labels and focus behavior must remain accessible without relying on color.

## Exit criteria

- Implementation, verification, changed-line scanning, and read-only review are complete.
- User verifies the localhost preview.
- Phase 3 completion evidence is added only after reviewer clearance and explicit user approval.

## Completion evidence

- User verified the dumbbell chart’s attendance and graduation endpoints, connecting gap distance, numeric labels, hover, click, keyboard focus, and responsive desktop/tablet/mobile behavior.
- User confirmed the existing table, warnings, year switching, and navigation remain unchanged.
- Automated verification passed: 15/15 tests.
- `git diff --check` passed.
- Read-only REVIEWER verdict: `APPROVE`.

## Status

Phase 3 complete. Implementation, review, commit, and push are complete.
