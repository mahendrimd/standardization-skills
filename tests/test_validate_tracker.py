from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "skills/standardize/scripts/validate_tracker.py"
SPEC = importlib.util.spec_from_file_location("validate_tracker", SCRIPT)
assert SPEC and SPEC.loader
validate_tracker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_tracker)


CONFIG = """\
# Standardization configuration

Working directory: .standardization
Release storage: side-by-side
Initial version: 1.0
"""


LEGACY_MAP = """\
# Create a standard

Phase: discovery
Status: active
Assessment: pending
Publication directory: unresolved

## Standardization aim

Create one shared expectation.

## Notes

None.

## Decisions

None yet.

## Fog

None.

## Out of scope

None.

## Outputs

None yet.
"""


REVISION_MAP = """\
# Revise timeout behavior

Effort kind: revision
Phase: validation
Status: active
Assessment: standardize
Standard identity: request-timeout
Baseline kind: standard release
Baseline artifact: standards/request-timeout/v1.0/standard.md
Baseline version: 1.0
Baseline tag: not applicable
Candidate: accepted
Propagation: pending
Target version: 1.1
Outcome kind: successor release
Outcome artifact: pending
Publication directory: standards/request-timeout/v1.1

## Standardization aim

Resolve reported timeout ambiguity without invalidating conforming clients.

## Notes

None.

## Decisions

None.

## Change set

- [Clarify timeout](changes/01-clarify-timeout.md) — resolved.

## Fog

None.

## Out of scope

Changing transport protocols.

## Outputs

Candidate release.
"""


REASSESSMENT_MAP = """\
# Reassess timeout standardization

Effort kind: reassessment
Phase: validation
Status: complete
Assessment: defer
Standard identity: request-timeout
Baseline kind: accepted assessment
Baseline artifact: assessments/request-timeout-defer.md
Baseline version: not applicable
Baseline tag: not applicable
Candidate: not applicable
Propagation: not applicable
Target version: not applicable
Outcome kind: successor assessment
Outcome artifact: assessments/request-timeout.md
Publication directory: assessments/request-timeout.md

## Standardization aim

Reassess whether timeout behavior is stable enough to standardize.

## Notes

None.

## Decisions

None.

## Change set

- [Reassess stability](changes/01-clarify-timeout.md) — resolved.

## Fog

None.

## Out of scope

Transport protocol design.

## Outputs

Accepted successor assessment.
"""


RESOLVED_CHANGE = """\
# Clarify timeout

Status: resolved
Classification: minor
Grouping: single report
Grouping rationale: not applicable
Grouping confirmed by:
Grouping confirmed on:
Disposition confirmed by:
Disposition confirmed on:

## Source reports

- GitHub example/standard#41, observed 2026-08-29.

## Problem

Clients interpret the timeout boundary differently.

## Intended resolution

Define the inclusive boundary without invalidating existing conforming clients.

## Affected material

Timeout clause and its example.

## Tickets

None required.

## Disposition

Resolved by defining the inclusive boundary; all previous conforming clients remain conforming.
"""


class ValidateTrackerTests(unittest.TestCase):
    def make_effort(
        self,
        map_text: str,
        change_text: str | None = None,
        config_text: str = CONFIG,
        outcome_text: str | None = None,
    ) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        working = root / ".standardization"
        effort = working / "effort"
        effort.mkdir(parents=True)
        (working / "config.md").write_text(config_text, encoding="utf-8")
        (effort / "map.md").write_text(map_text, encoding="utf-8")
        (effort / "tickets").mkdir()
        baseline_value = validate_tracker.field(map_text, "Baseline artifact")
        if baseline_value and baseline_value != "not applicable":
            baseline_path = root / baseline_value
            baseline_path.parent.mkdir(parents=True, exist_ok=True)
            baseline_path.write_text("# Baseline\n", encoding="utf-8")
        if change_text is not None:
            (effort / "changes").mkdir()
            (effort / "changes/01-clarify-timeout.md").write_text(
                change_text, encoding="utf-8"
            )
        if "Candidate: accepted" in map_text:
            (effort / "candidate").mkdir()
            (effort / "candidate/release.md").write_text(
                "# Accepted release record\n\nStatus: released\nAcceptance status: accepted\n",
                encoding="utf-8",
            )
            (effort / "candidate/standard.md").write_text(
                "# Accepted standard\n", encoding="utf-8"
            )
        if outcome_text is not None:
            outcome_value = validate_tracker.field(map_text, "Outcome artifact")
            assert outcome_value
            outcome_path = root / outcome_value
            outcome_path.parent.mkdir(parents=True, exist_ok=True)
            outcome_path.write_text(outcome_text, encoding="utf-8")
        return effort

    def test_legacy_creation_map_remains_valid(self) -> None:
        effort = self.make_effort(LEGACY_MAP)
        self.assertEqual(validate_tracker.validate_effort(effort), [])

    def test_side_by_side_revision_without_tag_is_valid(self) -> None:
        effort = self.make_effort(REVISION_MAP, RESOLVED_CHANGE)
        self.assertEqual(validate_tracker.validate_effort(effort), [])

    def test_single_current_revision_requires_tag(self) -> None:
        config = CONFIG.replace("side-by-side", "single-current-tagged-history")
        effort = self.make_effort(REVISION_MAP, RESOLVED_CHANGE, config_text=config)
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("requires a Baseline tag" in error for error in errors))

    def test_second_active_candidate_for_same_standard_is_rejected(self) -> None:
        effort = self.make_effort(REVISION_MAP, RESOLVED_CHANGE)
        sibling = effort.parent / "other-effort"
        sibling.mkdir()
        (sibling / "map.md").write_text(REVISION_MAP, encoding="utf-8")
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("another active candidate" in error for error in errors))

    def test_accepted_candidate_rejects_open_change(self) -> None:
        change = RESOLVED_CHANGE.replace("Status: resolved", "Status: in progress")
        effort = self.make_effort(REVISION_MAP, change)
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("candidate accepted while change items remain open" in e for e in errors))

    def test_revision_requires_identifiable_baseline_version(self) -> None:
        map_text = REVISION_MAP.replace("Baseline version: 1.0", "Baseline version: pending")
        effort = self.make_effort(map_text, RESOLVED_CHANGE)
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("Baseline version must identify" in e for e in errors))

    def test_maintenance_requires_existing_baseline_artifact(self) -> None:
        map_text = REVISION_MAP.replace(
            "Baseline artifact: standards/request-timeout/v1.0/standard.md",
            "Baseline artifact: standards/request-timeout/v1.0/missing.md",
        )
        effort = self.make_effort(map_text, RESOLVED_CHANGE)
        (effort.parents[1] / "standards/request-timeout/v1.0/missing.md").unlink()
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("Baseline artifact does not exist" in e for e in errors))

    def test_completed_release_requires_completed_propagation(self) -> None:
        map_text = REVISION_MAP.replace("Status: active", "Status: complete").replace(
            "Outcome artifact: pending", "Outcome artifact: standards/request-timeout/v1.1/standard.md"
        )
        effort = self.make_effort(map_text, RESOLVED_CHANGE, outcome_text="# Standard\n")
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("needs Propagation complete" in e for e in errors))

    def test_no_change_outcome_cannot_accept_successor_release(self) -> None:
        change = RESOLVED_CHANGE.replace("Classification: minor", "Classification: no release change")
        effort = self.make_effort(REVISION_MAP, change)
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("publish a revision assessment instead" in e for e in errors))

    def test_accepted_candidate_requires_candidate_directory(self) -> None:
        effort = self.make_effort(REVISION_MAP, RESOLVED_CHANGE)
        for path in (effort / "candidate").iterdir():
            path.unlink()
        (effort / "candidate").rmdir()
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("accepted candidate directory is missing" in e for e in errors))

    def test_terminal_change_requires_disposition(self) -> None:
        change = RESOLVED_CHANGE.replace(
            "Resolved by defining the inclusive boundary; all previous conforming clients remain conforming.",
            "<!-- pending -->",
        )
        effort = self.make_effort(REVISION_MAP, change)
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("terminal change needs a substantive Disposition" in e for e in errors))

    def test_deferred_change_requires_user_confirmation(self) -> None:
        change = RESOLVED_CHANGE.replace("Status: resolved", "Status: deferred")
        effort = self.make_effort(REVISION_MAP, change)
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("needs 'Disposition confirmed by'" in e for e in errors))

    def test_duplicate_grouping_requires_confirmation(self) -> None:
        change = RESOLVED_CHANGE.replace("Grouping: single report", "Grouping: confirmed duplicates")
        effort = self.make_effort(REVISION_MAP, change)
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("duplicate grouping needs" in e for e in errors))

    def test_completed_successor_assessment_is_valid(self) -> None:
        change = RESOLVED_CHANGE.replace("Classification: minor", "Classification: no release change")
        effort = self.make_effort(
            REASSESSMENT_MAP,
            change,
            outcome_text=(
                "# Assessment\n\nStatus: accepted\nAccepted by: Mahendri\n"
                "Accepted on: 2026-08-29\n"
            ),
        )
        self.assertEqual(validate_tracker.validate_effort(effort), [])

    def test_completed_assessment_requires_outcome_artifact(self) -> None:
        effort = self.make_effort(
            REASSESSMENT_MAP,
            RESOLVED_CHANGE.replace("Classification: minor", "Classification: no release change"),
        )
        errors = validate_tracker.validate_effort(effort)
        self.assertTrue(any("Outcome artifact does not exist" in e for e in errors))

    def test_first_standard_uses_configured_initial_version(self) -> None:
        map_text = REASSESSMENT_MAP.replace("Status: complete", "Status: active")
        map_text = map_text.replace("Candidate: not applicable", "Candidate: accepted")
        map_text = map_text.replace("Target version: not applicable", "Target version: 1.0")
        map_text = map_text.replace("Outcome kind: successor assessment", "Outcome kind: first standard")
        map_text = map_text.replace("Outcome artifact: assessments/request-timeout.md", "Outcome artifact: pending")
        effort = self.make_effort(
            map_text,
            RESOLVED_CHANGE.replace("Classification: minor", "Classification: no release change"),
        )
        self.assertEqual(validate_tracker.validate_effort(effort), [])


if __name__ == "__main__":
    unittest.main()
