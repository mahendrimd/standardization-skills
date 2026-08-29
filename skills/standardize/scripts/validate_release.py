#!/usr/bin/env python3
"""Validate a Standardization Skills release record."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FIELDS = {
    "Standard identity",
    "Version",
    "Status",
    "Release date",
    "Predecessor version",
    "Predecessor tag",
    "History locator",
    "Release tag",
    "Version policy",
    "Minimum classification",
    "Confirmed increment",
    "Publication directory",
    "Acceptance status",
    "Propagation status",
}
REQUIRED_HEADINGS = {
    "Summary",
    "Change items",
    "Compatibility and migration",
    "Current decisions and evidence",
    "Validation and acceptance",
    "Publication and propagation",
    "Notifications",
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


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
        if not (path.parent / target).resolve().exists():
            errors.append(f"{path}: broken relative link: {raw_target}")


def validate_release(
    bundle: Path, accepted: bool = False, final: bool = False
) -> list[str]:
    errors: list[str] = []
    path = bundle / "release.md"
    if not path.is_file():
        return [f"{path}: missing release record"]

    text = path.read_text(encoding="utf-8")
    for name in sorted(REQUIRED_FIELDS):
        value = field(text, name)
        if not value:
            errors.append(f"{path}: missing field '{name}'")
        elif re.fullmatch(r"<.*>", value, re.DOTALL):
            errors.append(f"{path}: unresolved field '{name}'")

    missing = REQUIRED_HEADINGS - headings(text)
    for name in sorted(missing):
        errors.append(f"{path}: missing heading '## {name}'")
    for name in sorted(REQUIRED_HEADINGS):
        if name in headings(text) and not substantive(section(text, name)):
            errors.append(f"{path}: {name} must be substantive")

    status = field(text, "Status")
    acceptance_status = field(text, "Acceptance status")
    propagation_status = field(text, "Propagation status")
    history_locator = field(text, "History locator")
    release_tag = field(text, "Release tag")
    if status not in {"candidate", "released"}:
        errors.append(f"{path}: invalid Status '{status}'")
    if acceptance_status not in {"pending", "accepted"}:
        errors.append(f"{path}: invalid Acceptance status '{acceptance_status}'")
    if propagation_status not in {"pending", "blocked", "complete", "not applicable"}:
        errors.append(f"{path}: invalid Propagation status '{propagation_status}'")
    if release_tag in {"none", "not applicable"} and history_locator != "not applicable":
        errors.append(f"{path}: untagged release needs History locator 'not applicable'")
    if release_tag not in {None, "pending", "none", "not applicable"}:
        if history_locator != release_tag:
            errors.append(f"{path}: History locator must equal the exact Release tag")

    if accepted or final:
        if status != "released":
            errors.append(f"{path}: accepted release must have Status 'released'")
        if acceptance_status != "accepted":
            errors.append(f"{path}: accepted release needs Acceptance status 'accepted'")
        for name in ("Version", "Release date", "History locator", "Release tag"):
            value = field(text, name)
            if value and value.lower() == "pending":
                errors.append(f"{path}: accepted release has pending field '{name}'")
        without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        unresolved = re.findall(r"<[^>\n]+>", without_comments)
        if unresolved:
            errors.append(
                f"{path}: accepted release has unresolved placeholders: "
                f"{', '.join(sorted(set(unresolved)))}"
            )
    if final and propagation_status not in {"complete", "not applicable"}:
        errors.append(f"{path}: final release needs completed or inapplicable propagation")

    validate_links(path, text, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a release directory containing release.md."
    )
    parser.add_argument("bundle", type=Path, help="Canonical or candidate release directory")
    parser.add_argument(
        "--accepted", action="store_true", help="Require an exact user-accepted bundle"
    )
    parser.add_argument(
        "--final", action="store_true", help="Require finalized release metadata"
    )
    args = parser.parse_args()

    bundle = args.bundle.expanduser().resolve()
    if not bundle.is_dir():
        print(f"ERROR: release directory does not exist: {bundle}", file=sys.stderr)
        return 2

    errors = validate_release(bundle, accepted=args.accepted, final=args.final)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} error(s)", file=sys.stderr)
        return 1

    if args.final:
        state = "final release"
    elif args.accepted:
        state = "accepted bundle"
    else:
        state = "release candidate"
    print(f"OK: {bundle} ({state})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
