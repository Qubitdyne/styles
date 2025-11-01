# Texas Greenbook 15th Edition CSL Development TODO

1. **Familiarize with source material**
   - Review the Greenbook PDF to catalog citation rule categories (cases, statutes, regulations, secondary sources, etc.) and note page references for each rule.
   - Identify any appendices or tables that contain abbreviations or special formatting guidance.
2. **Survey existing CSL styles**
   - Examine related legal CSL files (e.g., other Texas or Bluebook-derived styles) to understand reusable macros and layout patterns.
   - Document potentially reusable components in `temp/NOTES.md`.
3. **Define citation requirements**
   - Create a structured specification outlining each citation type, required variables, punctuation, and ordering per the Greenbook rules.
   - Include page references from the PDF for every rule to maintain traceability.
4. **Design style architecture**
   - Determine macro structure, categories, and localization needs for the new style.
   - Plan handling for short forms, cross-references, and internal/external document distinctions.
5. **Draft primary CSL file**
   - Scaffold a new CSL file (e.g., `texas-greenbook-15th-edition.csl`) with metadata, info, and base layout.
   - Implement macros and citation formatting for primary authorities (cases, statutes, constitutions, regulations).
6. **Implement secondary source rules**
   - Encode formatting for books, treatises, law reviews, journals, websites, and other non-primary sources.
   - Ensure support for both footnote and bibliography entries if required by the Greenbook.
7. **Handle special cases and tables**
   - Add logic for procedural histories, short citations, signals, explanatory phrases, and parentheticals.
   - Implement tables, appendices, and abbreviation handling as required (e.g., agencies, reporters).
8. **Create test fixtures**
   - Build CSL JSON test cases covering every citation category, including edge cases and mixed authorities.
   - Document expected outputs with references to Greenbook page numbers.
9. **Validate style**
   - Run `make test` or equivalent CSL testing tools against the new style and fixtures, iterating until tests pass.
   - Verify output manually against Greenbook examples, recording discrepancies in `temp/NOTES.md`.
10. **Prepare documentation**
   - Draft a README or summary within `temp/` describing coverage, assumptions, and any deviations from the Greenbook.
   - Outline maintenance considerations and usage instructions.
11. **Finalize for submission**
   - Review code for adherence to CSL repository conventions (naming, metadata, licensing).
   - Update changelog or submission notes as required and ensure Git history cleanly reflects development steps.
   - Create PR message summarizing implemented citation rules and referencing key Greenbook sections.
