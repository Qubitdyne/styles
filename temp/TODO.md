# Texas Greenbook 15th Edition CSL — Active TODO

_Completed tasks and the legacy backlog now live in `temp/archive/TODO-history-2025-12-21.md`. Keep this file focused on the current execution plan so sessions stay on track._

## Immediate priorities
- [x] **Session law short-form macros** (`2026-01-16T12:00Z` opened)
  - [x] Split `tx-session-law-citation` into first/short/cross-reference variants that honor CSL `position` and `references`.
  - [x] Ensure the short form omits codification/Gammel parentheticals while retaining chapter/section text per Greenbook ch. 11 (pp. 53–56).
  - [x] Route `note-body` and any TOA callsites through the new macros without regressing existing outputs.
- [x] **Session law regression coverage** (`2026-01-16T12:00Z` opened)
  - [x] Add repeat- and cross-reference fixtures for session laws to `temp/tests.json` and `temp/tests_short-form_smoke.json`.
  - [x] Regenerate `temp/expected*.txt` files (notes, short-form smoke, TOA if touched) and archive the confirmation logs.
  - [x] Note the new fixture IDs and Greenbook citations in `temp/NOTES.md`.
- [x] **Document session law short-form behavior** (`2026-01-16T12:00Z` opened)
  - [x] Summarize the new session law macros and test coverage in `temp/README.md` and `temp/NOTES.md` with Greenbook ch. 11 page cites.
  - [x] Update `temp/PR_DRAFT.md` so the upstream summary/testing checklist mentions the session law short-form changes.
  - [x] Record the regression commands and log filenames tied to this update in the documentation.
- [x] **AG opinion short-form restatement** (`2026-01-16T00:00Z` opened)
  - [x] Add position-aware `ag-opinion` macros so subsequent cites restate the opinion number without repeating the year while preserving Greenbook ch. 17 (p. 77) first-form output.
  - [x] Update documentation (`temp/README.md`, `temp/NOTES.md`, `temp/PR_DRAFT.md`) to reflect the new short-form behavior and cite the supporting Greenbook guidance.
- [x] **Municipal code short-form restatement** (`2026-01-16T00:00Z` opened)
  - [x] Teach the `municipal-code` macro to drop the year parenthetical on repeat citations per Greenbook ch. 13 (p. 62) and add a cross-reference variant that appends any `references` strings.
  - [x] Synchronize the documentation updates with the AG opinion task so both categories appear in the short-form narrative refresh.
- [x] **Expand short-form smoke coverage** (`2026-01-16T00:00Z` opened)
  - [x] Extend `temp/tests_short-form_smoke.json` and `temp/expected_short-form_smoke.txt` with AG opinion and municipal code fixtures that exercise the new restatement guardrails.
  - [x] Capture fresh regression logs for the updated smoke suite and record them in the active notes/README/testing ledger.
- [x] **Reconstruct register notice notes entry** (`2026-01-15T15:42Z` opened)
  - [x] Restore the `2025-11-03T05:30Z` block in `temp/NOTES.md` so it fully documents the register notice cleanup without ellipses or truncated sentences.
  - [x] Cite the controlling guidance from Greenbook ch. 16 (p. 83) and Appendix B (pp. 247–248) alongside the refreshed summary and referenced logs.
- [x] **Refresh active research threads** (`2026-01-15T15:42Z` opened)
  - [x] Update the "Active research threads" list in `temp/NOTES.md` to reflect the remaining follow-up items now that the short-form guardrails landed.
  - [x] Cross-check that the new bullets align with the current regression coverage and any outstanding PR packaging work captured in `temp/PR_DRAFT.md`.
- [x] **Re-run short-form smoke suite and document log** (`2026-01-15T15:42Z` opened)
  - [x] Execute `python temp/run_tests.py --tests temp/tests_short-form_smoke.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_short-form_smoke.txt` and archive the output under `temp/test-logs/` with an ISO 8601 timestamp.
  - [x] Record the new log in `temp/README.md`, `temp/NOTES.md`, and `temp/PR_DRAFT.md`, including the command, outcome, and how the run confirms the restated short-form behavior.
- [x] **Short-form restatement guardrails** (`2026-01-15T00:00Z` opened)
  - [x] Replace the `Id.` fallback for statutory short forms with restated code titles and sections per Greenbook ch. 4 (pp. 24, 34).
  - [x] Extend the administrative rule and regulation short-form macros to reuse the Chapter 13 authority/status text instead of emitting `Id.`.
  - [x] Update `temp/tests_short-form_smoke.json` and regenerate `temp/expected_short-form_smoke.txt` to confirm the repeated-text outputs.
  - [x] Capture the validation run in `temp/test-logs/` with a timestamped filename and cite it in `temp/NOTES.md`.
- [x] **Short-form documentation sweep** (`2026-01-15T00:00Z` opened)
  - [x] Summarize the new Chapter 4 guardrails in `temp/NOTES.md` with Greenbook page citations.
  - [x] Refresh `temp/README.md` and `temp/PR_DRAFT.md` so the outstanding work and testing checklist reference the updated short-form behavior.
  - [x] Record the short-form regression command and log path in `temp/test-logs/run-history.log` if the automation misses it.
- [x] **Build shared publication/status helpers** (`2025-11-03T06:04Z` verification)
  - [x] Inventory `temp/prototypes/` (CSL, JSON, expected output) and note which macros map directly into production styles.
  - [x] Extract controlling rules from *Greenbook* chs. 10–13 (record page citations in `temp/NOTES.md`).
  - [x] Design final helper macro signatures (inputs, outputs, parameter names) and document them in `temp/NOTES.md`.
  - [x] Implement helpers in `texas-greenbook-15th-edition.csl`, replacing duplicated status/publication logic.
  - [x] Update note and parenthetical fixtures to cover helper-driven outputs; regenerate `expected*.txt` with `--write-expected`.
  - [x] Port helpers into every `texas-greenbook-15th-toa*.csl` variant and verify cross-file parity.
  - [x] Follow up on TOA register notices: suppress duplicate `Tex. Reg.` cites when the base entry already prints the volume and page (e.g., 39 Tex. Reg. 573, 574 in grouped layouts). (`2025-11-03T05:30Z`)
  - [x] Capture fresh regression logs (notes, parentheticals, TOA) under `temp/test-logs/` with timestamped filenames. (`2025-11-03T05:30Z` → `20251103T012201Z_*`)
  - [x] Summarize helper roll-out decisions and citations in `temp/NOTES.md` and confirm documentation sync in `temp/README.md`. (`2025-11-03T05:30Z`)
- [x] **Add federal authority coverage to TOA fixtures and macros** (`2025-11-03T06:04Z` verification)
  - [x] Catalog Appendix B federal examples (case, statute, regulation, agency) and map them to fixture records. (`2025-12-22T16:45Z`)
  - [x] Restore or add the missing federal entries in `temp/tests_toa.json`, capturing rationale and sources. (`2025-12-22T17:05Z`)
  - [x] Refresh `expected_toa*.txt` files via `run_tests.py --mode bibliography --write-expected` and archive logs. (`2025-12-22T17:25Z`)
  - [x] Enhance TOA CSL macros to emit jurisdiction-aware headings and ensure mixed Texas/federal ordering matches Appendix B. (`2025-12-22T18:45Z`)
  - [x] Re-run grouped, grouped-leaders, leaders, and by-reporter suites; diff results and log artifacts to `temp/test-logs/`. (`2025-11-03T01:44Z` → `20251103T01433*`)
  - [x] Update `temp/README.md` and `temp/NOTES.md` with the new TOA coverage and any sorting nuances. (`2025-11-03T01:44Z`)
- [x] **Finalize upstream submission checklist** (`2025-12-22T19:30Z`)
  - [x] Audit `temp/PR_DRAFT.md` against current work to ensure the summary references real fixtures/logs. (`2025-11-03T01:44Z`)
  - [x] Flesh out coverage notes with page cites into Chapters 2, 4, 10, 17 as applicable. (`2025-11-03T04:12Z`)
  - [x] Confirm documentation alignment across `README.md`, `NOTES.md`, helper write-ups, and TOA instructions. (`2025-11-03T04:15Z`)
  - [x] Execute the full regression sweep (notes, bibliography mode, parenthetical suites, short-form smoke, TOA variants) and log outputs. (`2025-11-03T04:20Z`)
  - [x] Investigate the short-form smoke diffs where statute, regulation, and rule repeats emit `Id.`/`See also`; adjust guardrails to restate the source text and refresh `temp/expected_short-form_smoke.txt` with logged before/after runs. (`2025-12-22T18:45Z`)
  - [x] Populate the testing checklist in `temp/PR_DRAFT.md` with fresh timestamps and log paths before submission. (`2025-11-03T05:55Z`)
  - [x] Stage the final diff review and craft the upstream PR body referencing the completed tasks. (`2025-11-03T05:55Z`)

## Support tasks
- [x] **Avoid session drift** (`2025-11-03T09:11Z`)
  - [x] Capture in-flight reasoning inside `temp/NOTES.md` (or archive addendum) before stopping work. (`2025-11-03T05:55Z`)
  - [x] Commit incremental progress once a test suite passes to keep recovery points close to the active change. (`2025-12-22T19:30Z`)
  - [x] Add an automated log hook to `temp/run_tests.py` so every invocation can append its command, timestamp, and outcome to a file in `temp/test-logs/`, reducing reliance on manual session transcripts. (`2025-11-03T09:11Z`)
- [x] When running suites, note command invocations and outcomes (OK/DIFF counts) with ISO 8601 timestamps. (`2025-11-03T06:04Z` — logged in `temp/NOTES.md`)
- [x] **Documentation hygiene** (`2025-11-03T09:11Z`)
  - [x] Refresh `temp/PR_DRAFT.md` references to historical logs so they point at actual artifacts and dates. (`2025-11-03T00:08Z`)
  - [x] Review `temp/README.md` language about warning suppression after helper work to ensure it reflects the final harness behavior. (`2025-11-03T01:44Z`)
  - [x] Tag any additional markdown drift discovered during audits and file follow-up items here with timestamps. (`2025-12-22T19:30Z`)
  - [x] Replace the placeholder ellipsis in the 2025-11-03T05:30Z register-notice entry within `temp/NOTES.md` with a complete summary (including page citations) so future contributors are not left guessing about the cleanup work. (`2025-11-03T09:11Z`)
  - [x] Document the automated test logging workflow in `temp/README.md` and `temp/PR_DRAFT.md`, noting where the new log files will appear. (`2025-11-03T09:11Z`)

## Recently verified (informational)
- [x] `2025-11-03T00:05Z` — Re-ran note, parenthetical, and TOA grouped-leaders suites; all expectations matched (`run_tests.py` outputs logged in session 56ff88, 0b1637, 5c3ba9).

## Reference
- Historical context, prior checklists, and completed work: `temp/archive/TODO-history-2025-12-21.md`.
- Use the archive when you need the detailed reasoning behind an item; keep this list short enough to glance at between commits.
