# Phase 5 — Action Plans

## Objective

Add an authenticated, server-backed Action Plans workflow that records what a team should review next from observational school-equity patterns, without presenting recommendations as causal conclusions.

## Scope

- Supabase-backed Action Plans table and authenticated access.
- Create, view, edit, and reload saved plans.
- School DBN prefix search with an in-page results panel and no-results guidance.
- School-year selection from the API, defaulting to the initialized/current available year.
- Demographic selection and observational evidence context.
- Preset recommended review areas with a custom review-area option.
- Separate concrete Action Options checklist.
- Notes for team context and interpretation.
- Owner Team selection with an `Other` custom value.
- Optional Escalation Level selection.
- Status values: `Draft`, `In progress`, `Complete`, and `Deferred`.
- Optional follow-up date restricted to tomorrow through 30 days ahead, using real calendar and leap-year validation.
- Authenticated navigation, sign-in, session expiry handling, and nested sign-out behavior.
- Responsive, keyboard-accessible, readable validation and API-error states.

## Non-goals

- Causal claims about attendance, graduation, demographics, or school outcomes.
- Automatic action-plan recommendations beyond selectable review areas and action options.
- Email notifications, ticket IDs, ticket history, reminders, or escalation delivery.
- Delete-plan controls or high-tier administrative permissions.
- Invite-only production access and role-based administration.
- Budget context, action-plan analytics, or new school-equity datasets.
- Changes to the established Portfolio Review, Schools directory/profile, or chart metrics.

## Inputs

- Phase 4 shared header, navigation, and responsive layout.
- Existing Portfolio Review, Schools directory, and School Equity Profile APIs.
- Supabase project URL and publishable key provided through the ignored local `.env` file.
- Supabase `auth.users` authentication and the `public.action_plans` schema.
- RLS policies allowing authenticated users to select, insert their own plans, and update plans.
- Existing product framing that findings are observational and require review.

## Deliverables

- `action-plans.html` — authenticated Action Plans page and form.
- `action-plans.js` — authentication, API loading, validation, create/edit, saved-plan, and search behavior.
- `auth.js` — shared Supabase session and authenticated-request handling.
- `login.html` — email/password sign-in page and expired-session recovery.
- `server.py` and `api/portfolio.py` — configuration and DBN-prefix API support required by the workflow.
- `shared-header.js`, `index.html`, `schools.html`, and `styles.css` — navigation and shared responsive integration.
- Supabase `action_plans` schema, grants, and RLS policies configured outside the repository.
- This Phase 5 documentation and completion evidence.

## Acceptance criteria

- Unauthenticated users are directed to sign in; authenticated users can access Action Plans.
- Authenticated users can create a valid plan, view it in Saved Plans, edit it, and confirm edits persist after reload.
- Save remains disabled until required fields and valid values are present.
- School-year options load from the API and a usable initialization year is selected by default.
- DBN search calls on valid prefixes, keeps results beneath the textbox, limits visible suggestions, and gives actionable zero-result guidance.
- Recommended review area/custom review text, Action Options, and Notes remain distinct fields.
- Owner Team defaults to `Select owner team`; `Other` accepts a custom team value.
- Optional Escalation Level saves and reloads correctly.
- Status values are limited to Draft, In progress, Complete, and Deferred.
- Follow-up dates accept only tomorrow through 30 days from today and reject impossible dates, including invalid month lengths and leap-year dates.
- API errors, expired sessions, missing/invalid fields, no results, and insufficient data produce readable recovery guidance without exposing secrets.
- RLS permits authenticated select/create/update operations and blocks unauthenticated table access.
- Keyboard navigation, visible focus, field-associated errors, and screen-reader announcements remain available.
- Portfolio Review, Schools directory/profile, and shared navigation regressions are absent.
- Desktop, tablet, and mobile layouts work without content overflow or covered controls.
- Relevant tests pass and `git diff --check` passes.

## Risks

- Expired JWTs can appear as generic 401 failures unless the session is cleared and sign-in recovery is explicit.
- Browser/API cold starts can leave year metadata in a loading state without a visible error path.
- Supabase RLS or grants can prevent saves even when client validation succeeds.
- Native datalist behavior can escape the search field; the custom results panel must remain positioned within the field container.
- Date validation can accept impossible dates unless calendar and leap-year checks are performed at the boundary.
- Action Plans must remain observational and must not imply that an observed gap proves a cause or prescribes an unverified intervention.

## Exit criteria

- Implementation is complete within the approved scope.
- Supabase schema, grants, and RLS behavior are verified.
- Create, edit, reload, validation, API-error, expired-session, and no-results states are verified.
- Owner Team, `Other`, optional Escalation Level, status, and follow-up-date behavior are verified.
- Portfolio Review and Schools regression checks pass.
- Desktop, tablet, mobile, keyboard, focus, and error-announcement checks pass.
- Changed-file scanning is complete.
- Read-only REVIEWER returns `APPROVE`.
- Phase completion evidence is recorded only after reviewer clearance, explicit user approval, commit, and push.

## Completion evidence

- User verified save-plan behavior and the school-year API call.
- User verified error handling, input validation, disabled-save behavior, view/edit persistence, Owner Team/Other, and optional Escalation Level persistence.
- User verified the DBN results panel remains beneath the textbox, keyboard navigation, visible focus, readable errors, and announcements.
- User verified Portfolio Review and Schools regression behavior.
- User verified desktop, tablet, and mobile behavior.
- Supabase RLS policies and authenticated grants were verified; anonymous table access was revoked.
- Reviewer returned `APPROVE` with no functional blockers.
- Phase 5 implementation and documentation were committed in `161e29b` and pushed to `origin/main`.
- Render deployment compatibility was committed in `c980527` and the runtime configuration fix in `56ef33f`; both were pushed to `origin/main`.
- User verified the live Render deployment, including production login and Supabase configuration.
- Local `.env` remains ignored, untracked, and outside all commits.

## Status

Phase 5 complete and formally closed. Implementation, documentation, review, commit, push, and live deployment verification are complete.
