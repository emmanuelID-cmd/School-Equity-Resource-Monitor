# Phase 6.1 — Budget Source Validation

## Objective

Validate whether NYCPS School Budget At a Glance can support a controlled, source-separated budget-context integration without changing the completed product.

## Branch boundary

All prototype work in this document is isolated to `phase-6.1-budget-source-prototype`. No production UI, API, or data contract is changed by this prototype.

## Prototype deliverable

- `scripts/prototype_budget_source.py` performs a read-only request for one NYCPS school code and fiscal year.
- The prototype extracts source URL, fiscal year, reported school year, full DBN when present, total school funding, funding per student, and funding plus central services per student.
- The prototype returns `status: unavailable` when the report does not expose a usable school-year result.
- The prototype writes no files and does not persist or alter source data.

## Source-role decision

- School Budget At a Glance: primary recent school-level funding/spending source.
- One historical source at most: only if its units, population, year, and definitions are compatible.
- Fair Student Funding materials: methodology and allocation definitions.
- Comptroller/IBO material: validation and explanatory context, not replacement records.

## Read-only findings

- `M425` returns full identity `02M425` when queried with `fy=2026`.
- `fy=2026` reports school year `2025-26` and exposes total funding and per-student funding.
- `fy=2025` returns a usable report for school year `2024-25`.
- `fy=2024` did not return a usable report for this school during validation.
- The source exposes recent fiscal years rather than the full 2015–2022 equity-data range.
- The report is an interactive ASP.NET page; a stable public JSON/CSV API has not been confirmed.
- The report can contain different reporting periods for budget and demographic context.

### Coverage matrix

The read-only matrix tested confirmed school codes `M425`, `M292`, and `X269` across FY 2024, FY 2025, and FY 2026:

- 9 reports requested.
- 6 reports matched a reported school year.
- 3 reports were unavailable, all for FY 2024.
- 6 of 6 matched reports mapped to a full DBN.
- 6 of 6 matched reports exposed total funding, funding per student, and funding plus central services per student.
- 0 request errors occurred.

This is evidence that recent-year extraction is feasible for tested schools, not evidence of complete historical coverage.

## Compatibility rules

- Never infer a fiscal-year/school-year mapping from a numeric coincidence.
- Preserve fiscal year and school year as separate fields.
- Do not merge allocation, spending, and per-student measures.
- Do not compare records when the population, enrollment basis, or definitions differ.
- Keep source URL and provenance with every extracted record.
- Show budget context as unavailable or not directly comparable when alignment is unproven.

## Acceptance criteria

- The prototype retrieves a representative school report without modifying production files.
- Extracted fields preserve source labels and reporting periods.
- Available and unavailable fiscal years are distinguishable.
- DBN mapping is demonstrated for a representative school.
- No source is blended into the existing attendance/graduation data.
- `.env` remains ignored and outside all prototype artifacts.

## Exit criteria

- Prototype results are reviewed.
- Source availability and coverage limitations are documented.
- A decision is made whether to continue source discovery, use a controlled snapshot, or stop budget integration.
- Any production implementation receives a separate approved Builder plan.

## Status

Prototype implementation complete on the isolated branch. Production budget integration remains deferred.
