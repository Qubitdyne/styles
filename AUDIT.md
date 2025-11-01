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

# Texas Greenbook CSL Audit — 2025-12-05

## Scope & Materials Reviewed
- Re-ran the canonical note regression suite with `texas-greenbook-15th-edition.csl` and the latest `expected.txt` snapshot to confirm baseline coverage and highlight any lingering diffs.【8360ab†L1-L208】
- Executed the grouped-leaders Table of Authorities harness using `texas-greenbook-15th-toa-grouped-leaders.csl` against `expected_toa_grouped_leaders.txt`, then compared the mismatched output with both the fixture file and the 2025-05-06 reference log to understand ordering regressions.【e29318†L1-L37】【F:temp/expected_toa_grouped_leaders.txt†L1-L17】【F:temp/test-logs/20250506_toa_grouped_leaders.txt†L1-L40】
- Inspected `tests_toa.json` counts to verify that the current dataset only exercises 13 authorities, explaining why the grouped expectations still enumerate 17 entries.【4bd8bb†L1-L1】

## QA Activities
- Confirmed that the note suite continues to render all case, legislation, and secondary fixtures except for the known cross-jurisdiction cue gap that leaves test 74 emitting “See” instead of the expected “See also,” matching the outstanding follow-up in the short-form epic.【34ab82†L181-L209】【F:temp/TODO.md†L240-L292】
- Captured the TOA grouped-leaders run showing only 13 rendered entries and dotted leader alignment for the surviving fixtures, providing a fresh log to pair with the historical 17-line baseline during remediation.【e29318†L1-L37】

## Findings & Root Causes
1. **TOA fixture regression:** The grouped-leaders suite now renders 13 authorities while the expectations still cover 17, producing cascading diffs once the comparator advances past statutes. The root cause is a truncated `tests_toa.json` inventory that no longer includes entries such as `Tex. Gov’t Code Ann. § 311.021(1)` and `Tex. R. Civ. P. 21`, leaving the old expectations misaligned.【4bd8bb†L1-L1】【F:temp/expected_toa_grouped_leaders.txt†L1-L17】【e29318†L18-L36】
2. **Jurisdictional cue guard still pending:** Regression run 74 continues to output the baseline “See” signal for non-Texas authorities, reaffirming that the planned citeproc jurisdiction filtering follow-up remains outstanding before the short-form release can close the gap.【34ab82†L181-L209】【F:temp/TODO.md†L240-L292】

## Housekeeping & Documentation Updates
- Logged the TOA fixture regression and cross-reference cue status in `NOTES.md` under a new 2025-12-05 QA spot-check so future reviewers have immediate context for the failing expectations.【F:temp/NOTES.md†L1-L40】
- Added a dedicated `TODO.md` entry detailing the restoration steps for the missing TOA fixtures, including regeneration and documentation tasks to prevent the mismatch from resurfacing.【F:temp/TODO.md†L359-L375】

## Next Steps
- Restore the four missing TOA fixtures, regenerate all `expected_toa*.txt` baselines, and archive fresh grouped-leader logs before rerunning this audit checklist.【F:temp/TODO.md†L359-L375】
