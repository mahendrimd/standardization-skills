#!/usr/bin/env python3
"""Validate a Standardization Skills local Markdown effort."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


PHASES = {"discovery", "assessment", "resolution", "synthesis", "validation"}
TYPES = {"research", "decision", "task"}
TICKET_STATUSES = {"open", "claimed", "resolved"}
MAP_STATUSES = {"active", "complete"}
ASSESSMENTS = {"pending", "standardize", "standardize a subset", "defer", "decline"}
DECISION_STATUSES = {"pending", "active", "superseded"}
MAP_HEADINGS = {
    "Standardization aim",
    "Notes",
    "Decisions",
    "Fog",
    "Out of scope",
    "Outputs",
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TICKET_RE = re.compile(r"^(\d+)-.+\.md$")


def field(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:[ \t]*(.*)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def headings(text: str) -> set[str]:
    return set(re.findall(r"^##[ \t]+(.+?)[ \t]*$", text, re.MULTILINE))


def section(text: str, name: str) -> str | None:
    match = re.search(
        rf"^##[ \t]+{re.escape(name)}[ \t]*\n(.*?)(?=^##[ \t]+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else None


def substantive(value: str | None) -> bool:
    if value is None:
        return False
    without_comments = re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL).strip()
    return bool(without_comments and not re.fullmatch(r"<.*>", without_comments, re.DOTALL))


def validate_links(path: Path, text: str, errors: list[str]) -> None:
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target or "<" in target or ">" in target:
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path}: broken relative link: {raw_target}")


def parse_blockers(value: str | None, path: Path, errors: list[str]) -> list[str]:
    if value is None:
        errors.append(f"{path}: missing field 'Blocked by'")
        return []
    if not value:
        return []
    blockers = []
    for token in value.split(","):
        token = token.strip()
        if not token.isdigit():
            errors.append(f"{path}: invalid blocker identity '{token}'")
        else:
            blockers.append(token.zfill(2))
    return blockers


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency not in graph:
                continue
            if state.get(dependency, 0) == 0:
                visit(dependency)
            elif state.get(dependency) == 1:
                start = stack.index(dependency)
                cycles.append(stack[start:] + [dependency])
        stack.pop()
        state[node] = 2

    for node in graph:
        if state.get(node, 0) == 0:
            visit(node)
    return cycles


def validate_effort(effort: Path) -> list[str]:
    errors: list[str] = []
    map_path = effort / "map.md"
    tickets_dir = effort / "tickets"

    if not map_path.is_file():
        errors.append(f"{map_path}: missing map")
    else:
        map_text = map_path.read_text(encoding="utf-8")
        phase = field(map_text, "Phase")
        status = field(map_text, "Status")
        assessment = field(map_text, "Assessment")
        publication_directory = field(map_text, "Publication directory")
        if phase not in PHASES:
            errors.append(f"{map_path}: invalid Phase '{phase}'")
        if status not in MAP_STATUSES:
            errors.append(f"{map_path}: invalid Status '{status}'")
        if assessment not in ASSESSMENTS:
            errors.append(f"{map_path}: invalid Assessment '{assessment}'")
        if publication_directory is None:
            errors.append(f"{map_path}: missing field 'Publication directory'")
        missing = MAP_HEADINGS - headings(map_text)
        for name in sorted(missing):
            errors.append(f"{map_path}: missing heading '## {name}'")
        if not substantive(section(map_text, "Standardization aim")):
            errors.append(f"{map_path}: Standardization aim must be substantive")
        validate_links(map_path, map_text, errors)

    if not tickets_dir.is_dir():
        errors.append(f"{tickets_dir}: missing tickets directory")
        return errors

    ticket_paths = sorted(tickets_dir.glob("*.md"))
    identities: dict[str, Path] = {}
    blockers_by_id: dict[str, list[str]] = {}
    statuses: dict[str, str] = {}

    for path in ticket_paths:
        match = TICKET_RE.match(path.name)
        if not match:
            errors.append(f"{path}: filename must be NN-<slug>.md")
            continue
        identity = match.group(1).zfill(2)
        if identity in identities:
            errors.append(f"{path}: duplicate ticket identity {identity}")
        identities[identity] = path

        text = path.read_text(encoding="utf-8")
        ticket_type = field(text, "Type")
        phase = field(text, "Phase")
        status = field(text, "Status")
        claimed_by = field(text, "Claimed by")
        blockers = parse_blockers(field(text, "Blocked by"), path, errors)
        blockers_by_id[identity] = blockers
        statuses[identity] = status or ""

        if ticket_type not in TYPES:
            errors.append(f"{path}: invalid Type '{ticket_type}'")
        if phase not in PHASES:
            errors.append(f"{path}: invalid Phase '{phase}'")
        if status not in TICKET_STATUSES:
            errors.append(f"{path}: invalid Status '{status}'")
        if claimed_by is None:
            errors.append(f"{path}: missing field 'Claimed by'")
        elif status == "claimed" and not claimed_by:
            errors.append(f"{path}: claimed ticket has no claimant")
        elif status == "open" and claimed_by:
            errors.append(f"{path}: open ticket must not have a claimant")

        if ticket_type in {"research", "decision"}:
            if not substantive(section(text, "Question")):
                errors.append(f"{path}: {ticket_type} ticket needs a substantive Question")
        elif ticket_type == "task":
            if not substantive(section(text, "Completion criterion")):
                errors.append(f"{path}: task ticket needs a substantive Completion criterion")

        if status == "resolved" and not substantive(section(text, "Resolution")):
            errors.append(f"{path}: resolved ticket needs a substantive Resolution")

        if ticket_type == "decision":
            decision_status = field(text, "Decision status")
            if decision_status not in DECISION_STATUSES:
                errors.append(f"{path}: invalid Decision status '{decision_status}'")
            elif status == "resolved" and decision_status == "pending":
                errors.append(f"{path}: resolved decision cannot remain pending")
            elif status != "resolved" and decision_status != "pending":
                errors.append(f"{path}: unresolved decision must remain pending")
            if decision_status == "superseded" and not field(text, "Superseded by"):
                errors.append(f"{path}: superseded decision needs 'Superseded by'")

        validate_links(path, text, errors)

    for identity, blockers in blockers_by_id.items():
        for blocker in blockers:
            if blocker == identity:
                errors.append(f"{identities[identity]}: ticket blocks itself")
            elif blocker not in identities:
                errors.append(f"{identities[identity]}: unknown blocker {blocker}")

    for cycle in find_cycles(blockers_by_id):
        errors.append(f"{tickets_dir}: blocking cycle: {' -> '.join(cycle)}")

    for identity, blockers in blockers_by_id.items():
        if statuses.get(identity) == "claimed":
            unresolved = [item for item in blockers if statuses.get(item) != "resolved"]
            if unresolved:
                errors.append(
                    f"{identities[identity]}: claimed while blocked by {', '.join(unresolved)}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a .standardization/<effort> Markdown tracker directory."
    )
    parser.add_argument("effort", type=Path, help="Path containing map.md and tickets/")
    args = parser.parse_args()

    effort = args.effort.expanduser().resolve()
    if not effort.is_dir():
        print(f"ERROR: effort directory does not exist: {effort}", file=sys.stderr)
        return 2

    errors = validate_effort(effort)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} error(s)", file=sys.stderr)
        return 1

    ticket_count = len(list((effort / "tickets").glob("*.md")))
    print(f"OK: {effort} ({ticket_count} ticket(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
