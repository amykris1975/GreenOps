import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Local"))

from deterministic_controls import evaluate_carbon_gate  # noqa: E402


class CarbonGateTests(unittest.TestCase):
    def test_clean_grid_allows_work(self):
        decision = evaluate_carbon_gate("low", 75)
        self.assertTrue(decision.should_run)
        self.assertEqual(decision.reason, "clean_grid_index")
        self.assertFalse(decision.emergency_override)

    def test_non_clean_grid_fails_closed(self):
        decision = evaluate_carbon_gate("moderate", 230)
        self.assertFalse(decision.should_run)
        self.assertEqual(decision.reason, "carbon_index_not_clean")

    def test_invalid_measurement_fails_closed(self):
        decision = evaluate_carbon_gate("low", "not-a-number")
        self.assertFalse(decision.should_run)
        self.assertEqual(decision.reason, "invalid_carbon_measurement")

    def test_override_requires_attestation(self):
        decision = evaluate_carbon_gate(
            "high", 400, emergency_override=True, emergency_justification="Critical production recovery"
        )
        self.assertFalse(decision.should_run)
        self.assertEqual(decision.reason, "override_requires_systems_check")

    def test_override_requires_specific_justification(self):
        decision = evaluate_carbon_gate(
            "high", 400, emergency_override=True, systems_check_attested=True, emergency_justification="urgent"
        )
        self.assertFalse(decision.should_run)
        self.assertEqual(decision.reason, "override_requires_specific_justification")

    def test_authorized_override_is_explicit(self):
        decision = evaluate_carbon_gate(
            "high",
            400,
            emergency_override=True,
            systems_check_attested=True,
            emergency_justification="Critical production recovery required before the maintenance window closes.",
        )
        self.assertTrue(decision.should_run)
        self.assertTrue(decision.emergency_override)
        self.assertEqual(decision.reason, "emergency_override_authorized")

    def test_static_validator_passes(self):
        completed = subprocess.run(
            [sys.executable, "tools/validate_deterministic_controls.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Validated", completed.stdout)


if __name__ == "__main__":
    unittest.main()
