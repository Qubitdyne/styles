# Texas Greenbook CSL Working README

This workspace tracks the in-progress Citation Style Language (CSL) implementation for the *Texas Greenbook, 15th Edition*. Keep day-to-day notes lean and defer to the archive when you need historical detail so active sessions stay within context limits.

## Current objective
- Finish and document the Texas-specific CSL styles (`texas-greenbook-15th-edition.csl` and the TOA variants) so they are ready to propose to the upstream `citation-style-language/styles` repository.
- Align every change with the Greenbook PDF stored at `temp/Greenbook_15thEdition.pdf` and record supporting page citations in `temp/NOTES.md` when new rules are implemented.

## Recent updates
- **2025-11-03** — Register parenthetical cleanup: shared `tx-authority-status-parenthetical` logic now suppresses duplicate register cites in TOA layouts, matching the Texas Register guidance in Chapter 16 (Greenbook 15th ed. 83) and the Appendix B federal examples (pp. 247–248). Regression logs capturing the refreshed note, parenthetical, and TOA suites live at `temp/test-logs/20251103T012201Z_*.txt`.

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

## Running the regression suites
Run tests from the repository root unless noted otherwise.

```bash
python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt
python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt
python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt
```

Use `--mode bibliography` when you need to force bibliography output or `--write-expected` to refresh expectations after intentional updates. The harness suppresses the routine citeproc warnings by default.

## Archives and reference material
- A complete PDF of the Greenbook is at `temp/Greenbook_15thEdition.pdf`; supplemental manuals live alongside it.
- The original, verbose README, TODO, and NOTES are stored in `temp/archive/` (see filenames with the `2025-12-21` suffix). Consult them for deep dives, but avoid bringing their entire contents back into the active files unless the information is still current.
- Additional research matrices (`authority-note-matrix.md`, terminology inventories, regression logs) remain in place; prune or archive them if they become stale.
