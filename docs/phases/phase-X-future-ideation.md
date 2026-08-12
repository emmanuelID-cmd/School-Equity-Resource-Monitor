# Phase X — Future Ideation: Attendance and Graduation Comparisons

## Status

Temporary future-ideation reference only. This is not an approved implementation phase and does not authorize code changes.

## Product mapping

The School Equity Resource Monitor maps to the operational review workflow of an NYC Superintendent or DOE portfolio agent.

Its core decision-support question is:

> Which high schools show notable demographic attendance and graduation patterns, what evidence supports that observation, and which schools should receive closer review?

The product is an evidence and prioritization tool. It is not intended to function as a demographic visualization alone, an automated risk score, a budget-allocation engine, or a replacement for professional judgment and district review.

## Current product value

The completed product currently supports:

- Portfolio-level review of high schools.
- School Year, Borough, review-signal, and disparity filtering.
- School lookup by DBN or School Name.
- Deep navigation from a Portfolio Review record to a School Equity Profile.
- Demographic 90%+ attendance and four-year graduation comparisons.
- Attendance-versus-graduation gap visibility.
- Attendance and graduation denominators.
- Matched-record counts and data-quality warnings.
- Missing, suppressed, unmatched, and insufficient-data explanations.
- Year switching for a selected school.
- A visual comparison chart that preserves observational interpretation.

## Superintendent benefit

The product can help a Superintendent or portfolio agent:

- Scan a large high-school portfolio for records that warrant closer review.
- Move from a portfolio-level signal to detailed school-year evidence.
- Compare attendance and graduation measures using consistent definitions.
- Identify whether an apparent difference is supported by adequate denominators.
- Distinguish missing or suppressed data from genuinely observed low values.
- Examine demographic patterns without introducing unsupported causal explanations.
- Decide which schools, years, or demographic records should be discussed with district teams.
- Establish a documented evidence trail before considering a support review or follow-up action.

The product does not decide what intervention a school needs. It helps structure the evidence review that precedes that decision.

## Current product boundary

The current implementation is a strong evidence and prioritization layer, but it is not yet a complete school-improvement operating product.

It does not currently provide:

- Resource or budget context.
- Action-plan ownership, dates, status, or persistence.
- Follow-up metric tracking.
- Staffing, counseling, tutoring, attendance-intervention, or support-capacity context.
- Formal comparison cohorts or peer-school analysis.
- Automated causal explanations.
- A definitive school ranking that substitutes for professional review.

## Future datasets and product layers

Additional datasets may be required to expand the product into a fuller operational review system.

### Budget and resource context

Potential inputs include:

- NYCPS financial data and reports.
- Fair Student Funding allocations and proposals.
- School budget-at-a-glance data.
- Budget allocation categories by school and fiscal year.
- Resource or program support records aligned to DBN and year.

These datasets could help users ask whether available resources and support capacity should be reviewed alongside observed outcome patterns. They must not be used to claim that spending causes attendance or graduation outcomes.

### Enrollment and school composition

Potential inputs include:

- Enrollment totals.
- Grade and cohort composition.
- Student demographic composition.
- English learner, special education, and economically disadvantaged indicators where documented and appropriate.
- School type and program context.

These inputs would provide context for denominators and comparisons, but they would require careful population definitions and privacy-aware suppression handling.

### Student-support capacity

Potential inputs include:

- Counseling and social-work capacity.
- Attendance intervention programs.
- Tutoring and academic support availability.
- Staffing or vacancy context.
- School-based support program participation.

These data could support a structured review of available support context. They should remain descriptive and should not be converted into an opaque intervention score.

### Action-plan and follow-up data

A later action-plan layer may require:

- Concern or review area.
- Recommended review question.
- Responsible team.
- Due date.
- Review status.
- Follow-up metric.
- Review notes.
- Completion history or audit trail.

This would require explicit decisions about persistence, permissions, editing, audit history, and ownership before implementation.

### Peer and comparison-school context

Potential future inputs include:

- Comparable high-school group definitions.
- Borough or district peer groups.
- Similar enrollment or program context.
- Multi-year comparison windows.

Peer comparisons must define eligibility, year alignment, denominator rules, ties, missing data, and population boundaries before being used in product decisions.

## Data integration requirements

Before adding a future dataset, the Planner should confirm:

- Stable school identifier, preferably DBN.
- Time-grain alignment with `school_year` or an explicitly documented fiscal/calendar year relationship.
- Metric definitions and units.
- Denominator meaning.
- Missing and suppressed-value behavior.
- Duplicate and unmatched-record handling.
- Refresh cadence and source ownership.
- Privacy and disclosure constraints.
- Whether the data supports observation, context, or an action workflow.

No dataset should be added merely because it appears correlated with an outcome. Each addition needs a documented product purpose and a non-causal interpretation.

## Concept 1 — Highest versus lowest attendance comparison

For a selected school year, compare schools with the highest and lowest observed 90%+ attendance rates.

For each comparison, show:

- School name and DBN.
- Borough and school year.
- 90%+ attendance rate.
- Four-year graduation rate.
- Attendance-versus-graduation gap.
- Attendance and graduation denominators.
- Matched-record and data-quality warnings.

The comparison must remain observational. It should describe differences in the available records without suggesting that attendance, resources, demographics, or any other factor causes graduation outcomes.

## Concept 2 — Highest versus lowest graduation-gap comparison

Compare schools with the largest and smallest observed attendance-versus-graduation gaps for a selected year.

The display should make clear:

- Which metric defines the gap.
- Whether the gap is an absolute percentage-point difference or a directional difference.
- Which demographic or All Students record is being compared.
- The denominators supporting each value.
- Whether records are missing, suppressed, unmatched, or insufficient.

Do not create an opaque risk score from these comparisons.

## Concept 3 — School comparison filters

Consider filters that allow users to find individual schools by:

- Highest 90%+ attendance.
- Lowest 90%+ attendance.
- Highest attendance-versus-graduation gap.
- Lowest attendance-versus-graduation gap.
- Highest four-year graduation rate.
- Lowest four-year graduation rate.

Potential filter dimensions:

- School year.
- Borough.
- Demographic group.
- Minimum denominator, if an explicit threshold is approved.

Any ranking or filter must expose the underlying rate, gap, denominator, matched-record status, and warnings. Results should not be interpreted as causal or as a definitive school ranking without additional product decisions.

## Questions for a future Planner

- Should comparisons use All Students only, a selected demographic, or both?
- Should highest/lowest use absolute rates, percentage-point gaps, or another documented measure?
- What denominator rules should qualify a record for comparison?
- How should ties be displayed?
- Should the user compare two selected schools or view ranked results?
- How should missing, suppressed, and insufficient records be handled?
- Should the comparison remain within the existing high-school population and supported years?

## Explicit non-claims

These comparisons must not claim that attendance causes graduation outcomes, that a school is better or worse because of a single observed metric, or that the comparison identifies the reason for an observed difference.

## Observational hypothesis — learning experience review

Attendance and graduation disparities may serve as indicators for a future learning-experience review.

For example, a pattern of relatively high attendance alongside relatively low four-year graduation could warrant questions about:

- Whether course material or graduation requirements present barriers for students.
- Whether instructional methods and academic supports should be reviewed.
- Whether students are attending school but not receiving sufficient academic progress or completion support.
- Whether course access, credit accumulation, scheduling, mobility, or other school-context factors should be examined.

These possibilities must not be inferred directly from the attendance and graduation records. The current product may identify the pattern and surface it for observation only. It must not determine that material is too challenging, conclude that teacher methods are inadequate, or attribute an outcome to instruction without additional validated evidence.

For the current and near-term product:

- Use the disparity as an observation signal only.
- Preserve the attendance and graduation values, gaps, denominators, matched-record counts, and warnings.
- Use neutral language such as “This pattern may warrant a learning-experience review.”
- Do not generate instructional recommendations or causal explanations.
- Treat any future learning-experience analysis as a separate scoped phase requiring additional data and review criteria.

## Future access permissions for Action Plans

The initial Action Plans workflow should remain available to every authenticated user who has access to the product. This supports team collaboration while keeping unauthenticated visitors out of the workflow.

The current product should preserve the following boundaries:

- Authenticated users may view, create, and update Action Plans.
- Unauthenticated visitors may not access Action Plans.
- School evidence, attendance values, graduation values, denominators, demographic records, and warnings remain read-only.
- Workflow fields such as owner team, selected actions, status, notes, and follow-up date may be edited by authenticated users.

A later phase may introduce role-based permissions if the product requires different levels of access. Potential roles include:

- Admin — manage users, permissions, and Action Plans.
- Team editor — create and update Action Plans.
- Viewer — view Action Plans and evidence without editing.

Role-based permissions should not be added implicitly. A future Planner must define the role model, ownership rules, invitation process, audit requirements, and Row Level Security policies before implementation. Until then, authenticated team collaboration is the approved access model.

## Future ticketing and email notifications

The current Action Plans workflow status is not a ticketing system. Saved Plans may show Draft, In progress, Complete, or Deferred, but the initial workflow does not yet provide ticket numbers, status history, assignment notifications, or email delivery.

A future ticketing layer may add:

- A generated ticket identifier, such as `AP-2026-0001`.
- A status-history record for each transition.
- The user, team, timestamp, and note associated with each transition.
- Assignment and ownership-change events.
- Follow-up-date reminders.
- Email notifications when a plan is created, assigned, updated, completed, or deferred.
- Email escalation notifications that send the ticket details directly to the person or office selected in the escalation level.

Email delivery should be implemented through a server-side Supabase Edge Function and a configured email provider or SMTP service. Browser code must not contain email-provider secrets or send privileged messages directly.

Before implementation, a future Planner must define the ticket lifecycle, numbering rules, notification recipients, opt-out behavior, delivery-failure handling, audit retention, escalation-level email addresses, and whether notifications go to individual users, teams, or both. The initial Phase 5 workflow remains authenticated and collaborative without ticketing or email notifications.

## Future account access model — invite-only users

The eventual product should use invite-only access rather than open public registration. This is appropriate for an internal superintendent and school-support workflow where access should be limited to approved staff and collaborators.

The future account model may include:

- Administrators inviting approved users by email.
- Supabase Auth confirmation before first sign-in.
- A visible sign-in and sign-out experience.
- Password-reset and session-expiration recovery.
- Optional role assignment after invitation, such as Admin, Team editor, or Viewer.
- Disabling public self-registration in the production environment.

During development, open registration may remain enabled temporarily for testing. Before production deployment, the Planner must define the invitation process, administrator responsibilities, deactivation behavior, and access-review requirements. Invite-only access does not change the observational purpose of Action Plans or permit users to edit underlying school evidence.
