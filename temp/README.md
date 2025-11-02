# Texas Greenbook CSL Working README

This document summarizes the scope, capabilities, and maintenance guidance for the in-progress Citation Style Language (CSL) implementation of the *Texas Greenbook, 15th Edition*. Treat the resources listed here as the authoritative context when updating the CSL files in this directory. The canonical working style is `texas-greenbook-15th-edition.csl`; legacy drafts now live in `temp/archive/` for historical reference only.

## Scope of the Texas Greenbook CSL

- **Coverage:** The edition style (`texas-greenbook-15th-edition.csl`) automates Greenbook-compliant citations for Texas primary authorities (Supreme Court, Court of Criminal Appeals, intermediate courts, Commission of Appeals, trial courts, original proceedings) and secondary materials (constitution, statutes, session laws, administrative code/register, Attorney General opinions, bar publications, books, journals, web sources).【F:temp/texas-greenbook-15th-edition.csl†L1-L32】【F:temp/NOTES.md†L35-L137】
- **Citation modes:** Note/bibliography output and Table of Authorities (TOA) variants are maintained in parallel. The TOA-specific styles (`texas-greenbook-15th-toa*.csl`) share macros with the main note style while adding grouped headings and dotted leaders for Greenbook Chapter 20 compliance.【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L1-L52】【F:temp/expected_toa_grouped_leaders.txt†L1-L28】
- **Signals and parentheticals:** Italicized signals and parenthetical weights follow Chapters 1 and 2 guidance, including memo opinion indicators and petition history phrases.【F:temp/texas-greenbook-15th-edition.csl†L297-L357】【F:temp/Greenbook_15thEdition.pdf†L30-L55】

### File Inventory

| Location | Purpose |
| --- | --- |
| `texas-greenbook-15th-edition.csl` | Canonical note/bibliography style used for active development and regression testing. |
| `texas-greenbook-15th-toa*.csl` | Table of Authorities variants aligned with the edition macros. |
| `archive/` | Legacy drafts (`draft0`–`draft3`) retained only for historical reference. |
| `tests*.json`, `expected*.txt` | Citeproc regression fixtures for notes, secondary materials, and TOA outputs. |
| `tests_parentheticals.json`, `expected_parentheticals_notes.txt`, `expected_parentheticals_bibliography.txt` | Focused fixtures validating slip-opinion URLs and mandamus history ordering in both note and bibliography contexts. |
| `NOTES.md`, `TODO.md` | Research trail, design decisions, and prioritized implementation backlog. |

## Supported Citation Types

| Authority Class | Implemented Features | Greenbook Reference |
| --- | --- | --- |
| Texas appellate cases | First, short, and cross-reference forms with reporter vs. Westlaw branching, petition history, and memo opinion parentheticals.【F:temp/texas-greenbook-15th-edition.csl†L180-L296】 | Ch. 2 (pp. 7–9) & Ch. 4 (pp. 14–27)【F:temp/Greenbook_15thEdition.pdf†L16-L92】 |
| Original proceedings (mandamus, habeas) | Cause number cues, “slip op.” locators, and relief parentheticals.【F:temp/texas-greenbook-15th-edition.csl†L358-L417】 | Ch. 6 (pp. 31–33)【F:temp/Greenbook_15thEdition.pdf†L118-L134】 |
| Constitution & statutes | Article/section macros, code abbreviations, session law handling with chapter and section granularity.【F:temp/texas-greenbook-15th-edition.csl†L418-L545】 | Ch. 9–11 (pp. 39–56)【F:temp/Greenbook_15thEdition.pdf†L150-L212】 |
| Rules & administrative sources | Court rule and agency code/register macros, including section symbols and parenthetical authority identifiers.【F:temp/texas-greenbook-15th-edition.csl†L546-L673】 | Ch. 13 & 16 (pp. 61–84)【F:temp/Greenbook_15thEdition.pdf†L232-L318】 |
| Attorney General opinions & advisory materials | Opinion number formatting, issuing authority abbreviations, and issuance dates.【F:temp/texas-greenbook-15th-edition.csl†L674-L758】 | Ch. 15–17 (pp. 73–91)【F:temp/Greenbook_15thEdition.pdf†L286-L356】 |
| Secondary sources | Books, chapters, journals, CLE materials, and online resources share CSL macros for editors, pinpoint references, and accessed dates.【F:temp/texas-greenbook-15th-edition.csl†L759-L987】 | Ch. 18–19 (pp. 93–96)【F:temp/Greenbook_15thEdition.pdf†L360-L392】 |
| Table of Authorities | Grouped headings (e.g., “Cases,” “Constitution”), dotted leader alignment, and grouped-leader variants for multipage indexes.【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L53-L212】 | Appendix B TOA guidance (pp. 239–252)【F:temp/Greenbook_15thEdition.pdf†L612-L676】 |

## Known Limitations & Open Items

- **Statute and rule short forms:** Dedicated short-form macros are still pending, but the citation layout now guards `Id.` so code titles with `collection-title` or `chapter-number` metadata repeat the full cite instead of emitting `Id.`; remaining gaps are tracked in `TODO.md` and illustrated in `expected.txt`.【F:temp/texas-greenbook-15th-edition.csl†L1108-L1136】【F:temp/tests.json†L386-L409】【F:temp/expected.txt†L27-L35】【F:temp/TODO.md†L140-L158】【F:temp/Greenbook_15thEdition.pdf†L170-L250】
- **Federal authorities:** TOA fixtures lack federal examples; future updates should add them once macros support multi-jurisdiction sorting.【F:temp/NOTES.md†L194-L205】 (Greenbook Appendix B, pp. 239–252)【F:temp/Greenbook_15thEdition.pdf†L612-L676】

### Assumptions, Deviations, and Unresolved Questions

1. **Locale overrides consolidated via shared custom locale (assumption):** The drafts assume a future shared locale file to house abbreviations like “art.” and “ch.” to avoid duplication.【F:temp/NOTES.md†L209-L236】 (Greenbook Appendix A abbreviations, pp. 215–238)【F:temp/Greenbook_15thEdition.pdf†L560-L611】
2. **Petition history punctuation (deviation):** The edition style renders petition history separated by commas instead of semicolons to match Greenbook examples (e.g., `pet. denied`).【F:temp/texas-greenbook-15th-edition.csl†L236-L296】 (Greenbook Ch. 4, pp. 14–27)【F:temp/Greenbook_15thEdition.pdf†L40-L92】
3. **Unpublished memorandum opinions (resolved):** Chapter 4 examples confirm that `(mem. op.)` parentheticals remain in roman type; the `weight-parentheticals` macro now enforces `font-style="normal"` so slip-opinion parentheticals do not inherit italics from surrounding context.【F:temp/NOTES.md†L410-L430】【F:temp/texas-greenbook-15th-edition.csl†L143-L155】 (Greenbook Ch. 4, pp. 14–15 / PDF p. 32)【F:temp/test-logs/2025-03-17_memo-opinion.txt†L20-L39】

## Running the Test Suites

1. **Install citeproc test dependencies** (once per environment): run `pip install -r temp/requirements.txt` to install the minimal dependency set. The harness now checks for `citeproc` explicitly and exits with an actionable hint ("Missing required dependency 'citeproc'. Install it with 'pip install -r temp/requirements.txt' or 'pip install citeproc-py'.") if the library is missing.【F:temp/run_tests.py†L1-L46】
   - The runner suppresses citeproc's benign `UserWarning` messages about unsupported metadata keys (`comment`, `label`, `reviewed_title`, `grouping`, `related`) so regression logs stay readable. Set `PYTHONWARNINGS=default` when invoking `run_tests.py` if you need to audit the raw warning stream.【F:temp/run_tests.py†L1-L61】
2. **Run the core note/bibliography suite:**
   ```bash
   python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt
   ```
   The script compares generated citations with `expected.txt` (general authorities) and `expected_secondary.txt` (secondary sources) for regression checking.【F:temp/run_tests.py†L1-L186】【F:temp/tests.json†L1-L166】
3. **Run the Table of Authorities suite:** the harness automatically switches to bibliography mode when the style path contains `toa`, so the explicit flag is optional for standard TOA filenames.
   ```bash
   python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt
   ```
   Alternate TOA styles can be tested by swapping the `--style` and `--expected` paths (see `expected_toa.txt`, `expected_toa_grouped.txt`, `expected_toa_leaders.txt`, `expected_toa_by-reporter.txt`). Pass `--mode` explicitly if you are experimenting with nonstandard filenames or want to override the auto-detection behavior.【F:temp/tests_toa.json†L1-L200】
4. **Exercise the parenthetical subset in both contexts:** the dedicated fixtures mirror the slip-opinion and mandamus examples from `tests.json` while running quickly for focused regression checks.
   ```bash
   python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt
   python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography
   ```
   Use these runs to confirm `available at` ordering and petition-history chains stay synchronized across note and bibliography outputs after citation logic changes.
4. **Update fixtures:** Use the `--write-expected` flag to regenerate expected outputs after intentional changes; review diffs to ensure alignment with Greenbook requirements before committing.【F:temp/run_tests.py†L75-L114】
5. **Reproduce historical locator issues (optional):** The diagnostic pair `tests_locator_symbol.json` / `expected_locator_symbol.txt` exercises the non-page locator pathways that previously crashed when citeproc lacked a symbol-form term. Run them to confirm fallback behavior before altering locator macros.【F:temp/tests_locator_symbol.json†L1-L16】【F:temp/expected_locator_symbol.txt†L1-L1】

## Maintenance & Extension Guidance

- **Abbreviations and locales:** Centralize Greenbook-specific term overrides (e.g., `rule`, `chapter`, `paragraph`) in a dedicated locale file and include it across styles to prevent drift.【F:temp/NOTES.md†L209-L236】
- **Statute/rule terminology inventory:** Appendix H code and rule abbreviations plus conditional usage notes (e.g., `art.` vs. `arts.`, auxiliary-law brackets) are summarized in `NOTES.md` (2025-12-05) to guide the upcoming publication/status helper work.【F:temp/NOTES.md†L1225-L1294】
- **New authority types:** Add fixtures to `tests.json`/`tests_toa.json` before implementing macros so expectations remain test-driven; cite the controlling Greenbook pages in inline comments when adding new test cases.【F:temp/tests.json†L1-L166】【F:temp/tests_toa.json†L1-L200】
- **Macro evolution:** Follow the dispatcher diagram in `NOTES.md` when adding new citation branches to keep note and bibliography routing aligned.【F:temp/NOTES.md†L101-L170】
- **Web citation coverage:** Chapter 16 web fixtures now exercise undated press releases, quoted blog titles, and standalone PDF downloads; regenerate both `expected.txt` and `expected_secondary.txt` when touching related macros to keep punctuation aligned with pp. 76–77.【F:temp/tests.json†L594-L655】【F:temp/expected_secondary.txt†L5-L15】【F:temp/Greenbook_15thEdition.pdf†L452-L479】
- **Versioning:** Use `temp/archive/` to store experimental drafts if a major rewrite is required; promote the result back into `texas-greenbook-15th-edition.csl` only after regression tests and documentation are updated, per `AGENTS.md` guidance.【F:temp/AGENTS.md†L8-L16】
- **Change management guardrails:**
  1. Update `texas-greenbook-15th-edition.csl` and rerun both note and TOA test suites before committing.
  2. Mirror substantive logic updates into TOA variants or document deferred work in `TODO.md`.
  3. Record rationale, source citations, and outstanding questions in `NOTES.md` immediately to prevent drift.
  4. Summarize directory changes (new tests, archived drafts) in this README so future reviewers can trace file movements.
- **Documentation:** Record new assumptions or outstanding questions in `NOTES.md` with Greenbook page citations to maintain traceability for future reviewers.【F:temp/NOTES.md†L1-L31】

## Key Source Materials

- *Texas Greenbook, 15th Edition* (primary authoritative rules).【F:temp/Greenbook_15thEdition.pdf†L1-L676】
- CSL 1.0.2 Specification (for element and attribute behavior).【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1-L40】
- Texas Rules of Appellate, Civil, and Evidence procedure PDFs for rule abbreviation verification.【F:temp/texas-rules-of-appellate-procedure.pdf†L1-L10】【F:temp/texas-rules-of-civil-procedure-august-31-2025.pdf†L1-L12】【F:temp/texas-rules-of-evidence-effective-912025.pdf†L1-L12】
- Supplemental references: *Uniform Format Manual* and Texas court rulemaking background materials for historical cross-checks.【F:temp/Uniform-Format-Manual-07012010.pdf†L1-L12】【F:temp/How-Court-Rules-Are-Made.pdf†L1-L10】【F:temp/texas-court-rules-history-process.html†L1-L12】

For further context, review `NOTES.md` and `TODO.md` for prioritized follow-ups and research trails.
