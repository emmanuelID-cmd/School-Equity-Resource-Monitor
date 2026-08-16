# Phase 10.3 — Schools Directory

## Objective

Make school discovery clear and non-repetitive before a user enters a full School Equity Profile.

## Scope

- Present one directory record per DBN.
- Order schools by borough: Brooklyn, Bronx, Manhattan, Queens, Staten Island; then DBN ascending.
- Use the shared latest-record API to display the latest year with comparison-capable evidence where one exists; otherwise retain the school using its latest raw record.
- Open the School Equity Profile at the displayed year.
- Keep school-specific historical year selection inside the full profile.

## Acceptance criteria

- No school appears repeatedly because of historical school-year records.
- The directory does not require users to filter to a single year before finding a school.
- The displayed year represents the latest valid matched comparison, not a percentage-gap threshold.
- Schools without a comparison-capable year remain discoverable without repetitive per-row limitation labels.
- Ordering and search remain reliable through pagination and API responses.

## Boundaries

- The Portfolio Review school-year filter remains a separate outcome-review control.
- Budget / Resources keeps its separate fiscal-year context.
- Do not introduce causal claims or scores.

## Dependency

Phase 10.2 complete and committed.

## Status

Planned.
