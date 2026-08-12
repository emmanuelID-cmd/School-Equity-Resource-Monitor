# Phase 4 — Product Framing and Shared Header

## Objective

Make the product’s purpose explicit and consistent across Portfolio Review and Schools through shared branding, product framing, and persistent navigation context.

## Scope

- Shared product header across Portfolio Review and Schools.
- Selected Modern School Flat logo and full wordmark.
- Product-purpose statement describing the evidence-to-review workflow.
- Observational/non-causal framing.
- Sticky product header.
- Sticky left navigation on desktop and tablet.
- Normal-flow horizontal navigation on mobile.
- Mobile navigation overflow cues for additional tabs.
- Responsive desktop, tablet, and mobile presentation.
- Accessible logo text, navigation links, and focus behavior.

## Non-goals

- Action Plan implementation or persistence.
- New data, charts, filters, rankings, or review signals.
- Causal interpretation.
- Resource or budget integration.
- Changes to profile, Portfolio Review, or Schools data behavior.

## Inputs

- Phase 3 baseline at commit `8a13a27`.
- Selected logo design asset in `school-equity-resource-monitor-mockup/logo-modern-school-flat.svg`.
- Existing Portfolio Review and Schools navigation structure.
- Existing responsive layout and product color palette.

## Deliverables

- `shared-header.js` shared header and mobile navigation cue behavior.
- `styles.css` responsive header, navigation, logo, and cue styling.
- `app.js` and `school-profile.js` shared-header integration.
- Selected logo asset.
- This Phase 4 documentation and completion evidence.

## Acceptance criteria

- Portfolio Review and Schools display the same product header.
- The header includes the product name, purpose statement, and observational framing.
- The selected logo displays fully without cropping or wordmark truncation.
- Desktop and tablet left navigation remains visible during content scrolling.
- Mobile navigation remains non-sticky and horizontally scrollable.
- A right mobile cue appears when additional navigation exists.
- A left mobile cue appears after scrolling right.
- Existing routes, filters, charts, tables, warnings, and year switching remain unchanged.
- Desktop, tablet, and mobile layouts remain usable.
- Keyboard navigation and focus behavior remain available.
- No console errors or broken links are introduced.
- Existing tests pass and `git diff --check` passes.

## Risks

- Sticky elements can cover content if offsets or stacking order are incorrect.
- Large logo dimensions may consume mobile header space.
- Mobile cue positioning is a minor visual compromise and may require later refinement inside the navigation container.
- Product framing must remain observational and must not imply automated recommendations or causal findings.

## Exit criteria

- Implementation is complete within the approved scope.
- User verifies the shared header, logo, sticky navigation, and responsive behavior.
- Relevant tests pass and `git diff --check` passes.
- Changed-file scanning is complete.
- Read-only REVIEWER returns `APPROVE`.
- Phase completion evidence is recorded after reviewer clearance and explicit user approval.

## Completion evidence

- User verified Portfolio Review, Schools directory, and School Equity Profile previews.
- User verified desktop, tablet, and mobile scrolling behavior and confirmed no content was covered.
- User accepted the non-sticky mobile navigation design.
- User verified the mobile navigation arrows function, with the minor cue-positioning issue acknowledged for later refinement.
- User verified existing product behavior remains intact.
- Automated verification passed: 15/15 tests.
- `git diff --check` passed.
- Read-only REVIEWER verdict: `APPROVE`.

## Status

Phase 4 complete. Implementation, review, commit, and push are complete.
