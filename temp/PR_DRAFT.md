# PR Draft Notes

## Summary
- Expanded Chapter 16 web citation fixtures (undated press releases, quoted blog titles, standalone PDF downloads) and refreshed expectations/documentation to confirm punctuation alignment with pp. 76–77 of the Texas Greenbook.
- Added `Id.` guard logic for statute and rule repeats so citations with `collection-title` or `chapter-number` metadata restate the code instead of emitting `Id.`, per Greenbook Chapter 10 (pp. 42–45).
- Logged the short-form regression run in `temp/test-logs/2025-12-01_full-suite-post-guard-aligned.txt` for reviewer reference.
- Restored the Table of Authorities fixtures to the full 17-authority baseline and re-enabled `run_tests.py --write-expected` support so grouped/grouped-leaders/by-reporter outputs stay synchronized with Appendix B expectations.
- Expanded the regression harness warning filter to cover citeproc's `related` metadata, documenting the scope in `README.md` and archiving before/after logs under `temp/test-logs/20250314-related-warning-*.txt`.
- Logged the Appendix H code/rule abbreviation inventory in `NOTES.md`, cross-referenced it from `README.md`, and checked off the corresponding TODO subtasks so publication/status helper work has authoritative inputs.

## Testing
- python temp/run_tests.py --style temp/texas-greenbook-15th-edition.csl --tests temp/tests.json --expected temp/expected.txt
- python temp/run_tests.py --style temp/texas-greenbook-15th-edition.csl --tests temp/tests_parentheticals.json --expected temp/expected_parentheticals_notes.txt
- python temp/run_tests.py --style temp/texas-greenbook-15th-edition.csl --tests temp/tests_parentheticals.json --expected temp/expected_parentheticals_bibliography.txt --mode bibliography
- python temp/run_tests.py --style temp/texas-greenbook-15th-edition.csl --tests temp/tests_short-form_smoke.json --expected temp/expected_short-form_smoke.txt
- python temp/run_tests.py --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --tests temp/tests_toa.json --expected temp/expected_toa_grouped_leaders.txt --mode bibliography
- Documentation-only updates for the terminology inventory; no additional test runs required this cycle.
