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

- **Statute and rule short forms:** Cross-reference and id. logic for statutes, rules, and administrative materials remains incomplete; see flagged tests in `expected.txt` for desired output.【F:temp/NOTES.md†L172-L189】【F:temp/expected.txt†L150-L214】 (Greenbook Ch. 10–13, pp. 42–65)【F:temp/Greenbook_15thEdition.pdf†L170-L250】
- **Federal authorities:** TOA fixtures lack federal examples; future updates should add them once macros support multi-jurisdiction sorting.【F:temp/NOTES.md†L194-L205】 (Greenbook Appendix B, pp. 239–252)【F:temp/Greenbook_15thEdition.pdf†L612-L676】
- **Web citation pin cites:** Chapter 16 web examples use ligature-heavy scans; confirm precise quotation punctuation after OCR cleanup.【F:temp/NOTES.md†L189-L193】 (Greenbook Ch. 16, pp. 76–84)【F:temp/Greenbook_15thEdition.pdf†L274-L318】

### Assumptions, Deviations, and Unresolved Questions

1. **Locale overrides consolidated via shared custom locale (assumption):** The drafts assume a future shared locale file to house abbreviations like “art.” and “ch.” to avoid duplication.【F:temp/NOTES.md†L209-L236】 (Greenbook Appendix A abbreviations, pp. 215–238)【F:temp/Greenbook_15thEdition.pdf†L560-L611】
2. **Petition history punctuation (deviation):** The edition style renders petition history separated by commas instead of semicolons to match Greenbook examples (e.g., `pet. denied`).【F:temp/texas-greenbook-15th-edition.csl†L236-L296】 (Greenbook Ch. 4, pp. 14–27)【F:temp/Greenbook_15thEdition.pdf†L40-L92】
3. **Unpublished memorandum opinions (question):** The Greenbook allows `mem. op.` parentheticals but the PDF is unclear about italicization in slip opinions; confirm formatting from pp. 24–25 before finalizing the macro styling.【F:temp/texas-greenbook-15th-edition.csl†L208-L259】 (Greenbook Ch. 4, pp. 24–25)【F:temp/Greenbook_15thEdition.pdf†L70-L78】

## Running the Test Suites

1. **Install citeproc test dependencies** (once per environment): refer to `temp/run_tests.py` for required Python packages (primarily `citeproc-py`).
2. **Run the core note/bibliography suite:**
   ```bash
   python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt
   ```
   The script compares generated citations with `expected.txt` (general authorities) and `expected_secondary.txt` (secondary sources) for regression checking.【F:temp/run_tests.py†L1-L186】【F:temp/tests.json†L1-L166】
3. **Run the Table of Authorities suite:**
   ```bash
   python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt
   ```
   Alternate TOA styles can be tested by swapping the `--style` and `--expected` paths (see `expected_toa.txt`, `expected_toa_grouped.txt`, `expected_toa_leaders.txt`).【F:temp/tests_toa.json†L1-L200】
4. **Update fixtures:** Use the `--write-expected` flag to regenerate expected outputs after intentional changes; review diffs to ensure alignment with Greenbook requirements before committing.【F:temp/run_tests.py†L75-L114】

## Maintenance & Extension Guidance

- **Abbreviations and locales:** Centralize Greenbook-specific term overrides (e.g., `rule`, `chapter`, `paragraph`) in a dedicated locale file and include it across styles to prevent drift.【F:temp/NOTES.md†L209-L236】
- **New authority types:** Add fixtures to `tests.json`/`tests_toa.json` before implementing macros so expectations remain test-driven; cite the controlling Greenbook pages in inline comments when adding new test cases.【F:temp/tests.json†L1-L166】【F:temp/tests_toa.json†L1-L200】
- **Macro evolution:** Follow the dispatcher diagram in `NOTES.md` when adding new citation branches to keep note and bibliography routing aligned.【F:temp/NOTES.md†L101-L170】
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
