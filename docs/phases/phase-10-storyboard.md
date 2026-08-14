# Phase 10 — Storyboard, Visual Direction, and Delivery Roadmap

## Objective

Create a presentation and visual direction for Equity Signal that explains how leaders move from a visible school equity pattern to a responsible review action.

This phase is primarily a storytelling and product-direction phase. The generated visual boards are references for composition and flow; they are not a new data specification or a literal implementation requirement.

## Core product framing

> Equity Signal does not tell leaders what caused a disparity. It makes the disparity easier to see, understand, question, and act on responsibly.

## Linear sub-phase delivery plan

Phase 10 is delivered on the existing `phase-10-visual-alignment` branch through sequential, independently reviewed commits. The order follows the product story rather than grouping work by technical area.

| Sub-phase | Outcome | Dependency |
|---|---|---|
| 10.1 — Storyboard & visual reference | Approved five-beat narrative, visual boards, and delivery roadmap | None |
| 10.2 — Shared application shell | Shared visual language and Portfolio Review hierarchy | 10.1 |
| 10.3 — Schools Directory | Clear school discovery and latest evidence-year selection | 10.2 |
| 10.4 — School Equity Profile | Chart-first evidence, limitations, and observational framing | 10.3 |
| 10.5 — Action handoff & presentation QA | Responsible review handoff and verified five-beat walkthrough | 10.4 |

Each sub-phase requires an approved plan, Builder implementation, Reviewer approval explicitly confirming that sub-phase is complete, and user approval before its commit. No separate branches are required because each step builds on the previous one.

## Visual and product direction

### 1. Lock the visual language

Use the second visual direction board as the primary reference for:

- Warm white and light gray surfaces.
- Deep navy navigation and headings.
- Slate explanatory text.
- Muted teal for evidence and interaction accents.
- Amber for warnings and limitations.
- Restrained coral only for a visible gap that requires attention.
- Thin borders, modest corner radii, generous spacing, and accessible contrast.

The goal is close visual parity in layout, hierarchy, rhythm, and interaction—not pixel-perfect reproduction of generated image artifacts.

### 2. Recreate the product flow in the existing application

The implementation sequence should follow the visual story:

1. Portfolio Review — establish the context and select a school.
2. School Equity Profile — show the evidence, denominators, and warnings.
3. Equity comparison chart — make attendance and graduation endpoints visible.
4. Review question — frame the gap as an unresolved question.
5. Action Plan — document ownership, follow-up, and next evidence to inspect.

The existing Budget / Resources page remains a separate context destination and is not blended into outcome charts.

### 3. Use the current data foundation first

The first visual implementation should use the currently supported data:

- School and school year.
- Gender and race/ethnicity groups.
- 90%+ attendance.
- Four-year graduation.
- Denominators, matched records, and warnings.

Students with disabilities and English Language Learners are not yet part of the current normalized endpoint. NYCPS publishes school-level attendance and chronic-absenteeism information with these characteristics, but that source requires a separate coverage, format, definition, denominator, suppression, and year-alignment audit before implementation.

No new subgroup data is introduced by this phase.

### 4. Preserve the product boundaries

The visual and implementation direction must not introduce:

- Causal claims.
- Fixed performance targets.
- Rankings or hidden risk scores.
- Blended budget/outcome metrics.
- Automated recommendations.
- Unapproved datasets.

Every gap should remain an observational signal. Missing, suppressed, unmatched, or insufficient records should remain visible and understandable.

## Five-beat presentation storyboard

### Beat 1 — The Context

**Message:** Schools can show different attendance, graduation, and demographic patterns, but those patterns are difficult to review consistently across many schools.

**Screen:** Portfolio Review.

**Transition:** Begin with the portfolio view, then narrow to one school profile.

**Suggested language:**

> “The challenge is not a lack of data. It is turning scattered indicators into a reviewable question.”

### Beat 2 — The Data

**Message:** Equity Signal brings school-year outcomes, demographic groups, denominators, warnings, and limited resource context into one review experience.

**Screen:** School Equity Profile evidence table, with Budget / Resources shown only as a separate contextual destination.

**Transition:** Move from a selected school to the profile’s evidence table.

**Suggested language:**

> “The data gives us a clearer view of outcomes—but clarity about outcomes is not the same as certainty about causes.”

### Beat 3 — How We Analyzed the Data

**Message:** Attendance and graduation records are matched by school, school year, and demographic group. Comparisons are displayed only where the records support them.

**Screen:** Dumbbell chart, demographic table, matched-record details, and warnings.

**Transition:** Move from table rows to chart endpoints, then call attention to denominators and limitations.

**Suggested language:**

> “We compare like with like where the records support it. Where they do not, the uncertainty stays on screen.”

### Beat 4 — The Key Insight

**Message:** A visible gap is a signal for closer review, not proof of why the gap exists.

**Screen:** One highlighted chart gap with its denominator and warning context visible.

**Transition:** Hold on the gap, then reveal the observational framing and uncertainty.

**Suggested language:**

> “The gap is the beginning of the conversation—not the conclusion.”

### Beat 5 — The “So What?”

**Message:** The user can inspect the profile, compare evidence, document a review question, and assign follow-up to the appropriate team.

**Screen:** Authenticated Action Plan linked to the school review.

**Transition:** Move from the unresolved chart question to ownership, notes, status, and follow-up date.

**Suggested language:**

> “The product does not decide what caused the pattern. It helps the right people decide what to examine next.”

## Visual flow

```text
Portfolio context
        ↓
School and subgroup evidence
        ↓
Matched attendance/graduation comparison
        ↓
Visible gap plus uncertainty
        ↓
Documented review question and assigned follow-up
```

## Workflow timing

Recommended presentation length: **6–8 minutes**.

- Beat 1: 60–75 seconds.
- Beat 2: 75–90 seconds.
- Beat 3: 90–120 seconds.
- Beat 4: 60–75 seconds.
- Beat 5: 75–90 seconds.

## Implementation scope after storyboard approval

The next implementation should be limited to visual and interaction alignment with the approved direction:

- Refine shared shell, spacing, typography, and color tokens.
- Align Portfolio Review and School Equity Profile hierarchy to the visual board.
- Make the chart, warnings, denominators, and matched records visually central.
- Connect the profile review question to the existing Action Plan workflow.
- Preserve existing routes, data behavior, authentication, responsiveness, and accessibility.

SWD and ELL data expansion should remain a separately approved data-audit task before any related UI is added.

## Acceptance criteria

- The five beats form a coherent presentation narrative.
- Each beat maps to an existing product screen or visualization.
- The visual direction creates tension between observed evidence and uncertainty.
- The second visual board is treated as a close visual reference without inventing unsupported data.
- Denominators, matched records, missing data, and warnings remain visible.
- Budget / Resources remains separate from outcome analysis.
- No causation, rankings, hidden scores, fixed targets, or automated recommendations are introduced.
- The implementation plan remains compatible with the current application architecture.

## Non-goals

- No new API dataset in this phase.
- No SWD or ELL metric implementation in this phase.
- No replacement of the existing data model.
- No new ranking or risk-scoring system.
- No causal analysis.
- No production UI changes until the storyboard and visual implementation plan are approved.

## Development references

- [Phase 10 visual direction board](../../school-equity-resource-monitor-mockup/phase-10-visual-direction-board.png)
- [Phase 10 visual direction board alternate](../../school-equity-resource-monitor-mockup/phase-10-visual-direction-board-1.png)

## Status

Phase 10.1 documentation is in implementation. Application changes remain deferred to their respective sub-phases.
