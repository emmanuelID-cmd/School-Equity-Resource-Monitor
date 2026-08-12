# Phase 6.4 — Stable Source Discovery

## Objective

Identify and validate a stable official budget/resource source or repeatable export that could support a future integration without relying on fragile webpage parsing or blending incompatible measures.

## Branch boundary

This investigation is isolated to `phase-6.4-stable-source-discovery`. It does not modify production UI, APIs, Supabase data, or completed Phases 0–5 behavior.

## Source inventory

| Candidate | Machine-readable potential | Coverage | Intended role | Current assessment |
|---|---|---|---|---|
| NYCPS School Budget At a Glance | Interactive ASP.NET report; export/API not confirmed | Recent fiscal years | Recent school funding/spending | Useful fields, but runtime parsing is fragile |
| NYCPS School-Based Expenditure Reports | School, district, and system reports; report files and linked tables | FY 2000–FY 2018 | Historical estimated spending | Strong historical candidate; estimated spending only |
| NYS School Funding Transparency Forms | Year-specific forms and files | FY 2018–FY 2023 | Historical budget projections | Bridge candidate; not equivalent to spending |
| NYCPS Financial Status Reports | Periodic financial reports | Current-year reporting | System/current budget status | Not a direct school-level outcome companion yet |
| NYCPS Galaxy allocation/spending reports | School-level links; access and repeatability vary | Recent/year-specific | Allocation or spending detail | Requires access and format validation |
| NYC Open Data / NYS data portals | Depends on dataset | Dataset-specific | Discovery and validation | Candidate only after DBN/field inspection |
| NYC Comptroller / IBO reports | Reports and analysis | Report-specific | Independent validation | Reference only, not replacement records |

## Evaluation requirements

Each candidate must be checked for:

- School-level records.
- DBN, BN, school code, or a validated identifier mapping.
- Available years and reporting-period labels.
- Metric type: allocation, projection, estimate, spending, or summary.
- Enrollment basis and calculation method.
- Stable download, API, or repeatable export process.
- Source ownership, publication cadence, and update history.
- Missing, suppressed, and unavailable-record behavior.
- High-school population coverage.

## Current evidence

- NYCPS identifies School-Based Expenditure Reports as estimated per-pupil spending reports covering FY 2000–FY 2018.
- NYCPS identifies NYS School Funding Transparency Forms as budget projections covering FY 2018–FY 2023.
- School Budget At a Glance provides useful recent school-level funding and spending fields, but its public interface remains an interactive ASP.NET report.
- The Phase 6.1 prototype matched 6 of 9 tested School Budget At a Glance reports across three schools and three fiscal years.
- The tested source did not provide complete coverage for FY 2024 and does not cover the current equity dataset’s full 2015–2022 range.

## Candidate-level validation results

### School-Based Expenditure Reports

- The FY 2018 landing page is a repeatable official report endpoint.
- It identifies School Year 2017–2018 and supports school-level lookup using a BN such as `M015`.
- It exposes school, district, and system views with per-student amounts, salary, fringe, salary-plus-fringe, and OTPS fields.
- The report states that FY 2018 ran July 1, 2017 through June 30, 2018.
- Enrollment is based on audited registers as of October 31, 2017, with a specialized-education refinement as of December 31, 2017.
- It describes the values as estimated expenditures, not final individual-student spending.

Source: https://www.nycenet.edu/offices/d_chanc_oper/budget/dbor/sber/FY2018/FY2018_Default.aspx

### NYS School Funding Transparency Forms

- NYCPS publishes official FY 2018–FY 2023 form links, including downloadable ZIP files.
- The source page identifies these as DOE budget projections using state-defined reporting categories.
- The files are suitable for further format inspection, but not for direct comparison with SBER estimated expenditures without field-level reconciliation.

Source: https://infohub.nyced.org/reports/financial/financial-data-and-reports/new-york-state-school-funding-transparency-forms

### NYSED Financial Transparency Reports

- NYSED publishes school-level Financial Transparency Reports with per-pupil expenditures and category detail, including instruction, administration, support services, and total expenditures.
- The report distinguishes school-level amounts from district averages and documents exclusions such as tuition and debt service.
- Per-pupil calculations use reported enrollment and the state-defined reporting methodology; the published glossary warns that enrollment methodology changes can affect comparisons between years.
- This is a stronger recent comparison candidate than a generic citywide budget dataset, but it remains a separate state-defined expenditure measure and is not interchangeable with SBER, Transparency Forms, or Galaxy values.

Source example: https://data.nysed.gov/expenditures.php?instid=800000092316&year=2024

### Galaxy reports

- The official financial reports page links to public Galaxy Allocation and Galaxy Budget Summary endpoints.
- The Galaxy Budget Summary page identifies fiscal-year selection and four-digit school-code lookup and advertises coverage from FY 2006 through FY 2026.
- Both linked endpoint families are publicly reachable over HTTPS. The Budget Summary query behavior is confirmed below; machine-readable export behavior is not exposed.
- The Budget Summary form uses an ASP.NET POST with hidden view-state fields, a four-character `School_Code`, and a `Fiscal_Year` selector from 2006 through 2026. This confirms a repeatable human-facing query shape, but not a stable API or export contract.
- A controlled query using `M292` and FY 2026 returned Orchard Collegiate Academy with school-level leadership, staffing, position, and budget fields. A repeat query for FY 2025 returned the same school with a year-specific Galaxy data-source date.
- The accepted code format is `BSSS` (borough letter plus three digits); numeric-only `0292` was rejected by the form. The returned record links the code to DBN `01M292`.
- Retrieval is repeatable through a fresh GET followed by an ASP.NET POST carrying view-state fields, but the response is HTML and no CSV, XLSX, JSON, download, or export endpoint was exposed.
- The linked `budget_summary_glossary.pdf` is a valid official PDF response and should be retained as the field-definition reference.
- An invalid but correctly formatted code such as `M999` returns a no-record response; a numeric-only code such as `0000` is rejected by input validation. This distinguishes invalid format from unavailable school records.
- High-school coverage was confirmed for `M475` (Stuyvesant High School), `X445` (Bronx High School of Science), and `Q485` (Grover Cleveland High School) for FY2026.
- Galaxy therefore qualifies as a repeatable human-facing school-level source, not yet as a stable machine-readable integration source. Its full glossary mapping and broader missing-record coverage still require validation.

Sources:

- https://apps.schools.nyc/dsbpo/galaxybudgetsummaryto/default.aspx
- https://apps.schools.nyc/dsbpo/galaxyallocation/default.aspx

### NYC Open Data and other portal candidates

- The reviewed NYC Open Data results include citywide expense-budget, capital-project, and state-aid/construction datasets.
- No reviewed result was validated as a school-level operating allocation or expenditure dataset with a DBN-compatible identifier and documented per-school metric.
- These portals remain discovery sources, not approved budget records for this product.

### Validation conclusion

The candidate-level test confirms that historical files and school-level reports exist, but the source families measure different things. SBER is the stronger historical spending-context candidate; Transparency Forms are a separate projection-context candidate; NYSED reports provide a separate state-defined expenditure view. Neither should be used to create a blended historical per-student series.

Galaxy is confirmed as a repeatable human-facing school-level source, but its ASP.NET HTML response is not a stable machine-readable integration contract. Direct production integration is therefore deferred.

## Compatibility matrix

| Requirement | Minimum standard | Result so far |
|---|---|---|
| Identifier | DBN or reproducible school-code mapping | Partial; M425/M292/X269 mapped in prototype |
| Reporting period | Explicit fiscal or school year | Present, but must remain separate |
| Metric definition | Allocation, projection, estimate, spending, or summary labeled | Present across sources; not interchangeable |
| Enrollment basis | Published and retained | Present in some reports; must be captured per source |
| Historical coverage | Documented year range | Varies significantly by source |
| Repeatability | Stable file/API/export or controlled snapshot process | Not yet proven for all candidates |
| Population boundary | High-school coverage identified | Requires candidate-level validation |
| Provenance | Source URL, publication/capture date | Must be retained in any future adapter |

## Candidate scorecard

| Candidate | School-level evidence | Metric clarity | Period/coverage | Repeatable access | Current disposition |
|---|---|---|---|---|---|
| SBER | Confirmed by BN | Clear estimated expenditure fields | FY 2000–2018 | Official report endpoint; extraction still needs hardening | Historical candidate |
| NYS Transparency Forms | Confirmed through official files | Clear projection categories | FY 2018–2023 | Downloadable official files | Separate projection candidate |
| NYSED Financial Transparency Reports | Confirmed school-level report | Clear state-defined per-pupil expenditure and exclusions | Recent annual reports | Stable public report URLs; bulk/export path not yet confirmed | Recent comparison candidate |
| Galaxy | Confirmed: `M292` → DBN `01M292`; high schools `M475`, `X445`, `Q485` tested | School-level position/budget fields returned; official glossary PDF available | FY 2006–2026 advertised; FY2025 and FY2026 tested | Repeatable GET + POST, HTML only; no export/API found | Continue validation |
| NYC Open Data reviewed results | Not confirmed for operating school-level budget | Not applicable | Dataset-specific | Portal export available, but no matching dataset validated | Discovery only |

## Decision rules

- Do not choose a source because it merely contains a number for a school.
- Do not merge sources by year alone.
- Do not convert projections or estimates into actual spending.
- Do not use a district or citywide value as a school value.
- Do not infer school-year alignment from fiscal-year numbering.
- Do not allow an unavailable historical record to silently fall back to another source.
- Keep source transitions visible to the user.

## Planner disposition

- Primary recommendation: continue discovery for an official stable download or API that can be validated at school level.
- Galaxy disposition: do not integrate directly into production; retain as documented source evidence only.
- Snapshot disposition: controlled snapshot is a fallback option if budget context becomes necessary before a stable source is identified. It is not approved for implementation in Phase 6.4.
- Product boundary: budget/resource context remains outside the current production UI, API, and Action Plan workflow.

## Recommended investigation sequence

1. Inspect the linked SBER and transparency-form files for their actual formats and school-level identifiers.
2. Test one overlapping period where both source families are available.
3. Record field definitions, enrollment basis, and metric type side by side.
4. Inspect Galaxy and NYC Open Data candidates for public, repeatable access.
5. Score each candidate against the evaluation requirements.
6. Recommend one of:
   - Ready for a future implementation plan.
   - Snapshot fallback only.
   - Continue discovery.
   - Defer budget integration.

## Non-goals

- No production data ingestion.
- No budget UI.
- No snapshot creation.
- No blended budget metric.
- No funding ranking.
- No causal claims.
- No Action Plan automation based on budget values.

## Acceptance criteria

- Candidate sources and roles are documented.
- At least one historical source is checked at the file/endpoint level.
- DBN or school-code mapping is tested where available.
- Reporting periods, metric definitions, and enrollment bases are preserved.
- Repeatability and ownership are assessed.
- A source recommendation is supported by evidence.
- The primary disposition and snapshot fallback are explicitly documented.
- No production application files are changed.
- `.env` remains ignored and outside all artifacts.

## Risks

- A report may be readable by people but not reliably extractable by software.
- Historical source files may be estimates or projections rather than final spending.
- Identifier formats may differ across source families.
- Apparent overlap may hide different enrollment or population definitions.
- A source transition may look like a change in school resources.

## Verdict

Phase 6.4 is complete as a source-validation and disposition phase. Galaxy is not approved for production integration; a controlled snapshot remains a documented fallback only.

## Status

Complete — investigation and disposition are closed. Continued discovery of a stable machine-readable source, if pursued, belongs in Phase 6.5. Production budget integration remains deferred.
