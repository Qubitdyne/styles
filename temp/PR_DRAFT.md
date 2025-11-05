# PR Draft Notes

Keep this draft synchronized with the active TODO so we can file the upstream pull request without rediscovering the testing story.

## Summary (ready once helpers land)
- Added session law first/short/cross-reference macros so repeated acts restate the full cite while cross references append codification text per Greenbook ch. 11 (pp. 53–56), backed by new note and smoke fixtures.
- Normalized metadata across the note style and TOA variants: `version="1.0"`, refreshed `<updated>` timestamps, unified CC BY-SA 3.0 rights blocks, pointed documentation links at the Texas Style Manual landing page, and inlined the locale overrides so the package complies with upstream distribution rules.【F:temp/texas-greenbook-15th-edition.csl†L2-L212】【F:temp/texas-greenbook-15th-toa.csl†L2-L18】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L2-L17】
- Reworked every TOA bibliography to use CSL’s `left-margin`/`right-inline` alignment, added `page-first` driven TOA pagination, and updated fixtures/expectations to reflect the new layout and page-number field; downstream authors now populate `page-first` with the brief’s TOA pagination per the documented guidance.【F:temp/texas-greenbook-15th-toa.csl†L768-L807】【F:temp/texas-greenbook-15th-toa-leaders.csl†L736-L773】【F:temp/tests_toa.json†L1-L200】【F:temp/README.md†L67-L73】
- Simplified cross-reference cue handling so the default note style now falls back to “See” while honoring `annote` overrides and capitalizing free-form `note` text, keeping CSL 1.0 schema compliance without sacrificing manual signal control.【F:temp/texas-greenbook-15th-edition.csl†L570-L595】【F:temp/README.md†L103-L108】
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
- jing -c /tmp/csl-schema/schemas/styles/csl.rnc temp/*.csl

- Automation note: each invocation writes a summary line (timestamp, PASS/FAIL, OK/DIFF counts, command) to `temp/test-logs/run-history.log`. Reference this ledger when drafting the final PR narrative or when you need to confirm which suites have already been exercised in a session.

Documented the `page-first` TOA pagination requirement in the README to keep data entry aligned with the refreshed fixtures and summary narrative.【F:temp/README.md†L67-L73】

- Latest confirmation logs:
- PASS entries recorded at 2025-11-05T01:57Z in `temp/test-logs/run-history.log` confirm the refreshed notes, parenthetical, short-form, and TOA sweeps captured for the run-history ledger update.【c77cbe†L31-L75】
- `temp/test-logs/20251105T015713Z_notes.txt`
- `temp/test-logs/20251105T015724Z_parentheticals_notes.txt`
- `temp/test-logs/20251105T015729Z_parentheticals_bibliography.txt`
- `temp/test-logs/20251105T015732Z_short-form_smoke.txt`
- `temp/test-logs/20251105T015740Z_toa.txt`
- `temp/test-logs/20251105T015744Z_toa_leaders.txt`
- `temp/test-logs/20251105T015747Z_toa_grouped.txt`
- `temp/test-logs/20251105T015751Z_toa_grouped_leaders.txt`
- `temp/test-logs/20251105T015754Z_toa_by-reporter.txt`【011517†L1-L12】
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
