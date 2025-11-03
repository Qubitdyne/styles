# Texas Greenbook 15th Edition CSL — Active TODO

_Completed tasks and the legacy backlog now live in `temp/archive/TODO-history-2025-12-21.md`. Keep this file focused on the current execution plan so sessions stay on track._

## Immediate priorities
- [ ] **Build shared publication/status helpers**
  - [x] Inventory `temp/prototypes/` (CSL, JSON, expected output) and note which macros map directly into production styles.
  - [x] Extract controlling rules from *Greenbook* chs. 10–13 (record page citations in `temp/NOTES.md`).
  - [x] Design final helper macro signatures (inputs, outputs, parameter names) and document them in `temp/NOTES.md`.
  - [x] Implement helpers in `texas-greenbook-15th-edition.csl`, replacing duplicated status/publication logic.
  - [x] Update note and parenthetical fixtures to cover helper-driven outputs; regenerate `expected*.txt` with `--write-expected`.
  - [x] Port helpers into every `texas-greenbook-15th-toa*.csl` variant and verify cross-file parity.
  - [x] Follow up on TOA register notices: suppress duplicate `Tex. Reg.` cites when the base entry already prints the volume and page (e.g., 39 Tex. Reg. 573, 574 in grouped layouts). (`2025-11-03T05:30Z`)
  - [x] Capture fresh regression logs (notes, parentheticals, TOA) under `temp/test-logs/` with timestamped filenames. (`2025-11-03T05:30Z` → `20251103T012201Z_*`)
  - [x] Summarize helper roll-out decisions and citations in `temp/NOTES.md` and confirm documentation sync in `temp/README.md`. (`2025-11-03T05:30Z`)
- [ ] **Add federal authority coverage to TOA fixtures and macros**
  - [x] Catalog Appendix B federal examples (case, statute, regulation, agency) and map them to fixture records. (`2025-12-22T16:45Z`)
  - [x] Restore or add the missing federal entries in `temp/tests_toa.json`, capturing rationale and sources. (`2025-12-22T17:05Z`)
  - [x] Refresh `expected_toa*.txt` files via `run_tests.py --mode bibliography --write-expected` and archive logs. (`2025-12-22T17:25Z`)
  - [ ] Enhance TOA CSL macros to emit jurisdiction-aware headings and ensure mixed Texas/federal ordering matches Appendix B.
  - [x] Re-run grouped, grouped-leaders, leaders, and by-reporter suites; diff results and log artifacts to `temp/test-logs/`. (`2025-11-03T01:44Z` → `20251103T01433*`)
  - [x] Update `temp/README.md` and `temp/NOTES.md` with the new TOA coverage and any sorting nuances. (`2025-11-03T01:44Z`)
- [ ] **Finalize upstream submission checklist**
  - [x] Audit `temp/PR_DRAFT.md` against current work to ensure the summary references real fixtures/logs. (`2025-11-03T01:44Z`)
  - [x] Flesh out coverage notes with page cites into Chapters 2, 4, 10, 17 as applicable. (`2025-11-03T04:12Z`)
  - [x] Confirm documentation alignment across `README.md`, `NOTES.md`, helper write-ups, and TOA instructions. (`2025-11-03T04:15Z`)
  - [x] Execute the full regression sweep (notes, bibliography mode, parenthetical suites, short-form smoke, TOA variants) and log outputs. (`2025-11-03T04:20Z`)
  - [ ] Investigate the short-form smoke diffs where statute, regulation, and rule repeats emit `Id.`/`See also`; adjust guardrails to restate the source text and refresh `temp/expected_short-form_smoke.txt` with logged before/after runs.
  - [ ] Populate the testing checklist in `temp/PR_DRAFT.md` with fresh timestamps and log paths before submission.
  - [ ] Stage the final diff review and craft the upstream PR body referencing the completed tasks.

## Support tasks
- [ ] **Avoid session drift**
  - [ ] Capture in-flight reasoning inside `temp/NOTES.md` (or archive addendum) before stopping work.
  - [ ] Commit incremental progress once a test suite passes to keep recovery points close to the active change.
  - [ ] When running suites, note command invocations and outcomes (OK/DIFF counts) with ISO 8601 timestamps.
- [ ] **Documentation hygiene**
  - [x] Refresh `temp/PR_DRAFT.md` references to historical logs so they point at actual artifacts and dates. (`2025-11-03T00:08Z`)
  - [x] Review `temp/README.md` language about warning suppression after helper work to ensure it reflects the final harness behavior. (`2025-11-03T01:44Z`)
  - [ ] Tag any additional markdown drift discovered during audits and file follow-up items here with timestamps.

## Recently verified (informational)
- [x] `2025-11-03T00:05Z` — Re-ran note, parenthetical, and TOA grouped-leaders suites; all expectations matched (`run_tests.py` outputs logged in session 56ff88, 0b1637, 5c3ba9).

## Reference
- Historical context, prior checklists, and completed work: `temp/archive/TODO-history-2025-12-21.md`.
- Use the archive when you need the detailed reasoning behind an item; keep this list short enough to glance at between commits.
