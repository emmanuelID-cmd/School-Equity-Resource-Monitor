# School Equity Resource Monitor

## Product direction

**Working product name:** School Equity Resource Monitor

**Primary user:** NYC Superintendent or DOE district/portfolio agent.

**Core decision:**

> Which high schools show persistent demographic attendance and graduation concerns, what resources do they have, and what should the district review next?

This must be an operational review tool—not just a demographic visualization.

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

- Funding per student.
- Fair Student Funding.
- Budget allocation categories.
- Enrollment and school composition.
- Budget data is context, not a causal score.

### 4. Action plan

- Concern identified.
- Recommended review area.
- Responsible team.
- Due date.
- Follow-up metric and review status.

## Budget data direction

Potential official sources:

- NYCPS Financial Data and Reports.
- NYCPS School Budget At A Glance.
- Fair Student Funding allocations and proposals.

Budget data has not yet been integrated or validated against DBN/year.

Use budget to ask:

- Are resources aligned with student needs?
- Does the school have support capacity related to attendance, counseling, tutoring, or intervention?
- Which similar schools have different resource levels?
- Did outcomes change after a resource or support review?

Do not say spending causes graduation outcomes.

## Before coding

First complete a **data coverage audit**:

- Inventory `metric_display_name`.
- Classify each `metric_value` by unit and meaning.
- Check year, DBN, borough, and school coverage.
- Check missing, suppressed, duplicate, and small-denominator records.
- Match attendance and graduation by `dbn + school_year`.
- Audit budget availability and fiscal-year alignment.
- Define transparent review signals; avoid a hidden risk score.

## Security

- Public token-free API access is currently acceptable.
- Add `.gitignore` entries for `.env` and `.env.*`.
- Do not create a real `.env` unless a source requires credentials.
- Use `.env.example` with variable names only.
- Use hosting-managed secrets for production.
- Never commit API tokens.

## Current implementation status

This repository is starting from scratch. The provided mockup archive is included at [`school-equity-resource-monitor-mockup.zip`](school-equity-resource-monitor-mockup.zip).
