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

## 2025-11-03T02:30Z — Publication helper groundwork
- **Prototype inventory.** The sandbox in `temp/prototypes/` still aligns with the production macros we need to consolidate:
  - `publication-helper-prototype.csl` + JSON/expected fixtures cover the three publication/status flows. `publication-parenthetical` mirrors the `edition-publisher-year` parenthetical scaffolding that appears throughout statutes, books, and agency materials; `session-law-metadata` restates the `session-law` macro used in notes and TOA variants; and `administrative-status` reproduces the authority/status grouping that `tex-admin-code-first` and the TOA regulation stack currently duplicate.
  - `publication-helper-prototype.json` enumerates the record types we must support during extraction (codes with supplements, session laws with optional Gammel cites, TAC rules with authority/status pairs). `publication-helper-expected.txt` preserves the intended output order so we can diff the final helper implementation against a stable reference.
- **Greenbook Ch. 10–13 rule pulls.** Key directives for helper behavior:
  - **Chapter 10 (Current Statutes).** Cite current codes without a date, reserve parentheticals for supplements or special publications, and quote auxiliary pamphlet provenance for historical session laws (`Tex. Educ. Aux. Laws … [Act of Mar. 28, 1963 …]`). Greenbook 15th ed. 45–52.
  - **Chapter 11 (Statutes No Longer in Effect).** Repealed, amended, and expired session laws require parenthetical years or explicit “amended by/repealed by” citations, with parallel cites to Gammel for pre-1898 material. Greenbook 15th ed. 53–56.
  - **Chapter 12 (Comments and Notes).** Historical comments, Revisor’s Notes, U.C.C. comments, and Historical Notes each demand labeled suffixes and, when applicable, bracketed session-law cross-references. Greenbook 15th ed. 57–60.
  - **Chapter 13 (Rules of Procedure & Evidence).** Current rules omit dates, but repealed or superseded rules must append the promulgating source and adoption/repeal dates; the Rules of Judicial Administration also need a “reprinted in Tex. Gov’t Code …” parenthetical on first mention. Greenbook 15th ed. 61–65.
- **Helper signature decisions.** Consolidate the repeated logic into three reusable macros before wiring them into the production style and TOA files:
  - `tx-publication-parenthetical` — Builds the `(Publisher [Place] Year | Status | Medium | Note)` cluster, skipping empty segments but preserving supplement strings supplied via `note` and the fallback of `issued` → `status` → `medium` mirroring Chapter 10 guidance.
  - `tx-session-law-citation` — Emits the comma-delimited session law scaffold (title, legislature/session, chapter/section pairing, publication pages, locator, and optional `references`). The helper will accept the same variables the prototype exercises so both note and TOA contexts can call it.
  - `tx-authority-status-parenthetical` — Handles agency and rule post-script text `(Authority, Status, Year; Register Cite; Note)`, toggling parentheses only when at least one segment exists so we can share it across TAC entries, repealed rules, and Greenbook Chapter 13 scenarios that surface adoption/repeal metadata.

## 2025-11-03T04:15Z — Helper rollout and fixture refresh
- Implemented the three helper macros (`tx-publication-parenthetical`, `tx-session-law-citation`, `tx-authority-status-parenthetical`) in `texas-greenbook-15th-edition.csl`, replacing the bespoke `session-law`, `edition-publisher-year`, and TAC parenthetical code while appending the publication helper to statute and rule first-form outputs.
- Ported the same helpers into all TOA variants so each bibliography layout now reuses the shared publication/authority logic instead of duplicating the old `session-law` and TAC strings. Namespaced CSL files mirror the XML introduced in the note style.
- Regenerated all note, parenthetical, and TOA fixtures after the helper integration:
  - `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt --write-expected temp/expected.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt --write-expected temp/expected_parentheticals_notes.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography --write-expected temp/expected_parentheticals_bibliography.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa*.csl --expected temp/expected_toa*.txt --mode bibliography --write-expected temp/expected_toa*.txt` (ran for base, leaders, grouped, grouped-leaders, and by-reporter variants).
- New helper output now surfaces `(Supp. ####)` and agency authority/status clusters in notes and TOA entries per Greenbook chs. 10–13 guidance while keeping short-form cites unchanged.

## 2025-11-03T05:30Z — Register notice cleanup and log capture
- Updated `tx-authority-status-parenthetical` across the note style and all TOA variants to omit duplicate `Tex. Reg.`/`Fed. Reg.` entries when the base citation already prints the register volume and page. This keeps Texas Register contested case notices (Greenbook 15th ed. 83) and Appendix B federal register examples (Table of Authorities samples, Greenbook 15th ed. 247–248) to a single register cite per entry.
- Refreshed the TOA fixtures (`expected_toa*.txt`) so grouped, leaders, by-reporter, and base layouts reflect the streamlined parenthetical output.
- Captured regression artifacts after the update:
  - `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt` → `temp/test-logs/20251103T012201Z_notes.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt` → `temp/test-logs/20251103T012201Z_parentheticals_notes.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography` → `temp/test-logs/20251103T012201Z_parentheticals_bibliography.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped.csl --expected temp/expected_toa_grouped.txt --mode bibliography` → `temp/test-logs/20251103T012201Z_toa_grouped.txt`
