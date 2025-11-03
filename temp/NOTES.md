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

## 2025-11-03T01:44Z — TOA spot check and documentation sync
- Re-ran the four TOA bibliography variants to confirm expectations still match after the helper consolidation; commands logged below with fresh artifacts under `temp/test-logs/`:
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped.csl --expected temp/expected_toa_grouped.txt --mode bibliography` → `temp/test-logs/20251103T014332Z_toa_grouped.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography` → `temp/test-logs/20251103T014338Z_toa_grouped_leaders.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-leaders.csl --expected temp/expected_toa_leaders.txt --mode bibliography` → `temp/test-logs/20251103T014343Z_toa_leaders.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-by-reporter.csl --expected temp/expected_toa_by-reporter.txt --mode bibliography` → `temp/test-logs/20251103T014346Z_toa_by-reporter.txt`
- Updated `temp/PR_DRAFT.md` so the summary highlights the helper rollout, register cite suppression, and Appendix B fixture expansion while pointing at the new log set.
- Refreshed the warning-suppression blurb in `temp/README.md` to document the citeproc metadata keys (`comment`, `label`, `reviewed_title`, `grouping`, `related`) we silence by default and the `PYTHONWARNINGS=default` escape hatch.

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


## 2025-12-22T16:45Z — Appendix B federal coverage inventory
- Re-read Appendix B’s Table of Authorities exemplars to confirm the federal headings and representative citations that must accompany the Texas groupings (Greenbook 15th ed. Appendix B, printed pp. 239–248).
- Cataloged the eight federal headings that must follow the Texas cases in every TOA layout and the representative expectations they introduce:
  1. **United States Supreme Court Cases** — consolidated caption example with multiple parties (p. 239).
  2. **Federal Courts of Appeals Cases** — reporter cite with circuit authority and pinpoint (p. 240).
  3. **Federal District Courts and Specialized Tribunals** — docketed slip opinion pairing a Westlaw cite with a pinpoint (p. 240).
  4. **United States Constitution** — article-and-clause citation with no court/date parenthetical (p. 244).
  5. **United States Code** — title, section, and supplement parenthetical (pp. 245–246).
  6. **Federal Rules** — Federal Rules of Civil Procedure cite that retains subdivision locators (p. 246).
  7. **Code of Federal Regulations** — SEC rule entry with issuing agency parenthetical (pp. 247–248).
  8. **Federal Register** — codification notice capturing both the adopting agency and the “to be codified” note (pp. 247–248).
- Verified that each heading now maps to an explicit fixture in `temp/tests_toa.json`, ensuring the TOA variants can emit the correct labels once the grouped-heading macros are wired up: `toa_case_us_supreme` → “United States Supreme Court Cases”, `toa_case_federal_appellate` → “Federal Courts of Appeals Cases”, `toa_case_federal_district` → “Federal District Courts and Specialized Tribunals”, `toa_constitution_us` → “United States Constitution”, `toa_statute_us_code` → “United States Code”, `toa_rule_federal` → “Federal Rules”, `toa_regulation_cfr` → “Code of Federal Regulations”, and `toa_federal_register_80_fr_56577` → “Federal Register”.
- Follow-up: once the grouped-heading macros emit distinct federal labels, ensure the ordering logic keeps these eight sections contiguous immediately after the Texas authorities block.
- Rebuilt every TOA expectation (`expected_toa*.txt`) and captured passing regression logs for each variant after reordering the fixtures:
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa.csl --expected temp/expected_toa.txt --mode bibliography --write-expected temp/expected_toa.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-leaders.csl --expected temp/expected_toa_leaders.txt --mode bibliography --write-expected temp/expected_toa_leaders.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped.csl --expected temp/expected_toa_grouped.txt --mode bibliography --write-expected temp/expected_toa_grouped.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography --write-expected temp/expected_toa_grouped_leaders.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-by-reporter.csl --expected temp/expected_toa_by-reporter.txt --mode bibliography --write-expected temp/expected_toa_by-reporter.txt`
- Confirmed the refreshed outputs match expectations and archived the verification runs: `temp/test-logs/20251222T1728_toa.txt`, `temp/test-logs/20251222T1729_toa_leaders.txt`, `temp/test-logs/20251222T1730_toa_grouped.txt`, `temp/test-logs/20251222T1730_toa_grouped_leaders.txt`, `temp/test-logs/20251222T1731_toa_by-reporter.txt`.

## 2025-11-03T04:12Z — Regression sweep and chapter coverage audit
- Re-ran the full regression stack after the TOA fixture expansion to confirm nothing drifted before implementing headings:
  - `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography`
  - `python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa*.csl --expected temp/expected_toa*.txt --mode bibliography`
- Logged the renders under `temp/test-logs/20251103T041142Z_*.txt`; notes, parentheticals (note & bibliography), and every TOA variant matched expectations, while the short-form smoke suite still flags the planned `Id.`/`See also` guardrail fixes for statutes, TAC rules, and CFR entries.
- Chapter coverage snapshot (cite pages reference the Greenbook 15th ed. PDF in `temp/Greenbook_15thEdition.pdf`):
  - **Chapter 2 — Cases (pp. 2–5, 17, 24–36, 51, 94–100).** `legal-case`, `court-and-date`, and `cross-reference-cue` outputs in `tests.json` rows 1–24, 78–85 ensure the first-form case rules, prior/subsequent history, memorandum opinions, and `See`/`See also` cues track the examples on pp. 2–5 and the cross-reference discussion on p. 100.
  - **Chapter 4 — Short-form citations (pp. 4, 24, 34).** The `tex-short-form-base` logic plus the short-form smoke fixture exercise the `Id.` v. restatement guidance for statutes, regulations, and secondary sources; the remaining diffs align with the TODO item to restate statutory text instead of emitting `Id.` when Chapter 4 (pp. 24, 34) calls for a full repeat.
  - **Chapter 10 — Statutes (pp. 45–52).** `tx-publication-parenthetical` and `tex-statute-first` handle supplements, session-law parentheticals, and Gammel cites as demonstrated by fixture rows 66–70 in `tests.json`, matching the Chapter 10 instructions on pp. 45–52.
  - **Chapter 17 — Secondary authorities (pp. 76–78).** Treatise, CLE, periodical, and unpublished document entries (rows 67–77) confirm the consolidated publication helper prints edition, publisher, place, and year details per Chapter 17’s requirements.
- Next steps: add TOA group headings using the stored `grouping` metadata and revisit the short-form guardrails before freezing expectations.

