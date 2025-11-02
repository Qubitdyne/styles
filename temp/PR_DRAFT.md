# PR Draft Notes

Keep this draft synchronized with the active TODO so we can file the upstream pull request without rediscovering the testing story.

## Summary (ready once helpers land)
- Expanded Chapter 16 web citation fixtures (undated press releases, quoted blog titles, standalone PDF downloads) and refreshed expectations to align with pp. 76–77 of the Texas Greenbook.
- Added `Id.` guard logic for statute and rule repeats so citations with `collection-title` or `chapter-number` metadata restate the code instead of emitting `Id.`, per Greenbook Chapter 10 (pp. 42–45).
- Logged the short-form regression run in `temp/test-logs/2025-12-01_full-suite-post-guard-aligned.txt` for reviewer reference.
- Restored the Table of Authorities fixtures to the full 17-authority baseline and re-enabled `run_tests.py --write-expected` support so grouped/grouped-leaders/by-reporter outputs stay synchronized with Appendix B expectations.
- Expanded the regression harness warning filter to cover citeproc's `related` metadata, documenting the scope in `README.md` and archiving before/after logs under `temp/test-logs/20250314-related-warning-*.txt`.
- Logged the Appendix H code/rule abbreviation inventory in `NOTES` and cross-referenced it from the documentation to support the upcoming publication/status helper work.

## Testing
- python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt
- python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_notes.txt
- python temp/run_tests.py --tests temp/tests_parentheticals.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_parentheticals_bibliography.txt --mode bibliography
- python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt
- python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography

## Pending before submission
- Fold the publication/status helpers into the production styles and refresh fixtures.
- Add the federal authority coverage required by Appendix B to the TOA datasets.
- Run the full regression sweep (notes, bibliography mode, TOA variants, diagnostics) and update this testing section with the latest command output paths.
