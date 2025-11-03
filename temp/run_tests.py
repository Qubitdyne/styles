import argparse
import importlib.util
import json
import shlex
import sys
import warnings
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


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

# Keep citeproc's unsupported Reference argument warning quiet for metadata
# fields we intentionally preserve in the fixtures (e.g., provenance
# annotations). The message can list one or multiple arguments separated by
# commas, so build a regular expression that tolerates any combination of the
# known keys.
_REFERENCE_WARNING_FIELDS = (
    "comment",
    "label",
    "reviewed_title",
    "grouping",
    "related",
)

warnings.filterwarnings(
    "ignore",
    message=r"The following arguments for Reference are unsupported: "
    r"(?:" + r"|".join(_REFERENCE_WARNING_FIELDS) + r")"
    r"(?:, (?:" + r"|".join(_REFERENCE_WARNING_FIELDS) + r"))*",
    category=UserWarning,
)
warnings.filterwarnings(
    "ignore",
    message=r"The following arguments for CitationItem are unsupported: note",
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


def _format_timestamp() -> str:
    """Return an ISO 8601 UTC timestamp without fractional seconds."""

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append_run_history(
    *,
    ok_count: int,
    diff_count: int,
    expected_total: int,
    rendered_total: int,
    mode: str,
    args: argparse.Namespace,
) -> None:
    """Append a one-line summary of the run to temp/test-logs/run-history.log."""

    log_dir = Path("temp/test-logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "run-history.log"

    timestamp = _format_timestamp()
    status = "PASS" if diff_count == 0 and expected_total == rendered_total else "FAIL"
    summary = f"{ok_count} OK, {diff_count} DIFF"
    if expected_total != rendered_total:
        summary += f"; expected {expected_total}, rendered {rendered_total}"

    details: list[str] = [
        f"mode={mode}",
        f"style={args.style}",
        f"tests={args.tests}",
        f"expected={args.expected}",
    ]
    if args.write_expected:
        details.append(f"write_expected={args.write_expected}")

    command = shlex.join([sys.executable, *sys.argv])

    write_header = not log_path.exists() or log_path.stat().st_size == 0

    with log_path.open("a", encoding="utf-8") as handle:
        if write_header:
            handle.write("# timestamp | status | summary | details | command\n")
        handle.write(
            f"{timestamp} | {status} | {summary} | {'; '.join(details)} | {command}\n"
        )


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


def _should_auto_see_also(metadata: Mapping[str, Any]) -> bool:
    """Return True when the item merits an automatic “See also” cue."""

    # Bibliography/TOA renders should never receive automatic signals. The
    # Appendix B fixtures exercise grouped headings where cross-reference cues
    # would be inappropriate, so limit the automation to note-mode runs.
    if mode != "notes":
        return False

    item_type = metadata.get("type")
    if item_type != "legal_case":
        return False

    # Respect explicit cue metadata already provided in the item record.
    if metadata.get("note") or metadata.get("annote"):
        return False

    jurisdiction = metadata.get("jurisdiction")
    if isinstance(jurisdiction, str) and jurisdiction.lower().startswith("us:tx"):
        return False
    if isinstance(jurisdiction, str):
        return True

    def _has_texas_marker(value: Any) -> bool:
        return isinstance(value, str) and "tex" in value.lower()

    authority = metadata.get("authority")
    if _has_texas_marker(authority):
        return False

    container_title = metadata.get("container-title")
    if _has_texas_marker(container_title):
        return False

    return isinstance(authority, str) or isinstance(container_title, str)

for entry in test_items:
    if "id" in entry:
        entry_copy = deepcopy(entry)
        suffix = entry_copy.pop("_citation_suffix", None)
        locator = entry_copy.get("locator")
        label = entry_copy.get("label")

        if (
            _should_auto_see_also(entry_copy)
            and "annote" not in entry_copy
            and not entry_copy.get("references")
        ):
            entry_copy["annote"] = "See also"

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

        metadata = items_by_id[cite_id]
        if (
            _should_auto_see_also(metadata)
            and "annote" not in metadata
            and not metadata.get("references")
        ):
            citation_kwargs["note"] = "See also"

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

ok_count = 0
diff_count = 0

for index, (expected, actual) in enumerate(zip(expected_lines, rendered), start=1):
    status = "OK" if expected == actual else "DIFF"
    if status == "OK":
        ok_count += 1
    else:
        diff_count += 1
    comment = expected_comments[index - 1]
    comment_suffix = f" // {comment}" if comment else ""
    print(f"{index:02d}: {status}\n  expected: {expected}{comment_suffix}\n  actual:   {actual}\n")

if len(expected_lines) != len(rendered):
    print(f"Warning: expected {len(expected_lines)} lines but rendered {len(rendered)} citations.")

_append_run_history(
    ok_count=ok_count,
    diff_count=diff_count,
    expected_total=len(expected_lines),
    rendered_total=len(rendered),
    mode=mode,
    args=args,
)

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
