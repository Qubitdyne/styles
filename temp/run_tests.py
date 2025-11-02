import argparse
import importlib.util
import json
import sys
import warnings
from copy import deepcopy


def _ensure_citeproc_available() -> None:
    """Exit early with an actionable hint when citeproc is missing."""

    if importlib.util.find_spec("citeproc") is None:
        message = (
            "Missing required dependency 'citeproc'. Install it with "
            "'pip install -r temp/requirements.txt' or "
            "'pip install citeproc-py'."
        )
        sys.stderr.write(message + "\n")
        sys.exit(1)


_ensure_citeproc_available()

warnings.filterwarnings(
    "ignore",
    message=r"The following arguments for Reference are unsupported: (?:comment|label|reviewed_title)",
    category=UserWarning,
)

from citeproc import Citation, CitationItem, Locator
from citeproc import CitationStylesBibliography, CitationStylesStyle
from citeproc import formatter
from citeproc.source.json import CiteProcJSON

DEFAULT_STYLE_PATH = "temp/texas-greenbook-15th-edition.csl"
DEFAULT_TESTS_PATH = "temp/tests.json"
DEFAULT_EXPECTED_PATH = "temp/expected.txt"

parser = argparse.ArgumentParser(description="Render citeproc fixtures and compare against expected output.")
parser.add_argument("--style", default=DEFAULT_STYLE_PATH, help="Path to the CSL file under test.")
parser.add_argument("--tests", default=DEFAULT_TESTS_PATH, help="JSON fixture containing citeproc items and citations.")
parser.add_argument("--expected", default=DEFAULT_EXPECTED_PATH, help="Text file with expected cite strings (one per line).")
parser.add_argument(
    "--write-expected",
    default=None,
    help="Optional path for overwriting the expected-output fixture with the rendered cite strings.",
)
parser.add_argument(
    "--mode",
    choices=["notes", "bibliography"],
    default=None,
    help=(
        "Render note citations or bibliography entries. Defaults to bibliography "
        "when testing a Table of Authorities style and notes otherwise."
    ),
)
args = parser.parse_args()


def _infer_mode(style_path: str, requested_mode: str | None) -> str:
    if requested_mode:
        return requested_mode

    if "toa" in style_path.lower():
        return "bibliography"

    return "notes"


mode = _infer_mode(args.style, args.mode)

with open(args.tests, "r", encoding="utf-8") as f:
    test_items = json.load(f)

items_for_source = []
items_by_id = {}
notes = []

for entry in test_items:
    if "id" in entry:
        entry_copy = deepcopy(entry)
        suffix = entry_copy.pop("_citation_suffix", None)
        locator = entry_copy.get("locator")
        label = entry_copy.get("label")

        items_for_source.append(entry_copy)
        items_by_id[entry_copy["id"]] = entry_copy

        citation_kwargs = {}
        if locator:
            citation_kwargs["locator"] = Locator(label or "page", locator)
        if suffix:
            citation_kwargs["suffix"] = suffix

        notes.append(Citation([CitationItem(entry["id"], **citation_kwargs)]))
    elif "_cite" in entry:
        cite_id = entry["_cite"]
        if cite_id not in items_by_id:
            raise KeyError(f"Citation references unknown id: {cite_id}")

        locator = entry.get("locator")
        label = entry.get("label")
        suffix = entry.get("_citation_suffix")

        citation_kwargs = {}
        if locator:
            citation_kwargs["locator"] = Locator(label or "page", locator)
        if suffix:
            citation_kwargs["suffix"] = suffix

        notes.append(Citation([CitationItem(cite_id, **citation_kwargs)]))
    else:
        raise ValueError("Each test entry must declare either 'id' or '_cite'.")

style = CitationStylesStyle(args.style, validate=False)
source = CiteProcJSON(items_for_source)
bibliography = CitationStylesBibliography(style, source, formatter.plain)

rendered = []
for index, citation in enumerate(notes, start=1):
    citation.note_index = index
    bibliography.register(citation)
    citation_result = bibliography.cite(citation, lambda _: None)
    if mode == "notes":
        rendered.append(str(citation_result))

if mode == "bibliography":
    rendered = [str(entry) for entry in bibliography.bibliography()]

with open(args.expected, "r", encoding="utf-8") as f:
    raw_expected_lines = [line.rstrip("\n") for line in f]

expected_lines = []
expected_comments = []
for line in raw_expected_lines:
    if " // " in line:
        text, comment = line.split(" // ", 1)
        expected_lines.append(text.rstrip())
        expected_comments.append(comment)
    else:
        expected_lines.append(line)
        expected_comments.append("")

for index, (expected, actual) in enumerate(zip(expected_lines, rendered), start=1):
    status = "OK" if expected == actual else "DIFF"
    comment = expected_comments[index - 1]
    comment_suffix = f" // {comment}" if comment else ""
    print(f"{index:02d}: {status}\n  expected: {expected}{comment_suffix}\n  actual:   {actual}\n")

if len(expected_lines) != len(rendered):
    print(f"Warning: expected {len(expected_lines)} lines but rendered {len(rendered)} citations.")

if args.write_expected:
    max_len = max(len(rendered), len(expected_comments))
    with open(args.write_expected, "w", encoding="utf-8") as f:
        for i in range(max_len):
            actual = rendered[i] if i < len(rendered) else ""
            comment = expected_comments[i] if i < len(expected_comments) else ""
            if comment:
                f.write(f"{actual} // {comment}\n")
            else:
                f.write(f"{actual}\n")
    print(f"Wrote {len(rendered)} citations to {args.write_expected}")
