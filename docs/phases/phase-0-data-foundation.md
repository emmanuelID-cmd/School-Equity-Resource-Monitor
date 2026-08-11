# Phase 0 — Data Foundation

## Objective

Create an auditable, high-school-only data foundation for the Portfolio Review and School Equity Profile screens.

## Product question

How is demographic 90%+ attendance associated with demographic four-year graduation rates across NYC high schools?

## Scope

- Source the public NYC education API at `https://data.cityofnewyork.us/resource/dnpx-dfnc.json`.
- Filter to high-school records and retain `dbn`, school name, school year, report year, school type, report type, metric fields, and cohort denominator.
- Include aligned standalone demographic pairs:
  - Female attendance ↔ Female graduation.
  - Male attendance ↔ Male graduation.
  - Black attendance ↔ Black graduation.
  - White attendance ↔ White graduation.
- Include other demographic groups only when coverage is sufficient.
- Derive borough from the first two DBN characters.
- Record data-quality warnings and transparent review-signal inputs.

## Non-goals

- No gender-by-race intersections.
- No causal claims or hidden composite risk score.
- No budget integration until DBN/year and fiscal-year alignment are validated.
- No elementary or middle-school records in this product.
- No UI polish or action-plan persistence until the normalized data contract is stable.

## Audit checklist

- [x] Inventory relevant `metric_display_name` and `metric_variable_name` values.
- [x] Classify metric units: rate, percentage, attendance average, count, or suppressed/missing.
- [x] Normalize demographic labels, including Hispanic/Latinx and Native American variants.
- [x] Distinguish `90%+` from `>90%` attendance measures and document the selected production metric.
- [x] Check school year, DBN, school type, report type, borough, and school coverage.
- [x] Detect missing, suppressed, duplicate, and small-denominator records.
- [x] Match attendance and graduation by `dbn + school_year + demographic`.
- [x] Measure matched coverage by year and demographic.
- [x] Define transparent review signals and insufficient-data states.

## Planned deliverables

1. [x] A reproducible API audit report (`docs/audits/phase-0-api-audit.json`).
2. [x] A normalized record shape for attendance and graduation observations (`src/data/normalize.py`).
3. [x] A school-year coverage table with match and warning fields (`audit_rows`).
4. [x] Documented review-signal inputs with no opaque score.
5. [x] Test fixtures for complete, missing, duplicate, and small-denominator cases.

## Acceptance criteria

- Every production metric has a documented meaning and unit.
- Every joined observation identifies its DBN, school year, demographic, source metric, and denominator.
- High-school filtering is explicit and testable.
- Borough derivation is deterministic and tested.
- Unmatched and low-quality records remain visible as warnings rather than being silently discarded.
- A reviewer can trace each portfolio signal back to the underlying attendance and graduation records.

## Risks and decisions

- The source contains multiple school types and similarly named metrics; filtering and normalization must happen before joins.
- Demographic coverage changes by year; matched coverage must be reported rather than inferred.
- Small denominators can make rates unstable; the threshold and display treatment must be documented before ranking schools.

## Exit criteria

Phase 0 is complete when the audit report, normalized data contract, coverage/warning fields, review-signal rules, and representative tests are reviewed and approved. Only then should Phase 1 implement the Portfolio Review screen.
