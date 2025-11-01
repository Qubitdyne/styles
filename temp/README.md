# Temporary Workspace Inventory

The `temp/` directory stores working references and drafts for developing a CSL style set for the *Texas Greenbook, 15th Edition*. The table below lists each artifact with notes on how it can support further work.

| File | Format | Description & Potential Use |
| --- | --- | --- |
| `AGENTS.md` | Markdown | Scoped instructions for collaborating in this workspace; review before editing files here to follow process expectations. |
| `CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html` | HTML | Offline copy of the CSL 1.0.2 specification; consult when confirming element and attribute behavior during style development. |
| `Greenbook_15thEdition.pdf` | PDF | Complete scan of the *Texas Greenbook, 15th Edition*; primary citation authority for implementing rules in the new CSL definitions. |
| `How-Court-Rules-Are-Made.pdf` | PDF | Background on the Texas court rulemaking process; useful for understanding the provenance of Greenbook directives and related authorities. |
| `Uniform-Format-Manual-07012010.pdf` | PDF | Historical uniform citation manual reference; cross-check differences with the Greenbook when making design decisions. |
| `actual_toa.txt` | Text | Output from a current Table of Authorities (TOA) rendering; compare against expected TOA files to evaluate formatting gaps in draft styles. |
| `expected.txt` | Text | Expected citation output for standard bibliography tests; use alongside `tests.json` to validate footnote and bibliography formatting. |
| `expected_toa.txt` | Text | Baseline expected TOA entries in simple list form; compare with generator output to identify deviations in ordering or punctuation. |
| `expected_toa_grouped.txt` | Text | Expected TOA entries grouped by source type; reference when adjusting grouping logic in specialized TOA CSL variants. |
| `technology-standards.pdf` | PDF | Supplementary reference on technology standards cited by Texas courts; assists in modeling citations to administrative materials. |
| `tests.json` | JSON | Citeproc test suite for general citations; run against draft CSL files to ensure Greenbook compliance for typical authorities. |
| `tests_toa.json` | JSON | Citeproc test suite tailored for Table of Authorities output; pair with TOA drafts to verify grouping, leaders, and pin cite presentation. |
| `texas-court-rules-history-process.html` | HTML | Downloaded article on the history of Texas court rules; contextual reference for interpreting rule citations. |
| `texas-greenbook-15th-draft0.csl` | CSL | Earliest recorded draft of the main citation style; useful for tracking evolution of macros and layout decisions. |
| `texas-greenbook-15th-draft1.csl` | CSL | Intermediate iteration of the main style; compare diffs with later drafts to identify resolved issues. |
| `texas-greenbook-15th-draft2.csl` | CSL | Later draft of the primary style; likely closest to current working version before draft3 adjustments. |
| `texas-greenbook-15th-draft3.csl` | CSL | Most recent main style draft; starting point for further refinement toward a publication-ready Greenbook CSL. |
| `texas-greenbook-15th-toa.csl` | CSL | Base Table of Authorities CSL draft; renders TOA entries without additional grouping or leaders. |
| `texas-greenbook-15th-toa-by-reporter.csl` | CSL | TOA variant experimenting with reporter-based grouping; evaluate when testing alternate TOA organization strategies. |
| `texas-greenbook-15th-toa-grouped.csl` | CSL | TOA draft implementing grouped headings; align with `expected_toa_grouped.txt` expectations. |
| `texas-greenbook-15th-toa-grouped-leaders.csl` | CSL | Grouped TOA variant adding dotted leader support; validate leader alignment against `tests_toa.json`. |
| `texas-greenbook-15th-toa-leaders.csl` | CSL | Ungrouped TOA variant focusing on dotted leader formatting; combine with baseline TOA tests to isolate leader behavior. |
| `texas-rules-of-appellate-procedure.pdf` | PDF | Official Texas Rules of Appellate Procedure; cite when modeling rule references mandated by the Greenbook. |
| `texas-rules-of-civil-procedure-august-31-2025.pdf` | PDF | Effective 2025 Texas Rules of Civil Procedure; supports testing of rule citation formats. |
| `texas-rules-of-evidence-effective-912025.pdf` | PDF | Effective September 2025 Texas Rules of Evidence; aids in verifying citation handling for evidentiary rules. |
