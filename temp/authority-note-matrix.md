# Authority Note Output Matrix

This matrix documents the desired output patterns for the *Texas Greenbook (15th ed.)* draft CSL when generating first references, short-form follow-up references, and cross-references.  Each category lists the controlling macro(s), the CSL `position` test used to select the variant, and the CSL variables (`references`, `status`, `note`) that are expected to contribute to the output.

| Authority Category | First-Note Output | Short-Form Output | Cross-Reference Output | Macro(s) | CSL Switch | Variable Usage |
| --- | --- | --- | --- | --- | --- | --- |
| Texas & other cases | Case name, reporter or Westlaw cite, pinpoint, court/year, weight parentheticals, subsequent history | Case name with same reporter/Westlaw string plus pinpoint and court/year | Cross-reference cue ("See" vs. "See also"), short string, court/year, weight parentheticals, appended history or references | `legal-case`, `legal-case-first`, `legal-case-short`, `legal-case-cross-reference` | `position="first"`, fallback `position="subsequent"` with `references` detection | `status` within `court-and-date`; `references` appended for history; `note` provides manual cue override |
| Texas statutes & codes | Short title with section symbol and section, optional parenthetical from note | Short title and section only | Cross-reference cue followed by short title/section and note-derived parenthetical | `tex-statute`, `tex-statute-first`, `tex-statute-short`, `tex-statute-cross-reference` | `position="first"` (bibliography guard via `first-reference-note-number`) vs. `references` present | `container-title-short` supplies the abbreviated code title; `note` holds publisher/year or explanatory text; `references` drive cross cites; `annote` reserved for signal overrides |
| Session laws (Texas General Laws & special acts) | Act title + legislature/session + chapter/section with codification or status parenthetical | Act title + legislature/session + chapter/section (no codification parenthetical) | Cross-reference cue + abbreviated act string + references | `session-law`, `session-law-first`, `session-law-short`, `session-law-cross-reference` | `position="first"`, else `references` | `collection-number`, `number`, `section`, and `note` (codification/status); `references` for parallel cites |
| Statutory notes & commentary | Code cite + descriptor (historical note, revisor’s note, U.C.C. comment) + bracketed provenance | Descriptor + code cite (retain bracketed provenance) | Cross-reference cue + descriptor + short cite + references | `statute-note`, `statute-note-first`, `statute-note-short`, `statute-note-cross-reference` | `position="first"`, else `references` | `genre` or `note` to select descriptor; `note` for bracketed session-law strings |
| Non-Texas statutes/codes | Full code name with section, status parenthetical | Code name with section | Cross-reference cue plus code name/section and appended references | `statute-code`, variants | `position="first"`, else `references` | `status` appended on first note; `references` for cross cite |
| Texas administrative code & registers | Volume/title section string with year parenthetical and descriptive title | Abbreviated code/register string (no year) | Cross-reference cue + abbreviated string + descriptive title + references | `tex-admin-code`, `tex-admin-code-first`, `tex-admin-code-short`, `tex-admin-code-cross-reference`; `tex-register` variants | `position="first"` (bibliography guard via `first-reference-note-number`), else `references` | `note` carries adoption or filing parentheticals that persist across cites; `references` append additional sections; `annote` can still inject signals when needed |
| Treaties/administrative compilations | Core cite with container, section, issued year and authority | Abbreviated container + section | Cross-reference cue + abbreviated cite + references | `tac-core`, `tac-core-first`, `tac-core-short`, `tac-core-cross-reference` | `position="first"`, else `references` | `references` appended; `authority` retained on first cite |
| Court rules | Rule title with section | Rule title + section | Cross-reference cue + rule title/section + references | `rule-core`, `rule-core-first`, `rule-core-short`, `rule-core-cross-reference` | `position="first"` (bibliography guard via `first-reference-note-number`), else `references` | `note` surfaces adoption/reprint parentheticals on first cite; `references` append additional rules; `annote` overrides cues |
| Local court rules | Court name + “Loc. R.” + rule identifier + optional county parenthetical | Court name + “Loc. R.” + rule identifier | Cross-reference cue + court label + rule identifier + references | `local-rule`, `local-rule-first`, `local-rule-short`, `local-rule-cross-reference` | `position="first"`, else `references` | `authority` for court name, `title`/`section` for rule number, `note` for county list |
| Municipal codes & local ordinances | Municipality, code title + chapter/section, issued year | Municipality + code short cite | Cross-reference cue + short cite + references | `municipal-code`, `municipal-code-first`, `municipal-code-short`, `municipal-code-cross-reference` | `position="first"`, else `references` | `references` appended; `issued` year retained for first cite |
| Attorney General opinions | Authority + opinion number, issued year | Authority abbreviation + number | Cross-reference cue + short cite + references | `ag-opinion`, `ag-opinion-first`, `ag-opinion-short`, `ag-opinion-cross-reference` | `position="first"`, else `references` | `references` appended |
| Secondary sources (books, treatises) | Author(s), volume + italicized title, pinpoint, edition/year | Italicized title + pinpoint + year | Cross-reference cue + italic title + pinpoint + references | `book-like` variants | `position="first"`, else `references` | `references` appended, `note` optional |
| Law review & journal articles | Author(s), quoted title, volume-journal-page string, year | Author(s), quoted title, pinpoint page | Cross-reference cue + quoted title + pinpoint + references | `article-journal` variants | `position="first"`, else `references` | `references` appended |
| Internet sources | Title, site, year, URL, accessed date | Title and URL | Cross-reference cue + title + URL + references | `web` variants | `position="first"`, else `references` | `note` can override cue; `references` appended |

## Cross-Reference Cue Logic

The `cross-reference-cue` macro now centralizes the internal vs. external authority language:

- When `note` is present it is capitalized and used verbatim (e.g., "Cf." or "Contra").
- When `jurisdiction="us:tx"` (Texas authority) the cue defaults to “See.”
- All other jurisdictions default to “See also,” flagging external authorities.

## Publication/status terminology audit (2025-11-04)
- Ran the publication/status string scan (`rg "Supp\\.|Supp|session|effective" temp -n --glob '*.csl'`) while cataloguing the `session-law` macro duplication across the edition and TOA variants. Active styles currently rely solely on metadata fields (`note`, `collection-number`, `volume`) without emitting explicit `Supp.`/`R.S.`/`Tex. Reg.` strings.
- No new abbreviations surfaced beyond those already tracked in the requirement matrix and locale inventory (chs. 10–13, pp. 42–65), so the matrix rows for statutes, session laws, and agency materials remain accurate. Future helper work should inject the Greenbook-mandated parentheticals once the shared publication/status macros are built.

## Differentiating Internal vs. External Authorities

- Case, statute, and administrative macros call `cross-reference-cue`, which evaluates `jurisdiction` to distinguish Texas authorities from external ones.
- The `statute-code-first` macro appends `status` to track in-force vs. repealed codes; in Texas-specific macros the `note` field holds equivalent parentheticals.
- All authority macros listed above share the same `position`/`cross-reference-cue` pattern, keeping internal/external handling consistent.

## Position Mapping Summary

- `position="first"` → full citation macro (`*-first`).
- `references` present and not `position="first"` → cross-reference macro (`*-cross-reference`).
- Otherwise → short-form macro (`*-short`).

This structure explicitly ties the requested outputs to CSL logic, allowing validation against the JSON test fixtures in `temp/`.

## Publication helper fallback coverage (2025-12-10)
- Exercised the prototype helper style (`temp/prototypes/publication-helper-prototype.csl`) against incomplete metadata to ensure the eventual shared helpers can drop section symbols, commas, and register semicolons cleanly.【F:temp/prototypes/publication-helper-prototype.csl†L11-L113】【F:temp/prototypes/publication-helper-prototype.json†L58-L94】
- New fixtures `tex_code_without_section`, `session_law_partial`, and `tac_notice_with_note` confirm the macros emit bare code titles, abbreviated session strings, and note-only parentheticals without double spaces, matching Greenbook Chapters 10–11 guidance.【F:temp/prototypes/publication-helper-expected.txt†L7-L10】【F:temp/Greenbook_15thEdition.pdf†L170-L212】
- Regression run `python temp/run_tests.py --style temp/prototypes/publication-helper-prototype.csl --tests temp/prototypes/publication-helper-prototype.json --expected temp/prototypes/publication-helper-expected.txt` documents nine passing scenarios and serves as the smoke test for integrating the helpers into the production styles.【ac0ae3†L1-L36】
- Annotated the TOA federal fixtures with Appendix B references so the helper rollout keeps grouped headings aligned with the Greenbook table layout.【F:temp/tests_toa.json†L1-L200】【F:temp/Greenbook_15thEdition.pdf†L612-L676】
