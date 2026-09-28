"""Secret-safe Gemini runtime configuration for GreenOps local execution."""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from dataclasses import dataclass

DEFAULT_MODEL = "gemini-2.5-flash"
_MODEL_PATTERN = re.compile(r"^[A-Za-z0-9._/-]+$")


class GeminiConfigurationError(ValueError):
    """Raised when runtime Gemini settings are missing or malformed."""


@dataclass(frozen=True)
class GeminiSettings:
    """Non-persisted runtime settings; callers must never log ``api_key``."""

    api_key: str
    model: str
    project_label: str | None


def get_gemini_settings(environ: Mapping[str, str] | None = None) -> GeminiSettings:
    """Load Gemini settings with a deterministic, secret-safe precedence order.

    ``GEMINI_API_KEY`` takes precedence over the legacy ``GOOGLE_API_KEY``.
    This function deliberately validates shape only and never calls the provider,
    prints a credential, or persists it to disk.
    """

    env = os.environ if environ is None else environ
    raw_key = env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY")
    if not raw_key:
        raise GeminiConfigurationError(
            "Set GEMINI_API_KEY in the secure runtime environment; do not paste it into source files."
        )

    api_key = raw_key.strip()
    if api_key != raw_key or not api_key:
        raise GeminiConfigurationError("The Gemini API key is blank or contains leading/trailing whitespace.")
    if any(char.isspace() for char in api_key):
        raise GeminiConfigurationError("The Gemini API key must not contain whitespace.")

    model = (env.get("GREENOPS_GEMINI_MODEL") or DEFAULT_MODEL).strip()
    if not model or not _MODEL_PATTERN.fullmatch(model):
        raise GeminiConfigurationError(
            "GREENOPS_GEMINI_MODEL must be a provider model identifier without whitespace."
        )

    project_label = (env.get("GREENOPS_GEMINI_PROJECT_LABEL") or "").strip() or None
    return GeminiSettings(api_key=api_key, model=model, project_label=project_label)
