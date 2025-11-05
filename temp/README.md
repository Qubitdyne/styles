# Texas Greenbook CSL Working README

This workspace tracks the in-progress Citation Style Language (CSL) implementation for the *Texas Greenbook, 15th Edition*. Keep day-to-day notes lean and defer to the archive when you need historical detail so active sessions stay within context limits.

## Current objective
- Finish and document the Texas-specific CSL styles (`texas-greenbook-15th-edition.csl` and the TOA variants) so they are ready to propose to the upstream `citation-style-language/styles` repository.
- Align every change with the Greenbook PDF stored at `temp/Greenbook_15thEdition.pdf` and record supporting page citations in `temp/NOTES.md` when new rules are implemented.

## Recent updates
- **2026-01-18** — Completed the release metadata audit by refreshing `<updated>` timestamps on the main note style and every TOA variant, corrected each TOA file’s `rel="self"` link so the IDs match the published filenames ahead of the upstream submission, and inlined the custom locale terms directly into the styles to match upstream packaging.【F:temp/texas-greenbook-15th-edition.csl†L5-L18】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L5-L16】【F:temp/texas-greenbook-15th-edition.csl†L28-L212】
- **2026-01-17** — Added position-aware Texas Constitution macros (`tex-constitution-first`, `tex-constitution-short`, `tex-constitution-cross-reference`) so repeats restate the full article and section text instead of collapsing to `Id.` while cross references append additional provisions. Expanded the regression fixtures and smoke suite to cover locator overrides and cross-reference strings, then captured passing runs at `temp/test-logs/20251104T183550Z_notes_constitution.txt` and `temp/test-logs/20251104T183557Z_short-form_constitution.txt` (Greenbook 15th ed. 39).【F:temp/texas-greenbook-15th-edition.csl†L772-L835】【F:temp/tests.json†L474-L494】【F:temp/tests_short-form_smoke.json†L33-L42】
- **2026-01-16** — Introduced dedicated session law first/short/cross-reference macros so repeat cites restate the act string while cross references append codification text per Greenbook ch. 11 (pp. 53–56). Expanded the note and smoke fixtures with repeat and cross-reference coverage, then confirmed clean renders at `temp/test-logs/20251104T180708Z_notes.txt` and `temp/test-logs/20251104T180721Z_short-form_smoke.txt`.
- **2025-12-22** — Appendix B federal coverage verified: restored the federal headings and exemplars in `tests_toa.json`, regenerated every TOA expectation with `--mode bibliography`, and captured the passing renders at `temp/test-logs/20251222T1728_toa.txt`, `temp/test-logs/20251222T1729_toa_leaders.txt`, `temp/test-logs/20251222T1730_toa_grouped.txt`, `temp/test-logs/20251222T1730_toa_grouped_leaders.txt`, and `temp/test-logs/20251222T1731_toa_by-reporter.txt`. Documentation and fixtures now reflect the mixed Texas/federal ordering on Greenbook Appendix B pp. 239–248.
- **2025-11-05** — Refreshed the run-history ledger by rerunning the notes, parenthetical (note and bibliography), short-form smoke, and every TOA layout; archived the outputs under the `temp/test-logs/20251105T0157*.txt` bundle and confirmed the PASS entries recorded at 2025-11-05T01:57Z in `temp/test-logs/run-history.log`, keeping the short-form and TOA guardrails aligned with the Greenbook-driven macros documented in the styles.【011517†L1-L12】【c77cbe†L31-L75】【F:temp/texas-greenbook-15th-edition.csl†L705-L825】【F:temp/texas-greenbook-15th-toa.csl†L767-L819】
- **2025-11-04** — Refreshed the Jenkins parenthetical fixture so the short form now restates the case instead of emitting `Id. at 2.` in line with Greenbook Chapter 4 (p. 34) and Chapter 9 (p. 39). Archived the before/after expectations at `temp/test-logs/20251104T190629Z_expected_parentheticals_notes_pre-refresh.txt` and `temp/test-logs/20251104T190640Z_expected_parentheticals_notes_post-refresh.txt`, captured the regeneration diff at `temp/test-logs/20251104T190629Z_parentheticals_notes_refresh.txt`, confirmed the clean rerun at `temp/test-logs/20251104T190640Z_parentheticals_notes_post-refresh.txt`, and stored the bibliography snapshots/logs at `temp/test-logs/20251104T190657Z_expected_parentheticals_bibliography_pre-refresh.txt`, `temp/test-logs/20251104T190658Z_expected_parentheticals_bibliography_post-refresh.txt`, and `temp/test-logs/20251104T190657Z_parentheticals_bibliography_post-refresh.txt`.
- **2025-11-04** — Extended the short-form restatement guardrails to attorney general opinions (Greenbook 15th ed. 77) and municipal ordinances (Greenbook 15th ed. 62). Updated `texas-greenbook-15th-edition.csl` so repeat cites drop the year parenthetical while cross-references append `references`, refreshed the smoke fixtures, and logged the passing runs at `temp/test-logs/20251104T033421Z_short-form_smoke.txt` and `temp/test-logs/20251104T033428Z_notes.txt`.
- **2025-11-03** — Short-form restatement guardrails: adjusted the short-form layout in `texas-greenbook-15th-edition.csl` so repeated Texas statutes (Greenbook 15th ed. 24, 34), administrative rules (Greenbook 15th ed. 76–78), and Texas/Federal procedural rules (Greenbook 15th ed. 61–65) restate their full authority text instead of collapsing to `Id.`. Confirmed the behavior with the full note suite (`temp/test-logs/20251103T152401Z_notes_full-suite.txt`) and a fresh short-form smoke run (`temp/test-logs/20251103T155725Z_short-form_smoke.txt`).
- **2025-11-03** — Register parenthetical cleanup: shared `tx-authority-status-parenthetical` logic now suppresses duplicate register cites in TOA layouts, matching the Texas Register guidance in Chapter 16 (Greenbook 15th ed. 83) and the Appendix B federal examples (pp. 247–248). Regression logs capturing the refreshed note, parenthetical, and TOA suites live at `temp/test-logs/20251103T012201Z_*.txt`.
- **2025-11-03** — Full regression sweep ahead of TOA heading work: reran notes, parenthetical, short-form smoke, and every TOA bibliography variant; archived outputs under `temp/test-logs/20251103T055217Z_*.txt` with no diffs. Short-form smoke diffs still highlight the Chapter 4 guardrail TODO for repeating statutory and regulatory text instead of emitting `Id.`/`See also`.

## Where things live
| Path | Purpose |
| --- | --- |
| `texas-greenbook-15th-edition.csl` | Primary note/bibliography style under active development. |
| `texas-greenbook-15th-toa*.csl` | Table of Authorities layouts that must stay in sync with the main style macros. |
| `tests*.json`, `expected*.txt` | Citeproc regression fixtures (notes, secondary sources, TOA, diagnostics). |
| `run_tests.py` | Lightweight harness for executing the regression suites. |
| `locales/` | Locale overrides specific to the Greenbook effort. |
| `archive/` | Historical drafts, full backlogs, and the pre-cleanup documentation copies. |

## How to work
1. Start with `temp/TODO.md` for the active checklist. Completed work and exhaustive history live in `temp/archive/TODO-history-2025-12-21.md` if you need background.
2. Record new decisions, open questions, and page citations in the trimmed `temp/NOTES.md`. Spillover detail can go into a dated file under `temp/archive/`.
3. Update `temp/PR_DRAFT.md` whenever a change meaningfully affects the upstream submission story.

## Input mapping cheat-sheet
| Scenario | CSL fields | Greenbook reference |
| --- | --- | --- |
| Prefatory signals | `annote` to override; otherwise the style prints “See” by default and capitalizes `note` when present | Chapter 4, pp. 24–39【F:temp/texas-greenbook-15th-edition.csl†L42-L65】【F:temp/Greenbook_15thEdition.pdf†L120-L175】 |
| Explanatory parenthetical | `abstract` (stored verbatim inside parentheses) | Chapter 4, pp. 36–38【F:temp/texas-greenbook-15th-edition.csl†L170-L190】【F:temp/Greenbook_15thEdition.pdf†L150-L175】 |
| Procedural history / writ status | `status` for structured history, `note` for free-form supplements | Chapter 9, pp. 39–41【F:temp/texas-greenbook-15th-edition.csl†L141-L167】【F:temp/Greenbook_15thEdition.pdf†L176-L210】 |
| Docket numbers & slip opinions | `number` and `collection-number` (Westlaw/Lexis strings) | Chapter 4, pp. 30–33【F:temp/texas-greenbook-15th-edition.csl†L90-L118】【F:temp/Greenbook_15thEdition.pdf†L140-L165】 |
| Petition/writ history | Append to `status`; suppress duplicates through `references` | Chapter 4, pp. 34–35【F:temp/texas-greenbook-15th-edition.csl†L141-L163】【F:temp/Greenbook_15thEdition.pdf†L166-L175】 |
| Authority weight parenthetical | `references` for subsequent history or cross-references | Chapter 4, Appendix B, pp. 24–39, 239–248【F:temp/texas-greenbook-15th-edition.csl†L141-L210】【F:temp/Greenbook_15thEdition.pdf†L120-L175】【F:temp/Greenbook_15thEdition.pdf†L612-L676】 |

Signals, explanatory notes, and petition history travel with the note-style layouts as well as the Table of Authorities variants so the JSON fixtures stay faithful to *Texas Greenbook* examples.

## Running the regression suites
Run tests from the repository root unless noted otherwise.

```bash
python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt
python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt
python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt
python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa.csl --expected temp/expected_toa.txt --mode bibliography
python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-by-reporter.csl --expected temp/expected_toa_by-reporter.txt --mode bibliography
```

Every invocation now appends a one-line summary to `temp/test-logs/run-history.log` with the UTC timestamp, PASS/FAIL status, OK/DIFF counts, and the exact command that was executed. Use this file as the authoritative session trail when reconciling documentation or preparing the upstream PR; the per-suite log files under `temp/test-logs/` remain available for deeper diffs when expectations intentionally change.

Use `--mode bibliography` when you need to force bibliography output or `--write-expected` to refresh expectations after intentional updates. The runner filters citeproc’s harmless "unsupported argument" warnings for the metadata keys we intentionally keep (`comment`, `label`, `reviewed_title`, `grouping`, `related`) so log files stay readable; export `PYTHONWARNINGS=default` if you need to audit the raw warning stream.

## Archives and reference material
- A complete PDF of the Greenbook is at `temp/Greenbook_15thEdition.pdf`; supplemental manuals live alongside it.
- The original, verbose README, TODO, and NOTES are stored in `temp/archive/` (see filenames with the `2025-12-21` suffix). Consult them for deep dives, but avoid bringing their entire contents back into the active files unless the information is still current.
- Additional research matrices (`authority-note-matrix.md`, terminology inventories, regression logs) remain in place; prune or archive them if they become stale.

## Table of Authorities usage notes
- **Headings.** Populate `call-number` with the major TOA heading (e.g., “Cases”) and `reviewed-title` with any subsection label. The grouped styles read those fields to emit the multi-level headings used in Appendix B (pp. 239–248).【F:temp/texas-greenbook-15th-toa-grouped.csl†L330-L352】【F:temp/Greenbook_15thEdition.pdf†L612-L676】
- **Document page references.** Store the document’s page numbers in `page-first` as a comma-separated list. All TOA variants now route that field to a `right-inline` block, giving word processors a consistent tab stop for dotted leaders (Greenbook Appendix B).【F:temp/texas-greenbook-15th-toa.csl†L782-L803】【F:temp/tests_toa.json†L1-L200】【F:temp/Greenbook_15thEdition.pdf†L612-L676】
- **Reporter sorting.** The by-reporter variant sorts by reporter abbreviation, volume, and first page before falling back to court/authority so mixed Texas and federal reporters match the Appendix B ordering.【F:temp/texas-greenbook-15th-toa-by-reporter.csl†L730-L760】
- **Leaders and alignment.** Leader styles now rely on CSL’s `left-margin`/`right-inline` layout instead of literal tab characters, which keeps alignment intact across processors while still allowing office software to supply dotted leaders per Section 4.4 guidance.【F:temp/texas-greenbook-15th-toa-leaders.csl†L744-L773】【F:temp/Greenbook_15thEdition.pdf†L140-L165】

When preparing TOA fixtures, keep reporter pinpoint cites (`locator`) inside the core citation macros and dedicate `page-first` to the brief’s TOA pagination. This separation mirrors the Greenbook’s examples and avoids intermixing reporter pages with document references.
