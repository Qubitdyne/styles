# PR Draft Notes

Keep this draft synchronized with the active TODO so we can file the upstream pull request without rediscovering the testing story.

## Summary (ready once helpers land)
- Consolidated the publication/status helpers (`tx-publication-parenthetical`, `tx-session-law-citation`, `tx-authority-status-parenthetical`) across the main note style and every TOA variant, eliminating duplicated Chapter 10–13 logic while preserving annotated and supplement parentheticals.
- Suppressed duplicate register citations when a TOA entry already prints the underlying Tex. Reg./Fed. Reg. cite, then refreshed each TOA expectation file to keep the grouped layouts consistent with Appendix B.
- Restored Appendix B’s federal authority coverage in `tests_toa.json`, regenerated all TOA expectations with `--mode bibliography`, and captured fresh confirmation logs (`20251103T014332Z_toa_grouped.txt`, `20251103T014338Z_toa_grouped_leaders.txt`, `20251103T014343Z_toa_leaders.txt`, `20251103T014346Z_toa_by-reporter.txt`).
- Recorded the helper roll-out and TOA fixture decisions in `NOTES.md`/`README.md` so the documentation now matches the consolidated macros and new regression artifacts.

## Testing
- python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt
- python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt
- python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography
- python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt
- python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa.csl --expected temp/expected_toa.txt --mode bibliography
- python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-leaders.csl --expected temp/expected_toa_leaders.txt --mode bibliography
- python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped.csl --expected temp/expected_toa_grouped.txt --mode bibliography
- python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography
- python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-by-reporter.csl --expected temp/expected_toa_by-reporter.txt --mode bibliography

- Latest confirmation logs:
  - `temp/test-logs/20251103T000753Z_notes.txt`
  - `temp/test-logs/20251103T000757Z_parentheticals_notes.txt`
  - `temp/test-logs/20251103T000759Z_parentheticals_bibliography.txt`
  - `temp/test-logs/20251103T000801Z_short-form_smoke.txt`
  - `temp/test-logs/20251103T014332Z_toa_grouped.txt`
  - `temp/test-logs/20251103T014338Z_toa_grouped_leaders.txt`
  - `temp/test-logs/20251103T014343Z_toa_leaders.txt`
  - `temp/test-logs/20251103T014346Z_toa_by-reporter.txt`

## Pending before submission
- Enhance the TOA macros to emit jurisdiction-aware headings that mirror Appendix B and keep Texas/federal ordering intact.
- Update README/NOTES after the heading work so documentation covers the new grouping behavior and log set.
- Investigate the short-form smoke diffs where statutes, regulations, and rules collapse to `Id.`/`See also`; adjust guardrails and refresh `expected_short-form_smoke.txt`.
- Re-run the full regression sweep (notes, parenthetical modes, TOA variants) once the heading changes land and record fresh log paths here.
- Populate the PR body with the final testing checklist immediately before submission.
