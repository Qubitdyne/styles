# Texas Greenbook 15th Edition — Working Notes

Use this file to capture the minimum context required to resume work quickly. Detailed historical research logs are archived in `temp/archive/NOTES-2025-12-21.md`.

## Active research threads
- **Publication/status helpers:** The prototype in `temp/prototypes/` already demonstrates how to collapse session law and agency parentheticals. The next implementation pass needs Greenbook Chapter 10–13 references confirming when to emit `Supp.`, `R.S.`, and similar status tags.
- **TOA federal coverage:** Appendix B examples require the grouped TOA layout to interleave federal authorities with Texas entries. Document any sorting or heading decisions here once the fixtures are restored.
- **Session stability:** Record the command(s) you run at the end of each block of work (including any failing cases) so recovery is straightforward if a session terminates unexpectedly.

## Quick reference links
- `temp/TODO.md` — trimmed active backlog.
- `temp/PR_DRAFT.md` — running narrative for the eventual upstream pull request.
- `temp/Greenbook_15thEdition.pdf` — authoritative rule text; note page numbers here when citing new guidance.

## When pausing work
1. Summarize what changed, what still needs attention, and where to look next (tests, macros, etc.).
2. Note any commands to rerun along with expected outcomes.
3. If additional detail is required but would bloat this file, drop a dated note into `temp/archive/` and link to it from here.

## 2025-11-03T00:05Z — QA sweep and documentation spot-check
- Ran regression commands:
  - `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography`
- All suites matched their expectations with no citeproc warnings; capture permanent logs before the next helper integration pass.
- PR draft references (`temp/PR_DRAFT.md`) still point to placeholder log filenames (`20250314-related-warning-*`) that do not exist—log an update task before finalizing the submission narrative.

## 2025-11-03T00:08Z — Regression rerun and PR draft cleanup
- Re-ran the baseline suites and archived logs:
  - `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt` → `temp/test-logs/20251103T000753Z_notes.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt` → `temp/test-logs/20251103T000757Z_parentheticals_notes.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography` → `temp/test-logs/20251103T000759Z_parentheticals_bibliography.txt`
  - `python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt` → `temp/test-logs/20251103T000801Z_short-form_smoke.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography` → `temp/test-logs/20251103T000803Z_toa_grouped_leaders.txt`
- Notes, parentheticals (note & bibliography), and TOA grouped-leaders suites matched expectations with no warnings.
- The short-form smoke suite surfaced diffs where statutes, regulations, and rules collapse to `Id.`/`See also`; logged a new TODO to restore full-repeat citations before submission.
- Updated `temp/PR_DRAFT.md` to cite the real log filenames and avoid dangling `20250314` placeholders.
