# Texas Greenbook CSL Audit — 2025-11-18

## Scope & Materials Reviewed
- Verified the temporary working directory (`temp/`) contents against the working README, notes, and backlog to confirm expectations for the in-progress Texas Greenbook 15th Edition CSL styles.【F:temp/README.md†L1-L120】【F:temp/NOTES.md†L1-L120】【F:temp/TODO.md†L1-L200】
- Inspected `run_tests.py`, regression fixtures, and historical logs to trace how the harness validates both note and Table of Authorities outputs.【F:temp/run_tests.py†L1-L120】【F:temp/tests.json†L1-L166】【F:temp/tests_toa.json†L1-L200】【F:temp/test-logs/20250309-run_tests-regenerated.txt†L1-L120】

## QA Activities
- Installed the missing `citeproc-py` dependency after the initial `ModuleNotFoundError` and documented the setup step in `temp/README.md`.【bfbf00†L1-L6】【2f6cb0†L1-L9】【F:temp/README.md†L49-L68】
- Re-ran the full note regression suite; all 60 fixtures matched the stored expectations with only the known citeproc metadata warnings.【955aca†L1-L120】
- Executed the Table of Authorities grouped-leaders suite in bibliography mode to confirm dotted leader output aligns with `expected_toa_grouped_leaders.txt`.【2a9a0c†L1-L40】【F:temp/expected_toa_grouped_leaders.txt†L1-L16】

## Findings & Root Causes
1. **Environment prerequisite missing:** Fresh environments lack `citeproc-py`, causing the harness to crash until the package is installed. Captured this in documentation and logged a TODO to codify the dependency packaging.【bfbf00†L1-L6】【F:temp/README.md†L49-L52】【F:temp/TODO.md†L403-L415】
2. **TOA command mismatch:** The harness defaults to note rendering, so TOA runs must pass `--mode bibliography` to avoid false diffs. README instructions now spell this out, and a follow-up TODO will explore automatic detection.【eab112†L1-L41】【F:temp/README.md†L55-L63】【F:temp/TODO.md†L416-L423】
3. **Benign citeproc warnings:** Runs continue to emit unsupported-field warnings (`label`, `reviewed_title`). Logged a backlog item to evaluate whether to scrub the metadata or suppress the warnings for cleaner logs.【955aca†L1-L24】【F:temp/TODO.md†L424-L432】

## Housekeeping & Documentation Updates
- Updated `temp/README.md` test instructions to highlight the citeproc installation step and the TOA bibliography mode requirement.【F:temp/README.md†L49-L63】
- Added a 2025-11-18 QA audit entry to `temp/NOTES.md` summarizing the rerun results and outstanding tooling gaps.【F:temp/NOTES.md†L121-L137】
- Extended `temp/TODO.md` with infrastructure tasks covering dependency packaging, TOA automation, and warning suppression to keep future work organized.【F:temp/TODO.md†L403-L432】

## Next Steps
- Prioritize the new test-harness backlog so future audits encounter fewer setup issues and noisier logs, referencing the detailed tasks in `temp/TODO.md`.【F:temp/TODO.md†L403-L432】
