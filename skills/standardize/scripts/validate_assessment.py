#!/usr/bin/env python3
"""Validate a maintenance assessment artifact."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FIELDS = {
    "Standard identity",
    "Status",
    "Baseline kind",
    "Baseline artifact",
    "Baseline version",
    "Baseline tag",
    "Assessment date",
    "Outcome",
    "Accepted by",
    "Accepted on",
}
REQUIRED_HEADINGS = {
    "Question",
    "Considered change items",
    "Evidence and decisions",
    "Conclusion",
}
BASELINE_KINDS = {"standard release", "accepted assessment"}
OUTCOMES = {"baseline unchanged", "successor assessment"}
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


def validate_assessment(path: Path, final: bool = False) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"{path}: missing maintenance assessment"]

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
    baseline_kind = field(text, "Baseline kind")
    outcome = field(text, "Outcome")
    if status not in {"candidate", "accepted"}:
        errors.append(f"{path}: invalid Status '{status}'")
    if baseline_kind not in BASELINE_KINDS:
        errors.append(f"{path}: invalid Baseline kind '{baseline_kind}'")
    if outcome not in OUTCOMES:
        errors.append(f"{path}: invalid Outcome '{outcome}'")

    if final:
        if status != "accepted":
            errors.append(f"{path}: final assessment must have Status 'accepted'")
        for name in ("Assessment date", "Accepted by", "Accepted on"):
            value = field(text, name)
            if value and value.lower() == "pending":
                errors.append(f"{path}: final assessment has pending field '{name}'")
        without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        unresolved = re.findall(r"<[^>\n]+>", without_comments)
        if unresolved:
            errors.append(
                f"{path}: final assessment has unresolved placeholders: "
                f"{', '.join(sorted(set(unresolved)))}"
            )

    validate_links(path, text, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a maintenance assessment Markdown file."
    )
    parser.add_argument("assessment", type=Path, help="Path to the assessment Markdown file")
    parser.add_argument(
        "--final", action="store_true", help="Require accepted final assessment metadata"
    )
    args = parser.parse_args()

    path = args.assessment.expanduser().resolve()
    errors = validate_assessment(path, final=args.final)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} error(s)", file=sys.stderr)
        return 1

    state = "final assessment" if args.final else "assessment candidate"
    print(f"OK: {path} ({state})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
