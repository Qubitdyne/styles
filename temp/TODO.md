# Texas Greenbook 15th Edition CSL — Active TODO

_Completed tasks and the legacy backlog now live in `temp/archive/TODO-history-2025-12-21.md`. Keep this file focused on the current execution plan so sessions stay on track._

## Immediate priorities
- [ ] **Build shared publication/status helpers**
  - [ ] Review `temp/prototypes/` assets and decide which helper macros graduate into production.
  - [ ] Add targeted fixtures plus regenerated expectations covering statutes, session laws, and agency materials.
  - [ ] Mirror the finalized helpers into every `texas-greenbook-15th-toa*.csl` variant and rerun the TOA suite.
- [ ] **Add federal authority coverage to TOA fixtures and macros**
  - [ ] Restore the missing federal records in `temp/tests_toa.json` and update the paired `expected_toa*.txt` files.
  - [ ] Introduce jurisdiction-aware headings/sorting so Appendix B’s mixed-federal layout is satisfied.
- [ ] **Finalize upstream submission checklist**
  - [ ] Tighten `temp/PR_DRAFT.md` with the final narrative, cited rule coverage, and regression summary.
  - [ ] Ensure `README.md`, `NOTES.md`, and the new helper work stay consistent, then run the full regression sweep prior to submission.

## Support tasks
- [ ] **Avoid session drift**
  - [ ] Capture in-flight reasoning inside `temp/NOTES.md` (or archive addendum) before stopping work.
  - [ ] Commit incremental progress once a test suite passes to keep recovery points close to the active change.

## Reference
- Historical context, prior checklists, and completed work: `temp/archive/TODO-history-2025-12-21.md`.
- Use the archive when you need the detailed reasoning behind an item; keep this list short enough to glance at between commits.
