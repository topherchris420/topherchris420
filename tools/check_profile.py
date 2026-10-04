#!/usr/bin/env python3
"""Check that this profile says what its ledger says.

The rule this profile applies to every project is: a system proposes, an
inspectable process checks, and the outcome stays on the record. This script
applies the same rule to the profile itself. It runs on every push (see
.github/workflows/check.yml) and needs only the Python standard library.

Offline checks, always run:

  ledger   experiments/ledger.json is well formed: known schema, unique ids,
           states from the ladder, ISO dates, milestone day counts that agree
           with their dates, and a top-level review date equal to the latest
           per-entry review.
  table    every ledger entry has a row in experiments/README.md, and the
           row's question and state codes match the entry exactly.
  markers  every `<!-- ledger:ID -->` marker in README.md names a ledger
           entry, and the line after it shows that entry's states exactly.
  map      every ledger entry's repository is linked from docs/project-map.md.
  links    every relative link, image and heading anchor in the Markdown
           files resolves; anchors follow GitHub's heading slugs.
  svg      every SVG in assets/ is self-contained (valid XML, <title> and
           <desc>, no scripts, images, animation or remote references), and
           every light variant has a dark twin.
  dates    the front page's "Reviewed ..." line is a real date no later than
           the ledger's review date.
  claims   the sentences saying nothing has reached REPRODUCED or SUPPORTED
           are present only while that is what the ledger says.

Optional:

  --external  every http(s) link in the Markdown files answers with a status
              below 400. Needs network access, so it is not run on push.

Exit status is 0 when everything passes and 1 otherwise.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "experiments" / "ledger.json"
LEDGER_DOC = ROOT / "experiments" / "README.md"
FRONT_PAGE = ROOT / "README.md"
PROJECT_MAP = ROOT / "docs" / "project-map.md"
ASSETS = ROOT / "assets"

SCHEMA = "vers3dynamics-ledger/v1"
LADDER = (
    "CONCEIVED",
    "BUILDING",
    "EXECUTABLE",
    "OBSERVED",
    "REPRODUCED",
    "SUPPORTED",
    "NOT SUPPORTED",
)
SVG_NS = "{http://www.w3.org/2000/svg}"
FORBIDDEN_SVG_ELEMENTS = {
    "script",
    "image",
    "foreignObject",
    "animate",
    "animateTransform",
    "animateMotion",
    "animateColor",
    "set",
    "video",
    "audio",
    "iframe",
}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
MARKER = re.compile(r"<!--\s*ledger:([a-z0-9-]+)\s*-->")
BACKTICKED = re.compile(r"`([^`]+)`")
MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_REF = re.compile(r"\b(?:src|href|srcset)=\"([^\"]+)\"")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
EXTERNAL = re.compile(r"https?://[^\s<>()\[\]\"'`]+")
REVIEWED_LINE = re.compile(r"\*Reviewed (\d{1,2} [A-Z][a-z]+ \d{4})\.")


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.counts: dict[str, int] = {}

    def fail(self, where: str, message: str) -> None:
        self.failures.append(f"{where}: {message}")

    def count(self, check: str, n: int = 1) -> None:
        self.counts[check] = self.counts.get(check, 0) + n

    def summary(self) -> str:
        parts = [f"{k} {v}" for k, v in self.counts.items()]
        return " · ".join(parts)


# --- Markdown helpers -------------------------------------------------------


def markdown_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def lines_without_fences(text: str) -> list[str]:
    """Return the file's lines with fenced code blocks blanked, numbering kept."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return out


def slugify(heading: str) -> str:
    """GitHub's heading anchor: lowercase, drop punctuation, spaces to hyphens."""
    text = re.sub(r"<[^>]+>", "", heading)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("*", "")
    text = text.lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def heading_slugs(lines: list[str]) -> set[str]:
    seen: dict[str, int] = {}
    slugs: set[str] = set()
    for line in lines:
        m = HEADING.match(line)
        if not m:
            continue
        slug = slugify(m.group(2))
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        slugs.add(slug if n == 0 else f"{slug}-{n}")
    return slugs


def iter_targets(lines: list[str]):
    """Yield (line_number, target) for every link-like reference."""
    for number, line in enumerate(lines, 1):
        for m in MD_LINK.finditer(line):
            yield number, m.group(1)
        for m in HTML_REF.finditer(line):
            for candidate in m.group(1).split(","):
                target = candidate.strip().split(" ")[0]
                if target:
                    yield number, target


# --- Checks -----------------------------------------------------------------


def load_ledger(report: Report) -> dict | None:
    try:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report.fail(rel(LEDGER), f"cannot parse: {exc}")
        return None
    return data


def valid_date(value) -> dt.date | None:
    if not isinstance(value, str) or not ISO_DATE.match(value):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def check_ledger(ledger: dict, report: Report) -> dict[str, dict]:
    where = rel(LEDGER)
    entries: dict[str, dict] = {}

    if ledger.get("schema") != SCHEMA:
        report.fail(where, f"schema is {ledger.get('schema')!r}, expected {SCHEMA!r}")
    reviewed = valid_date(ledger.get("reviewed"))
    if reviewed is None:
        report.fail(where, "top-level 'reviewed' is not an ISO date")
    states = ledger.get("states")
    if not isinstance(states, dict) or set(states) != set(LADDER):
        report.fail(where, "'states' must define exactly the ladder: " + ", ".join(LADDER))
    questions = ledger.get("questions")
    if not isinstance(questions, dict) or not questions:
        report.fail(where, "'questions' must map a short keyword to each question")
        questions = {}
    question_texts = set(questions.values())

    experiments = ledger.get("experiments")
    if not isinstance(experiments, list) or not experiments:
        report.fail(where, "'experiments' must be a non-empty list")
        return entries

    latest_review: dt.date | None = None
    for entry in experiments:
        eid = entry.get("id")
        tag = f"{where} [{eid}]"
        if not isinstance(eid, str) or not re.fullmatch(r"[a-z0-9-]+", eid):
            report.fail(tag, "id must be lowercase letters, digits and hyphens")
            continue
        if eid in entries:
            report.fail(tag, "duplicate id")
            continue
        entries[eid] = entry

        for key in ("name", "repo", "question"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                report.fail(tag, f"missing '{key}'")
        repo = entry.get("repo", "")
        if isinstance(repo, str) and not repo.startswith("https://"):
            report.fail(tag, f"repo must be an https URL, got {repo!r}")
        if question_texts and entry.get("question") not in question_texts:
            report.fail(tag, f"question {entry.get('question')!r} is not one of the ledger's questions")

        state_list = entry.get("state")
        if not isinstance(state_list, list) or not state_list:
            report.fail(tag, "'state' must be a non-empty list")
        else:
            for item in state_list:
                if not isinstance(item, dict) or item.get("state") not in LADDER:
                    report.fail(tag, f"state {item!r} is not on the ladder")
                elif not isinstance(item.get("scope"), str) or not item["scope"].strip():
                    report.fail(tag, f"state {item['state']} has no scope; the scope is part of the state")

        if "last_reviewed" in entry:
            last = valid_date(entry["last_reviewed"])
            if last is None:
                report.fail(tag, "'last_reviewed' is not an ISO date")
            else:
                if reviewed and last > reviewed:
                    report.fail(tag, f"last_reviewed {last} is after the ledger's reviewed date {reviewed}")
                if latest_review is None or last > latest_review:
                    latest_review = last

        for url in entry.get("evidence", []):
            if not isinstance(url, str) or not url.startswith("https://"):
                report.fail(tag, f"evidence {url!r} is not an https URL")

        timeline = entry.get("timeline")
        if not isinstance(timeline, dict) or not isinstance(timeline.get("reconstructed"), bool):
            report.fail(tag, "'timeline.reconstructed' must be true or false")
            continue
        first = None
        if "first_commit" in timeline:
            first = valid_date(timeline["first_commit"].get("date"))
            if first is None:
                report.fail(tag, "'first_commit.date' is not an ISO date")
            sha = timeline["first_commit"].get("sha")
            if sha is not None and not SHA.match(sha):
                report.fail(tag, f"first_commit sha {sha!r} is not 40 hex digits")
        previous: dt.date | None = None
        for milestone in timeline.get("milestones", []):
            date = valid_date(milestone.get("date"))
            if date is None:
                report.fail(tag, f"milestone {milestone.get('label')!r} has no ISO date")
                continue
            if previous and date < previous:
                report.fail(tag, f"milestones out of order at {date}")
            previous = date
            if "day" in milestone:
                if first is None:
                    report.fail(tag, f"milestone day {milestone['day']} given without a first_commit date")
                elif (date - first).days != milestone["day"]:
                    report.fail(
                        tag,
                        f"milestone {date} is day {(date - first).days} after {first}, not day {milestone['day']}",
                    )
            sha = milestone.get("sha")
            if sha is not None and not SHA.match(sha):
                report.fail(tag, f"milestone sha {sha!r} is not 40 hex digits")

    if reviewed and latest_review and latest_review != reviewed:
        report.fail(where, f"'reviewed' is {reviewed} but the latest last_reviewed is {latest_review}")

    report.count("ledger entries", len(entries))
    return entries


def states_of(entry: dict) -> set[str]:
    return {s["state"] for s in entry.get("state", []) if isinstance(s, dict) and s.get("state") in LADDER}


def keyword_for(ledger: dict, question: str) -> str | None:
    for keyword, text in ledger.get("questions", {}).items():
        if text == question:
            return keyword
    return None


def check_table(ledger: dict, entries: dict[str, dict], report: Report) -> None:
    where = rel(LEDGER_DOC)
    lines = lines_without_fences(LEDGER_DOC.read_text(encoding="utf-8"))
    by_repo = {e["repo"]: e for e in entries.values() if isinstance(e.get("repo"), str)}
    seen: set[str] = set()
    in_section = False
    rows = 0
    for number, line in enumerate(lines, 1):
        if line.startswith("## "):
            in_section = line.strip() == "## Where things stand"
            continue
        if not in_section or not line.startswith("| ["):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            report.fail(f"{where}:{number}", "table row has fewer than three cells")
            continue
        m = re.search(r"\]\((https?://[^)]+)\)", cells[0])
        repo = m.group(1) if m else None
        entry = by_repo.get(repo)
        if entry is None:
            report.fail(f"{where}:{number}", f"row links {repo!r}, which is not a ledger repository")
            continue
        rows += 1
        seen.add(entry["id"])
        expected_keyword = keyword_for(ledger, entry.get("question", ""))
        if expected_keyword and cells[1] != expected_keyword:
            report.fail(f"{where}:{number}", f"{entry['name']}: question column is {cells[1]!r}, ledger says {expected_keyword!r}")
        shown = set()
        for token in BACKTICKED.findall(cells[2]):
            if token in LADDER:
                shown.add(token)
            else:
                report.fail(f"{where}:{number}", f"{entry['name']}: `{token}` is not a ladder state")
        if shown != states_of(entry):
            report.fail(
                f"{where}:{number}",
                f"{entry['name']}: table shows {sorted(shown)}, ledger has {sorted(states_of(entry))}",
            )
    for eid, entry in entries.items():
        if eid not in seen:
            report.fail(where, f"{entry['name']} ({eid}) has no row under 'Where things stand'")
    report.count("table rows", rows)


def check_markers(entries: dict[str, dict], report: Report) -> None:
    where = rel(FRONT_PAGE)
    lines = lines_without_fences(FRONT_PAGE.read_text(encoding="utf-8"))
    markers = 0
    for index, line in enumerate(lines):
        m = MARKER.search(line)
        if not m:
            continue
        markers += 1
        eid = m.group(1)
        entry = entries.get(eid)
        if entry is None:
            report.fail(f"{where}:{index + 1}", f"marker names unknown ledger entry {eid!r}")
            continue
        following = next((l for l in lines[index + 1 :] if l.strip()), "")
        shown = set()
        for token in BACKTICKED.findall(following):
            if token in LADDER:
                shown.add(token)
            elif token.isupper():
                report.fail(f"{where}:{index + 1}", f"{entry['name']}: `{token}` is not a ladder state")
        if shown != states_of(entry):
            report.fail(
                f"{where}:{index + 1}",
                f"{entry['name']}: page shows {sorted(shown)}, ledger has {sorted(states_of(entry))}",
            )
    if markers == 0:
        report.fail(where, "no <!-- ledger:ID --> markers found; the front page is unchecked")
    report.count("front-page markers", markers)


def check_project_map(entries: dict[str, dict], report: Report) -> None:
    text = PROJECT_MAP.read_text(encoding="utf-8")
    missing = 0
    for entry in entries.values():
        repo = entry.get("repo")
        if isinstance(repo, str) and repo not in text:
            report.fail(rel(PROJECT_MAP), f"{entry['name']} ({repo}) is not in the project map")
            missing += 1
    report.count("map entries", len(entries) - missing)


def check_links(report: Report) -> set[str]:
    external: set[str] = set()
    checked = 0
    slug_cache: dict[Path, set[str]] = {}

    def slugs(path: Path) -> set[str]:
        if path not in slug_cache:
            slug_cache[path] = heading_slugs(lines_without_fences(path.read_text(encoding="utf-8")))
        return slug_cache[path]

    for md in markdown_files():
        lines = lines_without_fences(md.read_text(encoding="utf-8"))
        for line in lines:
            external.update(u.rstrip(".,;:") for u in EXTERNAL.findall(line))
        for number, target in iter_targets(lines):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            path_part, _, anchor = target.partition("#")
            where = f"{rel(md)}:{number}"
            if path_part:
                resolved = (md.parent / path_part).resolve()
                if ROOT not in resolved.parents and resolved != ROOT:
                    report.fail(where, f"{target} points outside the repository")
                    continue
                if not resolved.exists():
                    report.fail(where, f"{target} does not exist")
                    continue
            else:
                resolved = md
            if anchor:
                if resolved.suffix.lower() != ".md":
                    continue
                if anchor not in slugs(resolved):
                    report.fail(where, f"{target}: no heading with anchor #{anchor} in {rel(resolved)}")
    report.count("relative links", checked)
    return external


def check_svgs(report: Report) -> None:
    files = sorted(ASSETS.glob("*.svg"))
    names = {f.name for f in files}
    for svg in files:
        where = rel(svg)
        try:
            root = ET.parse(svg).getroot()
        except ET.ParseError as exc:
            report.fail(where, f"invalid XML: {exc}")
            continue
        if root.tag != SVG_NS + "svg":
            report.fail(where, f"root element is {root.tag}, not <svg>")
            continue
        for required in ("title", "desc"):
            el = root.find(SVG_NS + required)
            if el is None or not (el.text or "").strip():
                report.fail(where, f"missing or empty <{required}>")
        if "aria-labelledby" not in root.attrib:
            report.fail(where, "root <svg> has no aria-labelledby")
        for el in root.iter():
            local = el.tag.split("}")[-1]
            if local in FORBIDDEN_SVG_ELEMENTS:
                report.fail(where, f"contains <{local}>; assets must be static and self-contained")
            if local == "style":
                css = el.text or ""
                if "@import" in css or "url(" in css:
                    report.fail(where, "<style> references an external resource")
            for attr, value in el.attrib.items():
                name = attr.split("}")[-1]
                if name.startswith("on"):
                    report.fail(where, f"event handler attribute {name}")
                if name == "href" and value.startswith(("http:", "https:", "//")):
                    report.fail(where, f"remote reference {value}")
                if "url(" in value and "http" in value:
                    report.fail(where, f"remote reference in {name}")
        for light, dark in (("-light.svg", "-dark.svg"), ("-dark.svg", "-light.svg")):
            if svg.name.endswith(light) and svg.name[: -len(light)] + dark not in names:
                report.fail(where, f"has no {dark[1:-4]} twin")
    report.count("svg assets", len(files))


def check_dates(ledger: dict, report: Report) -> None:
    where = rel(FRONT_PAGE)
    text = FRONT_PAGE.read_text(encoding="utf-8")
    reviewed = valid_date(ledger.get("reviewed"))
    found = REVIEWED_LINE.findall(text)
    if not found:
        report.fail(where, "no '*Reviewed D Month YYYY.*' line on the front page")
    for raw in found:
        try:
            date = dt.datetime.strptime(raw, "%d %B %Y").date()
        except ValueError:
            report.fail(where, f"'Reviewed {raw}' is not a real date")
            continue
        if reviewed and date > reviewed:
            report.fail(where, f"front page reviewed {date} is after the ledger's reviewed date {reviewed}")
    report.count("review dates", len(found))


TOP_RUNG_CLAIMS = (
    (FRONT_PAGE, "Nothing here has reached `REPRODUCED` or `SUPPORTED` yet."),
    (LEDGER_DOC, "No entry currently meets this profile's independent `REPRODUCED` or external/physical `SUPPORTED` definition."),
)


def check_claims(entries: dict[str, dict], report: Report) -> None:
    reached = sorted(
        f"{e['name']}: {s}" for e in entries.values() for s in states_of(e) if s in ("REPRODUCED", "SUPPORTED")
    )
    for path, sentence in TOP_RUNG_CLAIMS:
        present = sentence in path.read_text(encoding="utf-8")
        if present and reached:
            report.fail(rel(path), "says nothing has reached REPRODUCED or SUPPORTED, but the ledger has " + "; ".join(reached))
        if not present and not reached:
            report.fail(rel(path), f"the ledger has no REPRODUCED or SUPPORTED entry, but the sentence saying so is gone: {sentence!r}")
    report.count("top-rung claims", len(TOP_RUNG_CLAIMS))


def fetch_status(url: str) -> int | str:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "profile-check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405):
            request = urllib.request.Request(url, headers={"User-Agent": "profile-check/1.0"})
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    return response.status
            except urllib.error.HTTPError as again:
                return again.code
            except urllib.error.URLError as again:
                return f"error: {again.reason}"
        return exc.code
    except urllib.error.URLError as exc:
        return f"error: {exc.reason}"
    except Exception as exc:  # noqa: BLE001 - report whatever the network did
        return f"error: {exc}"


def check_external(urls: set[str], report: Report) -> None:
    bases = sorted({u.split("#")[0] for u in urls})
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for url, status in zip(bases, pool.map(fetch_status, bases)):
            if not isinstance(status, int) or status >= 400:
                report.fail(url, f"answered {status}")
    report.count("external links", len(bases))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--external", action="store_true", help="also check that external links answer")
    args = parser.parse_args(argv)

    report = Report()
    ledger = load_ledger(report)
    if ledger is not None:
        entries = check_ledger(ledger, report)
        if entries:
            check_table(ledger, entries, report)
            check_markers(entries, report)
            check_project_map(entries, report)
            check_claims(entries, report)
        check_dates(ledger, report)
    external = check_links(report)
    check_svgs(report)
    if args.external:
        check_external(external, report)

    for failure in report.failures:
        print(f"FAIL {failure}")
    print(f"checked: {report.summary()}")
    if report.failures:
        print(f"{len(report.failures)} problem(s) found")
        return 1
    print("The page agrees with the ledger.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
