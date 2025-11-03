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

# Texas Greenbook CSL Audit — 2025-12-19

## Scope & Materials Reviewed
- Verified current guidance in `temp/README.md`, `temp/TODO.md`, and `temp/NOTES.md` to confirm backlog structure, outstanding tasks, and prior QA notes remain accurate before executing checks.【F:temp/README.md†L1-L120】【F:temp/TODO.md†L1-L120】【F:temp/NOTES.md†L1-L40】
- Attempted to exercise the test harness aggregate flag to confirm available CLI options, documenting the `--all` rejection for follow-up backlog work.【291d2b†L1-L4】
- Reviewed the latest entries under `temp/test-logs/` to ensure the most recent regression artifacts remain accessible for comparison during this audit pass.【563fda†L1-L32】

## QA Activities
- Ran the primary note regression suite against `texas-greenbook-15th-edition.csl` to verify 89 fixtures still match `expected.txt` after recent backlog triage.【ff6d67†L1-L188】
- Executed the focused parenthetical suites in both note and bibliography modes to confirm slip-opinion URL placement and mandamus history continue to align with expectations.【3cd12f†L1-L36】【2fb238†L1-L28】
- Validated the grouped-leaders Table of Authorities run to confirm dotted leaders and restored fixture inventory remain synchronized with `expected_toa_grouped_leaders.txt`.【8c3d03†L1-L52】

## Findings & Root Causes
1. **Citeproc warning suppression incomplete:** Despite earlier guardrails, the harness still emits `UserWarning` messages for the `related` field during regression runs. The current filter only suppresses `comment`, `label`, `reviewed_title`, and `grouping`, leaving `related` unhandled.【ff6d67†L1-L10】【F:temp/run_tests.py†L25-L34】 This contradicts the README’s promise of a clean log stream.
2. **Documentation drift on warning behavior:** `temp/README.md` states that benign citeproc warnings are suppressed by default, which is now inaccurate given the persisting `related` notices observed in all three suites executed during this audit.【ff6d67†L1-L10】【F:temp/README.md†L47-L63】 The guidance must be updated once the harness filter is expanded.

## Housekeeping & Documentation Updates
- Logged a 2025-12-19 QA spot-check in `temp/NOTES.md` summarizing the executed test commands, the resurfaced `related` warnings, and the need to extend suppression coverage.【F:temp/NOTES.md†L26-L31】
- Expanded `temp/TODO.md` with new infrastructure tasks covering the warning filter enhancement and documentation correction so future work packages can address the drift systematically.【F:temp/TODO.md†L361-L370】

## Next Steps
- Extend the warning suppression filter in `run_tests.py` to include `related`, rerun the regression suites to confirm clean logs, and update README guidance accordingly once resolved.【F:temp/TODO.md†L361-L370】

# Texas Greenbook CSL Audit — 2025-12-21

## Scope & Materials Reviewed
- Walked the refreshed `temp/README.md` inventory and subdirectory spot-check to verify every artifact (archive drafts, prototypes, reports, logs) is documented for future contributors.【F:temp/README.md†L19-L77】
- Inspected the publication helper prototypes and expectations to confirm in-flight work remains captured in the sandbox directory for later integration.【F:temp/prototypes/publication-helper-prototype.csl†L1-L200】【F:temp/prototypes/publication-helper-prototype.json†L1-L72】【F:temp/prototypes/publication-helper-expected.txt†L1-L32】
- Reviewed the top-level TODO triage and outstanding sections to ensure remaining work is visible and cross-referenced with detailed checklists.【F:temp/TODO.md†L1-L23】【F:temp/TODO.md†L489-L609】【F:temp/TODO.md†L772-L858】

## QA Activities
- Executed the full note regression suite against `texas-greenbook-15th-edition.csl`; all 89 fixtures matched their expectations.【0d0224†L1-L210】
- Ran the focused parenthetical note suite to confirm explanatory parenthetical logic remains stable.【851bd2†L1-L31】
- Validated the grouped-leader TOA harness with `texas-greenbook-15th-toa-grouped-leaders.csl`; outputs aligned with `expected_toa_grouped_leaders.txt`.【419e4b†L1-L83】

## Findings & Root Causes
1. **Publication/status helper work parked but unfinished:** The helper prototypes and exhaustive checklist remain outstanding; without wiring these helpers into the main and TOA styles, publication parentheticals must still be maintained manually in multiple places.【F:temp/prototypes/publication-helper-prototype.csl†L1-L200】【F:temp/TODO.md†L489-L609】 The open task is captured in the Outstanding Work triage for prioritization.【F:temp/TODO.md†L9-L15】
2. **Federal TOA support still pending:** Although fixtures exist, the TOA macros have not yet been extended to emit federal headings; this remains a blocker for Appendix B parity until the outlined tasks are implemented.【F:temp/tests_toa.json†L1-L338】【F:temp/TODO.md†L772-L781】

## Housekeeping & Documentation Updates
- Updated `temp/README.md` with a 2025-12-21 inventory refresh and subdirectory annotations so future agents can locate prototypes, reports, and regression logs quickly.【F:temp/README.md†L19-L77】
- Added an Outstanding Work triage section to `temp/TODO.md` and expanded the release checklist subtasks to guide the final submission sequence.【F:temp/TODO.md†L1-L23】【F:temp/TODO.md†L828-L858】
- Logged this audit and helper handoff guidance in `temp/NOTES.md` for continuity across agents.【F:temp/NOTES.md†L1-L9】

## Next Steps
- Prioritize the publication/status helper integration, then resume the federal TOA macro work before tackling the final submission checklist to keep the Outstanding Work section short-lived.【F:temp/TODO.md†L9-L23】【F:temp/TODO.md†L489-L609】【F:temp/TODO.md†L772-L858】

# Texas Greenbook CSL Audit — 2025-11-03T00:05Z

## Scope & Materials Reviewed
- Re-ran all active regression suites (notes, parentheticals, TOA grouped-leaders) with the current CSL drafts to confirm the working baseline.【56ff88†L1-L209】【0b1637†L1-L55】【5c3ba9†L1-L87】
- Inspected `temp/README.md`, `temp/TODO.md`, `temp/NOTES.md`, and `temp/PR_DRAFT.md` to ensure live documentation aligns with observed harness behavior and backlog priorities.【F:temp/README.md†L1-L80】【F:temp/TODO.md†L1-L60】【F:temp/NOTES.md†L1-L60】【F:temp/PR_DRAFT.md†L1-L36】
- Reviewed `temp/run_tests.py` and the warning filter configuration to verify citeproc noise suppression now covers the `related` metadata key noted in prior audits.【F:temp/run_tests.py†L1-L80】
- Enumerated `temp/test-logs/` to confirm historic regression artifacts remain intact for cross-reference during future passes.【3ae9ab†L1-L67】

## QA Activities
- Executed the main note regression suite; all 89 fixtures matched expectations without warnings.【56ff88†L1-L209】
- Ran the parenthetical note suite to validate helper-adjacent behaviors; no diffs observed.【0b1637†L1-L55】
- Validated the grouped-leaders TOA suite in bibliography mode to confirm the restored 25-entry dataset still aligns with expectations.【5c3ba9†L1-L87】

## Findings & Root Causes
1. **PR draft references stale:** `temp/PR_DRAFT.md` still cites placeholder log filenames (`20250314-related-warning-*`) that do not exist, leaving the submission narrative unverifiable. The root cause is earlier template text that predates the latest log capture cadence; the document must be refreshed once new helper work lands.【F:temp/PR_DRAFT.md†L12-L18】【3ae9ab†L1-L67】
2. **Backlog lacked actionable subtasks:** The trimmed `temp/TODO.md` no longer captured granular steps for helper integration, TOA expansion, or documentation cleanup, reducing its usefulness for handoffs. Breaking each headline item into explicit subtasks will prevent future drift.【F:temp/TODO.md†L1-L24】

## Housekeeping & Documentation Updates
- Expanded `temp/TODO.md` with detailed subtask lists for helper work, TOA federal coverage, submission prep, and documentation hygiene, plus a timestamped record of this regression sweep.【F:temp/TODO.md†L5-L45】
- Logged the 2025-11-03 QA sweep in `temp/NOTES.md`, including the commands run and the outstanding PR draft cleanup need.【F:temp/NOTES.md†L21-L38】

## Next Steps
- Update `temp/PR_DRAFT.md` to reference real regression logs and incorporate new helper narratives once available, as captured in the documentation hygiene tasks.【F:temp/TODO.md†L37-L45】
- Capture permanent log files for this regression pass before commencing helper integration work so historical comparisons remain straightforward.【F:temp/TODO.md†L15-L23】
