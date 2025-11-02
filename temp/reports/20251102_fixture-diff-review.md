# Fixture Diff Review (2025-11-02)

## Scope
- `tests.json` vs. `expected.txt` using `texas-greenbook-15th-edition.csl`
- `tests_parentheticals.json` vs. `expected_parentheticals_notes.txt`
- `tests_toa.json` vs. `expected_toa_grouped_leaders.txt`

## Method
1. Ran the citeproc regression harness for each suite listed above.
2. Captured command output in `temp/test-logs/20251102_fixture-review_*.txt` for traceability.
3. Reviewed the console summaries to confirm that every fixture matched its expected output; no diffs were generated.

## Result
All suites completed without producing expectation diffs. The current expected files remain synchronized with citeproc output, so no fixture regeneration is required at this time.

## Follow-up
- Re-run this review after the next round of citation-logic changes.
- If new fixtures are introduced (e.g., publication/status helpers), add them to this checklist and archive the updated logs.
