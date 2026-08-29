#!/usr/bin/env python3
"""Validate a Standardization Skills local Markdown effort."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


PHASES = {"discovery", "assessment", "resolution", "synthesis", "validation"}
EFFORT_KINDS = {"creation", "revision", "reassessment"}
BASELINE_KINDS = {"not applicable", "standard release", "accepted assessment"}
OUTCOME_KINDS = {
    "not applicable",
    "pending",
    "successor release",
    "revision assessment",
    "successor assessment",
    "first standard",
}
RELEASE_OUTCOMES = {"successor release", "first standard"}
ASSESSMENT_OUTCOMES = {"revision assessment", "successor assessment"}
TYPES = {"research", "decision", "task"}
TICKET_STATUSES = {"open", "claimed", "resolved"}
MAP_STATUSES = {"active", "complete"}
ASSESSMENTS = {"pending", "standardize", "standardize a subset", "defer", "decline"}
DECISION_STATUSES = {"pending", "active", "superseded"}
CANDIDATE_STATES = {"not applicable", "not started", "drafting", "accepted"}
PROPAGATION_STATES = {"not applicable", "pending", "blocked", "complete"}
CHANGE_STATUSES = {"proposed", "accepted", "in progress", "resolved", "deferred", "rejected"}
TERMINAL_CHANGE_STATUSES = {"resolved", "deferred", "rejected"}
CHANGE_CLASSIFICATIONS = {"pending", "no release change", "patch", "minor", "major"}
GROUPINGS = {"single report", "confirmed duplicates"}
MAP_HEADINGS = {
    "Standardization aim",
    "Notes",
    "Decisions",
    "Fog",
    "Out of scope",
    "Outputs",
}
CHANGE_HEADINGS = {
    "Source reports",
    "Problem",
    "Intended resolution",
    "Affected material",
    "Tickets",
    "Disposition",
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


def substantive_field(value: str | None) -> bool:
    return bool(value and not re.fullmatch(r"<.*>", value, re.DOTALL))


def repository_root(effort: Path, config_text: str) -> Path:
    working_directory = field(config_text, "Working directory")
    if not working_directory:
        return effort.parent
    root = effort.parent
    for _ in Path(working_directory).parts:
        root = root.parent
    return root


def repository_path(root: Path, value: str) -> Path | None:
    resolved_root = root.resolve()
    resolved = (resolved_root / value).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return None
    return resolved


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
    changes_dir = effort / "changes"
    config_path = effort.parent / "config.md"
    config_text = config_path.read_text(encoding="utf-8") if config_path.is_file() else ""
    release_storage = field(config_text, "Release storage")
    initial_version = field(config_text, "Initial version")
    repo_root = repository_root(effort, config_text)
    effort_kind = "creation"
    baseline_kind = "not applicable"
    baseline_artifact = "not applicable"
    candidate = "not applicable"
    propagation = "not applicable"
    target_version = "not applicable"
    outcome_kind = "not applicable"
    outcome_artifact = "not applicable"
    map_status = ""
    standard_identity = ""

    if not map_path.is_file():
        errors.append(f"{map_path}: missing map")
    else:
        map_text = map_path.read_text(encoding="utf-8")
        phase = field(map_text, "Phase")
        status = field(map_text, "Status")
        map_status = status or ""
        assessment = field(map_text, "Assessment")
        publication_directory = field(map_text, "Publication directory")
        standard_identity = field(map_text, "Standard identity") or ""
        declared_effort_kind = field(map_text, "Effort kind")
        effort_kind = declared_effort_kind or "creation"
        baseline_kind = field(map_text, "Baseline kind") or "not applicable"
        baseline_artifact = field(map_text, "Baseline artifact") or "not applicable"
        candidate = field(map_text, "Candidate") or "not applicable"
        propagation = field(map_text, "Propagation") or "not applicable"
        target_version = field(map_text, "Target version") or "not applicable"
        outcome_kind = field(map_text, "Outcome kind") or "not applicable"
        outcome_artifact = field(map_text, "Outcome artifact") or "not applicable"
        if effort_kind not in EFFORT_KINDS:
            errors.append(f"{map_path}: invalid Effort kind '{effort_kind}'")
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

        if declared_effort_kind is not None:
            if not substantive_field(field(map_text, "Standard identity")):
                errors.append(f"{map_path}: Standard identity must be substantive")
            if baseline_kind not in BASELINE_KINDS:
                errors.append(f"{map_path}: invalid Baseline kind '{baseline_kind}'")
            if not substantive_field(baseline_artifact):
                errors.append(f"{map_path}: Baseline artifact must be substantive")
            if candidate not in CANDIDATE_STATES:
                errors.append(f"{map_path}: invalid Candidate '{candidate}'")
            if propagation not in PROPAGATION_STATES:
                errors.append(f"{map_path}: invalid Propagation '{propagation}'")
            if not substantive_field(target_version):
                errors.append(f"{map_path}: Target version must be substantive")
            if outcome_kind not in OUTCOME_KINDS:
                errors.append(f"{map_path}: invalid Outcome kind '{outcome_kind}'")
            if not substantive_field(outcome_artifact):
                errors.append(f"{map_path}: Outcome artifact must be substantive")

        if effort_kind in {"revision", "reassessment"}:
            baseline_version = field(map_text, "Baseline version")
            baseline_tag = field(map_text, "Baseline tag")
            if baseline_artifact in {"pending", "not applicable"}:
                errors.append(f"{map_path}: maintenance effort needs a Baseline artifact")
            else:
                baseline_path = repository_path(repo_root, baseline_artifact)
                if baseline_path is None:
                    errors.append(
                        f"{map_path}: Baseline artifact must stay inside the repository"
                    )
                elif not baseline_path.is_file():
                    errors.append(
                        f"{map_path}: Baseline artifact does not exist: {baseline_artifact}"
                    )
            if effort_kind == "revision":
                if baseline_kind != "standard release":
                    errors.append(f"{map_path}: revision needs Baseline kind 'standard release'")
                if not substantive_field(baseline_version) or baseline_version in {
                    "pending",
                    "not applicable",
                }:
                    errors.append(f"{map_path}: Baseline version must identify the release")
                if outcome_kind not in {
                    "pending",
                    "successor release",
                    "revision assessment",
                }:
                    errors.append(
                        f"{map_path}: revision cannot produce Outcome kind '{outcome_kind}'"
                    )
            else:
                if baseline_kind != "accepted assessment":
                    errors.append(
                        f"{map_path}: reassessment needs Baseline kind 'accepted assessment'"
                    )
                if not substantive_field(baseline_version) or baseline_version == "pending":
                    errors.append(
                        f"{map_path}: Baseline version must be a version or 'not applicable'"
                    )
                if outcome_kind not in {"pending", "successor assessment", "first standard"}:
                    errors.append(
                        f"{map_path}: reassessment cannot produce Outcome kind '{outcome_kind}'"
                    )
            if not substantive_field(baseline_tag) or baseline_tag == "pending":
                errors.append(f"{map_path}: Baseline tag must be a tag or 'not applicable'")
            if release_storage == "single-current-tagged-history" and (
                effort_kind == "revision" and baseline_tag == "not applicable"
            ):
                errors.append(
                    f"{map_path}: single-current-tagged-history requires a Baseline tag"
                )
            if "Change set" not in headings(map_text):
                errors.append(f"{map_path}: missing heading '## Change set'")
            if outcome_kind in RELEASE_OUTCOMES and candidate == "not applicable":
                errors.append(f"{map_path}: release outcome needs candidate state")
            if outcome_kind in ASSESSMENT_OUTCOMES:
                if candidate != "not applicable":
                    errors.append(
                        f"{map_path}: assessment outcome needs Candidate 'not applicable'"
                    )
                if propagation != "not applicable":
                    errors.append(
                        f"{map_path}: assessment outcome needs Propagation 'not applicable'"
                    )
                if target_version != "not applicable":
                    errors.append(
                        f"{map_path}: assessment outcome needs Target version 'not applicable'"
                    )
            if outcome_kind == "first standard" and initial_version:
                if target_version not in {"pending", initial_version}:
                    errors.append(
                        f"{map_path}: first standard Target version must be configured Initial version "
                        f"'{initial_version}'"
                    )
        validate_links(map_path, map_text, errors)

    if standard_identity and candidate in {"drafting", "accepted"}:
        for sibling in sorted(effort.parent.iterdir()):
            sibling_map = sibling / "map.md"
            if sibling == effort or not sibling_map.is_file():
                continue
            sibling_text = sibling_map.read_text(encoding="utf-8")
            if (
                field(sibling_text, "Status") == "active"
                and field(sibling_text, "Standard identity") == standard_identity
                and field(sibling_text, "Candidate") in {"drafting", "accepted"}
            ):
                errors.append(
                    f"{map_path}: another active candidate for '{standard_identity}' exists at "
                    f"{sibling_map}"
                )

    change_statuses: dict[str, str] = {}
    change_classifications: dict[str, str] = {}
    if effort_kind in {"revision", "reassessment"}:
        if not changes_dir.is_dir():
            errors.append(f"{changes_dir}: missing changes directory")
        else:
            for path in sorted(changes_dir.glob("*.md")):
                match = TICKET_RE.match(path.name)
                if not match:
                    errors.append(f"{path}: filename must be NN-<slug>.md")
                    continue
                identity = match.group(1).zfill(2)
                if identity in change_statuses:
                    errors.append(f"{path}: duplicate change identity {identity}")

                text = path.read_text(encoding="utf-8")
                change_status = field(text, "Status")
                classification = field(text, "Classification")
                grouping = field(text, "Grouping")
                change_statuses[identity] = change_status or ""
                change_classifications[identity] = classification or ""
                if change_status not in CHANGE_STATUSES:
                    errors.append(f"{path}: invalid Status '{change_status}'")
                if classification not in CHANGE_CLASSIFICATIONS:
                    errors.append(f"{path}: invalid Classification '{classification}'")
                if grouping not in GROUPINGS:
                    errors.append(f"{path}: invalid Grouping '{grouping}'")
                if grouping == "confirmed duplicates":
                    grouping_rationale = field(text, "Grouping rationale")
                    if (
                        not substantive_field(grouping_rationale)
                        or grouping_rationale == "not applicable"
                    ):
                        errors.append(f"{path}: duplicate grouping needs a substantive rationale")
                    for name in ("Grouping confirmed by", "Grouping confirmed on"):
                        if not substantive_field(field(text, name)):
                            errors.append(f"{path}: duplicate grouping needs '{name}'")

                missing = CHANGE_HEADINGS - headings(text)
                for name in sorted(missing):
                    errors.append(f"{path}: missing heading '## {name}'")
                for name in ("Source reports", "Problem"):
                    if not substantive(section(text, name)):
                        errors.append(f"{path}: {name} must be substantive")
                if change_status in {"accepted", "in progress", "resolved"} and not substantive(
                    section(text, "Intended resolution")
                ):
                    errors.append(f"{path}: Intended resolution must be substantive")
                if change_status in TERMINAL_CHANGE_STATUSES:
                    if classification == "pending":
                        errors.append(f"{path}: terminal change needs a final Classification")
                    if not substantive(section(text, "Disposition")):
                        errors.append(f"{path}: terminal change needs a substantive Disposition")
                if change_status in {"deferred", "rejected"}:
                    for name in ("Disposition confirmed by", "Disposition confirmed on"):
                        if not substantive_field(field(text, name)):
                            errors.append(f"{path}: {change_status} change needs '{name}'")
                if change_status == "resolved" and not substantive(section(text, "Affected material")):
                    errors.append(f"{path}: resolved change needs substantive Affected material")
                validate_links(path, text, errors)

            if not change_statuses:
                errors.append(f"{changes_dir}: revision or reassessment needs at least one change item")

        open_changes = [
            identity
            for identity, status in change_statuses.items()
            if status not in TERMINAL_CHANGE_STATUSES
        ]
        release_changes = [
            identity
            for identity, status in change_statuses.items()
            if status == "resolved"
            and change_classifications.get(identity) in {"patch", "minor", "major"}
        ]
        if candidate == "accepted" and outcome_kind not in RELEASE_OUTCOMES:
            errors.append(f"{map_path}: accepted candidate needs a standard-release outcome")
        if candidate == "accepted" and open_changes:
            errors.append(
                f"{map_path}: candidate accepted while change items remain open: "
                f"{', '.join(open_changes)}"
            )
        if (
            outcome_kind in RELEASE_OUTCOMES
            and target_version not in {"pending", "not applicable"}
            and open_changes
        ):
            errors.append(
                f"{map_path}: target version confirmed while change items remain open: "
                f"{', '.join(open_changes)}"
            )
        if candidate == "accepted" and target_version in {"pending", "not applicable"}:
            errors.append(f"{map_path}: accepted candidate needs a confirmed Target version")
        if candidate == "accepted":
            candidate_dir = effort / "candidate"
            if not candidate_dir.is_dir():
                errors.append(f"{candidate_dir}: accepted candidate directory is missing")
            else:
                release_path = candidate_dir / "release.md"
                if not release_path.is_file():
                    errors.append(f"{release_path}: accepted candidate release record is missing")
                else:
                    release_text = release_path.read_text(encoding="utf-8")
                    if field(release_text, "Status") != "released":
                        errors.append(
                            f"{release_path}: accepted candidate release must have Status 'released'"
                        )
                    if field(release_text, "Acceptance status") != "accepted":
                        errors.append(
                            f"{release_path}: accepted candidate needs Acceptance status 'accepted'"
                        )
                artifacts = [
                    path
                    for path in candidate_dir.rglob("*")
                    if path.is_file() and path != release_path
                ]
                if not artifacts:
                    errors.append(
                        f"{candidate_dir}: accepted candidate needs a standard artifact"
                    )
        if (
            outcome_kind == "successor release"
            and candidate == "accepted"
            and not release_changes
        ):
            errors.append(
                f"{map_path}: candidate accepted without a resolved standard change; "
                "publish a revision assessment instead"
            )
        if (
            outcome_kind == "successor release"
            and target_version not in {"pending", "not applicable"}
            and not release_changes
        ):
            errors.append(
                f"{map_path}: target version confirmed without a resolved standard change"
            )
        if outcome_kind == "revision assessment" and release_changes:
            errors.append(
                f"{map_path}: revision assessment cannot contain a resolved standard change"
            )
        if map_status == "complete":
            if outcome_kind in {"pending", "not applicable"}:
                errors.append(
                    f"{map_path}: completed maintenance effort needs a final Outcome kind"
                )
            if outcome_artifact in {"pending", "not applicable"}:
                errors.append(f"{map_path}: completed effort needs an Outcome artifact")
            else:
                artifact_path = repository_path(repo_root, outcome_artifact)
                if artifact_path is None:
                    errors.append(
                        f"{map_path}: Outcome artifact must stay inside the repository"
                    )
                elif not artifact_path.is_file():
                    errors.append(
                        f"{map_path}: Outcome artifact does not exist: {outcome_artifact}"
                    )
                elif outcome_kind in ASSESSMENT_OUTCOMES:
                    artifact_text = artifact_path.read_text(encoding="utf-8")
                    if field(artifact_text, "Status") != "accepted":
                        errors.append(
                            f"{artifact_path}: completed assessment outcome must be accepted"
                        )
                    for name in ("Accepted by", "Accepted on"):
                        value = field(artifact_text, name)
                        if not substantive_field(value) or value == "pending":
                            errors.append(
                                f"{artifact_path}: completed assessment needs final '{name}'"
                            )
            if outcome_kind in RELEASE_OUTCOMES and candidate != "accepted":
                errors.append(
                    f"{map_path}: completed release outcome needs Candidate 'accepted'"
                )
            if outcome_kind in RELEASE_OUTCOMES and propagation not in {
                "complete",
                "not applicable",
            }:
                errors.append(
                    f"{map_path}: completed release outcome needs Propagation complete "
                    "or not applicable"
                )
            if outcome_kind in ASSESSMENT_OUTCOMES and propagation != "not applicable":
                errors.append(
                    f"{map_path}: completed assessment outcome needs Propagation 'not applicable'"
                )

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
