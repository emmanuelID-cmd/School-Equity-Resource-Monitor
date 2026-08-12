# School Equity Resource Monitor

## Product direction

**Working product name:** School Equity Resource Monitor

**Primary user:** NYC Superintendent or DOE district/portfolio agent.

**Core decision:**

> Which high schools show persistent demographic attendance and graduation concerns, what resources do they have, and what should the district review next?

This is an observational operational review tool—not just a demographic visualization. It helps users identify patterns, document review questions, assign follow-up work, and record what should be examined next. It does not establish causation.

## Current data foundation

Primary API:

`https://data.cityofnewyork.us/resource/dnpx-dfnc.json`

Current supported comparisons:

- Standalone gender metrics: Female, Male, Neither Female nor Male.
- Standalone race metrics: White, Black, Asian, Hispanic, Multiracial, Native American, Native Hawaiian or Pacific Islander.
- No gender-by-race intersection metrics such as Female–White.
- Four-year graduation rate.
- Attendance:
  - Overall average attendance.
  - In-person and remote attendance.
  - Percentage of students with 90%+ attendance overall.
  - 90%+ attendance by race and by Female/Male.
- `number_of_students` is the demographic denominator, not total enrollment.
- Borough must be derived from DBN.
- All findings are observational; do not claim causation.

## Product thesis

The primary relationship should be:

> How is demographic 90%+ attendance associated with demographic four-year graduation rates across NYC high schools?

Overall attendance is secondary context. The aligned comparison should be:

- Female attendance ↔ Female graduation.
- Male attendance ↔ Male graduation.
- Black attendance ↔ Black graduation.
- White attendance ↔ White graduation.
- Other groups only where coverage is sufficient.

## Proposed product screens

### 1. Portfolio review

- Priority review queue.
- Borough/district/year filters.
- Persistent gap and attendance signals.
- Improving schools and insufficient-data states.

### 2. School equity profile

- Demographic graduation rates and gaps.
- Demographic 90%+ attendance rates and gaps.
- Attendance-versus-graduation relationship.
- Cohort size, matched records, borough, and data-quality warnings.

### 3. Resource context

- Live, partial NYCPS Galaxy budget context.
- School search by DBN, school code, or school name.
- Fiscal-year selection and source metadata.
- Partial-data, unavailable-data, validation, and source-warning states.
- Budget data is context, not a causal score or complete financial record.

### 4. Action plan

- Authenticated, server-backed action plans.
- Recommended review area and concrete action options.
- Owner team, status, notes, and follow-up date.
- Saved-plan viewing and editing.
- Action Plans document observational follow-up; they do not automate causal recommendations.

## Budget / Resources implementation

Potential official sources:

- NYCPS Financial Data and Reports.
- NYCPS School Budget At A Glance.
- Fair Student Funding allocations and proposals.

The current Budget / Resources page uses a controlled server-side adapter for the public NYCPS Galaxy source. It is implemented as live, clearly labeled partial context. Fiscal year remains distinct from school year, and records are not substituted with unrelated district, citywide, projected, estimated, or actual-spending values.

Use budget to ask:

- Are resources aligned with student needs?
- Does the school have support capacity related to attendance, counseling, tutoring, or intervention?
- Which similar schools have different resource levels?
- Did outcomes change after a resource or support review?

The source remains an HTML-form source rather than a stable machine-readable API. Returned records may be partial, unavailable, or require adapter maintenance if the source changes. Do not say spending causes attendance or graduation outcomes.

## Completed implementation phases

Phases 0–9 are complete for the approved product scope:

- Phase 0 — Data foundation and API audit.
- Phase 1 — Portfolio Review and review filters.
- Phase 2 — School Equity Profiles and deep-link navigation.
- Phase 3 — Equity comparison chart with attendance and graduation endpoints.
- Phase 4 — Product framing, shared header, navigation, and responsive behavior.
- Phase 5 — Authenticated, server-backed Action Plans.
- Phase 6 and sub-phases 6.1–6.6 — Budget-source validation, discovery, deferral boundaries, and implementation readiness.
- Phase 7 — Budget/resource context implementation readiness.
- Phase 8 — Live partial budget-context planning and handoff.
- Phase 9 — Budget / Resources implementation using partial Galaxy context.

The detailed records are in [`docs/phases/`](docs/phases/).

## Future ideation boundary

Additional datasets, workflow enhancements, ticketing, escalation, richer budget sources, and comparative resource analysis remain optional future work. They are recorded in [`docs/phases/phase-X-future-ideation.md`](docs/phases/phase-X-future-ideation.md) and are not required for the current product to function.

## Before coding

First complete a **data coverage audit**:

- Inventory `metric_display_name`.
- Classify each `metric_value` by unit and meaning.
- Check year, DBN, borough, and school coverage.
- Check missing, suppressed, duplicate, and small-denominator records.
- Match attendance and graduation by `dbn + school_year`.
- Audit any future budget source availability and fiscal-year alignment.
- Define transparent review signals; avoid a hidden risk score.

## Security

- Public token-free API access is currently acceptable.
- Add `.gitignore` entries for `.env` and `.env.*`.
- Do not create a real `.env` unless a source requires credentials.
- Use `.env.example` with variable names only.
- Use hosting-managed secrets for production.
- Never commit API tokens.

## Current implementation status

The current product is implemented and deployable. It includes the Portfolio Review, Schools Directory and Equity Profiles, comparison chart, authenticated Action Plans, and separate Budget / Resources context. The provided mockup archive remains available at [`school-equity-resource-monitor-mockup.zip`](school-equity-resource-monitor-mockup.zip) as a visual design reference.
