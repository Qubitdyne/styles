# Texas Greenbook 15th Edition CSL Development TODO

## Completed Work
- [x] **Familiarized with source material.** Cataloged rule coverage, appendices, and page citations from the Greenbook PDF and logged them in `NOTES.md` for traceability.
- [x] **Surveyed existing CSL styles.** Reviewed Bluebook-derived and legal-dependent templates, noting reusable macros and locale patterns in `NOTES.md`.
- [x] **Defined citation requirements.** Produced the citation requirement matrix with mandatory variables, abbreviations, and Greenbook page references.
- [x] **Designed style architecture.** Established the macro routing now preserved in `texas-greenbook-15th-edition.csl` and its Table of Authorities variants.
- [x] **Drafted primary CSL files.** Authored legacy drafts (`draft0`–`draft3`, now archived) along with TOA counterparts covering primary authorities.
- [x] **Implemented secondary source rules.** Completed book-, journal-, CLE-, and web-specific macros shared between citation and bibliography outputs.
- [x] **Created regression fixtures.** Added `tests.json`, `tests_toa.json`, and matching `expected*.txt` files for authorities and TOA scenarios.
- [x] **Prepared working documentation.** Wrote the `README.md` overview, expanded research `NOTES.md`, and tracked assumptions and deviations.

## Active Development
### Citation Logic Gaps
- [ ] **Complete statute and rule short-form logic.** Implement cross-reference and `Id.` handling for statutes, rules, and administrative materials, then update `expected.txt` fixtures. (See `README.md` Known Limitations and `NOTES.md` helper sketches.)
  - [ ] Audit the existing statute, rule, and administrative `*_short` macros in `texas-greenbook-15th-edition.csl` to catalog current branching and pinpoint missing reuse hooks documented in `NOTES.md`.
  - [ ] Outline Greenbook Chapter 10–13 short-form triggers (sections, chapters, and rule ranges) with page citations in `NOTES.md` to confirm requirements and edge cases.
  - [ ] Extend `tests.json` with statute, rule, and administrative cross-reference scenarios that cover `Id.`, short-form without `Id.`, and cross-volume citations.
  - [ ] Implement the shared short-form logic (including `substitute` fallbacks) within the style macros and mirror the changes into each TOA variant where applicable.
  - [ ] Regenerate `expected.txt` (and any affected TOA fixtures) with `run_tests.py --write-expected`, manually verify outputs against the Greenbook PDF, and document remaining discrepancies in `NOTES.md` if any.
- [ ] **Finish explanatory parentheticals.** Add shared helpers for slip-opinion pinpoints, procedural parentheticals, and docket metadata so case and mandamus citations emit relief/status consistently before promoting the next edition revision.
  - [ ] Compile the list of required explanatory parentheticals (slip opinion, procedural posture, relief granted, docket disposition) with page references from Chapters 2, 4, and 6 in `NOTES.md`.
  - [ ] Review existing macros handling parentheticals to identify duplicated logic between case notes and TOA outputs.
  - [ ] Design shared helper macros (e.g., `parenthetical-slip-op`, `parenthetical-procedural-status`, `parenthetical-docket`) that can be reused by case, mandamus, and habeas branches.
  - [ ] Add targeted fixtures in `tests.json` and `expected.txt` for each parenthetical scenario, including combinations with petition history.
  - [ ] Implement the helpers, adjust macro routing for both note and TOA styles, and confirm citeproc output matches the Greenbook examples before finalizing documentation updates.
- [ ] **Build shared publication/status helpers.** Create reusable macros for statutory publication parentheticals, session-law metadata, and administrative status notes to reduce duplication across code, rule, and agency citations.
  - [ ] Inventory where publication/status text is currently hard-coded across statute, session law, and administrative macros (main and TOA styles).
  - [ ] Extract common terminology requirements from Chapters 10–13 and Appendix A of the Greenbook, logging authoritative abbreviations in `NOTES.md`.
  - [ ] Draft shared helper macros (e.g., `publication-parenthetical`, `session-law-metadata`, `administrative-status`) with parameters for date/session ranges and adoption/recodification notes.
  - [ ] Update style code to call the new helpers in all relevant branches, ensuring no duplication remains and TOA variants reference the same logic.
  - [ ] Expand tests to include examples of session laws, codified statutes with publication notes, and administrative actions, then regenerate fixtures and document verification steps.

### Testing & Coverage
- [ ] **Expand Table of Authorities fixtures.** Introduce federal authorities and additional jurisdictional groupings to `tests_toa.json` and `expected_toa_*.txt` once the macro support exists.
  - [ ] Map the federal authority categories and grouping labels required by Appendix B, citing page numbers in `NOTES.md` for traceability.
  - [ ] Determine the minimal set of sample citations (cases, statutes, administrative materials) needed to exercise each new grouping and leader combination.
  - [ ] Add the new authorities to `tests_toa.json`, including jurisdiction metadata necessary for correct sorting and grouping.
  - [ ] Update each `expected_toa*.txt` fixture to reflect the new authorities, running the TOA-specific styles to confirm alignment.
  - [ ] Record any TOA macro adjustments or uncovered gaps in `NOTES.md` and feed follow-up tasks back into this TODO list if additional development is needed.
- [ ] **Broaden web citation verification.** Confirm punctuation and quotation usage for Chapter 16 web examples after OCR cleanup and add targeted fixture cases.
  - [ ] Complete OCR cleanup for the Chapter 16 examples in the Greenbook PDF and extract verbatim sample citations into `NOTES.md` with page references.
  - [ ] Compare existing web citation macros against the extracted examples to identify punctuation or quotation discrepancies.
  - [ ] Create new fixture entries in `tests.json` that capture the nuanced web citation formats (e.g., with publication dates, access dates, and quoted titles).
  - [ ] Update `expected_secondary.txt` (and related outputs) based on citeproc runs, verifying each change against the authoritative examples.
  - [ ] Document any remaining ambiguities or interpretive decisions in `NOTES.md` for future reviewers.

## Research & Backlog
- [ ] **Resolve memo opinion styling.** Verify italicization requirements for unpublished memorandum opinions (Greenbook Ch. 4, pp. 24–25) before locking typography rules.
  - [ ] Extract the memo opinion examples from the PDF and note the typography treatment (italics, capitalization, spacing) with precise citations in `NOTES.md`.
  - [ ] Review the current case macros to determine how memo opinion indicators are applied in both main and TOA outputs.
  - [ ] If adjustments are required, design the preferred formatting approach (e.g., new terms vs. styling attributes) and outline the implementation steps.
  - [ ] Prototype the change in a feature branch or local draft, run targeted tests, and evaluate against the Greenbook examples.
  - [ ] Update this TODO item with the chosen solution and file any residual questions in `NOTES.md`.
- [ ] **Decide on shared locale packaging.** Draft the consolidated locale file for terms like “art.” and “ch.” and plan integration across all drafts per the standing assumption.
  - [ ] Identify all non-default terms currently overridden in the main and TOA styles, listing them in `NOTES.md` along with their source citations.
  - [ ] Determine whether existing CSL locales cover these terms or if a custom `locales-en-US-texas-greenbook.xml` (or similar) file is required.
  - [ ] Draft the shared locale file structure, including `<term>` entries for abbreviations and any required pluralization forms.
  - [ ] Plan how the locale file will be distributed (e.g., bundled in this repository vs. submitted upstream) and document integration steps for each style.
  - [ ] Schedule updates to the styles and tests that will consume the locale file, noting dependencies or sequencing constraints in this TODO list.
- [ ] **Investigate supplemental references.** Follow up on OCR availability for the Uniform Format Manual and confirm TRCP/TRAP cross-references and historical reporter sources listed in `NOTES.md`.
  - [ ] Verify OCR readiness or perform text extraction for the supplemental manuals (Uniform Format Manual, rulemaking history PDFs) and store accessible copies or summaries.
  - [ ] Cross-reference TRCP/TRAP citations in `NOTES.md` with the supplemental materials to validate abbreviations and historical reporter references.
  - [ ] Update `NOTES.md` with confirmed cross-references, including any discrepancies or areas needing authoritative clarification.
  - [ ] Identify whether additional fixtures or macros are needed based on findings and create follow-up TODO entries if required.
  - [ ] Document the status of supplemental reference acquisition so future contributors know where canonical sources reside.

## Release Preparation
- [ ] **Finalize submission checklist.** Once logic gaps close, run `run_tests.py` suites, refresh documentation, and prepare the PR narrative referencing key Greenbook sections.
  - [ ] Confirm that all Active Development tasks are checked off and corresponding tests/fixtures are current.
  - [ ] Execute the full battery of regression tests for both note and TOA styles, capturing command output for inclusion in the eventual PR summary.
  - [ ] Sweep documentation (`README.md`, `NOTES.md`, `TODO.md`) to ensure they reflect the completed work, Greenbook citations, and outstanding questions.
  - [ ] Draft the PR narrative aligning with CSL submission requirements (title, summary, documentation links) and note specific Greenbook sections referenced during implementation.
  - [ ] Review the CSL repository contribution guidelines (`CONTRIBUTING.md`, `STYLE_REQUIREMENTS.md`) to double-check readiness before packaging the submission.
