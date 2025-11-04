# Texas Greenbook 15th Edition — Working Notes

Use this file to capture the minimum context required to resume work quickly. Detailed historical research logs are archived in `temp/archive/NOTES-2025-12-21.md`.

## Active research threads
- **Short-form verification:** Rerun `temp/tests_short-form_smoke.json` whenever the restatement macros shift to confirm statutes, TAC rules, federal regulations, attorney general opinions, and municipal ordinances continue to restate their authority text instead of falling back to `Id.`/`See also` (Greenbook 15th ed. 24, 34, 62, 76–78).
- **Upstream packaging:** Keep `temp/PR_DRAFT.md` aligned with the latest regression log names and outstanding checklist items so the PR summary and testing sections remain citation-ready without re-reading historical transcripts.
- **Session stability:** Continue logging every `run_tests.py` invocation (pass and fail) so `temp/test-logs/run-history.log` remains a reliable index when reconstructing prior QA sweeps.

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
- Extended `tx-authority-status-parenthetical` across the note style and all TOA variants to omit duplicate `Tex. Reg.`/`Fed. Reg.` entries when the base citation already prints the register volume and page. The contested-case example (`toa_register_39_tex_reg_573`) previously printed “39 Tex. Reg. 573, 574” followed by a parenthetical that repeated “Tex. Reg.” before the “to be codified” notice, even though Greenbook Chapter 16 shows the register cite only once (Texas Register guidance, Greenbook 15th ed. 83). Appendix B’s federal register sample (pp. 247–248) likewise places the agency/status parenthetical after a single `Fed. Reg.` cite, so the helper now mirrors that layout by dropping the redundant register string before appending the authority/status detail.
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

## 2025-11-03T05:55Z — Regression refresh and TOA baseline alignment
- Discovered the base, leaders, and by-reporter TOA expectations still reflected the pre-heading order (Texas authorities before the federal block). Regenerated `expected_toa.txt`, `expected_toa_leaders.txt`, and `expected_toa_by-reporter.txt` with `python temp/run_tests.py --tests temp/tests_toa.json --style … --expected … --write-expected … --mode bibliography` so all variants share the Appendix B ordering and jurisdiction labels.
- Re-ran the full regression sweep immediately after regenerating the fixtures:
  - `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt`
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography`
  - `python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa.csl --expected temp/expected_toa.txt --mode bibliography`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-leaders.csl --expected temp/expected_toa_leaders.txt --mode bibliography`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped.csl --expected temp/expected_toa_grouped.txt --mode bibliography`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography`
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-by-reporter.csl --expected temp/expected_toa_by-reporter.txt --mode bibliography`
- Archived the green runs under `temp/test-logs/20251103T055217Z_*.txt` and updated `temp/PR_DRAFT.md` to cite the new log bundle in the Summary/Testing sections alongside the follow-up instructions for the upstream PR body.

## 2025-11-03T06:04Z — Helper parity and federal TOA heading verification
- Reconfirmed the shared publication/status helper wiring and federal TOA headings remain stable after the last archived sweep; re-ran the focused regression trio with all expectations passing:
  - `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt` → all 89 rows `OK` (notes helper coverage) (`f03fc9`).
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt` → 10 `OK` results (parenthetical helper usage) (`f6ef44`).
  - `python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography` → 7 `OK` bibliography entries (publication helper) (`35da61`).
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography` → 25 grouped-heading entries `OK`, including federal sections (Appendix B alignment) (`50e0ac`).
  - `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa.csl --expected temp/expected_toa.txt --mode bibliography` → 25 base layout entries `OK` (federal ordering retained) (`078f98`).
- No citeproc warnings surfaced during the sweep; helper macros in the note style and TOA variants remain in sync, so the open backlog items for shared publication/status helpers and federal TOA coverage can be closed after this confirmation run.

## 2025-11-03T09:11Z — Automated run-history logging
- Extended `temp/run_tests.py` to append a summary line to `temp/test-logs/run-history.log` after each invocation. The log captures the UTC timestamp, PASS/FAIL status (based on DIFF counts and length parity), OK/DIFF tallies, resolved command arguments, and primary file paths (`style`, `tests`, `expected`, optional `write_expected`).
- Seeded the ledger with the short-form smoke run executed while testing the hook: `2025-11-03T09:11:44Z | PASS | 12 OK, 0 DIFF | mode=notes; style=temp/texas-greenbook-15th-edition.csl; tests=temp/tests_short-form_smoke.json; expected=temp/expected_short-form_smoke.txt | /root/.pyenv/versions/3.12.10/bin/python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt`.
- Updated `README.md` and `PR_DRAFT.md` to point maintainers to the new log stream so they can prove coverage without hunting through individual suite outputs. Logged the completion of the associated TODO subtasks (support-task automation and documentation hygiene) with timestamps in `temp/TODO.md`.

## 2025-11-03T15:24Z — Short-form restatement pass and log capture
- Implemented the new short-form guardrails in `texas-greenbook-15th-edition.csl` so repeated citations to Texas statutes (Greenbook 15th ed. 24, 34), agency rules and regulations (Greenbook 15th ed. 76–78), and Texas/Federal procedural rules (Greenbook 15th ed. 61–65) now restate the full authority instead of collapsing to `Id.` when the author field is empty.
- Re-ran the full note suite to confirm the guardrails and archived the passing output at `temp/test-logs/20251103T152401Z_notes_full-suite.txt`.
- Command for reference: `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt`.
- Appended the run summary to `temp/test-logs/run-history.log` so the new regression appears alongside earlier short-form smoke investigations.

## 2025-11-03T15:57Z — Short-form smoke verification
- Ran `python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt` and archived the passing output at `temp/test-logs/20251103T155725Z_short-form_smoke.txt`.
- All 12 fixtures returned `OK`, confirming the statute, TAC, and CFR repeats continue to restate their titles and locator strings per Greenbook Chapter 4 (pp. 24, 34) and Chapter 13’s agency guidance (pp. 76–78).
- Verified the command capture in `temp/test-logs/run-history.log`, which now lists the 2025-11-03T15:57:25Z PASS entry for future traceability.

## 2025-11-04T03:34Z — AG opinion and municipal short-form restatement
- Extended `ag-opinion` into position-aware first/short/cross-reference macros so repeat cites restate only the opinion number while the first cite keeps the year parenthetical mandated by Greenbook Chapter 17 (p. 77).
- Applied the same pattern to `municipal-code`, using Greenbook Chapter 13’s municipal ordinance guidance (p. 62) to drop the year parenthetical on repeat cites while allowing cross-references to append any stored `references` strings.
- Expanded `tests_short-form_smoke.json`/`expected_short-form_smoke.txt` with attorney general opinion and municipal ordinance fixtures so the smoke suite now covers the new guardrails.
- Ran the updated smoke suite (`python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt`) and the full notes regression (`python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt`); archived the passing outputs at `temp/test-logs/20251104T033421Z_short-form_smoke.txt` and `temp/test-logs/20251104T033428Z_notes.txt`.

## 2025-12-22T19:30Z — Documentation hygiene and submission checklist pass
- Updated `temp/README.md` recent-update bullets so the regression log references line up with the federal Appendix B sweep and the final 20251103 regression bundle.
- Reworked the “Active research threads” section above to focus on the remaining Chapter 4 short-form guardrails and PR packaging tasks.
- Ran `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt`; all 89 note fixtures returned `OK` with no warnings (see session `386ee1`).
- Next session: finish marking the upstream submission checklist complete and continue the short-form restatement work before drafting the PR body.

