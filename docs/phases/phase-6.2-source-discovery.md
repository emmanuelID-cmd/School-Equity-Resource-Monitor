# Phase 6.2 — Historical Budget Source Discovery

## Objective

Determine whether an additional official NYCPS or public-sector dataset can extend budget context beyond the recent School Budget At a Glance coverage without blending incompatible measures.

## Branch boundary

This investigation is isolated to `phase-6.2-source-discovery`. It does not modify production UI, APIs, Supabase data, or the completed Phases 0–5 behavior.

## Sources evaluated

| Source | Intended role | Coverage indicated by source | Initial decision |
|---|---|---|---|
| NYCPS School Budget At a Glance | Recent school-level funding/spending | Recent fiscal years, including FY 2025–FY 2026 | Retain as primary recent source |
| NYCPS School-Based Expenditure Reports | Historical per-pupil spending estimates | School years 2000–2018 | Candidate historical source; definitions require reconciliation |
| NYS School Funding Transparency Forms | State-defined budget projections | School years 2018–2023 | Candidate bridge source; not automatically equivalent to spending |
| NYCPS Fair Student Funding materials | Formula and allocation methodology | Year-specific proposals and explanations | Reference only, not a replacement data series |
| NYC Comptroller / IBO reports | Independent validation and interpretation | Report-specific snapshots | Validation/reference only |

NYCPS lists School-Based Expenditure Reports as estimates of per-pupil spending for each fiscal year and lists New York State School Funding Transparency Forms separately for school years 2018–2023. These are distinct source types and must not be combined without field-level validation:

https://infohub.nyced.org/reports-and-policies/financial-reports/financial-data-and-reports

## Findings

### Finding 1 — Coverage can be extended, but not with one seamless metric

The source inventory suggests possible coverage from historical spending reports, transparency forms, and recent budget-at-a-glance reports. However, the sources describe different concepts: estimated per-pupil spending, state-defined budget projections, and current school funding/spending summaries.

### Finding 2 — A source transition is safer than a blended series

The product could show source-specific context by period, but it should not present a single uninterrupted “funding per student” trend unless the definitions, enrollment basis, population, and reporting period are proven equivalent.

### Finding 3 — The 2018–2023 overlap requires special review

The historical expenditure source and state transparency forms overlap around 2018, while School Budget At a Glance begins with more recent years. This overlap is useful for comparison testing but does not prove interchangeability.

### Finding 4 — Methodology must remain visible

Fair Student Funding explains allocation rules and weights. It should support interpretation of source fields, not be converted into an outcome or resource score.

## Proposed source-separated model

```text
Budget context
├── Recent school funding/spending
│   └── School Budget At a Glance
├── Historical estimated spending
│   └── School-Based Expenditure Reports
├── Historical budget projections
│   └── NYS School Funding Transparency Forms
└── Definitions and validation
    ├── Fair Student Funding materials
    └── Comptroller / IBO reports
```

Every displayed record must retain:

- Source name
- Source URL
- DBN or source school identifier
- Fiscal year or school year exactly as published
- Metric type: allocation, projection, estimate, spending, or summary
- Enrollment basis
- Publication or snapshot date
- Compatibility status

## Compatibility rules

- Do not infer that fiscal year and school year are equivalent.
- Do not join records solely because their numeric year labels overlap.
- Do not merge allocation, projection, estimate, and actual spending fields.
- Do not compare per-pupil values when enrollment bases differ.
- Do not use a source to fill a missing year without labeling the source transition.
- Show “Not directly comparable” when definitions or periods cannot be reconciled.
- Preserve the existing high-school boundary unless a separate population plan is approved.

## Recommended next test

Obtain representative records from the historical expenditure reports and transparency forms for overlapping years, then compare:

- DBN coverage
- School population
- Year label and reporting period
- Enrollment definition
- Per-pupil calculation
- Allocation versus spending classification
- Suppression and missing-value rules

The comparison should produce a field-level compatibility matrix, not a merged dataset.

## Field-level compatibility result

The official NYCPS source pages confirm the following distinctions:

| Field or concept | School-Based Expenditure Reports | NYS School Funding Transparency Forms | Compatibility |
|---|---|---|---|
| Reporting period | Fiscal-year report; FY 2018 ran July 1, 2017 through June 30, 2018 | FY 2018–FY 2023 forms | Period labels require explicit preservation |
| Primary measure | Estimated per-pupil spending based on DOE expenditures | Budget projections using state-defined categories | Not interchangeable |
| School identifier | Individual school search uses BN, such as `M015` | Form-specific reporting structure | DBN/BN mapping requires validation |
| Enrollment basis | Audited registers and specialized-education enrollment refinements | Source-defined projection or reporting basis | Do not compare without enrollment metadata |
| Coverage level | School, district, and system-wide views | State-defined school funding categories | Different aggregation and category boundaries |
| Use in product | Historical spending context | Historical projection context | Separate labeled panels or records |

The SBER documentation explicitly describes estimates based on total DOE expenditures and enrollment, while the transparency-form page identifies FY 2018–FY 2023 forms as projections under state-defined categories. These differences prevent a single blended historical per-student series.

Sources:

- https://infohub.nyced.org/reports/financial/financial-data-and-reports/school-based-expenditure-reports
- https://infohub.nyced.org/reports/financial/financial-data-and-reports/new-york-state-school-funding-transparency-forms

## Non-goals

- No production data ingestion.
- No budget UI.
- No school funding rankings.
- No blended budget metric.
- No causal analysis.
- No Action Plan recommendations based on budget values.

## Acceptance criteria

- At least one historical candidate is documented with its official source and coverage.
- Source roles are explicit and non-overlapping.
- The 2018–2023 overlap is tested for comparability before any bridge is proposed.
- Metric definitions and enrollment bases are preserved.
- Non-comparable records receive an explicit status.
- No production application files are changed.
- `.env` remains ignored and outside all artifacts.

## Risks

- Historical reports may use estimates rather than final spending.
- Transparency forms may represent projections rather than expenditures.
- School identifiers and populations may change over time.
- Overlapping years may still use different definitions.
- A source transition may be mistaken for a real change in school resources.

## Verdict

Phase 6.2 source discovery is complete. The evidence supports a source-separated model, not a blended historical budget series. A controlled recent-year snapshot remains a fallback if historical sources cannot be reconciled.

## Status

Source-discovery findings and field-level compatibility results documented. Production integration remains deferred pending a separate approved implementation plan.
