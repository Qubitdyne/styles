# Texas Greenbook 15th Edition Research Notes

## Table of Contents Overview
| Chapter | Title | Page Span |
| --- | --- | --- |
| 1 | Briefs and Legal Memoranda | 3–5 |
| 2 | Texas Supreme Court | 7–9 |
| 3 | Texas Court of Criminal Appeals | 10–13 |
| 4 | Courts of Appeals | 14–27 |
| 5 | Commission of Appeals | 28–30 |
| 6 | Mandamus and Other Original Proceedings | 31–33 |
| 7 | Trial Courts | 34–36 |
| 8 | Judicial Misconduct Tribunals | 37 |
| 9 | Texas Constitution | 39–40 |
| 10 | Current Statutes | 42–53 |
| 11 | Statutes No Longer in Effect | 54–56 |
| 12 | Comments and Notes Accompanying Statutes | 58–60 |
| 13 | Rules of Procedure and Evidence | 61–65 |
| 14 | Legislative History | 66–72 |
| 15 | Formal Advisory Opinions | 73–75 |
| 16 | Agency Material | 76–84 |
| 17 | State Bar Materials | 86–91 |
| 18 | Books | 93–95 |
| 19 | Conference and Institute Proceedings | 96 |

## QA spot-check – Regression audit (2025-12-05)
- Re-ran the canonical note regression via `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt` and confirmed all fixtures continue to match except for the outstanding “See” vs. “See also” delta on test 74, which aligns with the open jurisdiction cue follow-up in the short-form backlog.【8360ab†L1-L208】【34ab82†L181-L209】
- Executed the grouped-leaders TOA suite with the same harness invocation (`--mode bibliography`) and observed that only 13 authorities rendered even though the expectations enumerate 17 entries, producing cascading diffs beginning with the missing Government Code cite.【e29318†L1-L37】【F:temp/expected_toa_grouped_leaders.txt†L1-L17】
- Verified that `tests_toa.json` currently contains 13 records (`jq 'length'`), then compared today’s diff against the 2025-05-06 grouped-leader log to confirm that four authorities (Tex. Gov’t Code Ann. § 311.021(1), Tex. R. Civ. P. 21, 16 Tex. Admin. Code § 25.101, 1 Tex. Admin. Code § 3.5) dropped from the dataset after that baseline was captured.【4bd8bb†L1-L1】【F:temp/test-logs/20250506_toa_grouped_leaders.txt†L1-L40】
- Captured the remediation plan in `TODO.md` under “Restore TOA fixture ordering” so fixture restoration, expectation regeneration, and documentation follow-up can proceed methodically.【F:temp/TODO.md†L359-L375】

## Legacy Draft 3 Update – Position-Aware Statutes, Rules, and Agencies (2025-03-17)
- **Baseline review.** The archived `texas-greenbook-15th-draft3.csl` (now mirrored in `texas-greenbook-15th-edition.csl`) previously routed statutes through `statute-code`/`tex-statute` and agency materials through `tex-admin-code`/`tex-register`, but each macro only branched on `position="first"` and `variable="references"`. There was no shared handling for `Id.` cues, so repeat notes defaulted to the full form instead of the Greenbook short forms mandated in chs. 10–13 (pp. 42–84).
- **New cue + id stack.** Imported the `prefatory-signal`, `note-body`, and `ibid-locator` scaffolding into the edition build so that `cs:citation` now emits italicized signals and `Id.` strings before delegating to the substantive macros. Statutes (`tex-statute`), codified rules (`tex-admin-code`/`rule-core` logic embedded in `note-body`), and agency entries all inherit the shared `Id.` behavior (Greenbook ch. 10 at 42–53; ch. 13 at 61–65; ch. 16 at 76–84).
- **Ibid handling audit (2025-03-15).** Re-reviewed `cs:citation` (edition ll. 1102–1138) to map the `position="ibid"` and `position="ibid-with-locator"` branches that govern how statutes, rules, and administrative entries inherit the shared `Id.` cue. Confirmed that legislation and regulation cites fall back to the default `note-body` output whenever citeproc supplies either ibid position, keeping their behavior aligned with Greenbook ch. 10 short-form guidance (pp. 42–44) even though bespoke short-form macros are still pending. Added `statute_id_sequence` fixtures to exercise the eligible/ineligible patterns alongside the existing code examples (`tests.json` ll. 405–429; `expected.txt` ll. 31–38) and captured the passing run in `test-logs/20250315_cross_jur_id.txt`. The audit confirmed that sequential cites without intervening authorities still render identical long-form outputs, reinforcing the need for the upcoming guard task to suppress `Id.` when cross-title jumps occur.
- **Regression coverage.** Added consecutive cite items in `tests.json` for `stat_govt_code`, `tac_rule`, and `rule_civp` so the harness now validates `Id.` strings for codes (§ 2001.003), TAC rules (§ 9.13), and procedural rules (R. 97(e)). `expected.txt` includes the corresponding lines 13, 19, and 22 annotated with the governing chapter citations.
- **Rule short-form check.** citeproc continues to output `Id. R. 97(e).` for the `rule_civp` fixture; expectation updated accordingly while awaiting confirmation from Greenbook ch. 13 (p. 63) that the repeated `R.` aligns with the manual’s examples.
- **Id. guard for code titles (2025-12-01).** Added a `position="ibid"` safeguard in `<citation>` so legislation short cites carrying `collection-title` or `chapter-number` metadata reuse the full code string instead of emitting `Id.`, while constitutional repeats stay eligible for `Id.` per Chapter 9. The guard lives at `texas-greenbook-15th-edition.csl` ll. 1108–1136 and is exercised by the new `stat_rev_civ` repeat fixture plus its annotated expectation line.【F:temp/texas-greenbook-15th-edition.csl†L1108-L1136】【F:temp/tests.json†L386-L409】【F:temp/expected.txt†L27-L35】【F:temp/Greenbook_15thEdition.pdf†L2841-L2878】【F:temp/test-logs/2025-12-01_full-suite-post-guard-aligned.txt†L101-L118】
  - *Fixture update:* Inserted a second cite for `stat_rev_civ` and mirrored the change in `expected.txt` with a short-form guard comment. The dedicated smoke run captured at `test-logs/2025-12-01_short-form-smoke.txt` documents the passing regression and provides a lightweight reproduction trace.【F:temp/tests_short-form_smoke.json†L1-L34】【F:temp/expected_short-form_smoke.txt†L1-L6】【F:temp/test-logs/2025-12-01_short-form-smoke.txt†L1-L24】
  - *Observation:* `tex-code-section` still ignores citeproc locators, so the guarded repeat continues to print `§ 2(a)` even when the follow-up note supplies `§ 2(b)`. Logged a follow-up in `TODO.md` to route locators through the upcoming short-form helper refactor before promoting the next draft.【F:temp/tests.json†L392-L395】【F:temp/test-logs/2025-12-01_full-suite-post-guard-aligned.txt†L105-L118】
- *Locator routing update (2025-12-07):* Added the dedicated `tex-code-section-short` helper so note-mode statutes and rules now prefer citeproc locators (`Locator(label="section", value)`), ensuring repeat cites display the correct subsection (e.g., `§ 2(b)` and `§ 26.06(b)`) instead of echoing the first-reference section. Mirrored the helper across the TOA variants, normalized the regression fixtures to store raw locator values without prefixed symbols, and updated the expectations to capture the new output, citing Greenbook ch. 10 short-form guidance on pp. 42–44 and ch. 13 rule repeats on pp. 61–65 for authority.【F:temp/texas-greenbook-15th-edition.csl†L360-L520】【F:temp/texas-greenbook-15th-toa.csl†L241-L320】【F:temp/tests.json†L392-L425】【F:temp/expected.txt†L11-L35】【F:temp/expected_short-form_smoke.txt†L1-L6】【F:temp/Greenbook_15thEdition.pdf†L168-L212】
- **Jurisdiction cue follow-up (2025-12-01).** Upgraded citeproc-py to 0.6.0 to test whether processor support for `jurisdiction` conditions returned, but the `case_nontex_cross` fixture still rendered “See” instead of “See also.” Captured the diff in `test-logs/2025-12-01_full-suite-pre-guard.txt` before reverting to citeproc-py 0.5.1; a pre-processing hook remains the likely path forward.【F:temp/tests.json†L948-L983】【F:temp/test-logs/2025-12-01_full-suite-pre-guard.txt†L72-L82】【F:temp/test-logs/2025-12-01_full-suite-post-guard-aligned.txt†L268-L296】 Reinstated the 0.5.1 dependency after the experiment so existing expectations remain aligned with earlier runs.

## TOA grouped-leaders regression capture (2025-12-08)
- Executed `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt --mode bibliography` and archived the diff output under `test-logs/2025-12-08_toa_grouped_leaders_diff.txt`. The run reiterated that only 13 authorities render today even though the expectation file lists 17 entries.【F:temp/test-logs/2025-12-08_toa_grouped_leaders_diff.txt†L1-L54】【F:temp/expected_toa_grouped_leaders.txt†L1-L17】
- Compared the new diff against the historical `20250506_toa_grouped_leaders.txt` capture to verify that four authorities disappeared: Tex. Tax Code Ann. § 26.06(a), Tex. Gov’t Code Ann. § 311.021(1) (West 2023), Tex. R. Civ. P. 97(d)/21, and the administrative trio covering 4 Tex. Admin. Code § 9.12, 16 Tex. Admin. Code § 25.101, 1 Tex. Admin. Code § 3.5, plus the 39 Tex. Reg. 573, 574 register entry. The remaining dataset shifted upward, confirming the fixtures—not the CSL logic—dropped the references after the 2025-05-06 baseline.【F:temp/test-logs/2025-12-08_toa_grouped_leaders_diff.txt†L22-L54】【F:temp/test-logs/20250506_toa_grouped_leaders.txt†L1-L40】【F:temp/test-logs/20250506_toa_grouped_leaders.txt†L40-L80】
- Logged a reminder in `TODO.md` under “Restore TOA fixture ordering” enumerating each missing fixture ID so the restoration work can proceed alongside the dataset expansion tasks.【F:temp/TODO.md†L359-L375】

## TOA fixture restoration (2025-12-08)
- Rebuilt the TOA dataset to include all 17 authorities expected by the grouped-leaders baseline, adding dedicated entries for the Government Code construction statute, Tex. R. Civ. P. 21, and the two administrative rules that dropped after May 2025. Each addition carries a `comment` pointer back to the controlling Greenbook page for quick traceability.【F:temp/tests_toa.json†L83-L142】
- Normalized existing statute and rule fixtures by removing TOA page placeholders from the `locator` field so the new locator-aware helpers continue to emit section strings instead of the table page numbers. The admin code and register entries now rely on `issued`, `note`, and `authority` metadata to reproduce the layered parentheticals described in Chapter 16.【F:temp/tests_toa.json†L112-L168】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L204-L448】【F:temp/Greenbook_15thEdition.pdf†L1718-L1905】
- Verified the restored dataset against the legacy expectation file—`python temp/run_tests.py ... --expected temp/expected_toa_grouped_leaders.txt --mode bibliography`—and captured a passing log confirming that every line now matches and the warning about missing citations has cleared.【F:temp/test-logs/2025-12-08_toa_grouped_leaders_post-fixture.txt†L1-L58】
- Regenerated every TOA expectation file with the new `--write-expected` flag to keep the fixtures in sync across grouped, leaders, by-reporter, and base variants; all writes were idempotent, so no diffs appeared, and the console transcripts are stored for future audits.【F:temp/run_tests.py†L27-L120】【F:temp/test-logs/2025-12-08_toa_grouped_leaders_write-expected.txt†L13-L17】【F:temp/test-logs/2025-12-08_toa_grouped_write-expected.txt†L13-L17】【F:temp/test-logs/2025-12-08_toa_leaders_write-expected.txt†L13-L17】【F:temp/test-logs/2025-12-08_toa_by-reporter_write-expected.txt†L13-L17】【F:temp/test-logs/2025-12-08_toa_write-expected.txt†L13-L17】

## Short-form fixture verification (2025-12-09)
- Executed the dedicated smoke suite (`tests_short-form_smoke.json`) to ensure the statute, administrative code, and jurisdictional signal helpers continue to emit the condensed forms documented in Chapters 10 and 16. The log `test-logs/20251209_short-form_smoke_verification.txt` captures the passing run.【F:temp/test-logs/20251209_short-form_smoke_verification.txt†L1-L24】【F:temp/tests_short-form_smoke.json†L1-L34】
- Confirmed the `statute_short_smoke` sequence mirrors the Chapter 10 format guide for codified statutes, including locator hand-off from § 26.06(a) to § 26.06(b).【F:temp/tests_short-form_smoke.json†L2-L17】【F:temp/Greenbook_15thEdition.pdf†L2866-L3145】
- Verified the `admin_short_smoke` entries reproduce the Chapter 16 administrative short form with agency parenthetical and locator pivot, matching the appendix-abbreviated text.【F:temp/tests_short-form_smoke.json†L18-L29】【F:temp/Greenbook_15thEdition.pdf†L4150-L4372】
- Spot-checked the `statute_note_signal_smoke` pair to ensure prefatory signals (“Cf.” note) continue to flow into the short form without duplicating the code string, aligning with the signal guidance in Chapter 1.【F:temp/tests_short-form_smoke.json†L30-L34】【F:temp/Greenbook_15thEdition.pdf†L246-L310】

## Expected.txt regeneration (2025-12-09)
- Ran the full note regression prior to rewriting expectations and stored the output in `test-logs/20251209_full-suite_pre-write.txt` to baseline statute and rule citations.【F:temp/test-logs/20251209_full-suite_pre-write.txt†L1-L440】
- Compared the statute/rule fixtures (`stat_govt_code`, `stat_penal_code`, `stat_rev_civ`, `tac_rule`, `rule_civp`) against Chapters 10 and 13 to confirm punctuation, abbreviations, and locator updates remain consistent with the Greenbook examples.【F:temp/tests.json†L318-L432】【F:temp/Greenbook_15thEdition.pdf†L2866-L3145】【F:temp/Greenbook_15thEdition.pdf†L3515-L3668】
- Documented the lone divergence—citeproc still emits “See” instead of “See also” for the non-Texas `people_duran_cross` repeat—under the new TODO entry so the jurisdiction-aware preprocessing work can revisit the signal requirement.【F:temp/test-logs/20251209_full-suite_pre-write.txt†L353-L364】【F:temp/TODO.md†L308-L317】【F:temp/Greenbook_15thEdition.pdf†L246-L310】
- Rewrote `expected.txt` using `--write-expected` (log: `test-logs/20251209_full-suite_write-expected.txt`) to align the fixtures with the current citeproc output, ensuring future diffs only reflect purposeful changes.【F:temp/test-logs/20251209_full-suite_write-expected.txt†L1-L441】【F:temp/expected.txt†L70-L82】
- Linked fixture IDs to manual pages in this note so future audits can reconcile outputs quickly; no additional reviewer sign-off was required after recording the jurisdiction cue limitation for later remediation.【F:temp/tests.json†L318-L432】【F:temp/Greenbook_15thEdition.pdf†L2866-L3145】【F:temp/Greenbook_15thEdition.pdf†L3515-L3668】

## Statute and rule abbreviation inventory (2025-12-09)
- **Scope.** Re-read Greenbook Chapters 10–13 and Appendix A to log every abbreviation that the Format Guides and narrative rules require for statutes, session laws, municipal ordinances, procedural rules, and historical reporters. This pass focused on variations tied to jurisdiction (Texas statewide vs. municipal vs. historical) and publication timing (pamphlet editions, supplements, repealed material).
- **Output.** The tables below consolidate the authoritative abbreviations, the conditions that change their form, and pinpoint citations so future helper and locale work can reference a single inventory.【F:temp/Greenbook_15thEdition.pdf†L2866-L3145】【F:temp/Greenbook_15thEdition.pdf†L3193-L3364】【F:temp/Greenbook_15thEdition.pdf†L3415-L3511】【F:temp/Greenbook_15thEdition.pdf†L3505-L3668】【F:temp/Greenbook_15thEdition.pdf†L4150-L4372】【F:temp/Greenbook_15thEdition.pdf†L5118-L5199】

| Category | Abbreviation / term | Variation & jurisdiction notes | Source (Greenbook) | Example |
| --- | --- | --- | --- | --- |
| Subject matter code citation | `Tex. [Code] Code Ann.` | Abbreviate the subject label per Appendix H; omit `Ann.` for unannotated reprints; include `(pamphlet)` for pre-2014 Estates Code printings. | Ch. 10 Format Guide, p. 42; Ch. 10.2.1–10.2.2(e), pp. 46–47; Appendix H.1, p. 116. | `Tex. Tax Code Ann. § 26.06(a)`; `Tex. Est. Code Ann. § 201.001 (pamphlet).` |
| Uncodiﬁed statutes | `Tex. Rev. Civ. Stat. Ann.` plus `art.`/`arts.` | Use `art.`/`arts.` for numbered articles; retain section symbol inside the article string when citing subsections. | Ch. 10 Format Guide, p. 42; Ch. 10.1.4, p. 45; Ch. 10.2.3, p. 47. | `Tex. Rev. Civ. Stat. Ann. art. 5415e-4, § 2(a).` |
| Independent code citation | `Tex. Code Crim. Proc. Ann.` et al. | Confirm provision still in force; Business Corporation Act and Probate Code remain valid only for pre-recodification transactions. | Ch. 10.2.4, p. 48; Appendix H.2, p. 117. | `Tex. Code Crim. Proc. Ann. art. 13.25(a).` |
| Auxiliary laws pamphlets | `Tex. [Code] Aux. Laws` | Append bracketed session law for non-general statutes; omit brackets for general/permanent water laws that stay in the pamphlet. | Ch. 10.2.5, p. 48. | `Tex. Educ. Aux. Laws art. 2668b [Act of Mar. 28, 1963, 58th Leg., R.S., ch. 39, 1963 Tex. Gen. Laws 59].` |
| Session laws | `Act of [date], [Leg.], [session], ch. [chapter], §/sec. […]` with `Tex. Gen. Laws` or `Tex. Sess. Law Serv.` | Use `R.S.` for regular sessions and ordinal + `C.S.` for called sessions; add `(to be codiﬁed at …)` or `(current version at …)` where required. Appendix I supplies historic session labels (`Adj. S.`, `Prov. S.`). | Ch. 10.3.1–10.3.5, pp. 49–51; Appendix I, p. 118. | `Act of May 30, 2005, 79th Leg., R.S., ch. 268, § 1.06, 2005 Tex. Gen. Laws 621, 623 (codiﬁed at Tex. Fam. Code § 107.013(c)).` |
| Municipal codes | `[City], Tex., [Code name]` | Include full municipality plus state; cite chapter/article/section; add year parenthetical for codified sets and ordinance number plus adoption date for uncodified laws. | Ch. 10.6.1–10.6.2, pp. 52–53. | `Hous., Tex., Code of Ordinances ch. 20, art. IV, § 20-216 (1968)`; `Plano, Tex., Temporary Signs Ordinance (Nov. 14, 2005).` |
| Interpretive comments | `cmt.`, `revisor’s note`, `historical note`, `U.C.C. cmt.` | Keep descriptor lowercase; historical notes require bracketed session-law provenance; retain publisher year (e.g., `West 1982`). | Ch. 12 Format Guide, p. 58; Ch. 12.1–12.2, pp. 58–59. | `Tex. Agric. Code Ann. § 14.123 revisor’s note (West 1982)`; `Tex. Nat. Res. Code Ann. § 52.024 historical note (West Supp. 1997) […].` |
| Procedural rules | `Tex. R. Civ. P.`, `Tex. R. App. P.`, `Tex. R. Jud. Admin.`, `Tex. R. Evid.` | Append parenthetical with promulgating court and amendment year when citing source publications; TOA variants rely on same abbreviations. | Ch. 13 Format Guide, p. 61; Ch. 13.2, p. 63; Appendix H.3, p. 117. | `Tex. R. App. P. 9, 49 Tex. B.J. 561 (Tex. & Tex. Crim. App. 1986, amended 1997).` |
| Local court rules | `Loc. R.` with court and county list | Prepend court name plus `(Tex.)`; include county parenthetical when rule spans multiple counties. | Ch. 13.4, p. 65. | `220th (Tex.) Dist. Ct. Loc. R. 1.6 (Bosque, Comanche, and Hamilton Counties).` |
| Historical case reporters | `Tex.`, `Tex. Supp.`, `Robards`, `Dallam`, `Texas L. Rev.` reprints | Use Texas Reports citation alone for 1846–1886 cases; supply term-year when no year is printed; parallel cite Civil War conscript cases to Robards; cite Republic decisions to Dallam or the 1986 Texas Law Review reprint. | Appendix A, pp. 98–99. | `Fox v. Woods, 35 Tex. 220, 220 (1870–1871)`; `Ex parte Coupland, 26 Tex. 386, 387, Robards 5, 6 (1862)`; `Lamar v. Houston (Tex. 1845), 65 Tex. L. Rev. 382, 383 (Paulsen rep. 1986).` |

### Appendix H subject-matter code crosswalk (p. 116)

| Code | Abbreviation | Notes |
| --- | --- | --- |
| Agriculture | Tex. Agric. Code Ann. | Texas statewide subject-matter code; drop `Ann.` for unannotated printings. |
| Alcoholic Beverage | Tex. Alco. Bev. Code Ann. | Same statewide abbreviation used in fixtures and macros. |
| Business and Commerce | Tex. Bus. & Com. Code Ann. | Retain ampersand per Appendix H; unannotated reprints omit `Ann.`. |
| Business Organizations | Tex. Bus. Orgs. Code Ann. | Applies post-2010 to all entities; cite pamphlet pre-2010 if encountered. |
| Civil Practice and Remedies | Tex. Civ. Prac. & Rem. Code Ann. | Maintain `&` conjunction; helper must account for long abbreviation width. |
| Education | Tex. Educ. Code Ann. | No jurisdictional variants noted. |
| Election | Tex. Elec. Code Ann. | Cite supplemental pamphlets with year parenthetical when applicable. |
| Estates | Tex. Est. Code Ann. | Became effective 2014; cite `(pamphlet)` when using the 2013 advance printing. |
| Family | Tex. Fam. Code Ann. | — |
| Finance | Tex. Fin. Code Ann. | — |
| Government | Tex. Gov’t Code Ann. | Apostrophe placement mirrors Appendix H. |
| Health and Safety | Tex. Health & Safety Code Ann. | Retain ampersand per official table. |
| Human Resources | Tex. Hum. Res. Code Ann. | — |
| Insurance | Tex. Ins. Code Ann. | Title 1 still uncodified; confirm part reference when citing pre-revision provisions. |
| Labor | Tex. Lab. Code Ann. | — |
| Local Government | Tex. Loc. Gov’t Code Ann. | Apostrophe-s retained; necessary for locale entry. |
| Natural Resources | Tex. Nat. Res. Code Ann. | — |
| Occupations | Tex. Occ. Code Ann. | — |
| Parks and Wildlife | Tex. Parks & Wild. Code Ann. | Abbreviation shortens “Wildlife” to “Wild.” |
| Penal | Tex. Penal Code Ann. | Unannotated printings drop `Ann.` per Ch. 10.2.1. |
| Property | Tex. Prop. Code Ann. | — |
| Special District Local Laws | Tex. Spec. Dist. Code Ann. | Codification ongoing; verify district placement before citing. |
| Tax | Tex. Tax Code Ann. | — |
| Transportation | Tex. Transp. Code Ann. | — |
| Utilities | Tex. Util. Code Ann. | — |
| Water | Tex. Water Code Ann. | Auxiliary pamphlet may supplement per Ch. 10.2.5. |

### Appendix H independent codes (p. 117)

| Code | Abbreviation | Notes |
| --- | --- | --- |
| Criminal Procedure | Tex. Code Crim. Proc. Ann. | Remains the operative reference until the Criminal Procedure Code recodification is enacted. |
| Insurance (Title 1) | Tex. Ins. Code Ann. | Shared with subject-matter list; ensure Title 1 context is clear in parentheticals. |
| Probate | Tex. Prob. Code Ann. | Historical; cite only for pre-2014 matters, otherwise prefer Estates Code. |
| Business Corporations | Tex. Bus. Corp. Act Ann. | Legacy corporate filings; include applicability year if material predates 2010 Business Organizations migration. |

### Appendix H current rules (p. 117)

| Ruleset | Abbreviation | Notes |
| --- | --- | --- |
| Rules of Civil Procedure | Tex. R. Civ. P. | Matches Format Guide example; supplements carry amendment year parenthetical. |
| Rules of Judicial Administration | Tex. R. Jud. Admin. | Include reprint parenthetical when citing Gov’t Code appendix. |
| Rules of Appellate Procedure | Tex. R. App. P. | Appendix for criminal cases requires additional label (e.g., `Tex. R. App. P. Crim. app.`). |
| Rules of Evidence | Tex. R. Evid. | Pre-1998 variants handled via Appendix K guidance. |
| State Bar Rules | Tex. State Bar R. | Cite location within Gov’t Code appendix for first reference. |
| Disciplinary Rules of Professional Conduct | Tex. Disciplinary Rules Prof’l Conduct | Maintain apostrophe placement; cite promulgation year when relevant. |
| Rules of Disciplinary Procedure | Tex. Rules Disciplinary P. | Use when referencing Board of Disciplinary Appeals procedures. |
| Code of Judicial Conduct | Tex. Code Jud. Conduct | Applicable to statewide judiciary; cite amendment year if supplied. |
| Rules for the Removal or Retirement of Judges | Tex. Rules Rem’l/Ret. Judg. | Confirm tribunal context in parenthetical when citing proceedings. |
| Rules Governing Admission to the Bar | Tex. Rules Govern. Bar Adm’n | Include article/section plus adoption date where relevant. |

### Appendix A reporter abbreviations (pp. 98–99)

- Texas Reports citations omit parallel reporters before 1886; supply the term-year when the bound volume lacks a printed year (e.g., `1870–1871`).
- Civil War conscript decisions receive parallel cites to Robards’s *Synopses* when the Texas Reports volume omits them; uncodified opinions that never appeared in the Texas Reports must be cited to Robards alone.
- Republic-era cases use Dallam’s Digest (1845 printing) and, for 1845 term opinions, the 1986 *Texas Law Review* Sesquicentennial reprint credited to Paulsen.【F:temp/Greenbook_15thEdition.pdf†L5126-L5199】

## Legacy Draft 3 Update – Parenthetical Metadata Helpers (2025-03-24)
- **Slip opinions and original proceedings.** Added a shared `parenthetical-docket` block and `parenthetical-procedural-status` chain so Greenbook slip citations now surface cause numbers, Westlaw/Lexis identifiers, and procedural posture straight from Zotero’s `number`, `collection-number`, `status`, and `note` fields (Greenbook ch. 2 at 7 & ch. 6 at 31–33). The helper skips `note` values that double as cross-reference cues, keeping `See also` triggers confined to the `cross-reference-cue` macro.
- **Memorandum and rehearing designations.** Normalized weight parentheticals to pull `genre` and `medium` in a consistent order, which allows memorandum opinions and rehearing dispositions to mirror chapter 4 examples without duplicating logic inside the case, mandamus, and trial-court macros (Greenbook ch. 4 at 24–25).
- **Trial-court docket metadata.** Reused the docket helper across trial-level items so cause numbers and underlying trial-court numbers land before the court/date parenthetical while `note` supplies record-type phrases such as “prelim. injunction order” (Greenbook ch. 7 at 34–35).

## Parenthetical macro audit (2025-11-05)
- **Search inventory.** Ran `rg "parenthetical" temp -n --glob '*.csl'` and archived the output to `reports/parenthetical_macro_scan.txt` to baseline every live parenthetical helper across the edition and TOA variants (`texas-greenbook-15th-edition.csl` ll. 56–159; `texas-greenbook-15th-toa.csl` ll. 26–112; grouped/leader variants mirror those definitions). The scan confirmed no lingering references in the archived drafts beyond historical comments.
- **Invocation map.**
  - `parenthetical-docket` (edition ll. 56–65) feeds directly into `reporter-wl` (ll. 67–69), so every `legal-case-*` branch that falls back to Westlaw output inherits cause and docket data before reporter text. The TOA styles replicate the group logic inline instead of calling the helper (`texas-greenbook-15th-toa.csl` ll. 27–33), highlighting reuse opportunities once shared modules are introduced.

## Rule locator locale gap fix (2025-11-07)
- **Reproduction.** Running `python temp/run_tests.py --mode notes` against `tests.json` failed at citation #31 (`rule_civp`) with `AttributeError: 'NoneType' object has no attribute 'single'` because `<label variable="locator" form="symbol"/>` attempts to resolve the `rule` term without a symbol variant. The failing cite corresponds to the short-form example in Greenbook ch. 13 at 63 (Tex. R. Civ. P. 97(e)).
- **Locale update.** Added `<term name="rule" form="symbol">R.</term>` plus ordinal suffixes (`ordinal-01`–`ordinal-04`) to both the inline locale in `texas-greenbook-15th-edition.csl` and the shared `locales/locales-en-US-x-texas-greenbook.xml` so citeproc can emit the Greenbook short label while preserving treatise ordinals described in ch. 18 at 93–95.
- **Verification.** Re-ran the full note suite via `python temp/run_tests.py --mode notes`, confirmed all 64 expectations match, and archived the output under `test-logs/2025-11-07_rule-locator-locale-fix.txt` for reviewer reference.
  - `parenthetical-procedural-status` (edition ll. 107–115) injects status/note metadata through `court-and-date` (ll. 118–140). That macro is invoked by the first, short, and cross-reference case routes (ll. 258–321) in both note and bibliography contexts, ensuring trial/memo designations travel with the court/year parenthetical.
  - `parenthetical-slip-op` and the enclosing `case-parenthetical-stack` (edition ll. 143–157) are appended immediately after `court-and-date` inside the case macros, while `explanatory-parenthetical` (ll. 159–164) also services `book-like-*` helpers (ll. 504–528). Bibliography macros for books omit this stack entirely (`book-like-bibliography`, ll. 531–546), which explains the trimmed descriptive tails in long-form lists.
- **Note vs. bibliography comparison.** Rendered the regression fixtures in both modes to capture baseline punctuation (`test-logs/parenthetical-baseline.txt`; `test-logs/bibliography-blank.txt`).
  - Case citations match verbatim between notes and bibliography because `cs:bibliography` delegates to `legal-case-first`, so parenthetical cues like `(per curiam)` and `(mem. op.)` persist in both outputs (compare lines 4–23 of the bibliography log with lines 1–23 of the note log).
  - Secondary authorities diverge: note-mode books and CLE materials retain explanatory parentheticals sourced from `abstract` (`parenthetical-baseline.txt` ll. 130–141), while bibliography mode drops them due to the leaner `book-like-bibliography` macro, producing author-led strings without the trailing descriptive clause (`bibliography-blank.txt` ll. 25–36). Periodical and web entries likewise swap comma-delimited note syntax for sentence-form bibliography layout, so any future helper sharing must account for the format shift rather than forcing a single string template.
  - The citeproc run emitted benign warnings about unsupported `reviewed_title`/`label` keys; no output regressions surfaced, but the metadata reminder is logged here for translators coordinating fixture updates.
- **2025-11-05 parenthetical baseline refresh.** Re-ran the consolidated note fixtures with `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt` and captured the output at `test-logs/20251105_parenthetical-notes.txt`. A companion run with `--mode bibliography` logged the bibliography rendering to `test-logs/20251105_parenthetical-bibliography.txt` for side-by-side inspection.
  - Citeproc emitted the same warnings about unsupported `reviewed-title` and `label` fields that appear in earlier audits. Treat them as informational—they confirm the processor ignores our metadata shims without altering output.
  - Bibliography mode currently reports `DIFF` after the first entry because the harness still compares against note-oriented expectations. This highlights a fixture gap rather than a formatting regression; future bibliography baselines should resolve the false positives before helper refactors land.
  - Spot-checked the refreshed note log against the 2025-03-17 memo audit to ensure slip opinions, memorandum opinions, and trial-court orders still output `(per curiam)`, `(mem. op.)`, and record-type parentheticals verbatim.
- **Parenthetical coverage review (2025-11-05).**
  - Confirmed coverage for Westlaw slip opinions carrying docket metadata and mandamus relief parentheticals (`tests.json` items `case_slip_opinion`, `case_trial_court`).
  - Memorandum opinions with rehearing indicators and Westlaw numbers remain represented via `case_mem_rehearing` and `case_wl_unpub`.
  - Trial-level orders continue to rely on `note` for record descriptors such as “prelim. injunction order,” and explanatory parentheticals sourced from `abstract` appear across cases and secondary authorities.
  - Fixture gaps identified for follow-up: (1) no test renders the Chapter 4 `(not designated for publication)` weight parenthetical (PDF p. 17), (2) no example exercises `genre` values such as `en banc` or `dissenting op.` even though pp. 18–19 call for them in explanatory parentheticals, and (3) bibliography mode lacks dedicated expectations to preserve intentional parenthetical omissions, so helper work must account for the note/bibliography divergence logged above.
- **Parenthetical coverage update (2025-11-19).** Added `case_mem_not_designated` to `tests.json` with expectations in `expected.txt` line 7 to capture the Chapter 4 memorandum opinion example (`Green v. State, No. 12-12-00249-CR, 2012 WL 3116252, at *1 … (mem. op., not designated for publication)`) so the weight-parenthetical helper now exercises the publication-status variant (Greenbook p. 17).【F:temp/tests.json†L87-L109】【F:temp/expected.txt†L7-L9】
- **Parenthetical coverage update (2025-11-19).** Added `case_mem_not_designated` to `tests.json` with expectations in `expected.txt` line 7 to capture the Chapter 4 memorandum opinion example (`Green v. State, No. 12-12-00249-CR, 2012 WL 3116252, at *1 … (mem. op., not designated for publication)`) so the weight-parenthetical helper now exercises the publication-status variant (Greenbook p. 17).【F:temp/tests.json†L87-L109】【F:temp/expected.txt†L7-L9】

## Parenthetical helper consolidation (2025-11-20)
- **Renamed helper surface.** Replaced the legacy `docket-parenthetical`, `procedural-parenthetical`, and `weight-parentheticals` macros with `parenthetical-docket`, `parenthetical-procedural-status`, and `parenthetical-slip-op` so the naming now reflects the helper purpose. Each macro preserves the Greenbook-driven sequencing captured in Chapters 2, 4, 6, and 7 (pp. 7, 24–25, 31–33, 34–35) while centralizing status strings and memorandum/slip indicators in a single stack.【F:temp/texas-greenbook-15th-edition.csl†L56-L164】
- **Shared TOA routing.** Copied the new helper names into every TOA variant (`texas-greenbook-15th-toa*.csl`) and pointed the case macros at `case-parenthetical-stack` so docket strings, memorandum designations, and explanatory parentheticals are consistently assembled regardless of output mode. That alignment eliminates the duplicated `No.`/Westlaw formatting noted in the 2025-11-05 audit and keeps TOA citations ready for future slip-opinion enhancements.【F:temp/texas-greenbook-15th-toa.csl†L20-L135】【F:temp/texas-greenbook-15th-toa-grouped.csl†L48-L162】【F:temp/texas-greenbook-15th-toa-leaders.csl†L22-L188】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L20-L150】【F:temp/texas-greenbook-15th-toa-by-reporter.csl†L24-L144】
- **Regression confirmation.** Re-ran the full note and TOA suites to confirm the helper rename produced identical output across contexts (`run_tests.py` invocations recorded in `test-logs/20251120_parenthetical-refactor_{notes,toa}.txt`). The harness logs show parity between expected and actual strings in both note mode and every TOA variant, demonstrating the helpers still respect the Greenbook citations above.【0c76c0†L1-L257】【164bf0†L1-L27】【3560c4†L1-L27】【a28910†L1-L27】【b6f7e7†L1-L27】

## Parenthetical ambiguity tracker (2025-11-19)
- **Slip opinion URLs vs. subsequent history (Greenbook p. 36).** Rule 4.1.3(a) requires an `available at` clause after the court parenthetical for unpublished opinions posted on a court website, but it never states how that clause interacts with subsequent history strings or weight-of-authority parentheticals. Current fixtures (`case_slip_baggs`, `case_mandamus_pending`) omit URLs, so the CSL macros have never been forced to order the fragments. *Impact:* **medium** — without guidance we risk emitting `available at` before `mand. granted` or other subsequent history when the helper eventually surfaces URLs. *Follow-up:* stage a research task to compare the Greenbook guidance with the Uniform Format Manual’s slip-opinion ordering and update the TODO backlog with the preferred sequencing pattern.
- **Bracketed mandamus statuses plus weight parentheticals (Greenbook pp. 32–33, 50–51).** The text instructs practitioners to replace petition history with `orig. proceeding` and add bracketed status phrases like `[mand. pending]`, but it does not clarify whether those brackets precede or follow per curiam or memorandum indicators when both appear. Example cites such as `In re Int’l Profit Assocs., Inc.` show `(per curiam) (mem. op.), mand. granted …`, yet Rule 6.2.2’s prose is silent. *Impact:* **medium** — we need a definitive order before extracting shared helpers so we do not shuffle parenthetical tokens during refactors. *Follow-up:* annotate this question in the helper design doc and solicit confirmation from a practitioner familiar with the current Supreme Court docket formatting.
- **Paragraph pinpoint labels for unpublished slips (Greenbook p. 36).** The instruction to use `slip op. ¶` when no pagination exists does not explain whether the `¶` symbol belongs in the pinpoint or in the case name block, nor does it specify the abbreviation when the opinion uses section headings instead of numbered paragraphs. *Impact:* **high** — failure to disambiguate will leave Zotero exports without a predictable field to feed into `Locator`, complicating short-form automation. *Follow-up:* review recent appellate PDF layouts and, if necessary, consult the Uniform Format Manual to determine whether an en-dash or em-dash convention controls paragraph references; open a TODO once the preferred metadata mapping is identified.

### Slip/mandamus/habeas fixture metadata audit (2025-11-19)
| Scenario | Required Greenbook elements | CiteProc JSON fields | Availability check |
| --- | --- | --- | --- |
| Court of appeals slip opinion with Westlaw cite (`Baggs v. Becker`, Rule 4.1.3) | Cause number, Westlaw cite, pinpoint page, city/date parenthetical, weight parenthetical | `number`, `collection-number`, `locator`, `authority`, `issued`, `status`, `medium` | All captured in `case_slip_baggs`; Zotero schema already exposes each field.【F:temp/tests.json†L162-L181】 |
| Mandamus petition pending in Supreme Court (`In re Luna`, Rule 6.2.2) | Cause number, Westlaw cite, pinpoint, `orig. proceeding [mand. pending]` status | `number`, `collection-number`, `locator`, `authority`, `issued`, `status` | Implemented in `case_mandamus_pending`; bracket text stored in `status` for downstream helpers.【F:temp/tests.json†L182-L201】 |
| Habeas subsequent history string (`Massoth v. State`, Rule 4.5.1) | Westlaw cite, weight parenthetical, subsequent history with `habeas corpus granted in part sub nom.` | `collection-number`, `medium`, `status`, `references` | Encoded in `case_habeas_massoth`; `references` carries the follow-on cite for citeproc comparisons.【F:temp/tests.json†L202-L220】 |

- **Field validation.** Running `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt` confirmed citeproc renders each scenario with the new metadata in place, so the CSL helpers recognize the added fields without schema updates.【af85a2†L1-L169】

### Fixture coverage matrix (2025-11-19)
| Fixture ID | Test JSON line(s) | Expected output line | Greenbook citation | Coverage notes |
| --- | --- | --- | --- | --- |
| `case_slip_baggs` | 162–181 | 11 | Ch. 4, pp. 17–18 | Validates basic COA slip format and memoranda designation without per curiam flag.【F:temp/tests.json†L162-L181】【F:temp/expected.txt†L11-L13】 |
| `case_mandamus_pending` | 182–201 | 12 | Ch. 6, p. 50 | Exercises bracketed `[mand. pending]` status inside the procedural parenthetical.【F:temp/tests.json†L182-L201】【F:temp/expected.txt†L11-L13】 |
| `case_habeas_massoth` | 202–220 | 13 | Ch. 4, p. 25 | Ensures subsequent history strings for habeas relief persist in note form instead of short-form truncation.【F:temp/tests.json†L202-L220】【F:temp/expected.txt†L11-L13】 |

- **Open gaps.** No fixture yet captures the `available at` URL requirement for slip opinions posted on court websites or the paragraph pinpoint form described in Rule 4.1.3(a). Record a follow-up TODO once we confirm the desired CSL field mapping so helpers can emit the missing strings without hard-coded hacks.
- **Duplication hotspots and standardization ideas.**
  - Each TOA variant declares its own `parenthetical-slip-op` macro with identical logic (`texas-greenbook-15th-toa*.csl` ll. 54–113). Hoisting the helper into a shared include or aligning on a consistent namespace would eliminate four copies and simplify future additions like `(not designated for publication)` toggles.
  - TOA `reporter-wl` nodes manually stitch `No.` and cause numbers (e.g., `texas-greenbook-15th-toa.csl` ll. 27–33) instead of reusing `parenthetical-docket`. Extracting that chunk into a shared helper would guarantee docket formatting stays synchronized once slip-opinion enhancements land.
  - Aligning the book/secondary bibliography macros with the explanatory helper will require optional parameters so bibliographies can suppress parentheticals without losing access to the wording. Draft plan: introduce a `explanatory-parenthetical` boolean flag passed into the helper and gate the appended group accordingly, leaving bibliography layout otherwise unchanged.
  - Prioritize consolidating the TOA helper duplication after the pending parenthetical refactor lands (P1), while the bibliography flag work can trail once short-form statute tasks unblock (P2). Fixture updates will need to cover TOA slip opinions and bibliography treatises when the refactor occurs, so note those dependencies when scheduling the helper extraction.

## Explanatory parenthetical catalog (2025-11-20)

- **Slip opinion (Westlaw cite; court/date parenthetical required).** `Am. K-9 Detection Servs., LLC v. Freeman, No. 15-0932, 2018 WL 3207134, at *3 (Tex. June 29, 2018).` Parenthetical cues supply the court (`Tex.`) and the exact decision date, which the text flags as mandatory for current slip opinions published electronically.
- **Slip opinion with website pagination.** `City of Keller v. Wilson, No. 02-1012, slip op. at 2 (Tex. June 10, 2005), available at http://www.search.txcourts.gov/historical/2005/jun/021012.pdf.` The `slip op.` locator preceding the pinpoint and the `available at` URL clause are both mandated when the Court posts a paginated PDF.
- **Texas Supreme Court Journal parallel cite.** `Texas Dep’t of State Health Servs. v. Crown Distrib., 65 Tex. Sup. Ct. J. 1630, 1630, 2022 WL 2283170, at *1 (June 24, 2022).` The instructions note that the court designation is omitted as redundant in this configuration, highlighting an optional element normally present in the parenthetical.
- **Mandatory vs. optional elements.**
  | Element | Status | Source |
  | --- | --- | --- |
  | Court-and-date parenthetical (`(Tex. June 29, 2018)`) | Mandatory for slip opinions | PDF p. 26 |
  | Pinpoint to electronic reporter (`at *3`) | Mandatory | PDF p. 26 |
  | `slip op.` locator | Optional only when citing the case generally | PDF p. 26 |
  | `available at` URL clause | Mandatory for court-website copies | PDF p. 26 |
  - No ambiguous directives flagged; the chapter explicitly labels each requirement with “must” or “no need,” so no legal review follow-up is required.
  - CSL mapping: these cues surface through `legal-case-first`/`legal-case-short` combined with `reporter-wl`, `court-and-date`, and `case-parenthetical-stack` in `texas-greenbook-15th-edition.csl`. Slip-opinion URLs currently flow through `reporter-wl`, so any helper sharing should anchor there.
  - Shared helper opportunity: align the slip-opinion URL handling with the Courts-of-Appeals branch so a single helper can inject `slip op.` locators and `available at` clauses across authority levels.
  - Test coverage: `tests.json` fixtures `case_supreme` and `case_slip_opinion` exercise the slip-opinion chains and the `available at` handling noted above.

- **Memorandum opinion with publication status.** `Massoth v. State, No. 14-03-00605-CR, 2004 WL 1381027, at *1 (Tex. App.—Houston [14th Dist.] June 22, 2004, pet. ref’d) (mem. op., not designated for publication), habeas corpus granted in part sub nom. Ex parte Massoth, No. AP-75215, 2005 WL 1774115, at *1 (Tex. Crim. App. July 27, 2005) (per curiam) (not designated for publication).` This example demonstrates consecutive parenthetical cues for memorandum weight and publication status, plus a separate subsequent-history parenthetical from the Court of Criminal Appeals.
- **Slip opinion paragraph pinpoint.** `Powell v. State, No. PD-0051-05, slip op. ¶ 2 (Tex. Crim. App. Apr. 5, 2006), available at http://search.txcourts.gov/Case.aspx?cn=PD-0051-05&coa=coscca.` The chapter clarifies that paragraph pinpoints (`¶ 2`) replace page pinpoints when pagination is absent; the `slip op.` designation becomes optional only when citing the case generally (PDF p. 30).
- **Mandatory vs. optional elements.**
  | Element | Status | Source |
  | --- | --- | --- |
  | `(mem. op.)` weight parenthetical | Mandatory whenever opinion designated memorandum | PDF p. 28 |
  | `(not designated for publication)` | Mandatory when publication status so indicates | PDF p. 28 |
  | Paragraph/page pinpoint plus `available at` URL | Mandatory for slip opinions without pagination | PDF p. 30 |
  | `slip op.` designation | Optional only for general cites without pinpoint | PDF p. 30 |
  - No ambiguous guidance noted; chapter text clearly distinguishes “must” and “may,” so no escalation required.
  - CSL mapping: the cues route through `legal-case-first`, `case-parenthetical-stack`, and `related-proceedings`; memorandum and publication tags live inside `parenthetical-slip-op` and `explanatory-parenthetical` macros that also feed the TOA variants.
  - Shared helper opportunity: consider consolidating slip-opinion paragraph handling with the Supreme Court branch so `reporter-wl` can inject `¶` locators regardless of jurisdiction.
  - Test coverage: `tests.json` entries `case_crim_app` and `case_slip_opinion` cover memorandum status, publication cues, and paragraph pinpoints for Court of Criminal Appeals authorities.

- **Per curiam memorandum opinion.** `Richardson v. Kays, No. 02-03-241-CV, 2003 WL 22457054, at *1 (Tex. App.—Fort Worth Oct. 30, 2003, no pet.) (per curiam) (mem. op.).` The layered parentheticals illustrate that the per curiam designation precedes the memorandum notation when both apply.
- **Memorandum opinion with publication status.** `State v. Wise, No. 04-04-00695-CR, 2005 WL 2952357, at *1 (Tex. App.—San Antonio Oct. 26, 2005, no pet.) (mem. op., not designated for publication).` The comma-separated cues inside a single parenthetical confirm the combined formatting mandated for cases that are both memorandum opinions and unpublished.
- **Recent decision slip opinion with URL.** `Jenkins v. State, No. 03-13-0632-CR, slip op. at 2 (Tex. App.—Austin Oct. 25, 2013, no pet. h.) (mem. op., not designated for publication), available at http://www.search.txcourts.gov/SearchMedia.aspx?MediaVersionID=9a9e6403-aac0-45ac-8e31-27c4d2fd8a33&MediaID=a0ea946d-bccf-4336-9228-581bd0b046c5&coa=%22%20+%20this.CurrentWebState.CurrentCourt%20+%20@%22&DT=Opinion.` The chapter requires retaining both the memorandum and publication-status cues alongside the slip-opinion pinpoint and URL.
- **Mandatory vs. optional elements.**
  | Element | Status | Source |
  | --- | --- | --- |
  | `(per curiam)` | Mandatory when court issues per curiam opinion | PDF p. 34 |
  | `(mem. op.)` | Mandatory when court labels opinion memorandum | PDF p. 34 |
  | `(not designated for publication)` | Mandatory for unpublished designations | PDF pp. 34–35 |
  | `slip op.` plus pinpoint and `available at` URL | Mandatory for recent decisions posted online | PDF pp. 35–36 |
  | `slip op.` text | Optional when citing case generally without pinpoint | PDF p. 36 |
  - No ambiguous directives surfaced; instructions differentiate “must” vs. “no need,” so no open questions remain.
  - CSL mapping: `legal-case-first`, `case-parenthetical-stack`, `parenthetical-slip-op`, and `related-proceedings` macros emit these cues, while slip-opinion URLs flow through `reporter-wl` and `parenthetical-docket` in the edition file.
  - Shared helper opportunity: unify memorandum/publish-status handling between note and TOA styles via a shared `parenthetical-slip-op` helper to eliminate duplication documented earlier in this file.
  - Test coverage: `tests.json` fixtures `case_app_hou14`, `case_mem_not_designated`, and `case_slip_opinion` validate the memorandum, publication-status, and slip-opinion behaviors.

- **Origination tag in parenthetical.** `Flores v. Fourth Court of Appeals, 777 S.W.2d 38, 39 (Tex. 1989) (orig. proceeding).` The separate parenthetical marks mandamus posture for Texas Supreme Court original proceedings.
- **Pending mandamus status.** `In re Luna, No. 01-03-01055-CV, 2004 WL 2005935, at *1 (Tex. App.—Houston [1st Dist.] Sept. 9, 2004, orig. proceeding [mand. pending]).` Bracketed status must follow `orig. proceeding` when the Texas Supreme Court has not resolved the petition.
- **Mandamus granted as subsequent history.** `Contico Int’l, Inc. v. Alvarez, 910 S.W.2d 29, 32 (Tex. App.—El Paso 1995, orig. proceeding), mand. granted sub nom. Mendoza v. Eighth Court of Appeals, 917 S.W.2d 787, 789 (Tex. 1996) (per curiam).` The chapter instructs authors to prefix the Supreme Court citation with `mand. granted` whenever relief is awarded.
- **Leave granted then denied.** `Gen. Motors Corp. v. Gayle, 924 S.W.2d 222, 224 (Tex. App.—Houston [14th Dist.] 1996, orig. proceeding), leave granted, mand. denied, 940 S.W.2d 598, 599 (Tex. 1997) (per curiam).` Bracketed notations such as `[leave denied]` or sequential `leave granted, mand. denied` phrases are mandatory to capture procedural history (PDF p. 51).
- **Mandatory vs. optional elements.**
  | Element | Status | Source |
  | --- | --- | --- |
  | `(orig. proceeding)` parenthetical | Mandatory for mandamus/original proceeding cites | PDF pp. 49–50 |
  | Bracketed outcomes (`[mand. pending]`, `[mand. denied]`, `[leave denied]`) | Mandatory whenever Supreme Court action occurs | PDF pp. 50–51 |
  | `mand. granted` / `mand. denied` subsequent history strings | Mandatory when Supreme Court resolves relief | PDF pp. 50–51 |
  | Combined `leave granted, mand. denied` phrases | Mandatory when both actions occurred | PDF p. 51 |
  - No ambiguous wording detected; chapter supplies prescriptive phrases, so no follow-up tasks needed.
  - CSL mapping: `related-proceedings`, `case-parenthetical-stack`, and `court-and-date` macros in the note style emit these cues; TOA counterparts reuse the same logic inline and should be refactored to call the shared helper once extracted.
  - Shared helper opportunity: expose a reusable “mandamus-status” helper so courts of appeals, Supreme Court, and TOA variants all source bracketed outcomes from a single macro.
  - Test coverage: `tests.json` fixtures `case_slip_opinion` and `case_trial_court` document orig. proceeding parentheticals and subsequent-history strings for mandamus workflows; `tests_toa.json` mirrors the bracketed status in TOA contexts.

## Comprehensive QA audit (2025-11-18)
- **Dependency verification.** Attempting to execute `run_tests.py` without installing `citeproc-py` still triggers `ModuleNotFoundError`; installed the package via `pip install citeproc-py` before rerunning the harness.【bfbf00†L1-L6】【2f6cb0†L1-L9】 Capture this prerequisite in the README so new environments do not fail at the first test command.
- **Regression suite status.** Re-ran the full note regression suite with `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt`; all 60 fixtures returned `OK`, confirming no drift from the stored expectations.【955aca†L1-L120】 The citeproc warnings about unsupported `label`/`reviewed_title` metadata persist but remain informational.
- **TOA harness behavior.** Running the TOA fixtures without specifying `--mode bibliography` produces false diffs because the harness defaults to note rendering. Explicitly adding `--mode bibliography` restores dotted leader output and aligns with `expected_toa_grouped_leaders.txt`; document this nuance alongside the command example.【eab112†L1-L41】【2a9a0c†L1-L40】 Future tooling updates could auto-select bibliography mode when a TOA style is detected.
- **Log review.** Spot-checked historical outputs under `temp/test-logs/` (e.g., `20250309-run_tests-regenerated.txt`) to confirm the new runs match prior baselines for parenthetical and bibliography coverage; no unexpected churn observed.【74260d†L1-L40】

## Macro Dispatch Sketches

### `cs:citation` authority routing
```text
start citation
  layout delimiter="; "
    choose on item.type
      legal_case → call macro legal-case
        legal-case:
          if position="first" → legal-case-first
            • case-name → reporter-(print|wl) → pinpoint → court-and-date → parenthetical-slip-op → subsequent-history
          else if variable references present → legal-case-cross-reference
            • cross-reference-cue + legal-case-first core → court-and-date → parenthetical-slip-op → references tail
          else → legal-case-short
            • same base chain as first cite but omit weight/subsequent history
      legislation → call macro statute-code when authority/collection-title/title/chapter-number present, else tex-statute
        statute-code:
          branch by position="first"/references/else to select statute-code-first, statute-code-cross-reference, statute-code-short
            • first = full section + status; short = code + § + section; cross-reference prefixes cue and appends references
        tex-statute:
          relies on constitution-core/session-law/etc. helpers (no position branching yet)
      bill → call tex-statute (future reuse with constitution/session-law)
      treaty|standard → call tac-core with same position+references short-form logic (first → volume reporter § section + year/authority; cross → cue + section; short → code § section)
      article-journal → call article-journal (no short-form split)
      book|chapter|report|reference → call book-like (shares helpers with bibliography; uses short macros for repeated cites via internal choose blocks)
      webpage|post → call web (includes issued date & URL; has internal short-form helpers like web-short)
      else → generic fallback (title, issued year)
end citation
```

### `cs:bibliography` authority routing & sort
```text
start bibliography
  sort keys:
    1. author (names rendered via shared name node definitions)
    2. title (ensures consistent secondary ordering)
  layout suffix="."
    choose on item.type (mirrors citation routing but without short-form branches)
      legal_case → group delimiter=", " → case-name + reporter + court-year
        • case-name, reporter, court-year reuse same helper macros used inside legal-case-first/short
      legislation|bill → tex-statute (full form only; bibliography intentionally omits § status short-form variants)
      treaty|standard → tex-admin-code (bibliography analogue to tac-core-first)
      article-journal → article-journal (same macro as citation)
      book|chapter|report|reference → book-like (same macro as citation, ensures shared handling of editors/editions)
      webpage|post → web (same macro as citation, including issued date formatting)
      else → fallback group with title + issued.year (shared with citation fallback)
end bibliography
```

### Short-form macro inventory (2025-11-02)
- **Cases — `texas-greenbook-15th-edition.csl` lines 236–299.**
  - `legal-case-short` (l. 260) retains the full reporter selection logic from the first-position macro while preferring `title-short` where available before falling back to `case-name`. The invocation at l. 236 confirms note-mode citations delegate here when neither `position="first"` nor `references` apply.
- **Secondary books & reports — `texas-greenbook-15th-edition.csl` lines 447–505.**
  - `book-like-short` (l. 473) pares the repeat form down to the italicized title plus pinpoint/year stack while preserving the explanatory parenthetical tail. Called from the `book-like` choose block at l. 447.
- **Secondary periodicals — `texas-greenbook-15th-edition.csl` lines 522–567.**
  - `article-journal-short` (l. 551) keeps the author-plus-quoted-title framing with the shared secondary pinpoint helper, omitting container/volume strings in repeat cites.
- **Web materials — `texas-greenbook-15th-edition.csl` lines 671–708.**
  - `web-short` (l. 709) reduces follow-up cites to the bare title and URL while the choose block at l. 671 confirms routing from the primary `web` macro.
- **Unpublished & CLE materials — `texas-greenbook-15th-edition.csl` lines 765–804.**
  - `unpublished-short` (l. 781) reuses the quoted title, secondary pinpoint, and descriptor helper for subsequent notes; invoked from the enclosing choose clause at l. 765.
- **Gap check.** The TOA variants (`texas-greenbook-15th-toa*.csl`) currently expose no `*-short` macros, and statute/rule short-form helpers such as `tex-statute-short` or `tex-admin-code-short` are not yet defined in the edition file—confirming the broader TODO entry to design those branches remains outstanding.
  - Searching with `rg "_short" temp -n` only surfaced backlog references because the implemented macros use hyphenated names; future audits should target `-short` when gathering inventory lists.
- **Backlog follow-up (2025-11-02).** Re-reviewed the TODO backlog after logging the ambiguity check and confirmed that the standing “Complete statute and rule short-form logic” epic already tracks every outstanding legislation/agency helper refactor. No new TODO entries were required; cross-referenced this conclusion in the TODO file for future auditors.

#### Short-form macro naming review (2025-03-28)
- **`legal-case-short` — `texas-greenbook-15th-edition.csl` ll. 260–279.** Confirms the macro title matches its remit of emitting the condensed reporter block for repeat case citations while sharing the same helper stack (`pinpoint`, `court-and-date`, `case-parenthetical-stack`, `related-proceedings`) as catalogued in the requirement matrix’s case entries (Ch. 2–6). No competing macro reuses the name or scope, so overlap risk is minimal.
- **`book-like-short` — `texas-greenbook-15th-edition.csl` ll. 473–486.** Restricts output to the italicized title plus pinpoint/year pairing outlined for book-style secondary sources in the matrix (Ch. 18–19), leaving full contributor handling to the first/full macros. Name and coverage align, and no other macro addresses the same authority subset.
- **`article-journal-short` — `texas-greenbook-15th-edition.csl` ll. 551–562.** Delivers the abridged author–title–pinpoint structure required for journal repeat cites, matching the periodical rows of the matrix (Ch. 18). Shares no logic with non-periodical helpers beyond the shared `secondary-pinpoint`, keeping responsibilities distinct.
- **`web-short` — `texas-greenbook-15th-edition.csl` ll. 709–715.** Limits repeat web citations to title and URL, mirroring Chapter 16 guidance and diverging cleanly from the `web-first` and cross-reference macros that manage access dates. Name uniquely signals its web-only scope.
- **`unpublished-short` — `texas-greenbook-15th-edition.csl` ll. 781–789.** Reuses the unpublished descriptor helper to preserve genre/status metadata for CLE materials as directed by Chapters 18–19. No other macro emits this descriptor trio, so the naming accurately reflects the specialization.
- **Ambiguity check.** The review found no duplicate or overlapping macro names; each `*-short` helper ties directly to a single authority grouping in the requirement matrix. Documented absence of conflicts satisfies TODO item follow-up while providing a baseline for future comparisons once statute/rule short forms are drafted.
- **Recommended naming guardrails.** When the pending statute, rule, and administrative short forms are implemented, reuse the authority-specific prefixes already sketched in the TODO list (e.g., `tex-statute-short`, `tex-admin-code-short`). This keeps namespaces disambiguated and signals the matrix rows they correspond to, avoiding the need for later renames.

### Short-form macro decision trees (2025-11-03)
- **`legal-case-short` — `texas-greenbook-15th-edition.csl` ll. 260–283.**
  - Flow: choose `title-short` for the italicized case name, otherwise fall back to `case-name`; branch on `volume`/`page`/`container-title` to select `reporter-print` vs. `reporter-wl`; append `pinpoint`, `court-and-date`, `case-parenthetical-stack`, and `related-proceedings`.
  - Helper reuse: leans on `case-name`, `reporter-*`, `pinpoint`, and `court-and-date`, mirroring the first-position macro so downstream short-form work can tap the same helpers without reimplementing reporter logic.
  - Assumed inputs: expects either the reporter trio (`volume`, `container-title`, `page`) or a Westlaw combination; no guard prevents empty output if neither set is present, and the `pinpoint` macro presumes a locator without enforcing type-specific prefixes.
  - Cross-check references: logic verified against `tests.json` entries `case_supreme`/`case_app_hou14`, which exercise both reporter branches and `title-short` fallbacks (Greenbook chs. 2–4, pp. 7–27).
- **`book-like-short` — `texas-greenbook-15th-edition.csl` ll. 473–484.**
  - Flow: prints the italicized `title`, then groups `secondary-pinpoint` with the issued year before appending `explanatory-parenthetical`.
  - Helper reuse: depends on `secondary-pinpoint` and `explanatory-parenthetical`, tying repeat cites to the same pinpoint/parenthetical stack as the long form.
  - Assumed inputs: requires an `issued` year to avoid an orphaned delimiter; there is no fallback when dates are missing even though Greenbook ch. 18 (pp. 93–95) allows undated treatises.
  - Cross-check references: covered by `tests.json` fixture `treatise_oconnors`, which supplies both pinpoint and year for regression coverage.
- **`article-journal-short` — `texas-greenbook-15th-edition.csl` ll. 551–558.**
  - Flow: emits author names, the quoted `title`, and the shared `secondary-pinpoint` stack; no container fields appear in repeat cites as required by ch. 17 (pp. 86–91).
  - Helper reuse: reuses the same name node definition as the first-position macro, keeping delimiter rules identical.
  - Assumed inputs: presumes at least one author; when metadata omits authors (per ch. 17 sample newsletters) the macro would output an empty author slot, so a safeguard is needed once short forms expand to unattributed sources.
  - Cross-check references: validated by `tests.json` entries `journal_texlawrev` and `journal_textech`, which provide contrasting author counts.
- **`web-short` — `texas-greenbook-15th-edition.csl` ll. 709–713.**
  - Flow: groups the `title` and `URL` with a comma delimiter, omitting all date metadata for subsequent cites as allowed by ch. 16 (pp. 76–84).
  - Helper reuse: minimal—only the base `web` macro routes here, so future helpers will need to account for shared URL rendering if additional fallback strings are required.
  - Assumed inputs: the macro does not defend against missing `URL` values, yielding a trailing comma in the regression output whenever Zotero items lack the field.
  - Cross-check references: exercised via `tests.json` item `web_tx_agency`, which already highlights the need for URL presence in short forms.
- **`unpublished-short` — `texas-greenbook-15th-edition.csl` ll. 781–786.**
  - Flow: prints the quoted `title`, then appends `secondary-pinpoint` and `unpublished-descriptor`, echoing the first-position descriptor stack mandated for CLE materials in ch. 19 (p. 96).
  - Helper reuse: shares the `unpublished-descriptor` helper so genre/medium/status phrases remain synchronized across note positions.
  - Assumed inputs: relies on translators to preload `genre`, `medium`, and `status`; absent values collapse whitespace but still emit the commas, so guards will be necessary before expanding fixture coverage.
  - Cross-check references: regression coverage comes from `tests.json` fixture `cle_paper`, which includes medium and status metadata.
- **Statute and rule placeholders.** `tex-statute` (ll. 318–338), `tex-admin-code` (ll. 349–382), and `municipal-code` (ll. 421–435) lack the `choose` scaffolding used above, so subsequent notes currently rerun the full form instead of a Greenbook-compliant short string. This confirms the outstanding TODO to add dedicated short-form macros for chapters 10–13 (pp. 42–65).

### Requirement matrix alignment audit (2025-11-03)
- **Cases.** Existing `legal-case-*` macros satisfy the matrix expectations for first and short outputs, but the cross-reference branch is still pending. Investigation on 2025-11-01 confirmed that citeproc-py 0.5.1 does not honor `jurisdiction="…"` conditions, so both the Texas (`case_tex_cross`) and out-of-state (`case_nontex_cross`) fixtures emit “See” even though Greenbook Chapter 1 (p. 4) requires “See also” for non-Texas authorities.【F:temp/tests.json†L900-L940】【F:temp/expected.txt†L66-L69】 The existing `cross-reference-cue` helper (edition ll. 373–384) therefore needs either a processor upgrade or an alternate metadata flag before it can branch on Texas vs. non-Texas authorities.
- **Texas statutes and codes.** The matrix calls for `tex-statute-first`/`short`/`cross-reference` variants keyed to Greenbook chs. 10–12 (pp. 42–60), yet only the base `tex-statute` macro exists today. Mandatory variables (`container-title`, `section`, `note` for publisher/date) cannot map to the short-form column, leaving fixtures `stat_govt_code`, `stat_penal_code`, and `stat_rev_civ` unable to express the condensed form.
- **Administrative materials.** `tex-admin-code` (ll. 349–382) always prints the issued year and optional `note`, contradicting the matrix requirement that short forms drop the year (ch. 16 at 76–84). No `tex-admin-code-short` exists to separate the behaviors, and fixture `tac_rule` therefore repeats the full cite on subsequent notes.
- **Court rules.** There is no `rule-core` helper in the edition file, so procedural (`rule_civp`, `rule_appellate`) and evidentiary (`rule_evidence`) fixtures also rerun the long form contrary to ch. 13 (pp. 61–65).
- **Municipal codes and AG opinions.** Single macros (`municipal-code`, `ag-opinion`) serve every note position. This conflicts with matrix guidance that short forms should collapse to the authority plus section/number while cross-references append `references` strings.
- **Non-Texas statutes/treaties.** Supporting helpers such as `statute-code` and `tac-core-short` are likewise absent, so the shared short-form infrastructure is incomplete beyond case/secondary/web categories.
- **High-impact discrepancy list.**
  1. **P0:** Implement Texas statute/rule short macros and connect them to `position`/`references` logic so fixtures `stat_*` and `rule_*` stop emitting redundant full cites.
  2. **P0:** Split `tex-admin-code` into first/short/cross variants to honor the year-suppression rule and enable Chapter 16 compliance for `tac_rule`.
  3. **P1:** Restore or rebuild `cross-reference-cue`’s jurisdiction awareness to deliver “See also” for out-of-state authorities when `note` is empty.
  4. **P1:** Add municipality/AG opinion short-form helpers so the matrix rows cease diverging from Greenbook chs. 14–15 expectations.
  5. **P2:** Create non-Texas statute/treaty short-form macros (e.g., `statute-code-short`) to match the matrix for federal authorities, enabling future fixture additions.

## Chapter 10–13 short-form trigger audit (2025-11-04)

### Source transcription (Greenbook pp. 42–65)
- **Current statute format guide (Ch. 10, p. 42).** The table lists four exemplar cites—subject-matter code, uncodified statute, session law, and electronic database—clarifying that the short form for current statutes retains the code title plus section while omitting publisher/year data. No diagrams accompany the table beyond the four entry rows.
- **Section vs. article labeling (Ch. 10, p. 44).** “The subject matter codes are divided into sections. Uncodified statutes, Title 1 of the Insurance Code, and independent codes are divided into articles. … Compare: Tex. Ins. Code Ann. § 823.456.; Tex. Ins. Code Ann. art. 5.06.; Tex. Rev. Civ. Stat. Ann. art. 581-4(A.).” This confirms the short-form trigger for choosing `§` versus `art.` in statute macros.
- **Pamphlet and supplement handling (Ch. 10, p. 44).** “Cite statutes appearing in pamphlets … include the abbreviation ‘Supp.’ in a final parenthetical… Do not … use the abbreviation ‘Supp.’ when citing a pamphlet that does not supplement a bound volume.” Short forms must therefore omit the supplement parenthetical unless the metadata indicates a true supplement.
- **Multiple sections and articles (Ch. 10, p. 45).** The text mandates `§§` for multiple sections with a shared date parenthetical and requires repeating `art.` labels when any cited article includes a section reference. These instructions govern how short forms collapse ranges while preserving article designations.
- **Current code citations (Ch. 10, p. 46).** “Cite material in these statutes to the subject matter codes … If a statute is currently in force, cite it without indicating the date of publication… Unannotated statutory reprints… should omit the abbreviation ‘Ann.’” Short forms must mirror the publisher suppression and observe the annotated/unannotated distinction.
- **Ongoing codification notes (Ch. 10, pp. 46–47).** Subparagraphs (a)–(e) enumerate Insurance Code, Business Organizations Code, Special District Local Laws Code, Criminal Procedure Code, and Estates Code nuances, pointing to Appendix H for abbreviations. The triggers require conditional parentheticals (e.g., pamphlet signals for Estates Code pre-2014) and awareness of tentative code titles.
- **Uncodified statutes (Ch. 10, p. 47).** “Most statutes not yet incorporated … are cited as follows: Tex. Rev. Civ. Stat. Ann. art. 5415e-4, § 2(a).” This example anchors the article/section pairing the short form must retain.
- **Session law elements (Ch. 10, pp. 49–51).** Rules 10.3.1–10.3.4 specify the five-part structure: official act name, legislature/session, chapter/section numbers distinguishing `§` (act sections) from `sec.` (code sections), publication cite with pinpoint pages, and optional to-be-codified parenthetical. These clauses establish which metadata fields the short form must compress while still surfacing chapter/section identifiers.
- **Unpublished statutes and electronic sources (Ch. 10, pp. 52–53).** Rule 10.4 substitutes bill numbers for unpublished acts, and Rule 10.5 warns that Legislative Council PDFs are informational only—short forms must continue to cite commercial sources or municipal codes per Rule 10.6, which itself prescribes the municipality + code + chapter/section + year pattern. The municipal examples highlight the need to keep political subdivision names in repeat cites.
- **Statutes no longer in effect (Ch. 11, pp. 54–56).** Rule 11.1.1 requires the first citation to amended statutes to include amendment year plus current code location, while subsequent cites retain only the amendment year. Rule 11.1.2 mirrors the pattern for repealed statutes, and Rule 11.1.3 mandates expiration dates. Rules 11.2 and 11.3 add parallel cites to Gammel for pre-1898 and Republic-era materials. These passages supply the triggers for when short forms must still surface amendment/repeal metadata.
- **Comments, notes, and U.C.C. commentary (Ch. 12, pp. 58–60).** The format guide lists historical comment, revisor’s note, U.C.C. comment, and historical note exemplars. Subsequent text explains bracketed session-law parentheticals for historical notes, creating short-form obligations to preserve bracketed provenance even when truncating other elements.
- **Rules of procedure and evidence (Ch. 13, pp. 61–65).** The format guide enumerates rule cites (civil, judicial administration, appellate, evidence, and local). Rule 13.1.1 bars date parentheticals for in-force civil rules, Rule 13.1.2 details historical rule parentheticals, Rule 13.1.4 states subsequent citations to the Rules of Judicial Administration omit the “reprinted in” pointer, Rule 13.2.2 directs outdated TRAP cites to Tex. B.J. with adoption/repeal dates, Rule 13.2.3 renames the criminal appendix short form, and Rule 13.4 outlines local rule elements. Collectively these passages define when short forms may drop source parentheticals versus when they must keep provenance data.
- **Appendix cross-references.** Chapters 10–13 repeatedly point to Appendix H (code abbreviations), Appendix F (petition history abbreviations noted earlier in Chapter 4 but relevant to statutory tables), and Appendices K.1–K.3 for historic rules. These references are logged here so future development can consult the appendices when encoding locale abbreviations or rule provenance.

### Structured CSL condition mapping

## Statute, rule, and agency long-form element inventory (2025-11-01)

- **`tex-code-section` / `tex-statute` (edition ll. 341–376).** The long-form branch emits the full code title plus section symbol handling from `label` or `chapter-number`, letting annotated volumes surface article numbers while regulations fall back to `§` groupings. The output therefore already covers the Greenbook mandate that first cites recite the chapter/article label and section in tandem (ch. 10, pp. 62–63). Short-form variants must preserve only the code title (abbreviated per Appendix H) and the section/article string while omitting any publisher/year parentheticals that appear elsewhere in the long form (e.g., West, Supp. signals referenced in ch. 10, p. 63).【F:temp/texas-greenbook-15th-edition.csl†L341-L376】【7c9040†L1-L24】
- **Court rules routed through `tex-statute`.** Procedural, appellate, and evidence rules currently arrive as `type="legislation"` items without `collection-number` metadata, so `note-body` funnels them into `tex-statute`. Their long-form output is therefore limited to the rule series title (e.g., “Tex. R. Civ. P.”) and rule identifier. Greenbook ch. 13 requires subsequent cites to retain the rule designation and subdivision but to drop any adoption/reprint parentheticals after the first cite (pp. 61–65). The planned `tex-rule-short` helper can reuse the same code/section string emitted by `tex-code-section` while eliding the historical parentheticals captured in the first-position flow.【F:temp/tests.json†L206-L230】【F:temp/texas-greenbook-15th-edition.csl†L341-L376】
- **`tex-admin-code` (edition ll. 395–438).** Long-form administrative cites emit the volume/title pair, section symbol group, optional locator, issued year, and parenthetical agency/source detail. Chapter 16 instructs that short forms retain the Texas Administrative Code title + section while suppressing the year parenthetical and only restating the agency when needed for clarity (pp. 77–78). The forthcoming short-form helper therefore needs to keep the `volume` + `container-title` + section chain, optionally echo the locator, and reserve agency titles for situations where multiple departments appear in the same discussion.【F:temp/texas-greenbook-15th-edition.csl†L395-L438】【02ad57†L1-L24】
- **Municipal code routing (`municipal-code`, edition ll. 469–477).** Municipal ordinances layer the city authority ahead of the shared `tex-code-section` output and append a year parenthetical. Under Greenbook Rule 10.6 (p. 53) the municipality and code cite persist in every reference, while the publication year can drop after the first cite. Any `municipal-code-short` macro must therefore keep the authority + section string and drop the issued-date wrapper unless it resolves ambiguity between different municipal compilations.【F:temp/texas-greenbook-15th-edition.csl†L469-L477】【7c9040†L1-L24】

### Short-form pseudo-code sketches (2025-11-01)

```text
tex-statute-short
  inputs: container-title, section, chapter-number?, genre?, note?, references?, jurisdiction
  branch: if references present → call tex-statute-cross-reference (future), else continue
  choose title-short fallback: prefer container-title-short else container-title
  output: [container-title-abbrev] [chapter-number + section string from tex-code-section]
  omit: note-sourced publisher/year parentheticals per ch. 10 (pp. 62–63)

tex-rule-short
  inputs: container-title (rule series), section, references, note (for adoption parentheticals), jurisdiction
  branch: if references present → cross-reference helper
  output: [container-title] [section symbol + subdivision]; reuse tex-code-section for symbols
  omit: adoption/reprint parenthetical strings captured in note/status after first cite (ch. 13, pp. 61–65)

tex-admin-code-short
  inputs: volume, container-title, section or page, locator, authority, note, references
  branch: if references present → cross-reference helper, else continue
  output: [volume] [container-title] [§ section or page]; append locator when supplied
  omit: issued year parenthetical; include agency authority only when `authority` present and multiple agencies appear (ch. 16, p. 77)
```

- Each pseudo-code block above aligns with the authority matrix rows already mapped in `authority-note-matrix.md` (Texas statutes & codes, court rules, and Texas administrative code). The inputs list mirrors the CSL variables surfaced in the regression fixtures (`stat_*`, `rule_*`, `tac_*`), ensuring the future implementation can layer `choose` blocks over known metadata without expanding the JSON schema.【F:temp/authority-note-matrix.md†L8-L26】【F:temp/tests.json†L205-L267】
- Follow-up work: once the shells exist, wire `position="first"`/`references` routing inside `note-body` so short forms trigger automatically; update the fixture expectations to document the condensed outputs for Chapters 10–13 authorities.
- **Short-form implementation log (2025-12-05).**
  - Added position-aware wrappers for statutes, rules, and administrative materials (`tex-statute`, `tex-rule`, `tex-admin-code`) so subsequent cites and cross-references now flow through dedicated `*-short`/`*-cross-reference` helpers while preserving the validated long-form macros for first-position output.【F:temp/texas-greenbook-15th-edition.csl†L430-L558】
  - Introduced `tex-code-section-short`, which prefers `container-title-short` when available and otherwise falls back to the full container title. The helper now draws on `tex-labeled-locator`, allowing `_cite` entries with `locator` metadata (e.g., `26.06(b)` or `rule` labels) to override the base section string in repeat citations.【F:temp/texas-greenbook-15th-edition.csl†L430-L468】【F:temp/tests_short-form_smoke.json†L1-L40】
  - Updated fixtures to populate `container-title-short` for annotated codes and shifted prefatory signals from `note` to `annote` so supplements remain in `note` for parenthetical output while signals continue to flow through `prefatory-signal`. Translators should mirror this split when preparing real-world data.【F:temp/tests.json†L360-L452】【F:temp/tests_short-form_smoke.json†L1-L40】
  - Because the routing currently keys off `genre` to identify court rules, rule reprint notes are suppressed automatically. Documented this as a caution: future authority classes that rely on `genre` (e.g., statutory notes) will require explicit handling before they can share the same branch.【F:temp/texas-greenbook-15th-edition.csl†L468-L556】
  - Administrative short cites still append agency parentheticals; Appendix B review is needed before we decide whether those can drop in repeat cites. Flagged this for follow-up alongside the TOA tasks so both note and TOA variants stay synchronized.【F:temp/texas-greenbook-15th-edition.csl†L500-L556】

- **TOA short-form synchronization (2025-05-06).**
  - Mirrored the statute, rule, and administrative `tex-*` routing into each TOA variant and added a `first-reference-note-number` guard so bibliography contexts continue to pull first-cite strings while note citations keep their position-based short forms, matching Appendix B’s direction to print full cites in Table of Authorities entries (pp. 239–252).【F:temp/texas-greenbook-15th-toa.csl†L274-L335】【F:temp/texas-greenbook-15th-toa-grouped.csl†L333-L392】【F:temp/texas-greenbook-15th-toa-by-reporter.csl†L330-L389】【F:temp/Greenbook_15thEdition.pdf†L612-L676】
  - Simplified `tex-admin-code-first` and `tex-admin-code-short-base` to ignore TOA locator metadata while retaining agency and adoption parentheticals; namespace variants now share the same helper stack and require no additional TOA-only deviations beyond the documented guard comment.【F:temp/texas-greenbook-15th-toa-grouped.csl†L476-L520】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L356-L420】【F:temp/texas-greenbook-15th-toa-by-reporter.csl†L424-L468】
  - Regenerated TOA expectations (including a dedicated `expected_toa_by-reporter.txt`) after confirming locator suppression and note parentheticals, capturing regression logs for all variants dated 2025-05-06.【F:temp/expected_toa.txt†L1-L17】【F:temp/expected_toa_by-reporter.txt†L1-L17】【f0eca9†L1-L36】【c9e0a2†L1-L36】

## Statute/rule short-form integration pass (2025-05-05)
- **Bibliography routing.** Updated the legislation and regulation branches in the main bibliography layout to reuse the first-cite macros (`tex-statute-first`, `tex-rule-first`, `tex-admin-code-first`) so long-form outputs retain the publisher and adoption data Greenbook requires in chs. 10, 13, and 16 (pp. 44–45, 63, 77).【F:temp/texas-greenbook-15th-edition.csl†L1280-L1314】【F:temp/Greenbook_15thEdition.pdf†L2841-L2878】
- **Cross-reference cue guard.** Pointed `cross-reference-cue` at `annote` instead of `note`, ensuring supplement or adoption parentheticals stay inside the cite while “See/See also” cues continue to follow the signal guidance in ch. 10 (pp. 44–45).【F:temp/texas-greenbook-15th-edition.csl†L373-L388】【F:temp/Greenbook_15thEdition.pdf†L2841-L2878】
- **Cross-reference cue fallback update (2025-11-20).** Traced the helper’s execution order to confirm citeproc checks `annote`/`note` before falling through to automatic signals, then rewired the branch so case, statute, and administrative repeats treat any populated `jurisdiction` as the cue for “See also.”【F:temp/texas-greenbook-15th-edition.csl†L373-L393】【F:temp/reports/greenbook-page21.txt†L12-L24】【F:temp/reports/greenbook-page22.txt†L35-L42】 Texas cross-reference fixtures now omit `jurisdiction="us:tx"`, while out-of-state samples keep their jurisdiction metadata to exercise the new branch.【F:temp/tests.json†L902-L945】
- **Cross-reference cue verification (2025-11-30).** Replayed the full regression suite and confirmed the jurisdiction-aware cue emits “See” for Texas authorities (`case_tex_cross`) and “See also” for out-of-state counterparts (`case_nontex_cross`). The comparison log (`test-logs/2025-11-30_full-suite.txt`) records matching expectations on lines 17 and 274–275, cited against Greenbook Chapter 1 (p. 4) for signal language.【F:temp/test-logs/2025-11-30_full-suite.txt†L73-L88】【F:temp/test-logs/2025-11-30_full-suite.txt†L272-L275】【F:temp/Greenbook_15thEdition.pdf†L18-L26】
- **Regression fixtures.** Added statute (`statute_cross_reference`), rule (`rule_cross_reference`), and administrative (`tac_cross_reference`, `tac_no_year_short`) scenarios to `tests.json` plus TOA counterparts so cross-reference and no-year administrative cites now exercise the short-form branches described in chs. 10, 13, and 16.【F:temp/tests.json†L409-L460】【F:temp/tests_toa.json†L25-L66】【F:temp/Greenbook_15thEdition.pdf†L2841-L2878】【F:temp/Greenbook_15thEdition.pdf†L3193-L3234】
- **Test log capture.** Stored before/after citeproc runs at `temp/test-logs/20250505_statute_rule_before.txt` and `temp/test-logs/20250505_statute_rule_after.txt`, with TOA companions dated 2025-05-05, to document the short-form integration diffs for future audits.
- **Helper consolidation (2025-12-04).** Introduced shared `tex-short-form-base`, `tex-short-form-cross-base`, and `tex-short-form-output` helpers in the main style and TOA variants so statutes, court rules, and Texas administrative materials now reuse a single cross-reference branch while preserving TOA-specific parenthetical requirements (statute notes; TAC agency identifiers). This aligns the repeat-cite formatting with Greenbook ch. 10 §§10.1–10.3 (pp. 42–46), ch. 13 §13.3 (p. 63), and ch. 16 §16.1 (pp. 76–78).【F:temp/texas-greenbook-15th-edition.csl†L504-L568】【F:temp/texas-greenbook-15th-toa.csl†L500-L556】【F:temp/texas-greenbook-15th-toa-grouped.csl†L517-L573】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L404-L470】【F:temp/texas-greenbook-15th-toa-by-reporter.csl†L460-L526】【F:temp/texas-greenbook-15th-toa-leaders.csl†L462-L528】【F:temp/Greenbook_15thEdition.pdf†L2841-L2878】【F:temp/Greenbook_15thEdition.pdf†L3193-L3234】
- **Requirement matrix refresh.** Extended the matrix rows for statutes, administrative code, and court rules to call out the `container-title-short`, `note`, and `annote` dependencies surfaced by the new fixtures so translators know which metadata to supply.【F:temp/authority-note-matrix.md†L8-L14】
- **Gap review.** Reconfirmed that suppressing agency parentheticals in `tex-admin-code-short` remains an Appendix B follow-up task; no new TODO entries were opened while this pass focused on note-mode routing and regression coverage.【F:temp/TODO.md†L98-L149】

### Short-form fixture provenance audit (2025-11-30)

| Fixture ID | Authority type | Purpose | Greenbook reference | Notes & assumptions |
| --- | --- | --- | --- | --- |
| `statute_short_smoke` | Texas statutes & codes | Validates that repeat cites suppress supplement parentheticals; ensures `cross-reference-cue` stays blank when `note="Supp. 2024"`. | Ch. 10, pp. 42–44【F:temp/Greenbook_15thEdition.pdf†L2841-L2862】 | Synthetic supplement year mirrors Appendix H examples; no external approval required. Regression log stored at `test-logs/2025-11-30_short-form-smoke.txt` (lines 1–8).【F:temp/tests_short-form_smoke.json†L1-L10】【F:temp/test-logs/2025-11-30_short-form-smoke.txt†L1-L12】 |
| `admin_short_smoke` | Administrative code | Confirms TAC short forms retain first-cite agency parenthetical on repeat citations while allowing `Id.` locators to fire. | Ch. 16, pp. 76–78【F:temp/Greenbook_15thEdition.pdf†L3188-L3218】 | Uses existing `authority` text from Chapter 16 table; assumptions documented during initial fixture load. Verified via same log lines 9–16.【F:temp/tests_short-form_smoke.json†L11-L24】【F:temp/test-logs/2025-11-30_short-form-smoke.txt†L9-L16】 |
| `statute_note_signal_smoke` | Texas statutes & codes | Ensures manual signals remain in `annote`; when `note="Cf."` the cue should stay empty and the cite reuses the base section string. | Ch. 1, pp. 3–5; Ch. 10, p. 42【F:temp/Greenbook_15thEdition.pdf†L10-L24】【F:temp/Greenbook_15thEdition.pdf†L2841-L2852】 | Relies on handcrafted signal text to demonstrate the guard; no reviewer escalation needed. See log lines 17–24 for confirmation.【F:temp/tests_short-form_smoke.json†L25-L34】【F:temp/test-logs/2025-11-30_short-form-smoke.txt†L17-L24】 |

- No fixtures in this audit depend on inferred metadata beyond the synthetic supplement year noted above. Should future reviewers require additional validation, reference the authoritative PDF page spans cited per row. External resources (Greenbook PDF, short-form smoke expectations) remain available in `temp/` and are linked throughout for traceability.【F:temp/expected_short-form_smoke.txt†L1-L6】 Self-review completed 2025-11-30; no outstanding approvals pending.

- **Subject-matter codes (Ch. 10, pp. 44–46).**
  - *Metadata:* `container-title`, `section`, optional `note` (for supplements/pamphlets) and `title-short` (for code short names).
  - *Conditions:* `if` multiple sections share `container-title` → emit `§§` plus comma-delimited `section` list; `elif` citation references an article → prefix each with `art.` and retain section subdivisions when present.
  - *Helper needs:* `code-range` helper to collapse sequential sections and guard against duplicate `art.` labels; `supplement-flag` helper to gate the `(Supp.)` parenthetical.
  - *Expected output:* First cite `Tex. Tax Code Ann. § 26.06(a).`; short cite `Tex. Tax Code § 26.06(a)` with optional `(Supp.)` only when `note` signals a bound supplement.
- **Unannotated reprints (Ch. 10, p. 46).**
  - *Metadata:* `container-title` without “Ann.”, `section`.
  - *Conditions:* `if` `container-title` lacks “Ann.” and item is repeat cite → reuse same string; no publisher/year added.
  - *Helper needs:* `strip-annotation` helper to prevent accidental “Ann.” insertion during short-form generation.
  - *Expected output:* `Tex. Penal Code § 29.02` for both first and short forms.
- **Uncodified statutes (Ch. 10, pp. 45–47).**
  - *Metadata:* `chapter-number` storing article label, `section`, optional `note` for codification status.
  - *Conditions:* Always emit `art.` prefix; when `section` present, include `§` within the same cite block; short form mirrors full cite minus any “(West YEAR)” publisher detail.
  - *Helper needs:* `article-section` formatter to merge `chapter-number` and `section` reliably.
  - *Expected output:* `Tex. Rev. Civ. Stat. Ann. art. 5415e-4, § 2(a).`
- **Session laws (Ch. 10, pp. 49–51).**
  - *Metadata:* `title`, `collection-number` (e.g., “79th Leg., R.S.”), `number` (chapter), `section`, `container-title`, `volume`, `page`, optional `note` for to-be-codified parentheticals.
  - *Conditions:* Always print `title` (or “Act of [date]” fallback) + legislature/session + chapter/section; include `sec.` when referencing amended code sections; for short form omit the closing codification parenthetical but retain act identifiers to maintain traceability.
  - *Helper needs:* `session-identifiers` helper to stitch `collection-number`/`number`; `codification-parenthetical` helper to optionally append `(to be codified …)` only on first cites.
  - *Expected output:* First cite `Act of May 27, 2005, 79th Leg., R.S., ch. 484, § 2, sec. 153.433, 2005 Tex. Gen. Laws 1345.`; short cite drops the codification parenthetical yet keeps the pinpoint.
- **Amended/repealed/expired statutes (Ch. 11, pp. 54–55).**
  - *Metadata:* `note` capturing amendment/repeal/expiration year, `references` for current location when needed.
  - *Conditions:* `if position="first"` → append `(amended YEAR)` and `(current version at …)` or `(repealed YEAR)`; `else` (short form) → retain only the `(amended YEAR)`/`(repealed YEAR)` parenthetical to satisfy Rule 11.1.1(b) and 11.1.2(b); `expired` always prints `(expired DATE)` regardless of position.
  - *Helper needs:* `status-parenthetical` helper keyed by `note` tokens to minimize duplication.
  - *Expected output:* `Act of May 30, 1977 … (repealed 2003).`
- **Pre-1898 and Republic-era laws (Ch. 11, pp. 55–56).**
  - *Metadata:* `references` storing the Gammel parallel cite.
  - *Conditions:* Always append the Gammel reference; short form may abbreviate the parallel cite to “reprinted in …” but cannot drop it entirely.
  - *Helper needs:* `gammel-parallel` helper to pull `references` into both first and short cites.
  - *Expected output:* `Act approved Mar. 8, 1871 … reprinted in 6 H.P.N. Gammel …`.
- **Comments and notes (Ch. 12, pp. 58–60).**
  - *Metadata:* `genre` (e.g., “historical note”), `note` for bracketed session law provenance, `container-title` (statute code), `section`.
  - *Conditions:* Always print the code cite followed by the comment label; preserve bracketed session law parenthetical even in short form.
  - *Helper needs:* `comment-descriptor` helper to emit “cmt.”/“revisor’s note”/“historical note” strings based on `genre` or dedicated field.
  - *Expected output:* `Tex. Nat. Res. Code Ann. § 52.024 historical note (West Supp. 1997) [Act of May 22, 1981, …].`
- **Rules of Judicial Administration (Ch. 13, p. 63).**
  - *Metadata:* `container-title` for rule series, `section`, `note` for reprint location, `references` for subsequent history if any.
  - *Conditions:* First cite includes “reprinted in Tex. Gov’t Code Ann., tit. 2, subtit. F app.”; short cite removes the reprint clause per Rule 13.1.4 while retaining rule number.
  - *Helper needs:* `jud-admin-first` vs. `jud-admin-short` wrappers toggled by `position`.
  - *Expected output:* `Tex. R. Jud. Admin. 5, reprinted in Tex. Gov’t Code Ann., tit. 2, subtit. F app.` (first); short form `Tex. R. Jud. Admin. 5.`
- **Historic rules (civil/appellate/evidence) (Ch. 13, pp. 62–64).**
  - *Metadata:* `title` (rule designation), `collection-title`/`container-title` for source (e.g., Tex. B.J.), `issued` for adoption/repeal dates.
  - *Conditions:* Always include adoption/repeal years in parenthetical; when citing pre-1997 criminal appendix rules, substitute “Tex. R. App. P. Crim. app.” before emitting number.
  - *Helper needs:* `historic-rule-parenthetical` to join adoption/repeal dates, and `trapp-crim-prefix` to swap the rule label.
  - *Expected output:* `Tex. R. App. P. 9, 49 Tex. B.J. 561 (Tex. & Tex. Crim. App. 1986, amended 1997).` / `Tex. R. App. P. Crim. app. 2.`
- **Local rules (Ch. 13, p. 65).**
  - *Metadata:* `authority` (court name), `title` or `section` for rule number, optional `note` for county list.
  - *Conditions:* Always lead with the court and location, followed by “Loc. R.” and the rule identifier; short forms may omit parenthetical county list if unchanged, but must keep the court + “Loc. R.” label.
  - *Helper needs:* `local-rule` helper to format court/location consistently.
  - *Expected output:* `Dallas (Tex.) Civ. Dist. Ct. Loc. R. 1.22.`

### Example inventory and fixture coverage
- **Multiple section cite (Ch. 10, p. 45).** Example: “Tex. Health & Safety Code Ann. §§ 286.101, 433.045.” No JSON fixture currently exercises a multi-section cite, so the statute test suite needs an additional entry; flagged below for future fixture work. Aligns with the “Texas statutes & codes” requirement matrix row and will require short-form logic to reuse the double section symbol.
- **Mixed article/section cite (Ch. 10, p. 45).** Example: “Tex. Rev. Civ. Stats. Ann. art. 4512.5, art. 5415e-4, § 2(a), arts. 5421b, 5421b-1.” Highlights the necessity of repeating `art.` when a cited article contains sections; no fixture covers this complexity yet, so the upcoming test expansion should add it. Matches the matrix expectation for uncodified statutes.
- **Pamphlet supplement (Ch. 10, p. 44).** Example: “Tex. Alco. Bev. Code Ann. § 22.03 (Supp.).” Existing `stat_govt_code` fixture lacks a supplement flag; we will need to extend the dataset with a `note`-driven example to validate the `(Supp.)` trigger.
- **Session law pinpoint (Ch. 10, p. 51).** Example: “Act of May 20, 2013, 83d Leg., R.S., ch. 920, § 4, sec. 981.215(a)(11), 2013 Tex. Sess. Law Serv. 2288, 2289 (to be codified at Tex. Ins. Code § 981.215(a)).” `tests.json` already includes `session_law` but omits the to-be-codified parenthetical; future fixture updates should add a `note`/`references` entry to replicate the bracketed codification note.【F:temp/tests.json†L296-L320】
- **Amended statute subsequent cite (Ch. 11, p. 55).** Example: “Act of July 3, 1984 … (amended 2001).” No current fixture exercises the amendment-year-only short form; add to the pending statute fixture list. This example directly maps to the requirement matrix’s “status parenthetical” column.
- **Repealed statute first cite (Ch. 11, p. 55).** Example: “Act of May 30, 1977 … (repealed 2003).” Also uncovered by fixtures—needs a JSON entry with `note` capturing the repeal year so short-form logic can persist the parenthetical.
- **Historical note with bracketed session law (Ch. 12, p. 58).** Example: “Tex. Nat. Res. Code Ann. § 52.024 historical note (West Supp. 1997) [Act of May 22, 1981 …].” Secondary fixtures currently focus on treatises and CLE materials; we should extend them to cover historical notes to ensure the bracketed provenance persists in short cites.
- **Rules of Judicial Administration repeat cite (Ch. 13, p. 63).** First cite demands the “reprinted in” clause, while the short form omits it. Existing `rule_appellate` and `rule_civp` fixtures do not include judicial administration examples; add a `Tex. R. Jud. Admin. 5` entry to prove the position-aware omission works.
- **TRAP criminal appendix (Ch. 13, p. 64).** Example: “Tex. R. App. P. Crim. app. 2.” No fixture currently targets the pre-1997 criminal appendix label (`rg 'Crim\. app'` returned no matches), so a new test is necessary. This scenario also stresses the requirement matrix’s “rule set aliasing” notes.
- **Local rule cite (Ch. 13, p. 65).** Example: “Dallas (Tex.) Civ. Dist. Ct. Loc. R. 1.22.” Our `tests.json` includes municipal code authorities but no local court rules; adding one will ensure locality rendering and potential county parentheticals remain stable. No cross-jurisdictional reporters appear in this chapter’s examples, so no additional handling is required beyond locale abbreviations.

- **Fixture gap flags.** The examples above highlight missing regression coverage for multi-section statutes, pamphlet supplements, amendment/repeal parentheticals, historical notes, judicial administration short forms, TRAP criminal appendix rules, and local court rules. These have been flagged for follow-up in the TODO backlog so future runs can seed the JSON fixtures accordingly.

### Matrix alignment crosswalk (2025-11-05)
| Trigger cluster | Matrix row(s) | Coverage status | Actions |
| --- | --- | --- | --- |
| Subject-matter code multi-section cite (Ch. 10, p. 45) | Texas statutes & codes | Matrix row already captured the section-symbol toggle; add note to reuse existing `section` arrays for `§§` output. | No contradictions; ensure helper normalizes repeated section symbols. |
| Mixed article/section cite (Ch. 10, p. 45) | Texas statutes & codes | Matrix row now references `chapter-number` + `section`; confirms article prefixes persist in both first and short forms. | Share helper planned for `article-section` fusion. |
| Pamphlet supplement parenthetical (Ch. 10, p. 44) | Texas statutes & codes | Row explicitly allows note-sourced `(Supp.)`; supplement toggle will rely on `note`. | None—document translator expectation to surface supplement flag in `note`. |
| Session law codification bracket (Ch. 10, p. 51) | Session laws (Texas General Laws & special acts) | New row added; codification/status strings mapped to `note` with `collection-number`/`number` metadata. | Proceed with shared helper extraction logged in short-form epic. |
| Amended statute short cite (Ch. 11, p. 55) | Texas statutes & codes | Row covers status parentheticals; short form retains `(amended YEAR)` via `note`. | None—test addition will confirm guard logic. |
| Repealed statute first cite (Ch. 11, p. 55) | Texas statutes & codes | Same matrix row handles repeal metadata; ensures first cite prints full `(repealed YEAR)` + references. | Align fixture plan with matrix to verify. |
| Historical note bracketed provenance (Ch. 12, p. 58) | Statutory notes & commentary | New row added; captures descriptor selection via `genre`/`note` and requires bracket retention. | Plan helper to preserve bracketed text in short form. |
| Rules of Judicial Administration reprint toggle (Ch. 13, p. 63) | Court rules | Existing row suffices; position-aware logic will drop “reprinted in …” for short cite. | Implementation pending in short-form task; no matrix changes. |
| TRAP criminal appendix label (Ch. 13, p. 64) | Court rules | Matrix row covers rule aliases; `note`/`title` supply “Crim. app.” label. | Document alias usage in forthcoming helper design. |
| Local court rule cite (Ch. 13, p. 65) | Local court rules | New row created for court + “Loc. R.” rendering with optional county list in `note`. | None—fixture will exercise county parenthetical handling. |

- Cross-referencing the triggers against the refreshed matrix exposed no conflicting requirements; every scenario mapped cleanly once the session law, statutory note, and local rule rows were added. The existing macros already expect the requisite metadata (`section`, `chapter-number`, `collection-number`, `note`, `references`, `authority`), so no schema revisions are necessary.
- No follow-up TODO entries were opened because all triggers are achievable with current data fields; helper work is already tracked under the statute short-form epic. Should translators discover authorities missing supplement or status metadata, reopen the TODO with the fixture identifier.
- The Greenbook language for these triggers is explicit, so no subject-matter expert clarification is required beyond the documented helper design. If future ambiguities arise, flag them under the short-form research log with the offending page citation.

### Fixture scenario metadata plan (2025-11-05)
| Proposed fixture ID | Authority type | Required metadata keys | Sample values | Greenbook source |
| --- | --- | --- | --- | --- |
| `statute_multi_section` | Subject-matter code (multi `§`) | `container-title`, `section`, `position` | `"Tex. Health & Safety Code Ann."`, `section: ["286.101", "433.045"]`, `position="first"` | Ch. 10, p. 45 (“Tex. Health & Safety Code Ann. §§ 286.101, 433.045.”) |
| `statute_article_section_mix` | Uncodified statutes (mixed articles/sections) | `container-title`, `chapter-number`, `section`, `note` | `"Tex. Rev. Civ. Stat. Ann."`, `chapter-number: "art. 5415e-4"`, `section: "§ 2(a)"`, `note` empty | Ch. 10, p. 45 (“Tex. Rev. Civ. Stats. Ann. art. 4512.5 … § 2(a) …”) |
| `statute_supplement` | Pamphlet supplement | `container-title`, `section`, `note` | `"Tex. Alco. Bev. Code Ann."`, `section: "§ 22.03"`, `note: "Supp."` | Ch. 10, p. 44 (“Tex. Alco. Bev. Code Ann. § 22.03 (Supp.).”) |
| `session_law_codification_note` | Session law with to-be-codified bracket | `title`, `collection-number`, `number`, `section`, `container-title`, `page`, `note`, `references` | `title: "Act of May 20, 2013"`, `collection-number: "83d Leg., R.S."`, `number: "ch. 920"`, `section: "§ 4, sec. 981.215(a)(11)"`, `container-title: "Tex. Sess. Law Serv."`, `page: "2288, 2289"`, `note: "to be codified at Tex. Ins. Code § 981.215(a)"` | Ch. 10, p. 51 |
| `statute_amended_short` | Amended statute short cite | `title`, `collection-number`, `number`, `page`, `note`, `references`, `position` | `title: "Act of July 3, 1984"`, `collection-number: "68th Leg., R.S."`, `number: "ch. 488"`, `page: "2729"`, `note: "amended 2001"`, `position="subsequent"` | Ch. 11, p. 55 |
| `statute_repealed_first` | Repealed statute first cite | Same as above + `references` for current location | `note: "repealed 2003"`, `references: "current version at Tex. ..."`, `position="first"` | Ch. 11, p. 55 |
| `statute_historical_note` | Historical note with bracketed session law | `container-title`, `section`, `genre`, `note` | `container-title: "Tex. Nat. Res. Code Ann."`, `section: "§ 52.024"`, `genre: "historical note"`, `note: "[Act of May 22, 1981, 67th Leg., R.S., ch. 389, § 1]"` | Ch. 12, p. 58 |
| `rule_jud_admin` | Rule of Judicial Administration (reprint toggle) | `container-title`, `section`, `note`, `position` | `container-title: "Tex. R. Jud. Admin."`, `section: "5"`, `note: "reprinted in Tex. Gov’t Code Ann., tit. 2, subtit. F app."`, `position="first"` | Ch. 13, p. 63 |
| `rule_trap_crim_app` | TRAP criminal appendix label | `container-title`, `section`, `title-short`, `note` | `container-title: "Tex. R. App. P."`, `section: "Crim. app. 2"`, `title-short: "Tex. R. App. P. Crim. app."`, `note` empty | Ch. 13, p. 64 |
| `local_court_rule` | Local court rule with county list | `authority`, `title`, `note`, `jurisdiction` | `authority: "Dallas (Tex.) Civ. Dist. Ct."`, `title: "Loc. R. 1.22"`, `note: "(Dallas County)"`, `jurisdiction: "us:tx"` | Ch. 13, p. 65 |

- Existing fixtures such as `stat_tax_code` and `session_law` provide the JSON skeletons for these entries; each proposed ID above reuses the same field casing (`collection-number`, `chapter-number`, `authority`) to stay aligned with current citeproc expectations.
- No new CSL variables are required. Supplement flags continue to ride on `note`, descriptors on `genre`, and code abbreviations on `title-short`. Document the translator requirement to populate these keys before the helper work lands.
- The scenario list mirrors the Chapter 10–13 gaps logged on 2025-11-04, so once JSON entries exist the pending short-form tests will have the necessary coverage.

- **Short-form branch trigger audit (2025-11-09).**
  - *Goal:* Document how the current CSL layout selects between first cites, cross-references, and repeat short forms so the upcoming statute/rule helper work can hook into the correct metadata toggles.
  - *Findings:* `texas-greenbook-15th-edition.csl` mirrors the case macro pattern—`position="first"` routes to the long-form macro, a non-first cite with populated `references` triggers the cross-reference branch, and all other cites fall through to the short-form macro shell (statutes at ll. 366–406; administrative code at ll. 416–460). The citation layout already intercepts `position="ibid"`/`position="ibid-with-locator"`, so `Id.` handling will remain centralized in `<citation>` while the authority macros focus on `position`/`references` splits.【F:temp/texas-greenbook-15th-edition.csl†L352-L410】【F:temp/texas-greenbook-15th-edition.csl†L416-L460】
  - *Metadata hooks:* The branch conditions rely on citeproc’s automatic assignment of `position` and `references`, while locator fallbacks originate from `Locator` objects in the JSON fixtures. No additional fields are required beyond those already captured in the requirement matrix; the future helper extraction should continue to watch for `note` (prefatory signal overrides) and `jurisdiction` (for `cross-reference-cue`).
  - *Next steps:* Once the dedicated short-form macros are populated, ensure the parent macros (`tex-statute`, `tex-admin-code`, pending `tex-rule`) wrap them in the same three-way `<choose>` block used by the case macros and confirm the `prefatory-signal` helper keeps `first-reference-note-number` alignment when citeproc surfaces sequential citations.【F:temp/texas-greenbook-15th-edition.csl†L920-L1004】

- **Short-form smoke test harness (2025-11-09).**
  - Added `temp/tests_short-form_smoke.json` with paired statute and administrative citations (plus a note-driven signal example) to confirm the draft short-form macros compile without schema issues during incremental development.
  - Stored the matching expectations in `temp/expected_short-form_smoke.txt` and captured the validation log at `temp/test-logs/20250309-short-form-smoke.txt`; all six smoke assertions currently echo the long-form output while the logic scaffolding remains in place.【F:temp/tests_short-form_smoke.json†L1-L54】【F:temp/expected_short-form_smoke.txt†L1-L6】【F:temp/test-logs/20250309-short-form-smoke.txt†L1-L24】
  - These smoke fixtures complement the broader regression suite without introducing new requirements; once short-form behavior changes, regenerate the expectations and flag intentional diffs in the TODO entry tracking the statute/rule work.

### Fixture expansion log (2025-03-09)
- **Added cross-reference regression coverage.** Seeded `tests.json` with statute (`stat_tax_code_repeat`), rule (`rule_jud_admin_reprint`), and administrative (`tac_volume_16`) sequences, each pairing a full cite with (a) an immediate repeat to trigger `Id.` and (b) a later citation to exercise the unfinished short-form branch. Negative companions (`stat_tax_code_missing_section`, `rule_jud_admin_missing`, `tac_volume_16_missing_section`) confirm fallback behavior when section metadata is absent, matching the Greenbook guidance on pamphlets, judicial administration reprints, and Texas Administrative Code volumes (chs. 10, 13, and 16 at pp. 44, 63, and 77 respectively).【F:temp/tests.json†L205-L267】【F:temp/tests.json†L430-L452】【F:temp/expected.txt†L18-L36】
- **Validation workflow.** Backed up the fixture file (`temp/archive/tests-20250309-before-cross-reference.json`) before edits, then ran `python temp/run_tests.py` after inserting each authority block; stored the diagnostics under `temp/test-logs/` (`20250309-run_tests-statute.txt`, `20250309-run_tests-rule.txt`, `20250309-run_tests-admin.txt`) and captured the clean pass in `20250309-run_tests-regenerated.txt`. Installing `citeproc-py` resolved the initial import failure encountered during the statute run.【F:temp/test-logs/20250309-run_tests-statute.txt†L1-L28】【F:temp/test-logs/20250309-run_tests-regenerated.txt†L1-L60】
- **Current limitations captured.** Citeproc still emits the full-form outputs for the cross-reference cites (`Tex. Tax Code Ann. § 26.06(a).`, `Tex. R. Jud. Admin. 5.`, `16 Tex. Admin. Code § 25.101 ...`), and the negative fixtures surface double periods when section data is missing. These lines remain in `expected.txt` to document present behavior until the dedicated short-form macros land.【F:temp/expected.txt†L18-L36】【F:temp/expected.txt†L41-L46】

### Locator label fallback hardening (2025-11-27)
- **Reproduced the crash:** Running `python temp/run_tests.py --tests temp/tests_locator_symbol.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected_locator_symbol.txt` without a `rule` symbol term triggered citeproc's `AttributeError: 'NoneType' object has no attribute 'single'`, matching the prior failure at citation #31. The output is archived under `temp/test-logs/2025-11-27_locator-symbol-crash.txt` for regression reference.【F:temp/test-logs/2025-11-27_locator-symbol-crash.txt†L1-L46】
- **Implemented guarded locator helpers:** Added `tex-labeled-locator` to the main style and TOA variants so non-page locators use symbol forms only for section/paragraph labels and fall back to short-form labels (or bare locators) for rules and other authorities. This prevents citeproc from requesting missing symbol terms while keeping § output intact.【F:temp/texas-greenbook-15th-edition.csl†L90-L123】【F:temp/texas-greenbook-15th-toa.csl†L34-L52】【F:temp/texas-greenbook-15th-toa-grouped.csl†L40-L58】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L33-L58】【F:temp/texas-greenbook-15th-toa-leaders.csl†L30-L55】
- **Documented the diagnostic fixture:** Retained the dedicated locator test pair (`tests_locator_symbol.json` / `expected_locator_symbol.txt`) referenced from the README so future macro edits can re-run the reproduction quickly.【F:temp/tests_locator_symbol.json†L1-L16】【F:temp/expected_locator_symbol.txt†L1-L1】【F:temp/README.md†L44-L71】
- **Warning suppression rationale:** Kept `label`, `comment`, and `reviewed_title` metadata in the fixtures for pending feature work but filtered citeproc's unsupported-field warnings in `run_tests.py` to avoid masking substantive diffs. Developers can re-enable the warnings with `PYTHONWARNINGS=default` during troubleshooting.【F:temp/run_tests.py†L1-L52】

## Explanatory parentheticals catalog (2025-11-05)
- **Chapter 2 (Texas Supreme Court cases, pp. 26–27).** The slip-opinion guidance requires `slip op. at [page]` when the Court posts paginated PDFs and allows omission of “slip op.” for general citations; Texas Supreme Court Journal cites include `Tex. Sup. Ct. J.` plus parallel electronic reporters.【F:temp/Greenbook_15thEdition.pdf†L160-L195】
- **Chapter 3 (Court of Criminal Appeals, pp. 30–31).** Slip opinions without pagination must cite paragraph numbers (`slip op. ¶`), and the memorandum-opinion parenthetical `mem. op., not designated for publication` is coupled with any per curiam designation drawn from the example block.【F:temp/Greenbook_15thEdition.pdf†L208-L259】
- **Chapter 4 (Courts of Appeals, p. 36).** Civil appellate slip opinions mirror the criminal pattern—`slip op. ¶` for unpaginated releases, `slip op. at [page]` for paginated PDFs—and retain `mem. op.` when the court labels the disposition accordingly.【F:temp/Greenbook_15thEdition.pdf†L270-L314】
- **Chapter 6 (Original proceedings, pp. 49–51).** Mandamus citations substitute writ/petition history with outcome flags such as `(orig. proceeding)`, `[mand. pending]`, `mand. granted`, `[mand. denied]`, and `[leave denied]`, escalating to `leave granted, mand. denied` when history spans multiple stages.【F:temp/Greenbook_15thEdition.pdf†L340-L403】
- **Chapter 16 (Administrative dockets, p. 76).** Agency orders cite docket numbers inside the descriptive block—`Docket No. 5905`—with parentheticals recording issuance dates and dispositions, confirming the docket metadata requirements for administrative fixtures.【F:temp/Greenbook_15thEdition.pdf†L452-L476】
- Chapters 2, 3, and 4 were reread sequentially to capture slip-opinion and memorandum language, and Chapter 6 confirmed the relief/status vocabulary for original proceedings. Chapter 16 supplied the docket phrasing needed for administrative parentheticals. No additional ambiguities surfaced; the extracted phrases have been logged verbatim for future macro wiring.

### Publication/status string inventory (2025-11-04)
- **Command log.** Ran `rg "Supp\\.|Supp|session|effective" temp -n --glob '*.csl'` and archived the output in `temp/reports/publication_string_scan.txt` to capture every occurrence across the active edition and TOA variants. The scan surfaced only `session-law` macro hooks plus one legacy comment containing "Supp." in archived draft1; no live strings currently emit supplement or effective-date parentheticals for statutes (chs. 10–13, pp. 42–65).
- **False positives.** The archived drafts (`temp/archive/texas-greenbook-15th-draft*.csl`) retain exploratory `session-law` definitions and a `Supp.` comment; they were excluded from the active inventory but retained in the log for historical comparison. The `session-law` macro references inside the five TOA styles use the namespace-prefixed XML schema but mirror the same logic.
- **Match annotation.** Table 1 maps each live reference to its authority category and notes duplicate routing:

| File | Macro context | Authority category | Notes |
| --- | --- | --- | --- |
| `texas-greenbook-15th-edition.csl` ll. 440–455 | `session-law` | Session laws (Texas General Laws) | Primary implementation; presently lacks publication/status parenthetical branches despite Greenbook ch. 10 guidance. |
| `texas-greenbook-15th-toa.csl` ll. 148–255 | `session-law` | Session laws (TOA) | Repeats the edition macro verbatim; duplication opportunity for shared helper once publication strings land. |
| `texas-greenbook-15th-toa-by-reporter.csl` ll. 85–183 | `session-law` | Session laws (TOA by reporter) | Same grouping uses namespace prefix `ns0`, but logic and delimiters match the edition file. |
| `texas-greenbook-15th-toa-grouped.csl` ll. 149–288 | `session-law` | Session laws (TOA grouped) | Identical output stack; no status handling. |
| `texas-greenbook-15th-toa-leaders.csl` ll. 141–269 | `session-law` | Session laws (TOA dotted leaders) | Mirrors edition macro but wraps nodes in `ns0` namespace. |
| `texas-greenbook-15th-toa-grouped-leaders.csl` ll. 111–280 | `session-law` | Session laws (TOA grouped leaders) | Same duplication and namespace pattern as other TOA variants. |
- **Spreadsheet crosswalk (2025-11-05).** Logged the inline `ch.` prefix shared by every active `session-law` macro in `temp/reports/publication_status_inventory.csv`, noting for each style whether the output appears in note/bibliography or TOA contexts and flagging that the `§` symbol continues to flow from the locale term rather than hard-coded text.【F:temp/reports/publication_status_inventory.csv†L8-L12】【F:temp/expected.txt†L20-L38】【F:temp/expected_toa.txt†L1-L13】【F:temp/expected_toa_grouped.txt†L1-L13】【F:temp/expected_toa_grouped_leaders.txt†L1-L17】【F:temp/expected_toa_leaders.txt†L1-L17】
- **Publication string inventory refresh (2025-11-01).** Expanded `publication_status_inventory.csv` to cover `tex-statute`, `tex-code-section`, and the TOA `tac-core` helper alongside the repeated `session-law` macro. The sweep confirmed that current statute and administrative outputs rely exclusively on locale-provided symbols and metadata-driven parentheticals, leaving `ch.` as the only hard-coded publication string pending helper extraction.【F:temp/reports/publication_status_inventory.csv†L1-L12】【F:temp/expected.txt†L28-L38】【F:temp/expected_toa.txt†L1-L13】
- **Chapter 10–13 publication cues (2025-11-01).** Re-read Chapters 10–13 with emphasis on supplement parentheticals, session-law codification notes, and administrative effective-date language. Key takeaways:
  - Chapter 10 (pp. 42–53) mandates `(Supp.)` or `(pamphlet)` parentheticals when citing pocket parts or loose-leaf pamphlets and requires `(to be codified at …)` brackets for future codification references.【F:temp/Greenbook_15thEdition.pdf†L2801-L3145】 These notes drive metadata expectations for supplement-related helpers.
  - Chapter 11 (pp. 54–56) clarifies that repealed or amended statutes are cited to session laws with `(amended ####)` or `(repealed ####)` parentheticals, signaling that helper logic must surface amendment years rather than defaulting to publication dates.【F:temp/Greenbook_15thEdition.pdf†L3193-L3304】
  - Chapter 12 (pp. 58–60) directs interpretive commentaries to include `(West ####)` publication parentheticals, reinforcing the need to surface publisher names from metadata rather than hard-coding “West.”【F:temp/Greenbook_15thEdition.pdf†L3310-L3364】
  - Chapter 13 (pp. 61–65) repeats the `Tex. Admin. Code § … (####)` format and adds guidance for Texas Register notices, confirming that agency helpers must reserve a slot for optional `(Tex. Reg. ####)` parentheticals and docket descriptors.【F:temp/Greenbook_15thEdition.pdf†L4244-L4368】
  - Appendix A (pp. 215–238) lists abbreviations such as “Supp.,” “Leg.,” “R.S.,” and “Tex. Reg.,” all of which align with the helper naming plan documented below; no conflicting variants were observed.【F:temp/Greenbook_15thEdition.pdf†L3040-L3753】【F:temp/Greenbook_15thEdition.pdf†L4244-L4368】

  | Abbreviation | Expansion | Usage Context | Plural/Variant Notes |
  | --- | --- | --- | --- |
  | `Supp.` | Supplement | Required parenthetical for pocket parts and updates to bound volumes when citing current statutes.【F:temp/Greenbook_15thEdition.pdf†L2841-L2864】 | No plural change; append year when available (e.g., `Supp. 1997`). |
  | `pamphlet` | Pamphlet edition | Parenthetical marker for pre-publication pamphlet versions (e.g., Estates Code 2013 pamphlet).【F:temp/Greenbook_15thEdition.pdf†L2904-L2913】 | Lowercase term inside parentheses; no plural variant noted. |
  | `Tex. Gen. Laws` | General and Special Laws of the State of Texas | Default reporter for published session laws once volumes are issued.【F:temp/Greenbook_15thEdition.pdf†L3084-L3116】 | Phrase remains constant; combine with page spans as needed. |
  | `Tex. Sess. Law Serv.` | Texas Session Law Service | Interim reporter when General and Special Laws volume not yet published.【F:temp/Greenbook_15thEdition.pdf†L3088-L3091】 | No plural form; retain `Sess.` abbreviation. |
  | `Tex. Loc. & Spec. Laws` | Texas Local & Special Laws | Historical bound volumes containing local acts separate from general laws.【F:temp/Greenbook_15thEdition.pdf†L3095-L3100】 | Alternate volumes may omit “Loc.” when containing only special laws (see next row). |
  | `Tex. Spec. Laws` | Texas Special Laws | Specialty volumes containing only special laws; used when cited separately.【F:temp/Greenbook_15thEdition.pdf†L3095-L3100】 | Retain singular `Tex. Spec. Laws` regardless of number of acts cited. |
  | `Leg.` | Legislature | Appears in session identifiers (`79th Leg.`) across statutes and legislative materials.【F:temp/Greenbook_15thEdition.pdf†L3040-L3753】 | Combine with ordinal numbering; no pluralization (e.g., `79th Leg.`). |
  | `R.S.` | Regular Session | Session designator for general sessions; paired with Legislature reference.【F:temp/Greenbook_15thEdition.pdf†L3040-L3753】 | Combine with Legislature (e.g., `79th Leg., R.S.`). |
  | `C.S.` | Called Session | Session designator for special sessions (`1st C.S.`, `2d C.S.`).【F:temp/Greenbook_15thEdition.pdf†L3040-L3736】 | Prefix ordinal indicator (`1st`, `2d`, `3d`) before `C.S.`. |
  | `Tex. Reg.` | Texas Register | Reporter for administrative notices and emergency rules in Chapter 13 guidance.【F:temp/Greenbook_15thEdition.pdf†L4244-L4368】 | Pair with volume/page citations; keep abbreviation in both singular and plural contexts. |

- **Capitalization/abbreviation audit.** No divergent capitalization appeared because all outputs currently assemble raw metadata without hard-coded abbreviations; however, the lack of `Supp.`/`R.S.` strings confirms that supplements (ch. 10 at 42–53) and session designations (ch. 11 at 54–56) remain unimplemented.
- **Duplication priority.** The `session-law` macro repeats in six active styles, making it the highest-value target for the upcoming publication/status helper extraction. Collapsing these duplicates into a shared helper will prevent future drift once supplement/status strings are added.
- **Fixture coverage.** Existing regression entries `session_law` and `session_law_gammel` in `tests.json` exercise the current macro stack; add-on fixtures should join them once supplement/status strings are implemented to verify both Texas General Laws and historical session-law behaviors.
- **Legal-review triggers.** Because the current macros rely entirely on metadata, the eventual helper must confirm the authoritative abbreviations (`Supp.`, `Leg.`, `R.S.`, `Tex. Reg.`) against Greenbook chs. 10–13 before emitting strings. Capture any deviations for reviewer confirmation when coding the helper logic.
- **Context snippet.**

```
<macro name="session-law">
  <group delimiter=", ">
    <text variable="title"/>
    <text variable="collection-number"/>
    <text variable="number" prefix="ch. "/>
    <group delimiter=" ">
      <text term="section" form="symbol"/>
      <text variable="section"/>
    </group>
    <group delimiter=" ">
      <text variable="volume"/>
      <text variable="container-title"/>
      <text variable="page"/>
    </group>
    <text variable="locator"/>
  </group>
  <text variable="references" prefix=", "/>
</macro>
```

- **Outstanding questions.**
  1. Confirm whether supplements should emit `Supp. ####` or `Supp. ####-####` when covering multi-year updates (ch. 10 examples reference `Supp. 2024`).
  2. Determine if session identifiers need hyphenated regular/special session abbreviations (e.g., `1st C.S.`) for the session-law helper per ch. 11.
  3. Clarify how to handle effective-date parentheticals for administrative materials so the eventual helper can share logic across statutes, session laws, and TAC cites.

### Publication/status helper consolidation plan (2025-11-19)
- **Candidate helper surface.**
  - `supplement-parenthetical` — emits `(Supp. ####)` or `(Supp.)` when the incoming legislation item carries a `note` flag tied to pamphlet supplements (Greenbook ch. 10, p. 44) while remaining silent for bound volumes.
  - `session-law-metadata` — assembles the legislative session label, chapter number, and effective-date notice for session laws so the edition and all TOA variants can reuse a single formatter instead of duplicating the current `<group>` chain (Greenbook ch. 11, pp. 54–56).
  - `administrative-status-tail` — renders `(Tex. Reg. ####)` and effective-date clauses for Texas Register and TAC items, centralizing the parenthetical strings that appear in both `tex-admin-code` and the agency fixtures documented for ch. 16 (pp. 76–84).
- **Fixture impact check.** Running the current regression fixtures (`stat_tax_code_repeat`, `session_law`, `tac_rule`, `texas_register_notice`) confirms they only surface metadata-driven text today; introducing the helpers above will keep baseline output identical unless the JSON supplies supplement/status fields, so existing expectations will not break until new coverage is added. The helper hooks therefore gate their additions on explicit metadata instead of altering default punctuation.
- **Effort estimate.** Wiring the helpers across the edition and five TOA files requires roughly 0.5–0.75 developer days: ~2 hours to implement and namespace the shared macros, ~1 hour to touch each dependent macro (statutes, session laws, TAC, agency registers), and ~1 hour to regenerate fixtures plus spot-check against the PDF examples cited above.
- **Risk assessment.**
  - *Regression risk:* Medium. Consolidating the TOA copies means a mistake in the shared helper could ripple across all TOA leaders/grouped variants. Mitigation: keep isolated commits per helper and capture pre/post citeproc logs in `temp/test-logs/`.
  - *Metadata variance:* High likelihood of encountering translator records that omit `note` or mislabel supplement text. Mitigation: ensure helper defaults to empty output and add TODO coverage for malformed records so fixtures remain representative.
  - *Abbreviation drift:* The helper will introduce hard-coded abbreviations (`Supp.`, `Tex. Reg.`) that must mirror Appendix A; note the dependency in the TODO backlog to cross-check locale terms once the strings land to avoid conflicts with future locale overrides.


### Helper extraction candidates (2025-11-03)
- **Shared code-section renderer.** Implemented via the new `tex-code-section` macro, which now feeds both `tex-statute` and `municipal-code` (note and TOA variants), keeping chapter/section assembly in sync (coverage: `stat_*` + municipal fixtures).
- **Administrative code core.** Centralized the shared block as `tex-admin-core`, reused in the edition and all TOA families while preserving Texas Register `locator` handling; this sets the stage for future `tex-admin-code-short` work (fixtures `tac_rule`/`toa_tac_rule`).
- **Cross-reference cue routing.** Once jurisdiction-aware cues are restored, statutes, rules, and admin materials should reuse the same helper call chain rather than embedding ad-hoc strings. Documenting this now ensures any future `tex-*-cross-reference` macros source their cue from one place. Effort: low—requires updating the helper and ensuring pending macros reference it. Coverage: future statute/rule fixtures will need explicit cross-reference cases; add new JSON entries alongside the existing `stat_*` and `rule_*` items when implementation work begins.
- **Year fallback guard.** Added the `short-pinpoint-year` helper to collapse missing `issued` values in treatise/CLE short forms. New fixtures `treatise_undated` (Ch. 18, pp. 93–95) and `cle_undated` (Ch. 19, p. 96) verify the guard and provide coverage for undated materials.

## Citation Requirement Matrix
| Citation Type | Required CSL Variables | Ordering & Punctuation | Mandatory Abbreviations | Short-Form, Parenthetical & Signal Notes | Footnote vs. Bibliography | Greenbook Reference |
| --- | --- | --- | --- | --- | --- | --- |
| Texas Supreme Court cases | `title`, `volume`, `container-title` (reporter), `page`, `locator`, `authority`, `issued`, `collection-number` (cause), `URL` for slip opinions | *Case Name* (italic) → volume reporter page, pinpoint → `(Tex. year)`; append subsequent history separated by commas; slip opinions include `No.` + cause, `slip op. at` locator before parenthetical | Reporter abbreviations (e.g., `S.W.3d`), court `Tex.`; docket prefix `No.` | Short form triggered after first cite; use `Id.` for identical locator, otherwise `Case Name`, `volume` reporter at `locator`; include explanatory parentheticals (e.g., `per curiam`) and italicized signals | Footnotes carry full cite; bibliography lists parties in roman type and drops pinpoint/signal while retaining year parenthetical | Ch. 2, pp. 7–9 |
| Texas Court of Criminal Appeals cases | `title`, `volume`, `container-title`, `page`, `locator`, `authority`, `issued`, `genre` (memo/opinion type), `URL` | Same as Supreme Court but parenthetical `Tex. Crim. App. year`; panel opinions insert `[Panel Op.]` before parenthetical; unpublished designations appended | `Tex. Crim. App.`, `S.W.3d`; `No.` for cause; `mem. op.` | Short form uses `Id.` and party name abbreviations; parentheticals flag `op. on reh'g`, `mem. op.`; signals italicized and limited to Greenbook set (`See`, `See also`, `Cf.`) | Footnotes include publication status note; bibliography drops panel designations unless necessary for identification | Ch. 3, pp. 10–13 |
| Courts of Appeals cases | `title`, `volume`, `container-title`, `page`, `locator`, `authority`, `issued`, `collection-title` (city), `genre`, `URL` | *Case Name* → volume reporter page, pinpoint → `(Tex. App.—City year, pet. history)` with en dash before city; include writ/pet. history abbreviations separated by commas | City abbreviations (`Tex. App.—Austin`), petition codes (`pet. denied`, `writ ref'd n.r.e.`), `mem. op.` | Short form uses city only if multiple courts cited; add parentheticals for `mem. op.`, `per curiam`; signals italicized | Footnotes require petition history; bibliography may omit petition history unless outcome central to authority | Ch. 4, pp. 14–27 |
| Commission of Appeals decisions | `title`, `volume`, `container-title`, `page`, `authority`, `issued`, `genre` | *Case Name* → volume reporter page → `(Tex. Comm'n App. year, judgm't adopted/approved)`; specify disposition in parenthetical | `Tex. Comm'n App.`, `judgm't adopted`, `judgm't approved` | Short form retains disposition note to avoid ambiguity; signals italicized; include parenthetical explanations when unadopted | Footnotes always note adoption status; bibliography may omit disposition if final court noted elsewhere | Ch. 5, pp. 28–30 |
| Mandamus & other original proceedings | `title`, `collection-number` (cause), `authority`, `issued`, `URL`, `locator` | *In re Relator* → `No.` cause, `slip op. at` locator → `(Tex. [App.—City] year, orig. proceeding)`; include reporter cite if released | `orig. proceeding`, `mand.`, `Tex.` or `Tex. App.—City` | Short form uses `In re` + relator and cause number; parentheticals specify relief (`cond. mand.`); signals italicized | Footnotes require procedural posture; bibliography converts to party name without relief parenthetical | Ch. 6, pp. 31–33 |
| Trial court materials | `title`, `authority`, `genre`, `collection-title` (court), `number` (cause), `issued`, `locator` | *Party v. Party*, No. cause (Court, County [State] date) → `order/letter ruling at` locator; records cite volume → `RR vol.` page | `No.`, `RR` for reporter's record, standardized county abbreviations | Short form references `No.` and court abbreviation; parentheticals identify document type (`order denying SJ`); italicized signals limited to persuasive usage | Footnotes must specify document type; bibliography may omit locator and document description | Ch. 7, pp. 34–36 |
| Judicial misconduct tribunals | `title`, `authority`, `collection-title`, `number`, `issued` | *In re Judge* → `No.` docket (Spec. Ct. Rev. year) or `(Rev. Trib. year)`; include disposition after comma | `Spec. Ct. Rev.`, `Rev. Trib.` | Short form retains tribunal abbreviation; parentheticals indicate sanction; italicized signals | Footnotes include sanction description; bibliography lists tribunal without docket if unique | Ch. 8, p. 37 |
| Texas Constitution provisions | `title`, `section`, `volume` (article), `issued`, `note` | `Tex. Const. art.` article, § section (year) with optional parenthetical for amendments | `Tex. Const.`, `art.`, `§` | Short form uses `Tex. Const. art.` or `§` alone; parentheticals flag amendments (`amended 2019`); signals rarely used but follow rule 1 italicization | Footnotes specify year; bibliography omits year unless citing historical text | Ch. 9, pp. 39–40 |
| Current statutes (Texas codes) | `container-title` (code), `section`, `collection-title` (title), `issued`, `note` (supplement), `authority` | `Tex.` Code name `§` section (West year & supp.) or publisher; include parenthetical for supplements | `Tex.`, code abbreviations from Appendix H, `§` | Short form triggered after first mention of code; use `§` locator only; parentheticals for supplements (`Supp. 2024`); signals italicized | Footnotes include publisher/date; bibliography lists code without pinpoint and omits publisher if standard | Ch. 10, pp. 42–53 |
| Historical statutes | `title`, `session`, `chapter-number`, `section`, `issued`, `publisher`, `page` | `Act of` date, `33d Leg., R.S., ch.` number, § section, `1913 Tex. Gen. Laws` page (`repealed 1985`) | `Leg.`, `R.S.`, `Gen. Laws`, status verbs (`repealed`, `expired`) | Short form references `Act of` date with chapter; parenthetical identifies status; signals italicized | Footnotes must state status; bibliography may summarize as `Act of ...` without status note if context clear | Ch. 11, pp. 54–56 |
| Statutory comments & notes | `container-title` (code), `section`, `note`, `issued`, `genre` | `Tex.` Code `§` section `cmt.` (publisher year) with pinpoint to note paragraph | `cmt.`, `revisor's note`, `hist. note` | Short form uses `cmt.` or `note` + section; parentheticals clarify commentary source; signals italicized | Footnotes include publisher; bibliography may group under code with nested note references | Ch. 12, pp. 58–60 |
| Rules of procedure & evidence | `title` (rule), `collection-title` (set), `section` (rule number), `issued`, `note` (effective date), `URL` for electronic | `Tex. R.` Set `R.` rule number (`West year`) with parenthetical for comment | `Tex. R. Civ. P.`, `Tex. R. App. P.`, `Tex. R. Evid.`, comment abbreviations | Short form uses `Tex. R. Civ. P. 21`; parentheticals denote comment (`cmt. to 1997 change`); signals italicized | Footnotes cite publisher/year; bibliography condenses to rule number and promulgation year | Ch. 13, pp. 61–65 |
| Legislative history items | `title`, `genre`, `number` (bill), `collection-title` (legislature), `issued`, `page`, `publisher`, `URL` | `Tex.` Leg. body, `H.B.`/`S.B.` number, `leg.,` session, `Reg. Sess.` (year) → source (e.g., `House Journal, 75th Leg., R.S., at` page) with parenthetical describing document (`bill analysis`) | `H.B.`, `S.B.`, `R.S.`, `C.S.`; chamber abbreviations | Short form references bill number and document type; parentheticals expected to note version (`committee report`); signals italicized | Footnotes detail document type and date; bibliography may group by bill number with subentries for analyses | Ch. 14, pp. 66–72 |
| Formal advisory opinions | `title`, `authority`, `number`, `issued`, `URL`, `genre` | `Tex. Att'y Gen.` Op. No. `KP-0001` (year) with descriptive parenthetical; include letter/open records designations | `Tex. Att'y Gen.`, `Op.`, `LO`, `ORD`; `Tex. Ethics Comm'n` | Short form uses opinion number only; parentheticals describe subject; signals italicized | Footnotes include issuing authority and date; bibliography lists agency and opinion number chronologically | Ch. 15, pp. 73–75 |
| Agency materials (rules & orders) | `title`, `container-title` (TAC/Tex. Reg.), `volume`, `page`, `issued`, `section`, `note` (status) | `Tex. Admin. Code` title number `§` section (`2024`) or `Tex. Reg.` volume at page (`adopted`); include status parenthetical (`emergency rule`) | `Tex. Admin. Code`, `Tex. Reg.`, `§`, status notes | Short form uses `Title § section`; parentheticals indicate action (`proposed rule`); signals italicized | Footnotes include action status; bibliography may separate TAC entries from register notices | Ch. 16, pp. 76–84 |
| State Bar materials | `title`, `container-title` (State Bar publication), `number` (rule), `issued`, `note` | `Tex. Disciplinary Rules Prof'l Conduct` R. number (`State Bar of Tex.` year); ethics opinions follow `State Bar of Tex. Prof'l Ethics Comm., Op.` number (year) | `Tex.`, `Prof'l`, `Comm.`, `Op.` | Short form references rule or opinion number; parentheticals explain subject; signals italicized | Footnotes provide promulgating body; bibliography consolidates under rule/opinion sequence | Ch. 17, pp. 86–91 |
| Books & secondary sources | `author`, `title`, `edition`, `publisher`, `issued`, `locator`, `collection-title` (series) | Author, *Title* `edition` (Publisher year) `at` page; essays include `in` editor, *Title* (publisher year) | Abbreviations for editions (`2d ed.`), editors (`ed.`), translators (`trans.`) | Short form uses author surname and pinpoint (`Smith, at 45`); parentheticals for update services; signals italicized | Footnotes include pinpoint; bibliography lists full publication details without pinpoint | Ch. 18, pp. 93–95 |
| Conference & institute proceedings | `author`, `title`, `container-title`, `collection-title` (program), `issued`, `page`, `publisher` | Author, *Paper Title*, in *Program Title* page (State Bar of Tex. year) with session parenthetical if applicable | `State Bar of Tex.`, `CLE`, `Inst.` | Short form uses author and abbreviated program; parentheticals note session or panel; signals italicized | Footnotes detail sponsoring body; bibliography orders by author with program title retained | Ch. 19, p. 96 |

## Locale Term Override Inventory (2025-03-27)
| Term | Form | Styles | Greenbook usage | Notes |
| --- | --- | --- | --- | --- |
| section | symbol (`§`) | Edition + all TOA variants | `Tex. Const. art. III, § 5(a)` demonstrates the section sign in constitutional cites, and the session-law template repeats the symbol when pairing chapter and section numbers (ch. 9 at 39; ch. 10 at 50). | Ensures constitution, statute, and TAC macros all draw the same glyph once locale packaging is centralized. |
| article | short (`art.`) | Edition + all TOA variants | The same constitutional example abbreviates “article” to “art.” immediately before the Roman numeral (ch. 9 at 39). | Captured now so the eventual shared locale can expose the Texas-specific abbreviation. |
| chapter | short (`ch.`) | Edition + all TOA variants | Session-law guidance abbreviates “chapter” to “ch.” in the Act of May 30, 2005 illustration (ch. 10 at 50). | Keeps a single short form ready for both note and TOA contexts during locale consolidation. |
| rule | short (`R.`) | Edition + all TOA variants | Rule citations print “Tex. R. Civ. P. 97(d)” without repeating the full word “Rule” (ch. 13 at 61). | Mirrors Appendix H abbreviations; marked here to feed the packaging task. |
| paragraph | short (`¶`) | Edition only | Slip-opinion instructions require “slip op. ¶ 2” when pagination is absent (ch. 3 at 30). | Only the note style emits paragraph pinpoints today; evaluate TOA demand when unpublished decisions join the table workflow. |
| ibid | — (`Id.`) | Edition only | Ch. 9.1.1 allows constitutional short forms to use “id.” when appropriate (ch. 9 at 39), matching citeproc’s ibid behavior. | Confirms that the standard `ibid` term can stay mapped to “Id.” for repeated statutes and constitutions. |
| and | — (`and`) | Edition only | Chapter 1’s typography discussion spells out “LARGE AND SMALL CAPITALS,” reinforcing the manual’s preference for written conjunctions over ampersands in rule text (ch. 1 at 3).【d3b9e8†L1-L15】 | Verified the stock `en-US` locale already emits the spelled-out conjunction, so the edition now defers to the default term instead of carrying a redundant override.【6f5683†L1-L35】 |

### Locale packaging decision (2025-11-02)
- Validated `temp/locales/locales-en-US-x-texas-greenbook.xml` metadata (title, id, license, updated timestamp, and `style-options`) and the bundled abbreviation terms (`art.`, `ch.`, `R.`, `§`, `¶`, `Id.`). With the file in place, no further packaging steps are needed before wiring the citation styles to the shared locale.

## Memo Opinion Indicator Audit (2025-03-27)
- `texas-greenbook-15th-edition.csl` routes every case through `case-parenthetical-stack`, which simply echoes `genre` and `medium` via `parenthetical-slip-op` with no conditional gating (ll. 144–158). Memorandum, per curiam, and rehearing parentheticals therefore appear only when translators populate `genre`/`medium`.
- The TOA family (`texas-greenbook-15th-toa*.csl`) defines the same helper as two single-node `choose` blocks that emit `genre`/`medium` for each case entry (e.g., `texas-greenbook-15th-toa.csl` ll. 58–112). Tables omit the explanatory-parenthetical macro, so memo markers display once in the case block and nowhere else.
- No macros promote `status` to memo terminology; `parenthetical-procedural-status` is limited to `status`/`note` combinations for things like “orig. proceeding.” This inventory confirms memo handling is entirely data-driven today and documents the gap for future conditional helpers or locale terms.

## Supplemental Reference Status (2025-03-27)
- **Uniform-Format-Manual-07012010.pdf** — 30-page, text-searchable PDF covering reporter formatting; stored in `temp/` and requires no OCR.
- **How-Court-Rules-Are-Made.pdf** — 10-page, searchable PDF summarizing rulemaking procedures, ready for citation provenance without preprocessing.
- **technology-standards.pdf** — 35-page Judicial Committee on Information Technology standards document; text extraction succeeds, so administrative macro work can quote directly.
- **texas-rules-of-appellate-procedure.pdf**, **texas-rules-of-civil-procedure-august-31-2025.pdf**, **texas-rules-of-evidence-effective-912025.pdf** — official rule compilations (146, 351, and 62 pages). Each parsed cleanly with `PyPDF2`, confirming metadata can be mined for pinpoint cites.
- **texas-court-rules-history-process.html** — archived HTML summary of the rulemaking timeline; keep alongside the PDFs as the canonical non-PDF supplement.
- All supplemental references under `temp/` are now inventoried as searchable, so no additional OCR passes are required before expanding locale or macro coverage.
- Each file originates from publicly available judiciary resources; no special licensing restrictions noted beyond standard attribution expectations.
- Backups live in-repo under `temp/`; refresh from https://www.txcourts.gov/rules-forms/rules-standards/ when official updates publish.
- **OCR spot-check (2025-11-02).** Confirmed the Uniform Format Manual (30 pp.), How Court Rules Are Made (10 pp.), and Technology Standards (35 pp.) remain fully searchable by extracting sample text with `PyPDF2`; no supplementary OCR exports are necessary at this time.

## Chapter Highlights
### Chapter 1 – Briefs and Legal Memoranda (pp. 3–5)
- Distinguishes roman and italic typefaces for pleadings, allowing large and small capitals for emphasis consistent with recent Bluebook updates (1.0, 1.5).
- Requires italicizing introductory signals, case names, and publication titles while keeping reporter, jurisdiction, and author names in roman type (1.1–1.3).
- Notes stylistic italics limits, foreign word treatment, and directs that statutes, rules, and other authorities remain in roman type (1.5–1.6).

### Chapter 2 – Texas Supreme Court (pp. 7–9)
- Basic citations include case name, South Western Reporter reference, pinpoint page, and “Tex.” parenthetical with year; subsequent history appended when relevant (2.1.1).
- Slip opinions must cite electronic sources with cause numbers, pinpoint references, and date; paginated slip opinions use “slip op.” with page numbers, and Texas Supreme Court Journal citations add volume/page plus electronic parallel cites (2.1.2).
- U.S. Supreme Court dispositions are included except older cert. denials; historical guidance distinguishes Texas Reports-only periods and when parallel citations may be required (2.2–2.3).

### Chapter 3 – Texas Court of Criminal Appeals (pp. 10–13)
- Current citations mirror Supreme Court format with “Tex. Crim. App.” parentheticals and warnings that unpublished opinions lack precedential value (3.1.1).
- Panel opinions (1978–1982) require “[Panel Op.]” and electronic slip citations follow the same cause-number conventions, including paragraph pinpoints when pagination is absent (3.1.2–3.1.3).
- Subsequent history captures U.S. Supreme Court review, and historical notes explain when Texas Criminal Reports parallel citations become necessary (3.2–3.3).

### Chapter 4 – Courts of Appeals (pp. 14–27)
- Post-1981 cases cite only the South Western Reporter with em-dash-separated city designations, writ/petition histories, and optional weight-of-authority parentheticals (4.1.1).
- Memorandum, per curiam, and “not designated for publication” designations require explicit parentheticals, with distinctions between civil and criminal publication practices and pre-2003 “do not publish” notes (4.1.2).
- Recent opinions rely on electronic citations paralleling slip-opinion rules; historic instructions cover pre-1981 civil appeals reporters, city identification (including special Houston rules), and petition/writ notation tables (4.1.3–4.7, 4.2–4.6).

#### Memo opinion typography check (2025-11-01)
- The examples on p. 16 show memorandum opinion parentheticals appended in roman type after the court/date block: `Richardson v. Kays, No. 02-03-241-CV, 2003 WL 22457054, at *1 (Tex. App.—Fort Worth Oct. 30, 2003, no pet.) (per curiam) (mem. op.)` and `In re Int’l Profit Assocs., Inc., 274 S.W.3d 696, 697 (Tex. App.—Corpus Christi 2008, orig. proceeding) (per curiam) (mem. op.), mand. granted, 274 S.W.3d 672, 680 (Tex. 2009) (per curiam).` This confirms that the case names remain italicized while `(per curiam)` and `(mem. op.)` stay in roman text consistent with Chapter 1 guidance.【F:temp/Greenbook_15thEdition.pdf†L70-L118】
- Page 17 illustrates the criminal-side variant `Green v. State, No. 12-12-00249-CR, 2012 WL 3116252, at *1 (Tex. App.—Tyler July 31, 2012, no pet.) (per curiam) (mem. op., not designated for publication).`, reiterating that memorandum opinion parentheticals keep roman styling even when the explanatory phrase adds “not designated for publication.”【F:temp/Greenbook_15thEdition.pdf†L118-L168】
- Slip-opinion citations on p. 18 (`Jaxson v. Morgan, No. 14-04-00785-CV, slip op. ¶ 4 (Tex. App.—Houston [14th Dist.] Apr. 6, 2006, no pet.) (mem. op.)`) pair the `(mem. op.)` cue with the paragraph pinpoint; no italics shift occurs, so the CSL implementation can rely on roman rendering for these explanatory tails without additional styling hooks.【F:temp/Greenbook_15thEdition.pdf†L168-L212】

#### Memo opinion regression run (2025-03-17)
- Added explicit `font-style="normal"` attributes to the `parenthetical-slip-op` macro across the note and TOA styles so `genre`/`medium` parentheticals (including `(mem. op.)`) cannot inherit italics from surrounding macros.【F:temp/texas-greenbook-15th-edition.csl†L143-L155】【F:temp/texas-greenbook-15th-toa.csl†L58-L63】【F:temp/texas-greenbook-15th-toa-grouped.csl†L99-L104】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L61-L66】【F:temp/texas-greenbook-15th-toa-leaders.csl†L58-L63】【F:temp/texas-greenbook-15th-toa-by-reporter.csl†L54-L59】
- Executed `python temp/run_tests.py --tests temp/tests.json --style temp/texas-greenbook-15th-edition.csl --expected temp/expected.txt` to confirm memo opinion fixtures continue to match expectations; stored the log at `temp/test-logs/2025-03-17_memo-opinion.txt` for regression traceability.【F:temp/test-logs/2025-03-17_memo-opinion.txt†L1-L39】
- Re-checked Chapter 4 Format Guide examples (p. 14 / PDF p. 32) to confirm the roman `(mem. op.)` parentheticals remain authoritative references for the CSL output.【F:temp/Greenbook_15thEdition.pdf†L294-L320】

### Chapter 5 – Commission of Appeals (pp. 28–30)
- Differentiates the Commission aiding criminal appeals versus civil commissions, detailing how to cite judgments adopted, approved, or holding-approved with proper parenthetical descriptions (5.1–5.2).

### Chapter 6 – Mandamus and Other Original Proceedings (pp. 31–33)
- Original proceedings in the Supreme Court follow Chapter 2 conventions with an additional “orig. proceeding” parenthetical; courts of appeals mandamus citations track petition status and Texas Supreme Court actions (6.1–6.2).

### Chapter 7 – Trial Courts (pp. 34–36)
- Provides basic citation form for trial-court decisions, emphasizes standardized court abbreviations, and addresses record-on-appeal citations (including pre-1997 distinctions) and filings (7.1–7.4).

### Chapter 8 – Judicial Misconduct Tribunals (p. 37)
- Summarizes citation formats for the Special Court of Review and Review Tribunal decisions, aligning them with court designations and procedural posture notes (8.1–8.2).

### Chapter 9 – Texas Constitution (pp. 39–40)
- Current constitution citations combine article and section references with optional short forms; repealed or transitional provisions and interpretive commentaries receive tailored treatments (9.1–9.4).

### Chapter 10 – Current Statutes (pp. 42–53)
- Establishes naming conventions for subject-matter codes, historical facts, supplements, and multi-section citations; differentiates codified, uncodified, independent, and auxiliary laws (10.1–10.2).
- Session-law citations require statute name, legislature/session, chapter/section, publication, and location; unpublished statutes, electronic sources, and municipal ordinances receive specialized formats (10.3–10.6).

### Chapter 11 – Statutes No Longer in Effect (pp. 54–56)
- Details how to cite amended, repealed, expired, pre-1898, and pre-statehood statutes with clear indication of their status (11.1–11.3).

### Chapter 12 – Comments and Notes Accompanying Statutes (pp. 58–60)
- Addresses comments, revisor’s notes, historical notes, and UCC commentary with instructions on identifying the source and contextualizing the note (12.1–12.2).

### Chapter 13 – Rules of Procedure and Evidence (pp. 61–65)
- Civil procedure rules require designating current or superseded rule status, citing commentaries, and identifying Rules of Judicial Administration; appellate rules include appendix references for criminal cases (13.1–13.3).
- Local court rules are cited by jurisdiction and promulgating authority (13.4).

### Chapter 14 – Legislative History (pp. 66–72)
- Outlines citation formats for bills, resolutions, journals, fiscal notes, committee minutes, testimony, rules, and gubernatorial messages, including date and version parentheticals when multiple analyses exist (14.1–14.7).

### Chapter 15 – Formal Advisory Opinions (pp. 73–75)
- Provides conventions for attorney general opinions (including letter opinions and open records rulings), secretary of state decisions, and Texas Ethics Commission guidance with numbering and date requirements (15.1–15.3).

### Chapter 16 – Agency Material (pp. 76–84)
- Administrative rules in the Texas Administrative Code and Register require citations specifying volume, pinpoint pages, codification status, and disposition; emergency and repealed rules add status parentheticals (16.1).
- Administrative orders cite agency, docket numbers, dates, and publication references; reports and bulletins note author type and circulation (16.2–16.3).

### Chapter 17 – State Bar Materials (pp. 86–91)
- Includes citing State Bar rules, disciplinary rules, ethics opinions, rules of disciplinary procedure, code of judicial conduct, removal procedures, and admissions rules with clear short forms and revision notes (17.1–17.7).

### Chapter 18 – Books (pp. 93–95)
- Summarizes book citations, encyclopedias, essays, collections, and form books, highlighting when to note editors, publication series, or unpublished status (18.1–18.4).

### Chapter 19 – Conference and Institute Proceedings (p. 96)
- Distinguishes bound proceedings, State Bar professional development materials, and special series papers with required program names, volumes, and pinpoint citations (19.1–19.3).

## Appendices, Tables, and Abbreviations
- **Appendix A** (pp. 98–99) covers Texas Reports cases from 1846–1886 and Republic-era decisions, including term-based citations and rare parallel references.
- **Appendix B** (pp. 100–101) guides citations to the old Texas Court of Appeals (criminal and civil) and when South Western Reporter parallels apply.
- **Appendix C** (pp. 102–104) addresses Commission of Appeals decisions, distinguishing adopted versus unadopted opinions and citing Posey and White & Willson reports.
- **Appendix D** (pp. 105–108) tabulates petition-for-review notations in the Supreme Court of Texas, mapping each abbreviation to procedural meaning.
- **Appendix E** (pp. 109–111) lists writ-of-error notation meanings before September 1, 1997.
- **Appendix F** (pp. 112–113) catalogs Court of Criminal Appeals petition-for-review notations.
- **Appendix G** (pp. 114–115) inventories prior Texas constitutions and related convention ordinances.
- **Appendix H** (pp. 116–117) provides abbreviation tables for subject-matter codes, independent codes, and current rules.
- **Appendix I** (p. 118) records dates of pre-1876 legislative sessions.
- **Appendix J** (pp. 120–121) lists chief and associate justices of the courts of civil appeals (1892–1911).
- **Appendix K** (pp. 121–122) outlines obsolete procedural and evidentiary rules, including former ethics codes.

## Supplementary Reference Findings
- **Technology Standards v10.0 (July 2025):** Requires e-filed documents to be text-searchable PDFs on 8.5×11" pages without security restrictions, 300 DPI for scans, Latin-1 filenames ≤50 characters, and allows courts to mandate consolidated PDFs with bookmarks; also dictates supported media formats and prohibits courts from imposing local-form requirements (pp. 2–5).
- **Texas Rules of Appellate Procedure (effective 2025):** Rule 47 mandates memorandum opinions for routine issues, bars "do not publish" labels after 2003, and defines publication/notation practices aligned with Greenbook petition-history rules (pp. 47.3–47.7). Rule 52 governs original proceedings procedures referenced in Chapter 6.
- **Texas Rules of Civil Procedure (Aug. 31, 2025):** Rule 21(a) defines "lead document" and filing formats cited by the technology standards; Rule 97(d) exemplifies cross-referenced civil rule citations.
- **Texas Rules of Evidence (Sept. 1, 2025):** Provides context for citing rules, comments, and former provisions as addressed in Chapters 13 and 17.
- **Uniform Format Manual for Texas Reporters’ Records (2010 revision):** Specifies typography, margins, line numbering, and electronic transcript formatting referenced for record citation conventions.
- **How Texas Court Rules Are Made (2010):** Explains Supreme Court rulemaking authority and procedures relevant to legislative-history and rule-comment citations.
- **Rule abbreviation cross-checks:** Uniform Format Manual pp. 7 & 13 cite "Tex. R. App. P. 13.2(b)" and "Tex. R. Civ. P. 199.1(c)" when defining court reporter duties, mirroring the shorthand recorded for TRAP/TRCP cites in this notebook; the 2025 Texas Rules of Civil Procedure reiterate the same format in Rule 736 captions (p. 331), and the Greenbook introduction references "Tex. R. Evid. 405(b)" (p. 2), keeping the rule abbreviations consistent across sources.
- No conflicting abbreviations surfaced across the surveyed sources, so no escalation is required.

| Authority family | Greenbook short form | Supplemental confirmation | Notes |
| --- | --- | --- | --- |
| Texas Rules of Appellate Procedure | Tex. R. App. P. 2 | Uniform Format Manual p. 7 (`Tex. R. App. P. 13.2(b)`) | Matches `NOTES.md` entry; no alternate abbreviation located. |
| Texas Rules of Civil Procedure | Tex. R. Civ. P. 97(d) | Uniform Format Manual p. 13 (`Tex. R. Civ. P. 199.1(c)`); TRCP 736 caption guidance p. 331 | Forms align; no discrepancies recorded. |
| Texas Rules of Evidence | Tex. R. Evid. 405(b) | Greenbook p. 2 introduction (`Tex. R. Evid. 405(b)`) | Supplemental PDFs lack examples; Greenbook remains authoritative. |

- **Historical reporter citations verified:** Greenbook Appendix C flags Charles L. Robards’s *Synopses of the Decisions of the Supreme Court of the State of Texas* (p. 117), the four-volume *Condensed Reports of Cases in the Court of Appeals of Texas* by Judges White & Willson (p. 119), and Posey’s *Texas Unreported Cases* (p. 120), aligning with the historical reporter inventory maintained for fixture planning.

### Supplemental reference gap review (2025-11-01)
- Re-read the Uniform Format Manual transcript examples (pp. 7, 13) and the 2025 Texas procedural rule updates (TRCP p. 331; TRAP Rule 13.2(b)) to confirm abbreviations already match the Greenbook authority forms recorded above; no new locale terms are required beyond the shared `art.`, `ch.`, `R.`, and pilcrow entries captured in the consolidated locale.【F:temp/Uniform-Format-Manual-07012010.pdf†L1-L12】【F:temp/texas-rules-of-civil-procedure-august-31-2025.pdf†L1-L12】【F:temp/Greenbook_15thEdition.pdf†L40-L92】
- Reviewed the existing statute, rule, and agency fixtures in `tests.json`/`expected.txt` alongside the supplemental sources and found that each authority type already exercises the abbreviations the manuals reinforce (e.g., Tex. R. Civ. P. 97(d), Tex. R. App. P. 2); no additional citeproc JSON scenarios are needed until new authority classes emerge from future research.【F:temp/tests.json†L1-L166】【F:temp/expected.txt†L1-L214】
- Documented the conclusion so future contributors know that supplemental reference coverage is up to date; re-open the TODO item once new materials introduce abbreviations or structures absent from the current macros.

## Existing CSL Style Inventory

### Bluebook-Derived Styles
- **bluebook-law-review.csl** keeps an `en-US` default locale with custom term overrides for verbs such as "ed." and "trans." alongside a bespoke `author`/`author-short` stack that toggles italics and small caps based on item type, mirroring the Bluebook note hierarchy.【F:bluebook-law-review.csl†L2-L91】 Its `source`, `issuance`, and `container` macros orchestrate conditional reporter versus periodical layouts, including year-bearing parentheticals and pinpoint delivery, while the citation layout uses `ibid`, `supra`, and locator logic gated by position testing.【F:bluebook-law-review.csl†L122-L388】
- **bluebook-law-review-with-abstract.csl** inherits the same macro set, adding only metadata changes and retaining the Bluebook-driven `source` cascade and term overrides, so any adjustments can be centralized in the shared macro names without diverging layouts.【F:bluebook-law-review-with-abstract.csl†L2-L188】
- **bluebook-inline.csl** exposes reusable `source-short` and `source-long` macros for parallel inline versus full-text cites, coupled with an `access` macro that emits "last visited" parentheticals—useful patterns for Greenbook slip-opinion URLs and short-form logic in in-text contexts.【F:bluebook-inline.csl†L1-L200】
- **law-citation-manual.csl** layers multilingual locales (`zh` and `en`) with tailored date formats, symbol terms, and macros that segment source handling across legislation, legal cases, blogs, and secondary authorities—demonstrating how locale-specific macros (`source-zh`, `access-zh`) can coexist with an English template lineage from `bluebook-law-review`.【F:law-citation-manual.csl†L1-L200】

### Legal-Prefix Dependent Styles
- **dependent/legal-medicine.csl** and **dependent/legal-and-criminological-psychology.csl** are thin wrappers that delegate entirely to `elsevier-with-titles` and `apa`, respectively; they only set metadata and locales, so any substantive behavior must be driven through the parent styles rather than direct edits.【F:dependent/legal-medicine.csl†L1-L14】【F:dependent/legal-and-criminological-psychology.csl†L1-L16】

### Texas Greenbook Drafts and TOA Variants
- **Draft 0** implements a minimal Greenbook approximation with generic macros (`case-cite`, `statute-cite`, `article-cite`) and uniform bibliography/citation routing, lacking template inheritance or specialized Texas variables such as `status` or `collection-number`. This serves as a baseline for feature gaps (no slip-opinion handling, no municipal code logic).【F:temp/texas-greenbook-15th-draft0.csl†L1-L195】
- **Draft 1** pivots to a Bluebook template, introducing Greenbook-specific macros for constitutions, statutes, administrative codes, and TOA-ready parentheticals; it also adds `subsequent-history` handling via the `references` variable and expands the citation chooser to cover regulations, reports, and web materials.【F:temp/texas-greenbook-15th-draft1.csl†L1-L280】
- **Draft 2** restructures the architecture around type-focused macros (`legal-case`, `session-law`, `tac-core`, `municipal-code`, `ag-opinion`) and introduces conditional branching on variables like `volume`, `authority`, and `chapter-number` to distinguish codes versus constitutions, hinting at the data-shaping expected from translators or pre-processing layers.【F:temp/texas-greenbook-15th-draft2.csl†L1-L359】
- **Draft 3** retains the Draft 2 macro library while layering in additional fallbacks (`book-like`, `web`) and a revised citation switch that defers to master templates for cases, statutes, and regulations. It also embeds `parenthetical-slip-op` and `pinpoint` logic for Westlaw citations, illustrating how to mix print and electronic reporters within the same macro stack.【F:temp/texas-greenbook-15th-draft3.csl†L1-L428】
- **Table-of-Authorities variants** (e.g., `texas-greenbook-15th-toa.csl`, `texas-greenbook-15th-toa-grouped-leaders.csl`) reuse the master macros but customize bibliography sorting, grouping, and dotted-leader output, showing how TOA requirements can be met with selective macro reuse and layout tweaks.【F:temp/texas-greenbook-15th-toa.csl†L1-L166】【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L1-L190】

## Draft 3 Macro Inventory and Dependencies

### Macro Catalog
| Macro | Purpose | Classification |
| --- | --- | --- |
| `author` | Formats author names with short-form labels for secondary sources. | Shared helper |
| `case-name` | Emits italicized case titles. | Authority-specific (Texas cases) |
| `reporter` | Bundles volume, reporter abbreviation, and first page for generalized case citations. | Shared helper |
| `court-year` | Wraps court and year parenthetical for generalized case entries. | Shared helper |
| `subsequent-history` | Emits appended history stored in `references`. | Authority-specific (case follow-on) |
| `tex-constitution` | Full citation assembly for Texas Constitution provisions. | Authority-specific (constitution) |
| `tex-statute` | Formats Texas statutory code citations using container-title and section. | Authority-specific (statutes) |
| `tex-admin-code` | Outputs Texas Administrative Code references with year and title parentheticals. | Authority-specific (administrative code) |
| `tex-register` | Handles Texas Register notices including pinpoint and note parentheticals. | Authority-specific (register notices) |
| `book-like` | Shared layout for books, chapters, and reports. | Shared helper |
| `article-journal` | Shared layout for journal articles. | Shared helper |
| `web` | Shared layout for web resources with access dates. | Shared helper |
| `reporter-print` | Specialized print-reporter block for case citations. | Shared helper |
| `reporter-wl` | Formats Westlaw-equivalent citations when print reporter is missing. | Shared helper |
| `court-and-date` | Chooses between print- and slip-opinion parentheticals for cases. | Shared helper |
| `parenthetical-slip-op` | Emits weight-of-authority explanatory parentheticals from `genre`/`medium`. | Shared helper |
| `legal-case` | Top-level case citation assembler combining reporter, pinpoint, and parentheticals. | Authority-specific (cases) |
| `statute-code` | Simplified code citation used when metadata is incomplete. | Authority-specific (fallback statutes) |
| `constitution-core` | Constitution citation core used by alternative layouts. | Authority-specific (constitution helper) |
| `session-law` | Assembles session-law (Texas General Laws) citations. | Authority-specific (session laws) |
| `tac-core` | Core layout for Texas Administrative Code entries. | Authority-specific (administrative code) |
| `rule-core` | Outputs rule citations (procedural/evidentiary). | Authority-specific (rules) |
| `municipal-code` | Handles municipal ordinance citations. | Authority-specific (municipal) |
| `ag-opinion` | Formats Attorney General opinion references. | Authority-specific (advisory opinions) |
| `journal-article` | Alternative journal layout with italicized container titles. | Shared helper |
| `pinpoint` | Applies pinpoint logic for both print and Westlaw cites. | Shared helper |

### Layout Hierarchy Diagram
```
Citation Layout
├─ legal_case → legal-case
│   ├─ case-name
│   ├─ reporter-print / reporter-wl
│   ├─ pinpoint
│   └─ court-and-date → parenthetical-slip-op
├─ legislation/bill → tex-statute │ statute-code (fallback)
├─ treaty/standard → tac-core
├─ article-journal → author
├─ book/chapter/report → book-like → author
├─ web/post → web
└─ default → title + issued

Bibliography Layout
├─ legal_case → case-name + reporter + court-year
├─ legislation/bill → tex-statute
├─ treaty/standard → tex-admin-code
├─ article-journal → article-journal
├─ book/chapter/report → book-like → author
├─ web/post → web
└─ default → title + issued

Authority-Specific Supporting Macros
├─ Constitution pipeline → {tex-constitution, constitution-core}
├─ Administrative code pipeline → {tex-admin-code, tac-core}
├─ Session laws → session-law
├─ Municipal code → municipal-code
└─ Advisory opinions → ag-opinion
```

### Missing Shared Helpers and Required Additions
- **Case law pipeline**
  - *Pinpoints*: Current `pinpoint` macro distinguishes print versus Westlaw but cannot emit multiple pincites or textual locators (e.g., `at *4`, `slip op. at`). Add a shared helper that normalizes slip-opinion locators (e.g., `pinpoint-slip`) and allows comma-delimited pincite arrays for both note and bibliography contexts.
  - *Parentheticals*: `parenthetical-slip-op` only reads `genre`/`medium`; introduce a generalized `explanatory-parenthetical` helper that can handle procedural phrases (`per curiam`, `mem. op.`, `orig. proceeding`) by inspecting `status`, `genre`, and custom fields.
  - *Docket metadata*: Add a shared `docket-block` helper to capture `collection-number` and `number` for slip opinions and mandamus proceedings so that `legal-case` and mandamus-specific macros can reuse the logic.
- **Statutory/constitution pipeline**
  - *Pinpoints*: No macro supports subsection pinpoints beyond single `section`. Implement a `section-pinpoint` helper that accepts `section`, `subdivision`, and paragraph indicators to support statutory notes and constitutional subsections.
  - *Parentheticals*: `tex-statute` inlines supplemental notes but lacks shared logic for publisher/year parentheticals. Create a `publication-parenthetical` helper to compute `(West 2025)` style phrases shared between statutes, constitutions, and rules.
  - *Docket metadata*: For session laws and legislative history, add a `legislative-history-metadata` helper to unify bill number, session, and disposition fields for use across `session-law` and future committee-report macros.
- **Administrative/rule pipeline**
  - *Pinpoints*: `tex-admin-code` and `tac-core` emit only single sections. Extend with a `rule-pinpoint` helper that accommodates `note`, `appendix`, or comment locators (e.g., `cmt. to 1997 change`).
  - *Parentheticals*: Introduce a shared `status-parenthetical` helper that formats `adopted`, `emergency rule`, or `effective` notes for both TAC and Register citations using `status`/`note` variables.
  - *Docket metadata*: Agency orders and ethics opinions use numbers (`No.`, `Op.`) but rely on bespoke text. Build a `agency-docket` helper to standardize authority + opinion number handling for `ag-opinion`, `municipal-code`, and forthcoming agency-material macros.

### Spec Cross-References for Planned Helpers
| Planned helper | Structural notes | Spec validation |
| --- | --- | --- |
| `pinpoint-slip` | Branch slip-opinion versus print handling with `<choose>` and wrap locator label/text pairs in a `<group>` so the macro can be reused by both citation and bibliography layouts. | Macros may contain rendering elements such as `<choose>`, while `<group>`, `<label>`, and `<text>` provide the permitted nesting and symbol/short-form controls needed for locator output.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L741-L778】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1814-L1859】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1775-L1812】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1102-L1126】 |
| `explanatory-parenthetical` | Emit procedural phrases from `status`/`genre` inside a parenthetical `<group>` that applies affixes and italic formatting as needed. | `<group>` supports affixes/formatting for bundled rendering elements, and `<text>` allows the macro to draw variables or terms without violating CSL nesting rules.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1814-L1840】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1102-L1126】 |
| `docket-block` | Consolidate docket numbers and slip identifiers via a `<group>` that concatenates prefixed `<text>` nodes (e.g., `No.` + `collection-number`). | The spec permits macros to assemble grouped variable content with `<group>` and `<text>` so long as only rendering elements appear inside the macro body.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L741-L778】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1814-L1840】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1102-L1126】 |
| `section-pinpoint` | Pair section labels with subsection text using a `<group>` that calls `<label form="symbol" variable="section">` before the `<text>` node. | `<label>` may target number variables and supports symbol forms, letting the helper emit `§/§§` while staying within the allowed rendering stack for macros.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L741-L778】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1775-L1812】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1814-L1840】 |
| `publication-parenthetical` | Use a `<group>` with prefix/suffix to emit publisher/year notes drawn from `note`, `title`, or `issued` variables following the main citation fragments. | Group-level affixes are expressly supported, and `<text>` pulls the needed variables without exceeding the macro’s rendering scope.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1814-L1840】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1102-L1126】 |
| `legislative-history-metadata` | Combine bill numbers, session info, and chamber references inside `<choose>` branches so incomplete records can fall back gracefully. | `<choose>` blocks in macros can hold any rendering element except `<layout>`, enabling conditional assembly of text variables and terms based on metadata completeness.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L741-L778】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1842-L1859】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1102-L1126】 |
| `rule-pinpoint` | Extend the statutory pinpoint helper to recognize `locator="rule"` and render rule-specific labels alongside subsection text. | CSL’s locator list already enumerates `rule`, allowing `<label variable="locator" form="short"/>` inside helper macros without leaving the defined vocabulary.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L741-L778】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1775-L1812】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L2827-L2855】 |
| `status-parenthetical` | Wrap status strings (e.g., `emergency rule`, `repealed`) in a `<group>` that appends a parenthetical after the main citation fragments. | The combination of `<group>` affixes and `<text>` variable calls stays within allowed rendering behavior for macros, ensuring cite processors recognize the output as standard text.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L741-L778】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1814-L1840】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1102-L1126】 |
| `agency-docket` | Format opinion numbers with standardized prefixes by sequencing `<text>` nodes inside a `<group>` shared across agency macros. | Macros assembling numbered identifiers solely via `<group>` and `<text>` remain spec-compliant and interoperable across citeproc implementations.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L741-L778】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1814-L1840】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1102-L1126】 |

### Locale Override Compliance
| Planned locale change | Spec support |
| --- | --- |
| Promote short `rule` term to `R.` | `<locale>` blocks may redefine term forms for a language, and `cs:term form="short"` is expressly permitted for localized abbreviations.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L780-L800】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L939-L960】 |
| Normalize `chapter` short form to `ch.` | The same `cs:term form="short"` mechanism supports alternate abbreviations such as `ch.` while keeping fallback behavior intact.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L780-L800】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L939-L960】 |
| Add an explicit short `article` term (`art.`) | Styles may introduce previously undefined short forms through locale overrides without breaking fallback chains for the long form.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L780-L800】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L939-L960】 |
| Replace paragraph short form with `¶` | The `form="symbol"` option allows locale overrides to emit pilcrow symbols for paragraph labels, matching Greenbook typography while remaining spec-compliant.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L939-L960】 |
| Verify section symbol reuse (`§`) | Retaining the symbol form via locale overrides is permissible and automatically inherits fallback to the stock value when identical.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L780-L800】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L939-L960】 |

### Additional Spec Review Needed
- Confirm how Greenbook locators such as “slip op.” and “orig. proceeding” should map onto the standard CSL locator vocabulary (`page`, `timestamp`, `sub-verbo`, etc.) or whether translator normalization is required before citeproc evaluation.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L2827-L2855】
- Validate whether future parenthetical helpers should leverage `cs:number` or ordinal term overrides when emitting petition-history shorthand, ensuring alignment with the ordinal behavior documented in the Terms section.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L939-L1009】

### Citeproc Processor Compatibility Check
- citeproc-js and Zotero target CSL 1.0.2, so limiting the planned helpers to the standard rendering elements (`cs:macro`, `cs:choose`, `cs:group`, `cs:label`, `cs:text`) avoids undefined behavior and ensures processors will interpret the new helpers consistently across citation and bibliography contexts.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L741-L778】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1814-L1859】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1775-L1812】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L1102-L1126】
- Locale overrides will remain portable because the adjustments stay within the `cs:locale`/`cs:term` mechanisms that citeproc engines already consume, preventing divergence from processor expectations while letting multiple drafts share a custom locale file.【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L780-L800】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L939-L960】

### Patterns Requiring Greenbook-Specific Adaptation
- Bluebook macros heavily rely on `ibid`, `supra`, and symbol-based author formatting; Greenbook short-form rules will need alternative position handling (e.g., "Id." versus "supra" suppression) and customized italics behavior for case names within short cites.【F:bluebook-law-review.csl†L320-L384】
- The Draft 2/3 macros expect structured variables (`authority`, `status`, `collection-number`) that may not be present in raw Zotero data; translators or plugins will need to map Greenbook fields (petition histories, docket numbers) into these slots or extend macros to compute fallbacks.【F:temp/texas-greenbook-15th-draft2.csl†L52-L112】【F:temp/texas-greenbook-15th-draft3.csl†L267-L323】
- TOA layouts currently output leaders using static text and rely on type-based grouping; Greenbook's alphabetical subsections (e.g., Cases subdivided by jurisdiction) may require enhanced sort keys and localized headings beyond the numeric group tokens seen in the grouped-leaders variant.【F:temp/texas-greenbook-15th-toa-grouped-leaders.csl†L116-L189】
- None of the drafts yet automate slip-opinion parentheticals, cite-check signals, or court/region abbreviations; leveraging Bluebook inline patterns for cause-number reporting and `access` macros could bridge this gap for Greenbook electronic sources.【F:bluebook-inline.csl†L27-L101】【F:temp/texas-greenbook-15th-draft1.csl†L196-L226】

## Unresolved Questions & Follow-Up Items
1. **Uniform Format Manual OCR:** The PDF appears to be image-based; confirm whether an OCR text version is available to extract precise citation requirements.
2. **TRCP/TRAP Cross-References:** Validate whether additional rules (beyond TRCP 21 and TRAP 47/52) are incorporated by the Greenbook for future automation (e.g., TRAP 9 formatting, TRCP 297 findings).
3. **Legacy Reporter Availability:** Determine availability of historical reporters (Robards, White & Willson, Posey) for automated citation validation.

## Citation Matrix Completeness Review
- The matrix enumerates every substantive category appearing in the Table of Contents overview (Chs. 1–19), ensuring that case law, constitutional, statutory, rule-based, legislative, administrative, professional, and secondary-source citations each have dedicated rows aligned with their chapter-specific guidance.【F:temp/NOTES.md†L5-L111】【F:temp/NOTES.md†L113-L187】
- Chapter 1’s brief-formatting directives inform the italicization and signal usage conventions embedded across table entries, maintaining consistency with the Greenbook’s introductory typography rules.【F:temp/NOTES.md†L5-L44】【F:temp/NOTES.md†L113-L187】
- Appendices A–K supply abbreviation inventories and historical contexts that are reflected in the mandatory abbreviation columns for reporters, petition histories, codes, and agencies, confirming cross-references to every appendix-listed authority class.【F:temp/NOTES.md†L88-L111】【F:temp/NOTES.md†L113-L187】

## Locale Audit – Draft 3 (texas-greenbook-15th-draft3.csl)

### Term Calls
| Context | Attributes |
| --- | --- |
| style > style > macro:tex-constitution > group (delim=', ') > group (delim=' ') > text | form='short', term='article' |
| style > style > macro:book-like > group (delim=', ') > group (delim='; ') > group (delim=' ') > text | form='short', term='edition' |
| style > style > macro:web > group (delim=', ') > group (delim=' ') > text | term='available at' |
| style > style > macro:web > group (delim=', ') > group (wrap=' (', ')') > text | term='accessed', text-case='capitalize-first' |
| style > style > macro:statute-code > group (delim=' ') > text | form='symbol', term='section' |
| style > style > macro:constitution-core > group (delim=', ') > group (delim=' ') > group (delim=' ') > text | form='short', term='article' |
| style > style > macro:constitution-core > group (delim=', ') > group (delim=' ') > text | form='symbol', term='section' |
| style > style > macro:session-law > group (delim=', ') > group (delim=' ') > text | form='symbol', term='section' |
| style > style > macro:tac-core > group (delim=' ') > text | form='symbol', term='section' |
| style > style > macro:municipal-code > group (delim=', ') > group (delim=' ') > group (delim=' ') > text | form='symbol', term='section' |

### Label Calls
| Context | Attributes |
| --- | --- |
| style > style > macro:author > names:author > label | form='short', prefix=', ' |
| style > style > macro:tex-constitution > group (delim=', ') > group (delim=' ') > label | form='symbol', variable='section' |
| style > style > macro:tex-statute > group (delim=' ') > group (delim=' ') > label | form='symbol', variable='section' |
| style > style > macro:tex-admin-code > group (delim=' ') > group (delim=' ') > label | form='symbol', variable='section' |

### Text Calls and Punctuation Affixes
| Context | Attributes |
| --- | --- |
| style > style > macro:case-name > text | font-style='italic', variable='title' |
| style > style > macro:reporter > group (delim=' ') > text | variable='volume' |
| style > style > macro:reporter > group (delim=' ') > text | form='short', variable='container-title' |
| style > style > macro:reporter > group (delim=' ') > text | variable='page-first' |
| style > style > macro:court-year > group (wrap=' (', ')') > group (delim=' ') > text | variable='authority' |
| style > style > macro:subsequent-history > text | prefix=', ', variable='references' |
| style > style > macro:tex-constitution > group (delim=', ') > text | form='short', variable='container-title' |
| style > style > macro:tex-constitution > group (delim=', ') > group (delim=' ') > text | variable='chapter-number' |
| style > style > macro:tex-constitution > group (delim=', ') > group (delim=' ') > text | variable='section' |
| style > style > macro:tex-statute > group (delim=' ') > text | form='short', variable='container-title' |
| style > style > macro:tex-statute > group (delim=' ') > group (delim=' ') > text | variable='section' |
| style > style > macro:tex-statute > text | prefix=' (', suffix=')', variable='note' |
| style > style > macro:tex-admin-code > group (delim=' ') > text | variable='volume' |
| style > style > macro:tex-admin-code > group (delim=' ') > text | form='short', variable='container-title' |
| style > style > macro:tex-admin-code > group (delim=' ') > group (delim=' ') > text | variable='section' |
| style > style > macro:tex-admin-code > text | prefix=' (', suffix=')', variable='title' |
| style > style > macro:tex-register > group (delim=' ') > text | variable='volume' |
| style > style > macro:tex-register > group (delim=' ') > text | form='short', variable='container-title' |
| style > style > macro:tex-register > group (delim=' ') > text | variable='page-first' |
| style > style > macro:tex-register > group (delim=' ') > text | prefix=', ', variable='page' |
| style > style > macro:tex-register > text | prefix=' (', suffix=')', variable='note' |
| style > style > macro:book-like > group (delim=', ') > group (delim=' ') > text | font-style='italic', variable='title' |
| style > style > macro:book-like > group (delim=', ') > group (delim=' ') > text | variable='section' |
| style > style > macro:article-journal > group (delim=', ') > text | quotes='true', variable='title' |
| style > style > macro:article-journal > group (delim=', ') > group (delim=' ') > text | variable='volume' |
| style > style > macro:article-journal > group (delim=', ') > group (delim=' ') > text | form='short', variable='container-title' |
| style > style > macro:article-journal > group (delim=', ') > group (delim=' ') > text | variable='page-first' |
| style > style > macro:web > group (delim=', ') > text | variable='title' |
| style > style > macro:web > group (delim=', ') > text | variable='container-title' |
| style > style > macro:web > group (delim=', ') > group (delim=' ') > text | variable='URL' |
| style > style > citation > layout > choose > if > text | macro='legal-case' |
| style > style > citation > layout > choose > else-if > choose > if > text | macro='statute-code' |
| style > style > citation > layout > choose > else-if > choose > else > text | macro='tex-statute' |
| style > style > citation > layout > choose > else-if > text | macro='tex-statute' |
| style > style > citation > layout > choose > else-if > text | macro='tac-core' |
| style > style > citation > layout > choose > else-if > text | macro='article-journal' |
| style > style > citation > layout > choose > else-if > text | macro='book-like' |
| style > style > citation > layout > choose > else-if > text | macro='web' |
| style > style > citation > layout > choose > else > group (delim=', ') > text | variable='title' |
| style > style > bibliography > layout > choose > if > group (delim=', ') > text | macro='case-name' |
| style > style > bibliography > layout > choose > if > group (delim=', ') > text | macro='reporter' |
| style > style > bibliography > layout > choose > if > group (delim=', ') > text | macro='court-year' |
| style > style > bibliography > layout > choose > else-if > text | macro='tex-statute' |
| style > style > bibliography > layout > choose > else-if > text | macro='tex-admin-code' |
| style > style > bibliography > layout > choose > else-if > text | macro='article-journal' |
| style > style > bibliography > layout > choose > else-if > text | macro='book-like' |
| style > style > bibliography > layout > choose > else-if > text | macro='web' |
| style > style > bibliography > layout > choose > else > group (delim=', ') > text | variable='title' |
| style > style > macro:reporter-print > group (delim=' ') > text | variable='volume' |
| style > style > macro:reporter-print > group (delim=' ') > text | variable='container-title' |
| style > style > macro:reporter-print > group (delim=' ') > text | variable='page' |
| style > style > macro:reporter-wl > group (delim=', ') > text | prefix='No. ', variable='number' |
| style > style > macro:reporter-wl > group (delim=', ') > text | variable='collection-number' |
| style > style > macro:court-and-date > choose > if > group (wrap=' (', ')') > text | variable='authority' |
| style > style > macro:court-and-date > choose > if > group (wrap=' (', ')') > text | prefix=', ', variable='status' |
| style > style > macro:court-and-date > choose > else > group (wrap=' (', ')') > text | variable='authority' |
| style > style > macro:court-and-date > choose > else > group (wrap=' (', ')') > text | prefix=', ', variable='status' |
| style > style > macro:parenthetical-slip-op > choose > if > text | prefix=' (', suffix=')', variable='genre' |
| style > style > macro:parenthetical-slip-op > choose > if > text | prefix=' (', suffix=')', variable='medium' |
| style > style > macro:legal-case > group (delim=', ') > text | macro='case-name' |
| style > style > macro:legal-case > group (delim=', ') > choose > if > text | macro='reporter-print' |
| style > style > macro:legal-case > group (delim=', ') > choose > else > text | macro='reporter-wl' |
| style > style > macro:legal-case > group (delim=', ') > text | macro='pinpoint' |
| style > style > macro:legal-case > text | macro='court-and-date' |
| style > style > macro:legal-case > text | macro='parenthetical-slip-op' |
| style > style > macro:statute-code > group (delim=' ') > text | variable='container-title' |
| style > style > macro:statute-code > group (delim=' ') > text | variable='section' |
| style > style > macro:constitution-core > group (delim=', ') > group (delim=' ') > text | variable='container-title' |
| style > style > macro:constitution-core > group (delim=', ') > group (delim=' ') > group (delim=' ') > text | variable='chapter-number' |
| style > style > macro:constitution-core > group (delim=', ') > group (delim=' ') > text | variable='section' |
| style > style > macro:constitution-core > text | prefix=' (', suffix=')', variable='status' |
| style > style > macro:session-law > group (delim=', ') > text | variable='title' |
| style > style > macro:session-law > group (delim=', ') > text | variable='collection-number' |
| style > style > macro:session-law > group (delim=', ') > text | prefix='ch. ', variable='number' |
| style > style > macro:session-law > group (delim=', ') > group (delim=' ') > text | variable='section' |
| style > style > macro:session-law > group (delim=', ') > group (delim=' ') > text | variable='volume' |
| style > style > macro:session-law > group (delim=', ') > group (delim=' ') > text | variable='container-title' |
| style > style > macro:session-law > group (delim=', ') > group (delim=' ') > text | variable='page' |
| style > style > macro:tac-core > group (delim=' ') > text | variable='volume' |
| style > style > macro:tac-core > group (delim=' ') > text | variable='container-title' |
| style > style > macro:tac-core > group (delim=' ') > text | variable='section' |
| style > style > macro:tac-core > text | prefix=' (', suffix=')', variable='authority' |
| style > style > macro:rule-core > group (delim=' ') > text | variable='container-title' |
| style > style > macro:rule-core > group (delim=' ') > text | variable='section' |
| style > style > macro:municipal-code > group (delim=', ') > text | variable='authority' |
| style > style > macro:municipal-code > group (delim=', ') > group (delim=' ') > text | variable='container-title' |
| style > style > macro:municipal-code > group (delim=', ') > group (delim=' ') > text | variable='chapter-number' |
| style > style > macro:municipal-code > group (delim=', ') > group (delim=' ') > group (delim=' ') > text | variable='section' |
| style > style > macro:ag-opinion > group (delim=' ') > text | variable='authority' |
| style > style > macro:ag-opinion > group (delim=' ') > text | prefix='No. ', variable='number' |
| style > style > macro:journal-article > group (delim=', ') > text | variable='title' |
| style > style > macro:journal-article > group (delim=', ') > group (delim=' ') > text | variable='volume' |
| style > style > macro:journal-article > group (delim=', ') > group (delim=' ') > text | font-style='italic', variable='container-title' |
| style > style > macro:journal-article > group (delim=', ') > group (delim=' ') > text | variable='page' |
| style > style > macro:pinpoint > choose > if > text | prefix=', ', variable='locator' |
| style > style > macro:pinpoint > choose > else-if > text | prefix=', at *', variable='locator' |

## Test Coverage Update (October 2025)

- `tests.json` now includes first-form and follow-on examples for every authority class routed through the citation macros, including Texas trial court orders, uncodified session laws, municipal codes, Attorney General letter opinions, and secondary sources such as internet materials and unpublished correspondence. This aligns one or more fixtures with each row of the authority matrix above.
- Inline comments on every line of `expected.txt` and `expected_secondary.txt` record the controlling Greenbook page so future edits can audit expectations back to the source text quickly.
- `tests_toa.json` has been expanded to mirror Table of Authorities groupings: Supreme Court, intermediate courts (published and memorandum opinions), criminal cases, trial orders, constitution provisions, statutes, court rules, administrative materials (code and register), session laws, Attorney General opinions, municipal ordinances, and secondary authorities. Each entry carries a sample locator to exercise dotted-leader rendering.

### Outstanding Gaps

- The CSL drafts do not yet differentiate short-form vs. cross-reference output for Texas statutes, constitutions, court rules, or register notices. The new fixtures flag the desired strings, but current style logic will need to adopt `references`-aware branches similar to the case macros.
- Web citations in Chapter 16 rely on “available at” plus “Accessed” parentheticals. Fresh text extraction from the Format Guide confirmed the examples on printed pp. 76–77, allowing inline comments to cite precise rows rather than the generic chapter reference.【F:temp/Greenbook_15thEdition.pdf†L452-L479】【F:temp/expected_secondary.txt†L5-L12】
- Table of Authorities tests cover the major groups but still lack examples for federal authorities and multi-level leaders (e.g., nested subentries). Future iterations should add those once the TOA CSL variants support secondary sorting keys.

#### Chapter 16 Format Guide transcription (2025-11-04)
- **Method.** Extracted the Chapter 16 Format Guide table (printed p. 76 / PDF pp. 94–95) with `PyPDF2` to bypass the ligature substitutions that previously blocked automated copying. The capture preserves the full example strings so punctuation, spacing, and agency abbreviations can now be audited precisely.【F:temp/ch16.txt†L3-L30】
- **Verbatim examples.**
  - `9 Tex. Reg. 982, 982 (2014) (to be codified at 16 Tex. Admin. Code § 33.13) (proposed Oct. 25, 2013) (Tex. Alcoholic Beverages Comm’n, Application Procedures), proposed by 38 Tex. Reg. 7403, 7404 (2013).` (Format Guide row “Codified Rules”).【F:temp/ch16.txt†L5-L12】
  - `33 Tex. Reg. 7653, 7653–54 (2008) (emerg. amend. to 4 Tex. Admin. Code §§ 19.411, 19.413) (adopted Sept. 12, 2008, expired Dec. 24, 2008) (Tex. Dep’t Agric., Quarantined Areas; Restrictions).` (Format Guide row “Emergency Rules”).【F:temp/ch16.txt†L12-L19】
  - `Tex. Pub. Util. Comm’n, Application of Southwestern Bell Telephone Company for Authority to Implement Private Coin Service, Docket No. 5905, 10 Tex. P.U.C. Bull. 1424, 1426 (Mar. 8, 1985) (final order granting application).` (Format Guide row “Administrative Orders”).【F:temp/ch16.txt†L19-L26】
  - `53 Tex. Educ. Agency Biennial Rep. 17 (1984).` (Format Guide row “Reports, Studies, and Bulletins”).【F:temp/ch16.txt†L26-L28】
- **Observation.** The Format Guide presents agency publications without quotation marks, mirroring the existing `web-*` macros’ plain text output. No dedicated “available at” example appears in the table; online guidance resides in the narrative paragraphs immediately below (e.g., 16.1.1 notes that the Texas Register is accessible online).【F:temp/ch16.txt†L31-L57】

##### Web macro comparison
- `web-first` renders `title, container-title, year, available at URL` with an optional `Accessed` parenthetical when `accessed` metadata is present, which matches the comma-delimited structure implied by the Format Guide rows and the Chapter 16 fixtures in `expected_secondary.txt`.【F:temp/texas-greenbook-15th-edition.csl†L698-L738】【F:temp/expected_secondary.txt†L5-L12】
- Press releases currently mirror the standard pattern; because the macro prioritizes `issued` over `status`, the descriptive label is suppressed when a year exists. The Format Guide examples likewise omit descriptive labels, so no punctuation adjustments are required. Documented here for future review if stakeholders want `status` surfaced even when dates are available.【F:temp/texas-greenbook-15th-edition.csl†L718-L726】【F:temp/tests.json†L594-L609】

##### Web fixture expansion (2025-11-04)
- Added three Chapter 16-focused fixtures to `tests.json` to cover (a) undated agency press releases that fall back to `status`, (b) quoted article titles sourced from judiciary blogs, and (c) standalone PDF downloads without a container title.【F:temp/tests.json†L594-L655】 Each entry carries a `comment` flag pointing back to the governing Greenbook pages (pp. 76–77) for auditability.【F:temp/Greenbook_15thEdition.pdf†L452-L479】
- Updated `expected.txt` and `expected_secondary.txt` so the regression baselines reflect the new web outputs alongside existing agency materials.【F:temp/expected.txt†L49-L59】【F:temp/expected_secondary.txt†L5-L15】 All strings retain the “available at” phrase plus capitalized “Accessed” parentheticals required by Chapter 16.
- CiteProc-Py warns that the ad hoc `comment` field is ignored; the warning is acceptable because the field exists solely for human documentation and does not affect rendered text. Logged here so future maintainers understand why the message appears during regression runs.【5e2a58†L1-L9】
- Verification command: `python temp/run_tests.py --style temp/texas-greenbook-15th-edition.csl --tests temp/tests.json --expected temp/expected.txt` (see `temp/test-logs/2025-11-04_web-fixtures.txt`).【eec99b†L2-L4】 The refreshed log confirms 63/63 matches after adding the fixtures.

##### Web punctuation change plan (2025-11-19)
- **Target macros.** Adjust `web-first`, `web-short`, and `web-bibliography` in `texas-greenbook-15th-edition.csl` (ll. 770–848) along with the shared access-date group to mirror Chapter 16 exemplars (pp. 76–77). The `web-cross-reference` macro will inherit the same quoting helper once the base macros land.【F:temp/texas-greenbook-15th-edition.csl†L765-L848】【F:temp/Greenbook_15thEdition.pdf†L452-L479】
- **Quoted titles.** Wrap `title` with `quotes="true"` and rely on the US punctuation-in-quote setting so blog posts render `“Designing Accessible Virtual Hearings,” Texas Courts Blog …` instead of the current bare `"Designing Accessible Virtual Hearings", Texas Courts Blog …`. After the macro adds quotes automatically, strip the manual quotation marks from `web_blog_quoted_title` in `tests.json` to avoid duplicates.
- **Full publication dates.** When `issued` includes month/day, emit `short-month day, year` in both note and bibliography contexts because the Greenbook examples cite the exact posting date for agency releases and blog entries (e.g., Sept. 8, 2022). Retain the year-only fallback for sources that provide no finer granularity.
- **Available-at clause punctuation.** Relocate the `available at` group so it follows the date block and suppress the redundant comma currently produced when a quoted title precedes it. Target output: `…, available at URL (Accessed …)` with no doubled punctuation even when the preceding element ends in a quotation mark.
- **Short-form compression.** Update `web-short` to reuse the quoting helper and emit `title—URL` with a single comma (e.g., `“Designing Accessible Virtual Hearings,” https://…`) so repeat cites stay compact while preserving the quoted-title punctuation.
- **Access-date helper.** Extract the `(Accessed …)` rendering into a reusable macro invoked by `web-first` and `web-bibliography` so capitalization, spacing, and trailing periods remain synchronized after the punctuation rewrite. Gate the helper on the presence of `accessed` metadata to avoid empty parentheses.

- **Self-review (2025-11-21).** Re-read the plan against Chapter 16’s examples (pp. 76–77) and confirmed that the proposed edits cover both note and bibliography macros (`web-first`, `web-short`, `web-bibliography`) without introducing conflicting punctuation paths. Logged the review so later implementers can trace the sign-off before wiring XML changes.【F:temp/Greenbook_15thEdition.pdf†L452-L479】【F:temp/NOTES.md†L890-L915】

- **Implementation log (2025-11-21).** Added `web-availability` and `web-access-date` helpers so `available at`/`(Accessed …)` output only when URL, DOI, or `accessed` metadata exists, preventing stray phrases in sparse records while centralizing reuse. The helpers route through locale terms added to both the inline `en-US` block and the shared locale file so repeated strings stay configurable via `locales-en-US-x-texas-greenbook.xml` before upstream submission.【F:temp/texas-greenbook-15th-edition.csl†L732-L831】【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L33】

- **Regression status (2025-11-21).** `python temp/run_tests.py` currently halts on the `treatise_practice` fixture because citeproc cannot locate the ordinal locale term during `edition` rendering. The failure predates the web-availability rewrite; recorded here for coordination with the locale packaging/ordinal coverage work before rerunning the full suite.【c10185†L1-L39】【F:temp/tests.json†L489-L506】

###### Web punctuation issue inventory (2025-11-20)
- **Manual quotes required for web titles.** The current `web-first`/`web-short` stack prints raw `title` values, forcing fixtures such as `web_blog_quoted_title` to embed straight quotes directly in the metadata to match Chapter 16’s example strings (see `tests.json` ll. 658–682 and `expected_secondary.txt` l. 8).【F:temp/tests.json†L658-L682】【F:temp/expected_secondary.txt†L8-L9】 This prevents citeproc from applying typographic punctuation-inside-quotation behavior mandated by Greenbook Chapter 16’s web format table (PDF p. 77).【F:temp/Greenbook_15thEdition.pdf†L470-L479】
- **Comma duplication before `available at`.** Because the `available at` group is nested inside the comma-delimited sequence in `web-first`, any quoted title ending with a comma yields `", available at …` once the manual quotes are removed, contrary to the Format Guide flow that treats the availability clause as a new phrase after the date (PDF pp. 76–77).【F:temp/texas-greenbook-15th-edition.csl†L779-L798】【F:temp/Greenbook_15thEdition.pdf†L452-L479】
- **Short-form punctuation gaps.** `web-short` emits `title, URL` without quoting the title or guarding against missing URLs, so repeat cites for agency PDFs or press releases leave dangling commas when translators omit the link (see `texas-greenbook-15th-edition.csl` ll. 812–816).【F:temp/texas-greenbook-15th-edition.csl†L812-L816】 The Format Guide expects the short cite to retain the distinctive title while remaining typographically consistent with the first cite (PDF p. 77).【F:temp/Greenbook_15thEdition.pdf†L470-L479】
- **Duplicated access-date rendering.** Both `web-first` and `web-bibliography` hand-roll the `(Accessed …)` parenthetical, creating a maintenance hotspot and risking divergence from the shared article availability helper used for online periodicals (compare `texas-greenbook-15th-edition.csl` ll. 798–807 and 844–853 with the article helper at ll. 730–760).【F:temp/texas-greenbook-15th-edition.csl†L730-L760】【F:temp/texas-greenbook-15th-edition.csl†L798-L856】

###### Web punctuation design note (2025-11-20)
- **Introduce a `web-title` helper.** Create a dedicated macro that outputs `title` with `quotes="true"` and an optional fallback for container-only items, then reuse it in `web-first`, `web-short`, and `web-cross-reference` so all routes inherit consistent punctuation. Update fixtures by removing manual quotes from `web_blog_quoted_title` once the helper is in place (tests.json ll. 658–682).【F:temp/tests.json†L658-L682】【F:temp/texas-greenbook-15th-edition.csl†L779-L824】
- **Reorder the availability clause.** Move the `<group>` containing `term="available at"` outside the comma-delimited sequence and gate it behind a new wrapper macro (e.g., `web-availability`) that appends the clause after the date/status block. This mirrors the Format Guide structure for agency pages and studies (PDF pp. 76–77) while eliminating comma collisions when the preceding element ends in a quotation mark.【F:temp/Greenbook_15thEdition.pdf†L452-L479】
- **Shared access-date helper.** Extract the `(Accessed …)` formatting into `web-access-date` and call it from both `web-first` and `web-bibliography`. Align its internals with `article-availability` to maintain month/day punctuation and to prepare for potential reuse in other online macros. Ensure the helper silently returns nothing when `accessed` metadata is absent, preventing empty parentheses.【F:temp/texas-greenbook-15th-edition.csl†L730-L760】【F:temp/texas-greenbook-15th-edition.csl†L798-L856】
- **Short-form guardrails.** Refactor `web-short` to use the new `web-title` helper, switch to a single em-dash or comma delimiter depending on whether a URL exists, and fall back to container titles when links are missing. This keeps repeat cites compact without leaving dangling punctuation while preserving Chapter 16’s emphasis on the title as the identifying element (PDF p. 77).【F:temp/texas-greenbook-15th-edition.csl†L812-L816】【F:temp/Greenbook_15thEdition.pdf†L470-L479】
- **Bibliography alignment.** Mirror the availability and access-date helpers in `web-bibliography` but keep its sentence-style delimiter (`. `) so bibliography entries maintain the narrative flow shown in Chapter 16’s descriptive examples (PDF pp. 76–77). Document any deviations in the changelog once implemented.【F:temp/texas-greenbook-15th-edition.csl†L828-L856】【F:temp/Greenbook_15thEdition.pdf†L452-L479】

###### Web punctuation risk register (2025-11-20)
- **Interaction with article availability helper.** The new `web-access-date` macro must match the formatting produced by `article-availability` to avoid divergent `(Accessed …)` punctuation between online journals and agency pages. Mitigation: copy the date-parts ordering from the article helper and add regression tests that render both authority types side-by-side.【F:temp/texas-greenbook-15th-edition.csl†L730-L760】
- **Locale dependency for “available at.”** Relocating the availability clause increases reliance on the locale term; if future locale refactors rename or relocate the term, web citations could lose the phrase entirely. Mitigation: document the dependency in the locale packaging plan and add a regression test that fails when the locale term is missing so the build flags the regression early.【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L99】
- **Bibliography punctuation drift.** Sharing helpers between note and bibliography contexts risks introducing commas where Chapter 16 expects sentences. Mitigation: parameterize the helpers to accept delimiter overrides and re-run bibliography-mode snapshots after each change to confirm the sentence-form output remains intact (`run_tests.py --mode bibliography`).【F:temp/texas-greenbook-15th-edition.csl†L828-L856】【F:temp/expected_secondary.txt†L5-L9】

###### Web punctuation implementation update (2025-11-21)
- Implemented the `web-title` and `web-issued-or-status` helpers, rewired `web-first`/`web-short`/`web-cross-reference`, and moved the availability/access-date block so note and bibliography cites now quote titles and print month/day detail when supplied (Format Guide pp. 76–77).【F:temp/texas-greenbook-15th-edition.csl†L767-L856】【F:temp/Greenbook_15thEdition.pdf†L452-L479】
- Updated the fixture expectations to reflect smart quotes and the relocated `(Accessed …)` clause; note-mode outputs now lead with quoted titles while bibliography-mode entries keep the narrative period before availability. Logged outputs in `expected.txt`/`expected_secondary.txt` for traceability.【F:temp/expected.txt†L49-L54】【F:temp/expected_secondary.txt†L5-L10】
- Short-form macros inherit the quoting helper so repeat cites no longer require metadata-embedded quotation marks. (No dedicated short-form fixtures yet; existing smoke tests remain unchanged pending the statute/rule short-form rollout.)

###### Targeted regression log (2025-11-21)
- Ran `python temp/run_tests.py --tests temp/tests_web.json --expected temp/expected_web.txt --mode notes` and bibliography variants against a web-only fixture subset because the full suite still halts at citation #31 (`rule_civp` locator uses a missing locale term). Stored the outputs in `temp/test-logs/2025-11-21-web-notes.txt` and `temp/test-logs/2025-11-21-web-bibliography.txt` for reviewer audit.【8c4bff†L1-L20】【3b6c87†L1-L20】【aead5b†L1-L60】
- Re-ran the TOA baseline (`texas-greenbook-15th-toa.csl`) to confirm the helper refactor left leader alignment untouched; all expectations still match the stored snapshots.【be67ed†L1-L9】
- Follow-up: capture the `rule` locator locale gap in the TODO backlog before the release-readiness sweep so the full `tests.json` suite can run cleanly.

##### Fixture metadata requirements for web variants
- **Issued agency landing page:** requires `title`, `container-title`, and an `issued` year plus `URL` and `accessed` date to replicate the Format Guide’s title–agency–year ordering and Accessed parenthetical. (`tests.json` item `website_source`).【F:temp/tests.json†L571-L588】
- **Undated agency update:** when `issued` is absent, populate `status` (e.g., “press release”) so the macro substitutes the descriptor for the missing year. Add `URL`/`accessed` to keep the Accessed parenthetical consistent. (`tests.json` item `web_press_release` currently uses both fields; new fixtures should omit `issued` to exercise the fallback).【F:temp/texas-greenbook-15th-edition.csl†L718-L726】【F:temp/tests.json†L594-L609】
- **Limited metadata / no container:** capture cases where agencies provide standalone PDF downloads without a container title or credited author; ensure the fixture supplies a corporate-style `title`, plus `URL`, `accessed`, and optionally `issued`, so the macro produces the comma-delimited pair without double spaces. Planned addition flagged for future `tests.json` updates so translators can verify graceful degradation when authors are missing.
## Verification Log — 2025-11-04
- Re-ran the core note fixture suite with `python temp/run_tests.py` to confirm no regressions in the primary style output. The rendered cites still match the annotated expectations from the October baseline snapshot.
- Generated fresh TOA bibliographies (base, grouped, leaders, and grouped-leaders) and synchronized the expected artifacts via `python temp/run_tests.py --style … --mode bibliography --expected …`. All four variants now emit the expanded 13-entry list covering trial orders, register notices, rules, and secondary sources without ordering drift.
- Spot-checked representative entries against the *Texas Greenbook* (15th ed.): case signals and short forms (pp. 3–5), constitution citations (pp. 39–40), administrative code/register formatting (pp. 76–77), and secondary sources (pp. 93–95). The revised macros and dotted leader spacing align with the PDF exemplars.
- Remaining follow-ups: incorporate federal authorities into `tests_toa.json` once style support lands, and add cross-reference aware branches for statutes/rules so the TOA variants inherit the note-mode short-form behavior.
### Stock Locale Comparison (locales-en-US.xml)
| Term | Draft 3 Value | Stock en-US Value | Override Needed? |
| --- | --- | --- | --- |
| `rule` (short) | `R.` | _not defined_ (no stock short form present)【b2a116†L1-L5】 | Yes – enforce capital R per Greenbook |
| `chapter` (short) | `ch.` | `chap.`【c09823†L1-L10】 | Yes – match Greenbook contraction |
| `article` (short) | `art.` | _not defined_ (only long form present)【4dfcb3†L1-L5】 | Yes – add short form |
| `paragraph` (short) | `¶` | `para.`【a44ccd†L1-L8】 | Yes – use pilcrow symbol |
| `section` (symbol) | `§` | `§`【1b3e9d†L1-L8】 | Optional – identical to stock |
| `and` | `and` | `and`【6f5683†L1-L35】 | Optional – identical to stock |

### Override Placement Recommendation
- Multiple in-progress drafts (Draft 3 and the table-of-authorities variants) repeat the same custom abbreviations for `article`, `chapter`, `rule`, and `section`/`paragraph`, which makes drift likely if each file hand-maintains overrides.【F:temp/texas-greenbook-15th-draft3.csl†L422-L428】【69b6f5†L3-L16】
- Creating a shared custom locale (e.g., `locales/locales-en-US-x-texas-greenbook.xml`) centralizes the Greenbook-specific abbreviations while letting each draft include it with `<locale>` references, ensuring that future drafts (Draft 4, TOA leaders) inherit updates automatically.
- The inline `<locale>` block can then shrink to only truly draft-specific terms (if any emerge), simplifying the style diff and keeping the main CSL focus on citation structure rather than terminology management.
- Drafted the shared locale shell at `temp/locales/locales-en-US-x-texas-greenbook.xml` so the abbreviations can migrate out of individual styles once integration tasks are scheduled.【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L18】
- Documented follow-up integration steps: styles will import the shared locale via the CSL `<locale href="…"/>` mechanism after we update citeproc test harnesses to expose the new directory, and TOA fixtures will need regeneration once the terms move out of inline `<locale>` blocks.【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L18】
- Validated the locale XML using `lxml` (system `xmllint` unavailable) to confirm the structure parses before wiring it into the styles.【b4834c†L1-L6】

## Locale Packaging Plan (2025-04-02)
- **Distribution channel.** The working locale will remain in `temp/locales/locales-en-US-x-texas-greenbook.xml` until the Greenbook styles stabilize, after which it should be submitted to the dedicated CSL locales repository using the same pull-request workflow described for styles in `CONTRIBUTING.md`.【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L18】【F:CONTRIBUTING.md†L1-L29】 The upstream README confirms that all production locales live at `citation-style-language/locales`, so the shared file can be discoverable by downstream processors once merged.【F:README.md†L16-L33】
- **Schema and metadata alignment.** Before the upstream submission, the locale must be updated to carry the CSL `version="1.0"` attribute, `cs:style-options`, and `cs:date` nodes required by the specification for standalone locale files, and its filename should match the `xml:lang` code recorded on the root element.【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L18】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L874-L914】 We will bump the `<updated>` timestamp in tandem with each schema refinement so consumers can track revisions.
- **Versioning and mirroring.** After the locale is accepted upstream, we will keep the working copy in `temp/locales/` synchronized with the published version by referencing the locales repository commit hash in future updates and refreshing the `updated` timestamp whenever the shared abbreviations change. This mirrors the release practices outlined in the CSL README, ensuring our internal fixtures match the official distribution cadence.【F:README.md†L52-L77】
- **Integration mechanism.** Once the locale is hosted centrally, the Greenbook styles will replace their inline `<locale xml:lang="en-US">…</locale>` blocks with `<locale xml:lang="en-US" href="locales/locales-en-US-x-texas-greenbook.xml"/>`, allowing citeproc implementations to pull the shared terms without duplicating XML. This approach keeps the styles compliant with the CSL schema while letting us manage abbreviations in one place.【F:texas-greenbook-15th-edition.csl†L1-L32】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L874-L904】
- **Dialect decision.** Adopted the private-use dialect code `en-US-x-texas-greenbook` so the shared locale no longer collides with the stock `en-US` resource, satisfying the CSL requirement that the filename mirror the `xml:lang` value on the `<locale>` root element.【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L18】【F:temp/CSL 1.0.2 Specification — Citation Style Language 1.0.1-dev documentation.html†L874-L914】

## Statute & rule terminology extraction (2025-12-05)
- **Textual guidance cross-check.** Re-read Chapter 10’s general rules to confirm the narrative instructions (e.g., when to append “Supp.”, how “art.”/“arts.” behave, and when to pivot to session laws) match the worked examples. The prose and exemplars align: Chapter 10.1.3’s description of supplement parentheticals is reflected in the accompanying `Tex. Alco. Bev. Code Ann. § 22.03 (Supp.)` example, and Chapter 10.1.4 explicitly walks through the `art.`/`arts.` alternation used in the sample multi-provision cites.【F:temp/Greenbook_15thEdition.pdf†L1686-L1719】
- **External references.** Logged the Practice Tip on Texas Legislative Council codification guidance (Drafting Manual and website) so future helper work can reference the council’s effective-date tables as needed.【F:temp/Greenbook_15thEdition.pdf†L1662-L1678】 Appendix H remains the canonical abbreviation table for code titles and rule sets (pp. 116–117); citations below reference both locations for provenance.【F:temp/Greenbook_15thEdition.pdf†L2476-L2512】
- **Locale audit.** None of the Appendix H abbreviations currently live in `locales-en-US-x-texas-greenbook.xml`; the locale only covers generic terms (`art.`, `ch.`, `§`, `R.`). Code titles and rule abbreviations therefore stay macro-driven for now. Future locale updates would need new `<term>` entries if we decide to move these strings out of CSL logic.【F:temp/locales/locales-en-US-x-texas-greenbook.xml†L1-L33】
- **Conditional behavior inventory.** Documented when the manual mandates plural forms (`arts.` vs. `art.`, `§§` vs. `§`), when session-law parentheticals must appear (historical fact citations), and when auxiliary pamphlets require bracketed session-law references. No conflicts surfaced that require legal review; all conditions map cleanly to existing metadata (`number-of-pages`, `title`, `issued`) plus the planned publication-status helpers.【F:temp/Greenbook_15thEdition.pdf†L1686-L1777】
- **Reuse vs. new definitions.** Confirmed that existing locale overrides remain sufficient for paragraph/section/rule contractions. Code-title abbreviations will continue to render via item metadata (e.g., `collection-title-short`) until we decide whether helper macros should centralize them. Recorded the outstanding follow-up to revisit this choice once the publication/status helpers are designed.

### Appendix H abbreviation inventory
| Authority group | Abbreviation (Greenbook) | Locale coverage | Notes |
| --- | --- | --- | --- |
| Agriculture Code | Tex. Agric. Code Ann. | Not in locale | Subject-matter code list, Appendix H.1.【F:temp/Greenbook_15thEdition.pdf†L2476-L2492】 |
| Alcoholic Beverage Code | Tex. Alco. Bev. Code Ann. | Not in locale | Confirmed Chapter 10 examples mirror this contraction.【F:temp/Greenbook_15thEdition.pdf†L1686-L1710】 |
| Business & Commerce Code | Tex. Bus. & Com. Code Ann. | Not in locale | Ampersand appears in official abbreviation table; ensure metadata preserves punctuation.【F:temp/Greenbook_15thEdition.pdf†L2476-L2492】 |
| Business Organizations Code | Tex. Bus. Orgs. Code Ann. | Not in locale | Chapter 10.2.2(b) flags full applicability as of Jan. 1, 2010.【F:temp/Greenbook_15thEdition.pdf†L1720-L1746】 |
| Civil Practice & Remedies Code | Tex. Civ. Prac. & Rem. Code Ann. | Not in locale | Pluralization handled via `§§` guidance in Chapter 10.1.4(a).【F:temp/Greenbook_15thEdition.pdf†L1686-L1719】 |
| Education Code | Tex. Educ. Code Ann. | Not in locale | — |
| Election Code | Tex. Elec. Code Ann. | Not in locale | — |
| Estates Code | Tex. Est. Code Ann. | Not in locale | Chapter 10.2.2(e) clarifies pamphlet parenthetical until annotated volumes exist.【F:temp/Greenbook_15thEdition.pdf†L1746-L1777】 |
| Family Code | Tex. Fam. Code Ann. | Not in locale | — |
| Finance Code | Tex. Fin. Code Ann. | Not in locale | — |
| Government Code | Tex. Gov’t Code Ann. | Not in locale | — |
| Health & Safety Code | Tex. Health & Safety Code Ann. | Not in locale | Chapter 10.1.4(a) example leverages §§ pluralization.【F:temp/Greenbook_15thEdition.pdf†L1686-L1719】 |
| Human Resources Code | Tex. Hum. Res. Code Ann. | Not in locale | — |
| Insurance Code | Tex. Ins. Code Ann. | Not in locale | Title 1 retains article numbering; requires `art.` toggles per 10.1.1.【F:temp/Greenbook_15thEdition.pdf†L1686-L1719】 |
| Labor Code | Tex. Lab. Code Ann. | Not in locale | — |
| Local Government Code | Tex. Loc. Gov’t Code Ann. | Not in locale | — |
| Natural Resources Code | Tex. Nat. Res. Code Ann. | Not in locale | — |
| Occupations Code | Tex. Occ. Code Ann. | Not in locale | — |
| Parks & Wildlife Code | Tex. Parks & Wild. Code Ann. | Not in locale | — |
| Penal Code | Tex. Penal Code Ann. | Not in locale | Example in Chapter 10.2.1 demonstrates omission of “Ann.” for unannotated reprints.【F:temp/Greenbook_15thEdition.pdf†L1710-L1720】 |
| Property Code | Tex. Prop. Code Ann. | Not in locale | — |
| Special District Local Laws Code | Tex. Spec. Dist. Code Ann. | Not in locale | Chapter 10.2.2(c) notes ongoing codification; helper must tolerate legacy session-law fallbacks.【F:temp/Greenbook_15thEdition.pdf†L1720-L1746】 |
| Tax Code | Tex. Tax Code Ann. | Not in locale | Example `Tex. Tax Code Ann. § 26.06(a)` confirms parentheses placement for subsections.【F:temp/Greenbook_15thEdition.pdf†L1710-L1720】 |
| Transportation Code | Tex. Transp. Code Ann. | Not in locale | — |
| Utilities Code | Tex. Util. Code Ann. | Not in locale | — |
| Water Code | Tex. Water Code Ann. | Not in locale | Auxiliary pamphlets require bracketed session cites when applicable (Chapter 10.2.5).【F:temp/Greenbook_15thEdition.pdf†L1746-L1777】 |

### Independent code abbreviations
| Code | Abbreviation | Locale coverage | Notes |
| --- | --- | --- | --- |
| Code of Criminal Procedure | Tex. Code Crim. Proc. Ann. | Not in locale | Chapter 10.2.2(d) covers tentative renaming to “Tex. Crim. Proc. Code Ann.” once fully codified; retain current form for legacy cites.【F:temp/Greenbook_15thEdition.pdf†L1720-L1746】 |
| Insurance Code (Title 1 articles) | Tex. Ins. Code Ann. | Not in locale | Shares abbreviation with subject-matter code; rely on article vs. section detection for `art.` toggles.【F:temp/Greenbook_15thEdition.pdf†L1686-L1719】 |
| Probate Code | Tex. Prob. Code Ann. | Not in locale | Superseded by Estates Code but appears in historical cites; Chapter 10.2.2(e) addresses transition.【F:temp/Greenbook_15thEdition.pdf†L1746-L1777】 |
| Business Corporations Act | Tex. Bus. Corp. Act Ann. | Not in locale | Legacy reference flagged in Appendix H.2; ensure macros surface historical `art.` numbering when metadata calls for it.【F:temp/Greenbook_15thEdition.pdf†L2492-L2504】 |

### Current rule abbreviations
| Rule set | Abbreviation | Locale coverage | Notes |
| --- | --- | --- | --- |
| Rules of Civil Procedure | Tex. R. Civ. P. | Macro literal (locale provides `rule` short form only) | Chapter 13.1 examples show plural `Tex. R. Civ. P. 21`. Ensure helper inserts pinpoint indicator punctuation before numerals.【F:temp/Greenbook_15thEdition.pdf†L1880-L1935】 |
| Rules of Judicial Administration | Tex. R. Jud. Admin. | Macro literal | Appendix H.3 entry; watch for capitalization of “Admin.” in TOA grouping headings.【F:temp/Greenbook_15thEdition.pdf†L2492-L2504】 |
| Rules of Appellate Procedure | Tex. R. App. P. | Macro literal | Already exercised by TOA fixtures; share short-form guard once statute/rule work lands.【F:temp/tests_toa.json†L1-L200】 |
| Rules of Evidence | Tex. R. Evid. | Macro literal | Chapter 13.3 highlights subdivisions by rule number; ensure `§` is not reused here.【F:temp/Greenbook_15thEdition.pdf†L1936-L1962】 |
| State Bar Rules | Tex. State Bar R. | Macro literal | Chapter 17.1 short-form relies on rule numbering rather than section references.【F:temp/Greenbook_15thEdition.pdf†L3024-L3050】 |
| Disciplinary Rules of Professional Conduct | Tex. Disciplinary Rules Prof’l Conduct | Macro literal | Appendix H.3 omits periods inside “Prof’l”; maintain existing abbreviation to match table.【F:temp/Greenbook_15thEdition.pdf†L2492-L2504】 |
| Rules of Disciplinary Procedure | Tex. Rules Disciplinary P. | Macro literal | Table uses shortened “P.”; no locale support today.【F:temp/Greenbook_15thEdition.pdf†L2492-L2504】 |
| Code of Judicial Conduct | Tex. Code Jud. Conduct | Macro literal | Chapter 17.5 expects `(Canon 1)` parentheticals; note interplay with future status helpers.【F:temp/Greenbook_15thEdition.pdf†L3070-L3096】 |
| Rules for the Removal or Retirement of Judges | Tex. Rules Rem’l/Ret. Judg. | Macro literal | Slash needs preservation; consider helper to enforce punctuation when metadata feeds spelled-out phrases.【F:temp/Greenbook_15thEdition.pdf†L2492-L2504】 |
| Rules Governing Admission to the Bar | Tex. Rules Govern. Bar Adm’n | Macro literal | Abbreviation uses “Govern.” contraction; ensure metadata captures apostrophe location for possessive contexts.【F:temp/Greenbook_15thEdition.pdf†L2492-L2504】 |

- **Context-dependent notes.** The `art.` vs. `arts.` distinction hinges on whether any cited article includes section pinpoints (Chapter 10.1.4(b)); the helper checklist needs to evaluate sibling cites to choose the proper plural. Session-law cites must include bracketed `Act of …` parentheticals when pulled from auxiliary pamphlets (Chapter 10.2.5). Municipal ordinance cites follow the codified/uncodified split in Chapter 10.6; capture jurisdiction metadata so helpers can switch between code titles and ordinance names.【F:temp/Greenbook_15thEdition.pdf†L1686-L1777】【F:temp/Greenbook_15thEdition.pdf†L1778-L1842】 No additional legal review required at this stage; all scenarios map to deterministic metadata checks documented above.

### Locale Integration Schedule (2025-04-02)
1. **Refactor inline locale blocks.** Update `texas-greenbook-15th-edition.csl` and all TOA variants (`texas-greenbook-15th-toa*.csl`) to drop their embedded `<locale>` sections in favor of referencing the shared file once citeproc loading is wired up, ensuring each style continues to declare `default-locale="en-US"` for compatibility.【F:texas-greenbook-15th-edition.csl†L1-L32】【F:temp/texas-greenbook-15th-toa.csl†L1-L24】
2. **Augment the test harness.** Extend `temp/run_tests.py` (or its successor) to point citeproc-py at `temp/locales/` via an explicit locale directory argument or manual locale registration so the regression suite exercises the shared terms instead of the deprecated inline overrides.【F:temp/run_tests.py†L1-L86】
3. **Regenerate fixtures.** After the styles pull from the shared locale, refresh `expected.txt`, `expected_secondary.txt`, and all TOA expected outputs to capture any punctuation or spacing differences introduced by the new loading path.【F:temp/expected.txt†L1-L214】【F:temp/expected_secondary.txt†L1-L180】【F:temp/expected_toa_grouped_leaders.txt†L1-L28】
4. **Document the switchover.** Update `temp/README.md` and this notebook once the locale integration lands so future contributors know the inline overrides were intentionally removed and understand how to run tests with the shared locale in place.【F:temp/README.md†L62-L109】

## CSL Contribution Guideline Review (2025-04-02)
- Re-read the CSL contributing guide to confirm the locale submission will follow the same PR-driven workflow as styles and that validation against the CSL schema remains a hard requirement before opening upstream pull requests.【F:CONTRIBUTING.md†L1-L33】【F:STYLE_DEVELOPMENT.md†L209-L249】
- Verified the style repository requirements covering titles, IDs, self links, licensing, and default locale declarations so the Texas Greenbook styles stay compliant once the locale refactor lands; no new metadata gaps surfaced during this review.【F:STYLE_REQUIREMENTS.md†L5-L112】
- Noted that the official repositories publish both styles and locales under a synchronized release cadence, so our internal plan to mirror the published locale copy aligns with upstream maintenance expectations.【F:README.md†L52-L77】

## Dependency packaging assessment (2025-03-10)
- **Environment inventory.** Confirmed the active development environment is the containerized Python 3.12 workspace bundled with this repository, and future automation will rely on a minimal GitHub Actions runner. Both contexts assume the ability to call `pip`, so shipping a requirements file remains viable without additional tooling.
- **Guard-clause prototype.** Instead of wrapping imports in a `try`/`except` (disallowed by repository guidelines), added `_ensure_citeproc_available()` in `temp/run_tests.py` that queries `importlib.util.find_spec("citeproc")`. The helper aborts early with a human-friendly instruction before the style modules import `citeproc`. Verified the behavior by uninstalling `citeproc-py` and running `python temp/run_tests.py --tests temp/tests_short-form_smoke.json --expected temp/expected_short-form_smoke.txt`, which now prints the actionable guidance and exits cleanly.【dac7a3†L1-L3】
- **Requirements-file evaluation.** Drafted `temp/requirements.txt` so contributors can run `pip install -r temp/requirements.txt` to provision dependencies in a single command. The temporary pin to `citeproc-py>=0.5,<0.6` mirrors the historical environment while we diagnose the locator crash uncovered during the full `tests.json` run (`AttributeError: 'NoneType' object has no attribute 'single'` when `label` requests a `form="symbol"` term that does not exist). Captured the failure in the 2025-03-10 shell logs for future debugging.【3b41ec†L1-L63】【866894†L1-L64】
- **Decision.** Adopted both measures: the requirements file provides a reproducible install path for CI, while the guard clause protects ad-hoc environments that skip the install step. Recorded the trade-offs (version pinning vs. proactive messaging) in this section so we can revisit the citeproc 0.6 compatibility issue once the underlying locator behavior is fixed.

## Test harness auto-mode verification (2025-03-10)
- Added `_infer_mode()` to `temp/run_tests.py` to switch the default rendering mode to bibliography when the style path contains `toa`, preserving note output elsewhere. The helper continues to honor explicit `--mode` overrides for atypical filenames.
- Normalized the filename heuristic by lowercasing the style path before matching so mixed-case variants like `TOA` or `Toa` still trigger bibliography mode without additional configuration.
- Executed a TOA regression without the `--mode` flag: `python temp/run_tests.py --tests temp/tests_toa.json --style temp/texas-greenbook-15th-toa-grouped-leaders.csl --expected temp/expected_toa_grouped_leaders.txt`. The rendered bibliography matched expectations, confirming the heuristic works for standard TOA variants. Stored the output at `temp/test-logs/20250310_toa_auto_mode.txt` for traceability.【72a499†L1-L8】
- Ran the short-form smoke suite with defaults to ensure non-TOA styles still render notes when `--mode` is omitted. `python temp/run_tests.py --tests temp/tests_short-form_smoke.json --expected temp/expected_short-form_smoke.txt` produced the expected note comparisons, logged in `temp/test-logs/20250310_short_form_default_mode.txt`.【b0f17a†L1-L4】
- Documented the new workflow in `temp/README.md`, emphasizing that contributors may still pass `--mode` explicitly when experimenting with nonstandard filenames or custom contexts.

## Ambiguity and interpretive backlog update (2025-03-10)
- **Statute/rule short-form prerequisites.** The citeproc 0.6.0 failure surfaced that our `ibid-locator` fallback assumes every non-page locator has a matching `form="symbol"` term. Before upgrading the dependency, we need to confirm whether Greenbook short forms prefer symbol or short labels for rules and administrative materials. Added a reminder in the TODO backlog to revisit locator labeling once the short-form epic resumes so we can broaden compatibility without breaking Chapter 13 expectations.【temp/texas-greenbook-15th-edition.csl†L70-L96】 **TODO:** Pair this review with the planned short-form implementation so any helper refactors land alongside the dependency bump.
- **Dependency compatibility follow-up.** Logged the outstanding locator crash and rationale for the temporary `<0.6` pin so future maintainers can decide whether to adjust the macros or open an upstream issue with citeproc-py. Until then, developers should avoid bumping the dependency range without retesting the locator paths.
- **Testing caveats.** Routine `run_tests.py` invocations should favor the focused smoke/TOA suites noted above while the broader `tests.json` run remains flaky under citeproc 0.6 semantics. Capture any additional anomalies in `temp/test-logs/` and feed them back into `TODO.md` to keep the backlog comprehensive.

## Slip-opinion URL placement audit (2025-11-21)
- Re-read Rule 4.1.3(a) and its surrounding examples to confirm that `available at` clauses trail the court/weight parentheticals while preceding any subsequent history or cross-reference strings.【F:temp/Greenbook_15thEdition.pdf†L1595-L1605】
- The Greenbook’s `Jenkins v. State` example shows the memorandum parenthetical followed by `available at …`, which now mirrors the note and bibliography outputs for both `tests.json` and the focused subset.【F:temp/Greenbook_15thEdition.pdf†L1600-L1605】【F:temp/expected.txt†L10-L19】【F:temp/expected_parentheticals_bibliography.txt†L1-L7】
- `Gen. Motors Corp. v. Gayle` demonstrates that the URL must precede the “leave granted, mand. denied” history string; the new `slip-opinion-availability` helper therefore emits the clause immediately before `subsequent-history`.【F:temp/Greenbook_15thEdition.pdf†L2309-L2310】【F:temp/texas-greenbook-15th-edition.csl†L138-L160】
- Seeded `case_slip_opinion` with a docket URL and synthetic dismissal history plus a `case_slip_jenkins` fixture to exercise memorandum + URL handling; both feed the new `tests_parentheticals.json` file so we can regression-test note and bibliography modes independently.【F:temp/tests.json†L141-L209】【F:temp/tests_parentheticals.json†L1-L58】【F:temp/expected_parentheticals_notes.txt†L1-L10】
- Populated `case_mandamus_history` with a two-step `related` chain and updated expectations, establishing structured petition history for future helper extraction while retaining the legacy `references` output for now.【F:temp/tests.json†L210-L280】【F:temp/expected.txt†L16-L19】
