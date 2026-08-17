# Phase 10.2 — Shared Application Shell

## Objective

Apply the approved visual language to the shared application shell and establish the Portfolio Review as the presentation entry point.

## Scope

- Shared header, navigation, surfaces, spacing, typography, controls, and responsive behavior.
- Portfolio Review hierarchy that establishes the Context beat.
- Portfolio Review queue ordering: Brooklyn, Bronx, Manhattan, Queens, Staten Island; then DBN and school year.
- Display a disabled `Select a Year` placeholder on initialization; while no explicit year is selected, load one latest comparison-capable record per school.
- Preserve current routes, logo image, navigation behavior, data behavior, and accessibility.

## Acceptance criteria

- The shared shell reflects the approved visual direction without altering the Equity Signal logo asset or design.
- Portfolio Review clearly establishes the review context before school selection.
- The default Portfolio queue begins with one latest comparison-capable record per school and Brooklyn records when no year is selected; an explicit year filters the queue to that year.
- Portfolio pagination remains correct after borough-first ordering.
- Existing controls and routes remain functional and responsive.
- The shared latest-record API may support the Portfolio default; Schools Directory UI, profile analytics, and Action Plan behavior are not included.

## Non-goals

- No new datasets or endpoints.
- No rankings, causal claims, targets, or automated recommendations.
- No Directory, profile, or Action Plan workflow work beyond styles strictly required by the shared shell.

## Dependency

Phase 10.1 complete and committed.

## Status

Planned.
