import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Local"))

from gemini_config import (  # noqa: E402
    DEFAULT_MODEL,
    GeminiConfigurationError,
    get_gemini_settings,
)


class GeminiSettingsTests(unittest.TestCase):
    def test_prefers_gemini_api_key_over_legacy_key(self):
        settings = get_gemini_settings(
            {
                "GEMINI_API_KEY": "preferred-key",
                "GOOGLE_API_KEY": "legacy-key",
                "GREENOPS_GEMINI_MODEL": "gemini-2.5-flash",
                "GREENOPS_GEMINI_PROJECT_LABEL": "Project HarmonyFarms",
            }
        )

        self.assertEqual(settings.api_key, "preferred-key")
        self.assertEqual(settings.model, "gemini-2.5-flash")
        self.assertEqual(settings.project_label, "Project HarmonyFarms")

    def test_uses_legacy_key_only_when_preferred_key_is_absent(self):
        settings = get_gemini_settings({"GOOGLE_API_KEY": "legacy-key"})

        self.assertEqual(settings.api_key, "legacy-key")
        self.assertEqual(settings.model, DEFAULT_MODEL)
        self.assertIsNone(settings.project_label)

    def test_rejects_missing_key_without_logging_a_secret(self):
        with self.assertRaisesRegex(GeminiConfigurationError, "GEMINI_API_KEY"):
            get_gemini_settings({})

    def test_rejects_key_whitespace(self):
        with self.assertRaisesRegex(GeminiConfigurationError, "whitespace"):
            get_gemini_settings({"GEMINI_API_KEY": " key-with-space "})

    def test_rejects_invalid_model_identifier(self):
        with self.assertRaisesRegex(GeminiConfigurationError, "model identifier"):
            get_gemini_settings(
                {"GEMINI_API_KEY": "key", "GREENOPS_GEMINI_MODEL": "gemini model"}
            )


if __name__ == "__main__":
    unittest.main()
