import json
from copy import deepcopy
from citeproc import Citation, CitationItem, Locator
from citeproc import CitationStylesBibliography, CitationStylesStyle
from citeproc import formatter
from citeproc.source.json import CiteProcJSON

STYLE_PATH = "temp/texas-greenbook-15th-edition.csl"
TESTS_PATH = "temp/tests.json"
EXPECTED_PATH = "temp/expected.txt"

with open(TESTS_PATH, "r", encoding="utf-8") as f:
    test_items = json.load(f)

items_for_source = []
notes = []
for entry in test_items:
    entry_copy = deepcopy(entry)
    suffix = entry_copy.pop("_citation_suffix", None)
    locator = entry_copy.pop("locator", None)
    label = entry_copy.pop("label", None)
    # Preserve any remaining metadata for citeproc
    items_for_source.append(entry_copy)

    citation_kwargs = {}
    if locator:
        citation_kwargs["locator"] = Locator(label or "page", locator)
    if suffix:
        citation_kwargs["suffix"] = suffix

    notes.append(Citation([CitationItem(entry["id"], **citation_kwargs)]))

style = CitationStylesStyle(STYLE_PATH, validate=False)
source = CiteProcJSON(items_for_source)
bibliography = CitationStylesBibliography(style, source, formatter.plain)

rendered = []
for index, citation in enumerate(notes, start=1):
    citation.note_index = index
    bibliography.register(citation)
    citation_result = bibliography.cite(citation, lambda _: None)
    rendered.append(str(citation_result))

with open(EXPECTED_PATH, "r", encoding="utf-8") as f:
    expected_lines = [line.rstrip("\n") for line in f]

for index, (expected, actual) in enumerate(zip(expected_lines, rendered), start=1):
    status = "OK" if expected == actual else "DIFF"
    print(f"{index:02d}: {status}\n  expected: {expected}\n  actual:   {actual}\n")

if len(expected_lines) != len(rendered):
    print(f"Warning: expected {len(expected_lines)} lines but rendered {len(rendered)} citations.")
