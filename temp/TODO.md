# Texas Greenbook 15th Edition CSL Development TODO

## Completed Work
- [x] **Familiarized with source material.** Cataloged rule coverage, appendices, and page citations from the Greenbook PDF and logged them in `NOTES.md` for traceability.
- [x] **Surveyed existing CSL styles.** Reviewed Bluebook-derived and legal-dependent templates, noting reusable macros and locale patterns in `NOTES.md`.
- [x] **Defined citation requirements.** Produced the citation requirement matrix with mandatory variables, abbreviations, and Greenbook page references.
- [x] **Designed style architecture.** Established Draft 3 macro routing for citation and bibliography layouts, including Table of Authorities variants.
- [x] **Drafted primary CSL files.** Authored `texas-greenbook-15th-draft0` through `draft3` along with TOA counterparts covering primary authorities.
- [x] **Implemented secondary source rules.** Completed book-, journal-, CLE-, and web-specific macros shared between citation and bibliography outputs.
- [x] **Created regression fixtures.** Added `tests.json`, `tests_toa.json`, and matching `expected*.txt` files for authorities and TOA scenarios.
- [x] **Prepared working documentation.** Wrote the `README.md` overview, expanded research `NOTES.md`, and tracked assumptions and deviations.

## Active Development
### Citation Logic Gaps
- [ ] **Complete statute and rule short-form logic.** Implement cross-reference and `Id.` handling for statutes, rules, and administrative materials, then update `expected.txt` fixtures. (See `README.md` Known Limitations and `NOTES.md` helper sketches.)
- [ ] **Finish explanatory parentheticals.** Add shared helpers for slip-opinion pinpoints, procedural parentheticals, and docket metadata so case and mandamus citations emit relief/status consistently before finalizing Draft 4.
- [ ] **Build shared publication/status helpers.** Create reusable macros for statutory publication parentheticals, session-law metadata, and administrative status notes to reduce duplication across code, rule, and agency citations.

### Testing & Coverage
- [ ] **Expand Table of Authorities fixtures.** Introduce federal authorities and additional jurisdictional groupings to `tests_toa.json` and `expected_toa_*.txt` once the macro support exists.
- [ ] **Broaden web citation verification.** Confirm punctuation and quotation usage for Chapter 16 web examples after OCR cleanup and add targeted fixture cases.

## Research & Backlog
- [ ] **Resolve memo opinion styling.** Verify italicization requirements for unpublished memorandum opinions (Greenbook Ch. 4, pp. 24–25) before locking typography rules.
- [ ] **Decide on shared locale packaging.** Draft the consolidated locale file for terms like “art.” and “ch.” and plan integration across all drafts per the standing assumption.
- [ ] **Investigate supplemental references.** Follow up on OCR availability for the Uniform Format Manual and confirm TRCP/TRAP cross-references and historical reporter sources listed in `NOTES.md`.

## Release Preparation
- [ ] **Finalize submission checklist.** Once logic gaps close, run `run_tests.py` suites, refresh documentation, and prepare the PR narrative referencing key Greenbook sections.
