# Phase 6 — Budget and Resource Context

## Objective

Evaluate and prepare a second, official NYCPS dataset that can provide budget and resource context alongside the existing observational attendance and graduation evidence. This phase defines the data contract and integration boundary; it does not yet build a budget interface.

## Scope

- Evaluate NYCPS School Budget At a Glance as the primary source candidate.
- Evaluate Fair Student Funding and related school financial reports as supporting sources.
- Confirm source access method, publication cadence, coverage, definitions, and attribution requirements.
- Match records using DBN and an explicitly documented year relationship.
- Resolve fiscal-year versus school-year alignment before any combined display.
- Define safe budget/resource fields and their units.
- Define missing, suppressed, stale, incomparable, and unmatched-record warnings.
- Recommend placement in the School Equity Profile, with Portfolio Review remaining focused on observable review signals.
- Preserve observational, non-causal language throughout the product.

## Non-goals

- No budget UI or API integration in this planning phase.
- No changes to Portfolio Review, Schools, charts, or Action Plans.
- No causal claims about spending, staffing, resources, attendance, or graduation.
- No ranking schools by funding or labeling funding as adequate or inadequate.
- No recommendations about how a school should spend money.
- No additional authentication, permissions, ticketing, email, or workflow changes.
- No elementary or middle-school population expansion.

## Inputs

- Existing high-school school-equity records keyed by DBN and school year.
- NYCPS Funding Our Schools and School Budget At a Glance materials:
  https://www.schools.nyc.gov/about-us/funding/funding-our-schools
- NYCPS school-level financial reports and budget references:
  https://www.schools.nyc.gov/schools/M425
- NYCPS Fair Student Funding methodology and allocation context.
- NYC Comptroller school-budget allocation reports for independent comparison:
  https://comptroller.nyc.gov/reports/spotlight-school-budget-allocations/
- NYC Independent Budget Office Fair Student Funding methodology context:
  https://www.ibo.nyc.gov/content/budget-glossary

## Source assessment

### Primary candidate — NYCPS School Budget At a Glance

NYCPS describes School Budget At a Glance as a school-level report showing total funding per student compared with the citywide average, along with funding, spending, and demographic context. It is the preferred primary candidate because it is an official NYCPS source designed for school-level budget interpretation.

Before implementation, the Builder must confirm whether the report exposes a stable downloadable file, API, or repeatable export with DBN, reporting year, and field definitions. A human-facing webpage alone is not sufficient for an automated integration.

### Supporting candidate — Fair Student Funding

Fair Student Funding is useful for explaining allocation categories and methodology. It may be a supporting dataset rather than a complete replacement for School Budget At a Glance because allocation snapshots, projected enrollment, audited enrollment, and final spending can represent different moments in the budget cycle.

### Validation sources

NYC Comptroller and NYC Independent Budget Office materials may validate definitions, categories, and historical interpretation. They should not silently replace NYCPS records without a documented source decision because they may publish analysis or snapshots rather than the operational school-level source.

## Proposed data contract

The implementation plan must confirm the exact field names and definitions, but the initial candidate fields are:

- `dbn`
- `fiscal_year`
- `school_name`
- `school_type`
- `total_funding`
- `funding_per_student`
- `citywide_funding_per_student`
- `fair_student_funding`
- `other_or_restricted_funding`
- `enrollment_basis`
- `source_url`
- `published_at`
- `data_quality_status`

Fields must retain source units, currency year, projected versus audited enrollment basis, and whether a value represents allocation, budget, or spending. Do not combine these concepts into one generic “budget” number.

## Year alignment rule

The current product uses school years such as `2020`; budget sources commonly use fiscal years such as `FY 2020` or `FY 2021`. No automatic one-year offset may be assumed.

The Builder must document and test one explicit mapping rule, such as:

```text
school_year 2020–21 → fiscal_year FY 2021
```

If the existing product’s year labels represent a different convention, the mapping must be revised before integration. When alignment cannot be proven, the UI must show budget context as unavailable rather than presenting a misleading comparison.

## DBN and coverage checks

- Confirm DBN format and normalization against the existing high-school records.
- Measure exact DBN match rate by reporting year.
- Identify schools with renamed, merged, closed, or missing records.
- Confirm whether charter, District 75/79/84, alternative, or other populations use different funding rules.
- Keep the current high-school boundary unless a separate population plan is approved.
- Preserve source-specific school names for auditability; do not use names as the primary join key.

## Warning and display rules

Show a clear warning when:

- No budget record matches the DBN and aligned year.
- The source year cannot be aligned to the selected school year.
- The record is an allocation rather than final spending.
- Enrollment is projected, preliminary, or audited and affects per-student calculations.
- A field is suppressed, incomplete, or defined differently across years.
- The source covers a different school population or funding formula.

Use wording such as “Budget context unavailable for this school year” or “Allocation context only; this is not final spending.” Do not use “underfunded,” “overfunded,” “cause,” or equivalent causal or evaluative labels without a separately approved standard.

## Product placement recommendation

Place budget/resource context in the School Equity Profile after the existing observational evidence, warnings, and chart. The profile is the appropriate location because it gives users context after they inspect the pattern. Keep Portfolio Review focused on finding and prioritizing observable evidence.

The first implementation should be a clearly labeled, collapsible “Budget and resource context” section with source, year, definitions, and warnings. This placement remains subject to final Builder implementation planning and Reviewer approval.

## Deliverables

- Confirmed primary source and access method.
- Field-level data dictionary with units and definitions.
- DBN coverage report.
- Fiscal-year/school-year mapping decision.
- Normalized source adapter or import contract, only after the preceding items are approved.
- Warning and provenance rules.
- Builder-ready implementation plan for the School Equity Profile.
- Updated tests for matching, alignment, missing data, and source boundaries.

## Acceptance criteria

- One official primary source is selected and its access method is reproducible.
- The source provides or can be reliably matched to DBN and reporting year.
- Fiscal-year versus school-year alignment is explicitly documented and tested.
- Funding, allocation, spending, enrollment basis, and per-student fields are not conflated.
- Coverage and unmatched records are measured.
- Missing, suppressed, stale, and incomparable data have explicit user-facing warnings.
- Product placement is limited to the approved School Equity Profile context area.
- Observational and non-causal language is preserved.
- No implementation begins until the data contract and source decision are reviewed and approved.

## Risks

- Official reports may be human-facing and lack a stable machine-readable interface.
- Fiscal-year and school-year labels may appear comparable while representing different periods.
- Budget allocations and final spending are materially different measures.
- Per-student values depend on enrollment definitions and timing.
- Historical coverage may not match the current equity dataset.
- Different school populations may use different funding formulas.
- Budget context can be misread as an explanation or causal factor; provenance and warnings must remain visible.

## Exit criteria

- Source assessment and data dictionary are complete.
- DBN coverage and year alignment are documented with evidence.
- Primary source and product placement are approved.
- Warning and observational framing rules are approved.
- A separate Builder implementation plan exists if integration is authorized.
- Read-only REVIEWER approves the Phase 6 planning deliverable.

## Status

Phase 6 planning deliverable complete. Data integration and UI implementation are not authorized until the source, alignment rule, and data contract receive separate approval.
