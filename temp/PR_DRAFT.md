# PR Draft Notes

Keep this draft synchronized with the active TODO so we can file the upstream pull request without rediscovering the testing story.

## Summary (ready once helpers land)
- Added session law first/short/cross-reference macros so repeated acts restate the full cite while cross references append codification text per Greenbook ch. 11 (pp. 53–56), backed by new note and smoke fixtures.
- Completed the release metadata audit by updating `<updated>` timestamps on the note style, locale, and every TOA variant and fixing each TOA file’s `rel="self"` link to match its ID ahead of the upstream submission.【F:temp/texas-greenbook-15th-edition.csl†L5-L18】【F:temp/texas-greenbook-15th-toa-leaders.csl†L5-L14】【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L12】
- Consolidated the publication/status helpers (`tx-publication-parenthetical`, `tx-session-law-citation`, `tx-authority-status-parenthetical`) across the main note style and every TOA variant, eliminating duplicated Chapter 10–13 logic while preserving annotated and supplement parentheticals.
- Suppressed duplicate register citations when a TOA entry already prints the underlying Tex. Reg./Fed. Reg. cite, then refreshed each TOA expectation file to keep the grouped layouts consistent with Appendix B.
- Restored Appendix B’s federal authority coverage in `tests_toa.json`, regenerated all TOA expectations with `--mode bibliography`, and captured fresh confirmation logs (`20251103T055217Z_toa.txt`, `20251103T055217Z_toa_leaders.txt`, `20251103T055217Z_toa_grouped.txt`, `20251103T055217Z_toa_grouped_leaders.txt`, `20251103T055217Z_toa_by-reporter.txt`).
- Updated the short-form layout so repeated Texas statutes (Greenbook 15th ed. 24, 34), administrative rules (Greenbook 15th ed. 76–78), and Texas/Federal procedural rules (Greenbook 15th ed. 61–65) restate the full authority text instead of emitting `Id.`. Regression logs: `temp/test-logs/20251103T152401Z_notes_full-suite.txt`, `temp/test-logs/20251103T155725Z_short-form_smoke.txt`.
- Extended the short-form restatement guardrails to Texas attorney general opinions (Greenbook 15th ed. 77) and municipal ordinances (Greenbook 15th ed. 62), ensuring repeat cites drop the year parenthetical while cross-references append any `references` strings. Regression logs: `temp/test-logs/20251104T033421Z_short-form_smoke.txt`, `temp/test-logs/20251104T033428Z_notes.txt`.
- Added position-aware Texas Constitution macros so subsequent cites restate the full article/section text and cross-references append companion provisions per Greenbook ch. 9 (p. 39). Regression logs: `temp/test-logs/20251104T183550Z_notes_constitution.txt`, `temp/test-logs/20251104T183557Z_short-form_constitution.txt`.
- Refreshed the Jenkins parenthetical fixture so the short form restates the case instead of emitting `Id. at 2.` consistent with Greenbook ch. 4 (p. 34) and ch. 9 (p. 39), and archived the before/after expectation snapshots plus regeneration logs for reviewer diffing (`temp/test-logs/20251104T190629Z_expected_parentheticals_notes_pre-refresh.txt`, `temp/test-logs/20251104T190640Z_expected_parentheticals_notes_post-refresh.txt`, `temp/test-logs/20251104T190629Z_parentheticals_notes_refresh.txt`, `temp/test-logs/20251104T190640Z_parentheticals_notes_post-refresh.txt`, `temp/test-logs/20251104T190657Z_expected_parentheticals_bibliography_pre-refresh.txt`, `temp/test-logs/20251104T190658Z_expected_parentheticals_bibliography_post-refresh.txt`, `temp/test-logs/20251104T190657Z_parentheticals_bibliography_post-refresh.txt`).
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

- Automation note: each invocation writes a summary line (timestamp, PASS/FAIL, OK/DIFF counts, command) to `temp/test-logs/run-history.log`. Reference this ledger when drafting the final PR narrative or when you need to confirm which suites have already been exercised in a session.

- Latest confirmation logs:
- PASS entries recorded at 2025-11-04T19:26Z in `temp/test-logs/run-history.log` confirm the latest notes, parenthetical, short-form, and TOA sweeps after the metadata audit.【F:temp/test-logs/run-history.log†L53-L61】
- `temp/test-logs/20251103T152401Z_notes_full-suite.txt`
- `temp/test-logs/20251103T055217Z_notes.txt`
- `temp/test-logs/20251103T055217Z_parentheticals_notes.txt`
- `temp/test-logs/20251103T055217Z_parentheticals_bibliography.txt`
- `temp/test-logs/20251104T190629Z_parentheticals_notes_refresh.txt`
- `temp/test-logs/20251104T190640Z_parentheticals_notes_post-refresh.txt`
- `temp/test-logs/20251104T190657Z_parentheticals_bibliography_post-refresh.txt`
- `temp/test-logs/20251103T055217Z_short-form_smoke.txt`
- `temp/test-logs/20251103T055217Z_toa.txt`
- `temp/test-logs/20251103T055217Z_toa_leaders.txt`
- `temp/test-logs/20251103T055217Z_toa_grouped.txt`
- `temp/test-logs/20251103T055217Z_toa_grouped_leaders.txt`
- `temp/test-logs/20251103T055217Z_toa_by-reporter.txt`
- `temp/test-logs/20251104T033421Z_short-form_smoke.txt`
- `temp/test-logs/20251104T033428Z_notes.txt`
- `temp/test-logs/20251104T180708Z_notes.txt`
- `temp/test-logs/20251104T180721Z_short-form_smoke.txt`
- `temp/test-logs/20251104T183550Z_notes_constitution.txt`
- `temp/test-logs/20251104T183557Z_short-form_constitution.txt`
- Archived expectation snapshots for the Jenkins refresh: `temp/test-logs/20251104T190629Z_expected_parentheticals_notes_pre-refresh.txt`, `temp/test-logs/20251104T190640Z_expected_parentheticals_notes_post-refresh.txt`, `temp/test-logs/20251104T190657Z_expected_parentheticals_bibliography_pre-refresh.txt`, `temp/test-logs/20251104T190658Z_expected_parentheticals_bibliography_post-refresh.txt`.

## Pending before submission
- Re-run `git diff --stat` and a quick visual spot-check if additional CSL or fixture edits land after 2026-01-18 so the upstream summary still matches the final diff (see `temp/NOTES.md` entry `2026-01-18T05:40Z`).
- Use `temp/upstream_pr_template.md` as the ready-to-paste PR body; keep it synchronized with `temp/PR_DRAFT.md` if new regression logs or summary items are added before filing.
