# Phase 2 — School Equity Profile

## Objective

Build a searchable Schools directory and detailed School Equity Profile experience linked from Portfolio Review.

## Scope

- Schools directory at `/schools.html`.
- Directory search by DBN or School Name.
- Borough and School Year filters.
- 100-record API pagination with internal scrolling.
- DBN-aware search across all boroughs.
- Server-side School Name search across the full available dataset.
- Detailed School Equity Profile keyed by `dbn + school_year`.
- Portfolio Review DBN links to the matching School Equity Profile.
- Profile-to-directory back navigation.
- School Year switching for the selected school.
- Demographic 90%+ attendance, four-year graduation, gaps, denominators, matched-record counts, and data-quality warnings.
- Loading, empty, API-error, not-found, and insufficient-data states.
- Responsive layout, keyboard navigation, visible focus, and accessible status messaging.
- Observational interpretation only.

## Non-goals

- Budget or resource context.
- Fair Student Funding integration.
- Persistent action plans.
- Elementary or middle schools.
- Gender-by-race intersection metrics.
- New opaque risk scores or review-signal definitions.
- Causal claims.
- Replacing the existing Portfolio Review data presentation with the Schools profile presentation.

## Inputs

- Phase 1 Portfolio Review implementation at commit `4307db8`.
- `data/portfolio-snapshot.json`.
- Existing normalized attendance and graduation pair records.
- Existing Portfolio Review API and filter behavior.
- Phase 1 responsive and accessibility conventions.

## Deliverables

- `api/profile.py` profile lookup route.
- Schools directory and profile UI in `schools.html` and `school-profile.js`.
- Portfolio Review DBN/profile navigation in `app.js`.
- Local routing support in `server.py`.
- Schools/profile layout additions in `styles.css`.
- API and interaction verification coverage.
- This phase documentation and final review evidence.

## Acceptance criteria

- The Schools tab opens a directory when no school is selected.
- The directory shows available schools through 100-record pagination and internal scrolling.
- DBN and School Name searches query the full available dataset.
- A valid DBN search ignores Borough filtering.
- Borough and School Year filters query the API and reset pagination.
- Clicking a DBN from Portfolio Review opens the matching `dbn + school_year` profile.
- A profile displays all available demographic rows for the selected school/year.
- Missing or suppressed values display as unavailable rather than zero.
- Data Quality Notes explain missing, suppressed, unmatched, and insufficient evidence.
- School Year switching reloads the same school’s profile for the selected year.
- Invalid or unavailable profiles show a clear not-found or insufficient-data state.
- Loading, empty, API-error, and no-results states are present and understandable.
- Profile-to-directory back navigation works.
- Console errors are absent during verified flows.
- Keyboard navigation and visible focus states work for directory, filters, links, and profile controls.
- Desktop, tablet, and mobile layouts remain usable.
- Existing Portfolio Review filters, disparity behavior, and Action Plans navigation are preserved.

## Risks

- Demographic coverage varies by school year; 2015–2017 and 2019 currently contain All Students-only records, while 2018 is partial.
- Snapshot freshness and source coverage may change.
- Missing, suppressed, and small-denominator values may limit profile evidence.
- DBN normalization and year alignment must remain consistent.
- Directory filtering and pagination must not reintroduce borough/search coupling.
- Browser caching can obscure newly changed frontend scripts during local verification.

## Exit criteria

- Implementation is complete within the approved scope.
- Relevant tests pass and `git diff --check` passes.
- Changed-file line scanning is complete.
- Read-only REVIEWER returns `APPROVE` with no unresolved blocker or major findings.
- User verifies the localhost preview.
- User explicitly approves staging, commit, and push if requested.
- After review and approved Git operations, this document is updated with final evidence and completion status.

## Completion evidence

- Phase 2 implementation completed at the approved Schools directory and School Equity Profile routes.
- User verified profile lookup, validation, directory search, Borough and School Year filters, pagination, internal scrolling, profile year switching, navigation, loading, empty, API-error, not-found, insufficient-data, console, keyboard, and focus behavior.
- Automated verification passed: 14/14 tests.
- `git diff --check` passed.
- Read-only REVIEWER verdict: `APPROVE`.
- The intentional untracked `school-equity-resource-monitor-mockup/` reference artifact was retained for visual alignment.

## Status

Phase 2 complete.
