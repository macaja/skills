#!/usr/bin/env python3
"""Check a project's spec in docs/projects/<name>/ against the rules a machine can check.

Usage:
    python3 check_docs.py docs/projects/<name>

Checks G1, G2, G3, G7, S1, S3, E1, A1, L1, L4, L6 (ids and types), L7 and L9 from
references/writing.md, plus the `<project name>` placeholder from setup.md.
Prints one line per broken rule as `<file>: <rule id>: <what is wrong>`.
Exits 1 when a rule is broken, 0 otherwise. The other rules need a reader.
"""

import re
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "assets" / "template"
DOCS = ["01-discovery.md", "02-scope.md", "03-design/design.md", "04-delivery.md"]
ADR_DIR = "03-design/adrs"
ADR_TEMPLATE = "0000-template.md"

DOC_STATUS_RE = re.compile(r"^Status: (draft|in review|approved)$")
ADR_STATUS_RE = re.compile(r"^Status: (proposed|accepted|superseded by \d{4})$")
MILESTONE_STATUS_RE = re.compile(r"^(not started|in progress|done)$")
COMMIT_TYPE_RE = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?$")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
ITEM_ID_RE = re.compile(r"\bI(\d+)\b(?!\.\d)")
ANY_SCOPE_ID_RE = re.compile(r"\bI\d+(?:\.\d+)?\b")
MAX_LINES = 200

findings: list[str] = []


def report(file: str, rule: str, message: str) -> None:
    findings.append(f"{file}: {rule}: {message}")


def strip_comments(text: str) -> str:
    return COMMENT_RE.sub("", text)


def sections(text: str, level: int = 2) -> dict[str, str]:
    """Map each heading of the given level to the text under it."""
    marker = "#" * level + " "
    result: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        if line.startswith(marker):
            current = line[len(marker):].strip()
            result[current] = ""
        elif re.match(r"^#{1,%d} " % (level - 1), line):
            current = None
        elif current is not None:
            result[current] += line + "\n"
    return result


def normalized(text: str) -> str:
    body = "\n".join(line for line in text.splitlines() if not line.startswith("# "))
    return re.sub(r"\s+", " ", body).strip()


def untouched(text: str, template: str) -> bool:
    """True while a file still holds its template text (setup.md, step 4)."""
    return normalized(text) == normalized(template)


def check_common(name: str, raw: str, template: str, is_adr: bool) -> str:
    """G1, G2, G3, G7 and the placeholder. Returns the status value."""
    lines = raw.splitlines()
    if "<project name>" in raw:
        report(name, "setup", "the <project name> placeholder is still there")
    if len(lines) >= MAX_LINES:
        report(name, "G7", f"{len(lines)} lines, the limit is under {MAX_LINES}")

    after_title = [l for l in lines[1:] if l.strip()] if lines and lines[0].startswith("# ") else []
    status_line = after_title[0].strip() if after_title else ""
    status_re = ADR_STATUS_RE if is_adr else DOC_STATUS_RE
    if not lines or not lines[0].startswith("# "):
        report(name, "G1", "the first line is not a title (# ...)")
    elif not status_re.match(status_line):
        report(name, "G1", f'the first line after the title is "{status_line}", not a valid Status line')
    status = status_line.removeprefix("Status: ")

    present = set(sections(raw))
    for heading in sections(template):
        if heading not in present:
            report(name, "G2", f'section "## {heading}" from the template is missing')

    if status in ("approved", "accepted"):
        text = strip_comments(raw)
        for number, line in enumerate(text.splitlines(), start=1):
            if re.search(r"\b(TODO|TBD)\b", line):
                report(name, "G3", f"{status} but has TODO or TBD: {line.strip()[:60]}")
        if not is_adr:
            questions = strip_comments(sections(raw).get("Open questions", ""))
            for line in questions.splitlines():
                if line.strip().startswith("- ") and "(not blocking)" not in line:
                    report(name, "G3", f"approved but has a blocking open question: {line.strip()[:60]}")
    return status


def scope_ids(text: str, name: str) -> tuple[list[int], dict[int, list[str]]]:
    """S1. Returns the In scope item numbers and the criteria ids of each item."""
    parts = sections(strip_comments(text))
    items: list[int] = []
    for line in parts.get("In scope", "").splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        match = re.match(r"^- I(\d+): \S", line)
        if not match:
            report(name, "S1", f'In scope item without an id "I<n>: ": {line[:60]}')
            continue
        number = int(match.group(1))
        if number in items:
            report(name, "S1", f"I{number} is used twice in In scope")
        elif items and number < max(items):
            report(name, "S1", f"I{number} is out of order in In scope")
        items.append(number)

    criteria: dict[int, list[str]] = {}
    subsections = sections(parts.get("Acceptance criteria", ""), level=3)
    acceptance_text = strip_comments(text).split("## Acceptance criteria", 1)
    subsections = sections(acceptance_text[1].split("\n## ", 1)[0], level=3) if len(acceptance_text) > 1 else {}
    for heading, body in subsections.items():
        match = re.match(r"^I(\d+): \S", heading)
        if not match:
            report(name, "S1", f'Acceptance criteria subsection not titled "I<n>: <item>": {heading[:60]}')
            continue
        number = int(match.group(1))
        ids = []
        for line in body.splitlines():
            line = line.strip()
            if not line.startswith("- "):
                continue
            cmatch = re.match(r"^- I(\d+)\.(\d+): \S", line)
            if not cmatch:
                report(name, "S1", f'criterion without an id "I{number}.<m>: " under I{number}: {line[:60]}')
                continue
            if int(cmatch.group(1)) != number:
                report(name, "S1", f"criterion I{cmatch.group(1)}.{cmatch.group(2)} is under the subsection of I{number}")
                continue
            cid = f"I{number}.{cmatch.group(2)}"
            if cid in ids:
                report(name, "S1", f"{cid} is used twice")
            ids.append(cid)
        if not ids:
            report(name, "S1", f"I{number} has no acceptance criterion")
        criteria[number] = ids
    for number in items:
        if number not in criteria:
            report(name, "S1", f"I{number} has no subsection under Acceptance criteria")
    for number in criteria:
        if number not in items:
            report(name, "S1", f"the subsection I{number} has no In scope item")
    return items, criteria


def delivery(text: str, name: str) -> dict[str, dict]:
    """L1, L6, L7. Returns each milestone with its delivered ids and deliverables."""
    body = strip_comments(text)
    milestones_text = body.split("## Milestones", 1)[1].split("\n## ", 1)[0] if "## Milestones" in body else ""
    milestones: dict[str, dict] = {}
    for heading, block in sections(milestones_text, level=3).items():
        match = re.match(r"^M(\d+): \S", heading)
        if not match:
            report(name, "L1", f'milestone not titled "M<k>: <name>": {heading[:60]}')
            continue
        key = f"M{match.group(1)}"
        fields = {}
        for line in block.splitlines():
            fmatch = re.match(r"^- (Goal|Delivers|Definition of done|Status)\b[^:]*:\s*(.*)$", line.strip())
            if fmatch:
                fields[fmatch.group(1)] = fmatch.group(2).strip()
        for field in ("Goal", "Delivers", "Definition of done", "Status"):
            if field not in fields:
                report(name, "L1", f"{key} has no {field}")
        if "Goal" in fields and not fields["Goal"]:
            report(name, "L1", f"{key} has an empty Goal")
        status = fields.get("Status", "").strip("` ")
        fields["Status"] = status
        if "Status" in fields and not MILESTONE_STATUS_RE.match(status):
            report(name, "L1", f'{key} has the status "{status}", not one of: not started, in progress, done')

        delivered = set(ANY_SCOPE_ID_RE.findall(fields.get("Delivers", "")))
        deliverables: dict[str, set[str]] = {}
        for line in block.splitlines():
            cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or not re.match(r"^M\d+\.\d+$", cells[0]):
                continue
            did, dtype, _, ddelivers = cells[0], cells[1], cells[2], cells[3]
            if not did.startswith(key + "."):
                report(name, "L6", f"deliverable {did} is in the table of {key}")
            if did in deliverables:
                report(name, "L6", f"deliverable {did} is used twice")
            if not COMMIT_TYPE_RE.match(dtype):
                report(name, "L6", f'deliverable {did} has the type "{dtype}", not a Conventional Commits type')
            deliverables[did] = set(ANY_SCOPE_ID_RE.findall(ddelivers))
        if not deliverables:
            report(name, "L6", f"{key} has no Deliverables table rows")
        milestones[key] = {"delivers": delivered, "deliverables": deliverables, "status": fields.get("Status", "")}
    return milestones


def check_status(raw: str) -> str:
    lines = [l.strip() for l in raw.splitlines()[1:] if l.strip()]
    return lines[0].removeprefix("Status: ") if lines else ""


def expand(ids: set[str], criteria: dict[int, list[str]]) -> set[str]:
    """L2: an item id means all its criteria. Unknown items stay as they are."""
    result: set[str] = set()
    for sid in ids:
        match = re.match(r"^I(\d+)$", sid)
        if match and criteria.get(int(match.group(1))):
            result.update(criteria[int(match.group(1))])
        else:
            result.add(sid)
    return result


def dependencies(text: str, name: str, milestones: dict[str, dict]) -> None:
    """L9."""
    section = strip_comments(sections(text).get("Dependencies", ""))
    blocks = re.findall(r"```mermaid\s*\n(.*?)```", section, re.S)
    if len(blocks) != 1 or "flowchart" not in blocks[0]:
        report(name, "L9", "the Dependencies section needs exactly one Mermaid flowchart")
        return
    graph = blocks[0]
    nodes = set(re.findall(r"\bM(\d+)_(\d+)\b", graph))
    for milestone in milestones.values():
        for did in milestone["deliverables"]:
            k, n = did[1:].split(".")
            if (k, n) not in nodes:
                report(name, "L9", f"deliverable {did} has no node M{k}_{n} in the graph")

    edges: dict[str, set[str]] = {}
    for line in graph.splitlines():
        if "-->" not in line:
            continue
        parts = re.split(r"-->(?:\|[^|]*\|)?", line)
        names = []
        for part in parts:
            match = re.search(r"\b(M\d+_\d+)\b", part)
            names.append(match.group(1) if match else None)
        for source, target in zip(names, names[1:]):
            if source and target:
                edges.setdefault(source, set()).add(target)
                if int(source[1:].split("_")[0]) > int(target[1:].split("_")[0]):
                    report(name, "L9", f"arrow {source} --> {target} goes from a later milestone to an earlier one")

    state: dict[str, int] = {}

    def visit(node: str, path: list[str]) -> None:
        state[node] = 1
        for nxt in edges.get(node, ()):
            if state.get(nxt) == 1:
                report(name, "L9", "cycle: " + " --> ".join(path[path.index(nxt):] + [nxt]) if nxt in path else f"cycle at {nxt}")
            elif nxt not in state:
                visit(nxt, path + [nxt])
        state[node] = 2

    for node in list(edges):
        if node not in state:
            visit(node, [node])


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"{root} is not a folder")
        return 2

    texts: dict[str, str] = {}
    live: dict[str, bool] = {}
    for doc in DOCS:
        path = root / doc
        template = (TEMPLATE_DIR / doc).read_text(encoding="utf-8")
        if not path.exists():
            report(doc, "setup", "the file from the template is missing")
            continue
        raw = path.read_text(encoding="utf-8")
        texts[doc] = raw
        live[doc] = not untouched(raw.replace(raw.splitlines()[0], "# <project name>", 1) if raw else raw,
                                  template.replace(template.splitlines()[0], "# <project name>", 1))
        check_common(doc, raw, template, is_adr=False)

    items: list[int] = []
    criteria: dict[int, list[str]] = {}
    if live.get("02-scope.md"):
        items, criteria = scope_ids(texts["02-scope.md"], "02-scope.md")

    if live.get("03-design/design.md") and items:
        design = strip_comments(texts["03-design/design.md"])
        mentioned = {int(n) for n in ITEM_ID_RE.findall(design)} | {
            int(m) for m in re.findall(r"\bI(\d+)\.\d+\b", design)
        }
        for number in items:
            if number not in mentioned:
                report("03-design/design.md", "E1", f"I{number} from 02-scope.md does not appear in the design")

    if live.get("04-delivery.md"):
        milestones = delivery(texts["04-delivery.md"], "04-delivery.md")
        dependencies(texts["04-delivery.md"], "04-delivery.md", milestones)
        statuses = {doc: check_status(texts.get(doc, "")) for doc in ("02-scope.md", "03-design/design.md", "04-delivery.md")}
        not_approved = [doc for doc, status in statuses.items() if status != "approved"]
        for key, milestone in milestones.items():
            if milestone["status"] in ("in progress", "done") and not_approved:
                report("04-delivery.md", "L4", f"{key} is {milestone['status']}, but these are not approved: {', '.join(not_approved)}")
        for key, milestone in milestones.items():
            covered = set().union(*milestone["deliverables"].values()) if milestone["deliverables"] else set()
            missing = expand(milestone["delivers"], criteria) - expand(covered, criteria)
            for sid in sorted(missing, key=lambda x: [int(p) for p in x[1:].split(".")]):
                report("04-delivery.md", "L7", f"{key} delivers {sid}, but none of its deliverables does")
        if criteria:
            delivered = set().union(*(m["delivers"] for m in milestones.values())) if milestones else set()
            for number, ids in criteria.items():
                for cid in ids:
                    if f"I{number}" not in delivered and cid not in delivered:
                        report("02-scope.md", "S3", f"{cid} has no milestone in 04-delivery.md")

    adr_root = root / ADR_DIR
    adr_template = (TEMPLATE_DIR / ADR_DIR / ADR_TEMPLATE).read_text(encoding="utf-8")
    numbers = []
    for path in sorted(adr_root.glob("*.md")) if adr_root.is_dir() else []:
        rel = f"{ADR_DIR}/{path.name}"
        if path.name == ADR_TEMPLATE:
            continue
        match = re.match(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$", path.name)
        if not match:
            report(rel, "A1", 'the name is not "NNNN-<slug>.md" in lowercase kebab-case')
            continue
        numbers.append(int(match.group(1)))
        check_common(rel, path.read_text(encoding="utf-8"), adr_template, is_adr=True)
    for expected, number in enumerate(sorted(numbers), start=1):
        if number != expected:
            report(ADR_DIR, "A1", f"ADR numbers are not in order from 0001: expected {expected:04d}, found {number:04d}")
            break

    for finding in findings:
        print(finding)
    print(f"{len(findings)} broken rule(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
