from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "skills/standardize/scripts/validate_release.py"
SPEC = importlib.util.spec_from_file_location("validate_release", SCRIPT)
assert SPEC and SPEC.loader
validate_release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_release)


FINAL_RELEASE = """\
# Request timeout 1.1

Standard identity: request-timeout
Version: 1.1
Status: released
Release date: 2026-08-29
Predecessor version: 1.0
Predecessor tag: request-timeout-v1.0
History locator: request-timeout-v1.1
Release tag: request-timeout-v1.1
Version policy: standard-versioning
Minimum classification: minor
Confirmed increment: minor
Publication directory: standards/request-timeout/v1.1
Acceptance status: accepted
Propagation status: complete

## Summary

Clarifies the timeout boundary.

## Change items

C01 resolves the reported ambiguity.

## Compatibility and migration

All previously conforming clients remain conforming.

## Current decisions and evidence

The timeout decision and evidence index are retained beside this record.

## Validation and acceptance

Traceability and compatibility checks passed; the user accepted the candidate.

## Publication and propagation

The current site page displays version 1.1 and was verified.

## Notifications

None configured.
"""


class ValidateReleaseTests(unittest.TestCase):
    def make_bundle(self, release_text: str) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        bundle = Path(temp.name)
        (bundle / "release.md").write_text(release_text, encoding="utf-8")
        return bundle

    def test_final_release_is_valid(self) -> None:
        bundle = self.make_bundle(FINAL_RELEASE)
        self.assertEqual(validate_release.validate_release(bundle, final=True), [])

    def test_accepted_release_can_have_pending_propagation(self) -> None:
        release = FINAL_RELEASE.replace("Propagation status: complete", "Propagation status: pending")
        bundle = self.make_bundle(release)
        self.assertEqual(validate_release.validate_release(bundle, accepted=True), [])

    def test_final_release_rejects_pending_propagation(self) -> None:
        release = FINAL_RELEASE.replace("Propagation status: complete", "Propagation status: pending")
        bundle = self.make_bundle(release)
        errors = validate_release.validate_release(bundle, final=True)
        self.assertTrue(any("needs completed" in error for error in errors))

    def test_final_release_rejects_pending_tag(self) -> None:
        release = FINAL_RELEASE.replace(
            "Release tag: request-timeout-v1.1", "Release tag: pending"
        )
        bundle = self.make_bundle(release)
        errors = validate_release.validate_release(bundle, final=True)
        self.assertTrue(any("pending field 'Release tag'" in error for error in errors))

    def test_final_release_rejects_section_placeholder(self) -> None:
        release = FINAL_RELEASE.replace(
            "Clarifies the timeout boundary.", "<What this release changes.>"
        )
        bundle = self.make_bundle(release)
        errors = validate_release.validate_release(bundle, final=True)
        self.assertTrue(any("unresolved placeholders" in error for error in errors))

    def test_untagged_release_uses_not_applicable_history_locator(self) -> None:
        release = FINAL_RELEASE.replace(
            "History locator: request-timeout-v1.1", "History locator: not applicable"
        ).replace("Release tag: request-timeout-v1.1", "Release tag: none")
        bundle = self.make_bundle(release)
        self.assertEqual(validate_release.validate_release(bundle, final=True), [])


if __name__ == "__main__":
    unittest.main()
