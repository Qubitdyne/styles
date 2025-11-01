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

## Legacy Draft 3 Update – Position-Aware Statutes, Rules, and Agencies (2025-03-17)
- **Baseline review.** The archived `texas-greenbook-15th-draft3.csl` (now mirrored in `texas-greenbook-15th-edition.csl`) previously routed statutes through `statute-code`/`tex-statute` and agency materials through `tex-admin-code`/`tex-register`, but each macro only branched on `position="first"` and `variable="references"`. There was no shared handling for `Id.` cues, so repeat notes defaulted to the full form instead of the Greenbook short forms mandated in chs. 10–13 (pp. 42–84).
- **New cue + id stack.** Imported the `prefatory-signal`, `note-body`, and `ibid-locator` scaffolding into the edition build so that `cs:citation` now emits italicized signals and `Id.` strings before delegating to the substantive macros. Statutes (`tex-statute`), codified rules (`tex-admin-code`/`rule-core` logic embedded in `note-body`), and agency entries all inherit the shared `Id.` behavior (Greenbook ch. 10 at 42–53; ch. 13 at 61–65; ch. 16 at 76–84).
- **Regression coverage.** Added consecutive cite items in `tests.json` for `stat_govt_code`, `tac_rule`, and `rule_civp` so the harness now validates `Id.` strings for codes (§ 2001.003), TAC rules (§ 9.13), and procedural rules (R. 97(e)). `expected.txt` includes the corresponding lines 13, 19, and 22 annotated with the governing chapter citations.
- **Open questions.** The current `Id.` output for rules appears as `Id. 97(e).` without repeating the `R.` prefix. This mirrors the production edition but may warrant a follow-up confirmation against Greenbook ch. 13 (p. 63) to ensure no locator prefix is required when the preceding cite already supplied the rule set.

## Legacy Draft 3 Update – Parenthetical Metadata Helpers (2025-03-24)
- **Slip opinions and original proceedings.** Added a shared `docket-parenthetical` block and `procedural-parenthetical` chain so Greenbook slip citations now surface cause numbers, Westlaw/Lexis identifiers, and procedural posture straight from Zotero’s `number`, `collection-number`, `status`, and `note` fields (Greenbook ch. 2 at 7 & ch. 6 at 31–33). The helper skips `note` values that double as cross-reference cues, keeping `See also` triggers confined to the `cross-reference-cue` macro.
- **Memorandum and rehearing designations.** Normalized weight parentheticals to pull `genre` and `medium` in a consistent order, which allows memorandum opinions and rehearing dispositions to mirror chapter 4 examples without duplicating logic inside the case, mandamus, and trial-court macros (Greenbook ch. 4 at 24–25).
- **Trial-court docket metadata.** Reused the docket helper across trial-level items so cause numbers and underlying trial-court numbers land before the court/date parenthetical while `note` supplies record-type phrases such as “prelim. injunction order” (Greenbook ch. 7 at 34–35).

## Macro Dispatch Sketches

### `cs:citation` authority routing
```text
start citation
  layout delimiter="; "
    choose on item.type
      legal_case → call macro legal-case
        legal-case:
          if position="first" → legal-case-first
            • case-name → reporter-(print|wl) → pinpoint → court-and-date → weight-parentheticals → subsequent-history
          else if variable references present → legal-case-cross-reference
            • cross-reference-cue + legal-case-first core → court-and-date → weight-parentheticals → references tail
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

## Memo Opinion Indicator Audit (2025-03-27)
- `texas-greenbook-15th-edition.csl` routes every case through `case-parenthetical-stack`, which simply echoes `genre` and `medium` via `weight-parentheticals` with no conditional gating (ll. 144–158). Memorandum, per curiam, and rehearing parentheticals therefore appear only when translators populate `genre`/`medium`.
- The TOA family (`texas-greenbook-15th-toa*.csl`) defines the same helper as two single-node `choose` blocks that emit `genre`/`medium` for each case entry (e.g., `texas-greenbook-15th-toa.csl` ll. 58–112). Tables omit the explanatory-parenthetical macro, so memo markers display once in the case block and nowhere else.
- No macros promote `status` to memo terminology; `procedural-parenthetical` is limited to `status`/`note` combinations for things like “orig. proceeding.” This inventory confirms memo handling is entirely data-driven today and documents the gap for future conditional helpers or locale terms.

## Supplemental Reference Status (2025-03-27)
- **Uniform-Format-Manual-07012010.pdf** — 30-page, text-searchable PDF covering reporter formatting; stored in `temp/` and requires no OCR.
- **How-Court-Rules-Are-Made.pdf** — 10-page, searchable PDF summarizing rulemaking procedures, ready for citation provenance without preprocessing.
- **technology-standards.pdf** — 35-page Judicial Committee on Information Technology standards document; text extraction succeeds, so administrative macro work can quote directly.
- **texas-rules-of-appellate-procedure.pdf**, **texas-rules-of-civil-procedure-august-31-2025.pdf**, **texas-rules-of-evidence-effective-912025.pdf** — official rule compilations (146, 351, and 62 pages). Each parsed cleanly with `PyPDF2`, confirming metadata can be mined for pinpoint cites.
- **texas-court-rules-history-process.html** — archived HTML summary of the rulemaking timeline; keep alongside the PDFs as the canonical non-PDF supplement.
- All supplemental references under `temp/` are now inventoried as searchable, so no additional OCR passes are required before expanding locale or macro coverage.
- Each file originates from publicly available judiciary resources; no special licensing restrictions noted beyond standard attribution expectations.
- Backups live in-repo under `temp/`; refresh from https://www.txcourts.gov/rules-forms/rules-standards/ when official updates publish.

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
- **Draft 3** retains the Draft 2 macro library while layering in additional fallbacks (`book-like`, `web`) and a revised citation switch that defers to master templates for cases, statutes, and regulations. It also embeds `weight-parentheticals` and `pinpoint` logic for Westlaw citations, illustrating how to mix print and electronic reporters within the same macro stack.【F:temp/texas-greenbook-15th-draft3.csl†L1-L428】
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
| `weight-parentheticals` | Emits weight-of-authority explanatory parentheticals from `genre`/`medium`. | Shared helper |
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
│   └─ court-and-date → weight-parentheticals
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
  - *Parentheticals*: `weight-parentheticals` only reads `genre`/`medium`; introduce a generalized `explanatory-parenthetical` helper that can handle procedural phrases (`per curiam`, `mem. op.`, `orig. proceeding`) by inspecting `status`, `genre`, and custom fields.
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
| style > style > macro:weight-parentheticals > choose > if > text | prefix=' (', suffix=')', variable='genre' |
| style > style > macro:weight-parentheticals > choose > if > text | prefix=' (', suffix=')', variable='medium' |
| style > style > macro:legal-case > group (delim=', ') > text | macro='case-name' |
| style > style > macro:legal-case > group (delim=', ') > choose > if > text | macro='reporter-print' |
| style > style > macro:legal-case > group (delim=', ') > choose > else > text | macro='reporter-wl' |
| style > style > macro:legal-case > group (delim=', ') > text | macro='pinpoint' |
| style > style > macro:legal-case > text | macro='court-and-date' |
| style > style > macro:legal-case > text | macro='weight-parentheticals' |
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
- Web citations in Chapter 16 rely on “available at” plus “Accessed” parentheticals. The PDF text uses ligatures that complicate automated extraction, so the inline comments cite the chapter generally (`Greenbook 15th ed. 76`). A follow-up task should confirm the precise pin cites once optical text cleanup is available.
- Table of Authorities tests cover the major groups but still lack examples for federal authorities and multi-level leaders (e.g., nested subentries). Future iterations should add those once the TOA CSL variants support secondary sorting keys.

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

### Locale Integration Schedule (2025-04-02)
1. **Refactor inline locale blocks.** Update `texas-greenbook-15th-edition.csl` and all TOA variants (`texas-greenbook-15th-toa*.csl`) to drop their embedded `<locale>` sections in favor of referencing the shared file once citeproc loading is wired up, ensuring each style continues to declare `default-locale="en-US"` for compatibility.【F:texas-greenbook-15th-edition.csl†L1-L32】【F:temp/texas-greenbook-15th-toa.csl†L1-L24】
2. **Augment the test harness.** Extend `temp/run_tests.py` (or its successor) to point citeproc-py at `temp/locales/` via an explicit locale directory argument or manual locale registration so the regression suite exercises the shared terms instead of the deprecated inline overrides.【F:temp/run_tests.py†L1-L86】
3. **Regenerate fixtures.** After the styles pull from the shared locale, refresh `expected.txt`, `expected_secondary.txt`, and all TOA expected outputs to capture any punctuation or spacing differences introduced by the new loading path.【F:temp/expected.txt†L1-L214】【F:temp/expected_secondary.txt†L1-L180】【F:temp/expected_toa_grouped_leaders.txt†L1-L28】
4. **Document the switchover.** Update `temp/README.md` and this notebook once the locale integration lands so future contributors know the inline overrides were intentionally removed and understand how to run tests with the shared locale in place.【F:temp/README.md†L62-L109】

## CSL Contribution Guideline Review (2025-04-02)
- Re-read the CSL contributing guide to confirm the locale submission will follow the same PR-driven workflow as styles and that validation against the CSL schema remains a hard requirement before opening upstream pull requests.【F:CONTRIBUTING.md†L1-L33】【F:STYLE_DEVELOPMENT.md†L209-L249】
- Verified the style repository requirements covering titles, IDs, self links, licensing, and default locale declarations so the Texas Greenbook styles stay compliant once the locale refactor lands; no new metadata gaps surfaced during this review.【F:STYLE_REQUIREMENTS.md†L5-L112】
- Noted that the official repositories publish both styles and locales under a synchronized release cadence, so our internal plan to mirror the published locale copy aligns with upstream maintenance expectations.【F:README.md†L52-L77】
