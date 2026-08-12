# Phase 6.5 — Stable Budget-Source Discovery

## Objective

Determine whether an official school-level budget or resource source is stable enough to support a future product integration while preserving source definitions and observational boundaries.

## Scope

- Reassess Galaxy, SBER, NYS Transparency Forms, NYSED Financial Transparency Reports, and relevant NYC/NYS portal candidates.
- Test public API, download, export, and repeatable retrieval behavior.
- Validate DBN, BN, or school-code mapping.
- Validate fiscal-year coverage and its relationship to the product's school-year data.
- Check high-school coverage, missing records, suppressed records, and source transitions.
- Preserve each source's metric definition, enrollment basis, ownership, and publication cadence.
- Score sources for authority, stability, school-level detail, historical coverage, repeatability, and integration risk.

## Non-goals

- No production UI or API changes.
- No Supabase or database changes.
- No snapshot creation.
- No budget metric blending or ranking.
- No Action Plan automation based on budget values.
- No causal claims about spending, attendance, graduation, or demographic outcomes.

## Inputs

- Phase 6.1 School Budget At a Glance validation.
- Phase 6.2 source comparison.
- Phase 6.3 source-integration decision.
- Phase 6.4 Galaxy validation and disposition.
- Official NYCPS, NYSED, NYC Open Data, Comptroller, and IBO source pages and files.

## Deliverables

- Candidate-by-candidate source validation record.
- API/export and repeatability findings.
- Identifier, period, metric, enrollment, and population compatibility matrix.
- Source scorecard with evidence and unresolved risks.
- Final recommendation choosing one of:
  - Ready for a future implementation plan.
  - Controlled snapshot fallback.
  - Continue discovery.
  - Defer budget integration.

## Validation findings

### NYCPS Galaxy

- Owner: NYCPS Division of Finance / Department of Education financial reporting.
- Official NYCPS identifies Galaxy Allocation Details and Galaxy Budget Spending Details as school-based financial reports.
- The public Galaxy Budget Summary accepts a `BSSS` school code and fiscal year through an ASP.NET GET/POST flow with view-state fields.
- Repeated school-level tests returned budget and position records for `M292`/DBN `01M292` in FY2025 and FY2026, and high-school records for `M475`, `X445`, and `Q485` in FY2026.
- Invalid formatted code `M999` returned no record; numeric-only `0000` was rejected by input validation.
- The tested Galaxy page distinguishes invalid format from no-record responses, but it does not expose a separate suppressed-record status; suppression behavior remains unresolved and must not be interpreted as zero.
- No stable JSON, CSV, XLSX, or documented API export was exposed. The response is HTML and requires browser-form state.
- NYCPS documentation states Galaxy captures budgeted inputs and does not represent definitive actual spending.

Sources:

- https://infohub.nyced.org/reports/financial/financial-data-and-reports
- https://apps.schools.nyc/dsbpo/galaxybudgetsummaryto/default.aspx
- https://apps.schools.nyc/dsbpo/galaxybudgetsummaryto/budget_summary_glossary.pdf

### SBER and NYS Transparency Forms

- Owner: NYCPS financial reporting, with NYS-defined categories for the Transparency Forms.
- NYCPS describes SBER as estimated per-pupil spending for school years 2000–2018, with audited-register and specialized-education enrollment rules.
- NYCPS describes NYS Transparency Forms as DOE budget projections for school years 2018–2023 under state-defined categories.
- Both are official and school-level where applicable, but their measures are not interchangeable and do not provide one consistent historical spending series.

Sources:

- https://infohub.nyced.org/reports/financial/financial-data-and-reports/school-based-expenditure-reports
- https://infohub.nyced.org/reports/financial/financial-data-and-reports/new-york-state-school-funding-transparency-forms

### NYSED Financial Transparency Reports

- Owner: New York State Education Department.
- NYSED provides school-level per-pupil expenditure reports with category detail and explicit exclusions.
- The reports use state-defined enrollment and expenditure rules, and the glossary warns that methodology changes can affect year-to-year comparisons.
- Public report pages are repeatable for individual institutions, but a stable bulk API/export path and direct DBN mapping were not confirmed in this phase.

Source example: https://data.nysed.gov/expenditures.php?instid=800000092316&year=2024

### NYC Open Data and related portals

- Owner: NYC Open Data and the publishing NYC agencies; SAMs are owned and published by NYCPS.
- Reviewed NYC Open Data results provided education reference datasets such as school zones and citywide budget/capital data, but no validated school-level operating allocation or expenditure dataset with a DBN-compatible metric.
- NYCPS School Allocation Memoranda explain allocation purpose, source, amount, and intended use, but are document-oriented rather than a stable normalized school-level API.

Sources:

- https://data.cityofnewyork.us/
- https://infohub.nyced.org/reports/financial/financial-data-and-reports/school-allocation-memorandums

## Compatibility matrix

| Candidate | Identifier | Period and metric | Access result | Population result | Disposition |
|---|---|---|---|---|---|
| Galaxy | `BSSS` maps to DBN in tested records | Fiscal-year budgeted positions/amounts; not actual spending | Repeatable HTML POST; no stable API/export | High schools tested; broad coverage unresolved | Do not integrate directly |
| SBER | BN/school report mapping available | FY2000–2018 estimated per-pupil spending | Official report pages/files; extraction hardening required | School-level coverage documented; current coverage ends FY2018 | Historical reference only |
| NYS Transparency Forms | School-level forms/files | FY2018–2023 projected budget categories | Official downloadable files | Coverage and mapping require per-file inspection | Separate projection reference |
| NYSED Reports | Institution identifiers; DBN mapping unresolved | Recent state-defined per-pupil expenditures | Repeatable public pages; bulk path unresolved | School-level reports available; NYC coverage needs systematic test | Comparison reference only |
| NYC Open Data/SAM | Dataset/document-specific identifiers | Citywide, capital, allocation, or document measures | Exports/documents available, but no matching normalized school metric | No validated operating-budget school record | Discovery/reference only |

Fiscal-year records must not be joined to the product's school-year outcomes by year number alone. Each source's fiscal period, publication date, enrollment basis, and metric definition must be retained before any future comparison is considered.

## Source scorecard

| Candidate | Authority | Stability | School detail | Historical fit | Integration risk | Score outcome |
|---|---:|---:|---:|---:|---:|---|
| Galaxy | High | Low | High | Medium | High | Not ready |
| SBER | High | Medium | High | High historically | Medium | Reference only |
| NYS Transparency Forms | High | Medium | Medium | Medium | Medium | Reference only |
| NYSED Reports | High | Medium | High | Medium | Medium | Reference only |
| NYC Open Data/SAM | High | Medium | Low for target metric | Variable | High | Not a validated candidate |

## Recommendation

Defer budget/resource integration. No tested candidate currently provides the required combination of official authority, school-level compatibility, stable machine-readable access, comparable historical periods, and sufficiently clear metric definitions.

Controlled snapshots remain a future fallback only if budget context becomes a separately approved product need. No snapshot is created in Phase 6.5. Further source discovery may resume as a new phase or sub-phase with new acceptance criteria.

## Acceptance criteria

- Every selected candidate has an official source URL and ownership recorded.
- At least one school-level record is tested where the candidate claims school-level coverage.
- Retrieval is repeated for multiple schools and reporting periods where possible.
- API, export, or browser-state requirements are explicitly documented.
- DBN/BN/school-code mapping is tested and retained.
- Fiscal-year and school-year compatibility is documented without assuming equivalence.
- Missing, invalid, suppressed, and unavailable-record behavior is documented.
- High-school coverage is tested or explicitly marked unresolved.
- Metric definitions and enrollment bases are preserved separately.
- The recommendation is evidence-based and does not authorize production integration.
- No production application files are changed.
- `.env` remains ignored and outside all artifacts.

## Risks

- A human-facing report may require fragile HTML parsing or session state.
- A downloadable file may change format or publication cadence.
- Sources may use different definitions for allocation, projection, estimate, and expenditure.
- Fiscal-year data may not align with school-year outcome data.
- School-code mappings may change or fail for closed, merged, or reorganized schools.
- Missing records may represent non-public data, no allocation, suppression, or source failure.

## Exit criteria

Phase 6.5 may close after the candidates are scored, unresolved limitations are documented, and the defer-integration recommendation is approved by REVIEWER. The phase must not imply that budget integration is complete.

## Status

Phase 6.5 Builder validation complete; Reviewer disposition approval is pending. Production budget integration remains deferred.
