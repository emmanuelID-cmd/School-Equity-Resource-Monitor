# Phase 6.6 — Budget-Context Deferral and Handoff

## Objective

Close Phase 6's budget/resource research boundary and define the conditions for any future budget-context implementation without implying that budget integration has been built.

## Scope

- Record the Phase 6 decision that no current source is approved for production integration.
- Preserve the findings from Galaxy, SBER, NYS Transparency Forms, NYSED Financial Transparency Reports, and NYC Open Data review.
- Define readiness requirements for any future budget/resource implementation.
- Document controlled snapshots as a fallback only.
- Define the handoff boundary for a possible Phase 7 UI and integration effort.
- Preserve the observational product boundary.

## Non-goals

- No production UI.
- No production API.
- No Supabase or database changes.
- No snapshot creation.
- No budget metric blending or ranking.
- No Action Plan changes.
- No causal claims about resources, attendance, graduation, or demographics.

## Phase 6 decision

Phase 6 remains research-only. Phase 6.5 found no source that combines official authority, school-level compatibility, stable machine-readable access, comparable historical periods, and sufficiently clear metric definitions. Budget/resource context is therefore deferred from the current product.

Galaxy is not approved for direct integration. SBER, NYS Transparency Forms, and NYSED reports remain source-separated references. Controlled snapshots are a fallback only and are not created by this phase.

## Future implementation readiness requirements

Before a future implementation phase may begin, it must have:

- An explicitly approved source and ownership record.
- A stable API, download, or controlled retrieval contract.
- Validated DBN, BN, or school-code mapping.
- Explicit fiscal-year and school-year relationship.
- Preserved metric definitions and enrollment basis.
- Defined behavior for invalid, missing, unavailable, and suppressed records.
- Documented high-school and population coverage.
- Publication cadence and source-transition handling.
- A separate observational interpretation that does not claim causation.
- A user-approved UI and integration plan.

## Phase 7 handoff boundary

Phase 7 may begin only as a separately approved implementation phase. It may address budget/resource UI and backend integration only after the readiness requirements above are satisfied. Phase 7 must not silently treat Galaxy HTML parsing, a snapshot, a projection, or an estimate as actual spending.

## Acceptance criteria

- Phase 6's research-only boundary is explicit.
- The Phase 6.5 defer-integration decision is preserved.
- Future source and integration readiness requirements are documented.
- Snapshot use is identified as fallback only.
- The Phase 7 handoff boundary is explicit.
- No production application files are changed.
- `.env` remains ignored and outside all artifacts.

## Exit criteria

Phase 6.6 is complete when this deferral boundary and future handoff are Reviewer-approved. Completion does not mean that budget integration exists or that Phase 7 has started.

## Status

Phase 6.6 Builder documentation complete; Reviewer approval is pending.
