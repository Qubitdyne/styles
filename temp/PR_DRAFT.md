# PR Draft Notes

Keep this draft synchronized with the active TODO so we can file the upstream pull request without rediscovering the testing story.

## Summary (ready once helpers land)
- Consolidated the publication/status helpers (`tx-publication-parenthetical`, `tx-session-law-citation`, `tx-authority-status-parenthetical`) across the main note style and every TOA variant, eliminating duplicated Chapter 10–13 logic while preserving annotated and supplement parentheticals.
- Suppressed duplicate register citations when a TOA entry already prints the underlying Tex. Reg./Fed. Reg. cite, then refreshed each TOA expectation file to keep the grouped layouts consistent with Appendix B.
- Restored Appendix B’s federal authority coverage in `tests_toa.json`, regenerated all TOA expectations with `--mode bibliography`, and captured fresh confirmation logs (`20251103T055217Z_toa.txt`, `20251103T055217Z_toa_leaders.txt`, `20251103T055217Z_toa_grouped.txt`, `20251103T055217Z_toa_grouped_leaders.txt`, `20251103T055217Z_toa_by-reporter.txt`).
- Recorded the helper roll-out and TOA fixture decisions in `NOTES.md`/`README.md` so the documentation now matches the consolidated macros and new regression artifacts.
- Documented Chapter 2, 4, 10, and 17 coverage with explicit Greenbook page cites in `NOTES.md` (`2025-11-03T04:12Z` entry) to support the upstream narrative once headings and short-form guardrails land.

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
- `temp/test-logs/20251103T055217Z_notes.txt`
- `temp/test-logs/20251103T055217Z_parentheticals_notes.txt`
- `temp/test-logs/20251103T055217Z_parentheticals_bibliography.txt`
- `temp/test-logs/20251103T055217Z_short-form_smoke.txt`
- `temp/test-logs/20251103T055217Z_toa.txt`
- `temp/test-logs/20251103T055217Z_toa_leaders.txt`
- `temp/test-logs/20251103T055217Z_toa_grouped.txt`
- `temp/test-logs/20251103T055217Z_toa_grouped_leaders.txt`
- `temp/test-logs/20251103T055217Z_toa_by-reporter.txt`

## Pending before submission
- Run a final `git diff --stat`/visual review of the CSL changes once documentation touch-ups settle so the upstream summary captures every updated macro and fixture.
- When opening the upstream pull request, port the Summary/Testing sections above (with the archived log links) into the PR body and note the TODO archive location for reference.
