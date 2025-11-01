# PR Draft Notes

## Summary
- Expanded Chapter 16 web citation fixtures (undated press releases, quoted blog titles, standalone PDF downloads) and refreshed expectations/documentation to confirm punctuation alignment with pp. 76–77 of the Texas Greenbook.
- Added `Id.` guard logic for statute and rule repeats so citations with `collection-title` or `chapter-number` metadata restate the code instead of emitting `Id.`, per Greenbook Chapter 10 (pp. 42–45).
- Logged the short-form regression run in `temp/test-logs/2025-12-01_full-suite-post-guard-aligned.txt` for reviewer reference.

## Testing
- python temp/run_tests.py --style temp/texas-greenbook-15th-edition.csl --tests temp/tests.json --expected temp/expected.txt
- python temp/run_tests.py --style temp/texas-greenbook-15th-edition.csl --tests temp/tests_short-form_smoke.json --expected temp/expected_short-form_smoke.txt
