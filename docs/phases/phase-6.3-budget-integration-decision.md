# Phase 6.3 — Budget Integration Decision

## Objective

Decide whether budget and resource context is reliable enough for production integration, should continue through source discovery, or should be deferred. A recent-year snapshot is a fallback option only; it is not selected automatically.

## Branch boundary

This decision work is isolated to `phase-6.3-budget-integration-decision`. It does not modify production UI, APIs, Supabase data, or completed Phases 0–5 behavior.

## Current evidence

- School Budget At a Glance provides useful recent school-level funding and spending fields.
- The read-only prototype matched 6 of 9 tested recent-year reports and extracted key fields from all matched reports.
- The source is an interactive ASP.NET report; a stable public JSON/CSV API has not been confirmed.
- Historical School-Based Expenditure Reports describe estimated per-pupil spending.
- NYS School Funding Transparency Forms describe state-defined budget projections.
- These source types are not interchangeable and cannot form one blended historical metric.
- Fiscal-year and school-year alignment remains an explicit compatibility requirement.

## Decision options

### Option A — Continue source discovery

Choose this option if a stable official export, API, or more complete historical dataset can be identified and validated.

Benefits:

- Better repeatability and maintainability.
- Greater potential for historical coverage.
- Less reliance on webpage structure.

Risks:

- Delays budget-context functionality.
- A suitable source may not exist publicly.

### Option B — Use a controlled recent-year snapshot

Choose this only if recent budget context provides sufficient value and the limitations can be made visible.

Required safeguards:

- Label every record with source, fiscal year, school year if provided, capture date, and metric type.
- Limit coverage to verified recent years.
- Preserve allocation, projection, estimate, spending, and per-student measures separately.
- Include an explicit refresh procedure and source validation checklist.
- Display “Budget context unavailable” or “Not directly comparable” when requirements fail.
- Never present the snapshot as a complete historical series.

Benefits:

- Provides constrained recent-year context.
- Can be tested without depending on a live page at runtime.

Risks:

- Requires manual or scheduled maintenance.
- Remains incomplete historically.
- May create false confidence if scope labels are not prominent.

### Option C — Defer budget integration

Choose this if neither the live source nor a snapshot meets the reliability requirements.

Benefits:

- Protects the accuracy of the completed product.
- Avoids misleading cross-year or cross-source comparisons.

Cost:

- The product remains without budget context, while the existing observational workflow remains fully usable.

## Production acceptance requirements

No budget UI or production data integration may begin unless the selected approach provides:

- Reliable DBN or validated school-code mapping.
- Explicit fiscal-year and school-year handling.
- Stable access or a documented snapshot process.
- Field definitions and units.
- Enrollment basis.
- Source provenance and capture/update date.
- Missing, unavailable, suppressed, and non-comparable states.
- Population and school-type boundaries.
- Tests for representative schools and years.

## Decision rule

Select the least risky option that meets all production acceptance requirements. If no option meets them, choose Option C and preserve the current product unchanged.

The decision must not be based on whether a budget number can be displayed. It must be based on whether the number can be displayed accurately, with its meaning and limitations intact.

## Product impact

The existing product remains complete without budget context:

```text
Find an observable pattern → inspect the evidence → decide what to review next.
```

If budget context is eventually approved, it belongs in a source-labeled section of the School Equity Profile. Portfolio Review should remain focused on observable attendance and graduation evidence.

## Non-goals

- No production UI or API integration.
- No snapshot creation.
- No budget ranking or universal budget score.
- No causal claims.
- No Action Plan automation based on budget values.
- No changes to completed phases.

## Acceptance criteria

- All three options are documented with benefits, risks, and safeguards.
- Snapshot use is explicitly treated as a fallback.
- Production acceptance requirements are explicit.
- Fiscal-year/school-year and source-type incompatibility rules are preserved.
- The existing product’s completeness is not dependent on budget integration.
- `.env` remains ignored and outside all artifacts.

## Verdict

Option A is selected: continue source discovery. Do not begin production budget integration or create a snapshot yet. The next step is to identify and validate a stable official source or export against the documented acceptance requirements.

## Status

Phase 6.3 decision complete. Option A approved; source discovery continues in the next scoped step.
