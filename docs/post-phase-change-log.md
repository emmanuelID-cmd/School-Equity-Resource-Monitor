# Post-Phase Change Log

This log records small maintenance and clarity improvements made after the approved implementation phases are complete. It does not reopen or rewrite historical phase scope.

## 2026-08-12 — Schools Directory total-result count

- The Schools Directory continues to load up to 100 records per API page and supports internal scrolling.
- The portfolio API now returns `total`, representing the number of schools matching the active DBN/name, borough, school-year, and review filters before pagination.
- The directory status now reports the loaded count against the filtered total, for example: `100 of 1,452 schools`.
- No-results behavior, filters, profile navigation, and pagination behavior are otherwise changed.

## 2026-08-12 — Portfolio Review total-result count

- Portfolio Review now reports the loaded count against the filtered total beside its Priority review queue and status message.
- The existing 100-record page size, infinite scrolling, filters, selected-school behavior, and observational framing remain unchanged.
