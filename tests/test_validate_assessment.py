from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "skills/standardize/scripts/validate_assessment.py"
SPEC = importlib.util.spec_from_file_location("validate_assessment", SCRIPT)
assert SPEC and SPEC.loader
validate_assessment = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_assessment)


FINAL_ASSESSMENT = """\
# Timeout revision assessment

Standard identity: request-timeout
Status: accepted
Baseline kind: standard release
Baseline artifact: v1.0/standard.md
Baseline version: 1.0
Baseline tag: not applicable
Assessment date: 2026-08-29
Outcome: baseline unchanged
Accepted by: Mahendri
Accepted on: 2026-08-29

## Question

Does the reported ambiguity require a standard change?

## Considered change items

The timeout report was resolved without changing normative content.

## Evidence and decisions

The existing examples consistently support the current interpretation.

## Conclusion

The baseline remains current; conflicting implementation evidence triggers another revision.
"""


class ValidateAssessmentTests(unittest.TestCase):
    def make_assessment(self, text: str) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        baseline = root / "v1.0/standard.md"
        baseline.parent.mkdir()
        baseline.write_text("# Standard\n", encoding="utf-8")
        path = root / "revision-assessment.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_final_assessment_is_valid(self) -> None:
        path = self.make_assessment(FINAL_ASSESSMENT)
        self.assertEqual(validate_assessment.validate_assessment(path, final=True), [])

    def test_final_assessment_requires_acceptance(self) -> None:
        path = self.make_assessment(
            FINAL_ASSESSMENT.replace("Status: accepted", "Status: candidate")
        )
        errors = validate_assessment.validate_assessment(path, final=True)
        self.assertTrue(any("must have Status 'accepted'" in error for error in errors))

    def test_final_assessment_rejects_pending_acceptance(self) -> None:
        path = self.make_assessment(
            FINAL_ASSESSMENT.replace("Accepted by: Mahendri", "Accepted by: pending")
        )
        errors = validate_assessment.validate_assessment(path, final=True)
        self.assertTrue(any("pending field 'Accepted by'" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
