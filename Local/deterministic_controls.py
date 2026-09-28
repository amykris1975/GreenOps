"""Deterministic control functions used around GreenOps AI recommendations."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

CLEAN_GRID_INDICES = frozenset({"very low", "low"})
MIN_OVERRIDE_JUSTIFICATION_LENGTH = 20


@dataclass(frozen=True)
class CarbonGateDecision:
    """A reproducible release decision independent of any model response."""

    should_run: bool
    reason: str
    index: str
    intensity: float | None
    emergency_override: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_carbon_gate(
    index: object,
    intensity: object,
    *,
    emergency_override: bool = False,
    systems_check_attested: bool = False,
    emergency_justification: str = "",
) -> CarbonGateDecision:
    """Return a fail-closed carbon decision from explicit, testable inputs.

    AI agents may explain this decision, but they may not change its result. An
    emergency override is allowed only with a systems-check attestation and a
    minimally specific human justification; identity verification belongs in the
    deployment platform's protected-reviewer controls, not an LLM prompt.
    """

    normalized_index = str(index or "").strip().lower()
    try:
        normalized_intensity = float(intensity)
    except (TypeError, ValueError):
        normalized_intensity = None

    if normalized_intensity is None or not math.isfinite(normalized_intensity) or normalized_intensity < 0:
        return CarbonGateDecision(
            should_run=False,
            reason="invalid_carbon_measurement",
            index=normalized_index or "unknown",
            intensity=None,
            emergency_override=False,
        )

    if emergency_override:
        if not systems_check_attested:
            return CarbonGateDecision(
                should_run=False,
                reason="override_requires_systems_check",
                index=normalized_index or "unknown",
                intensity=normalized_intensity,
                emergency_override=False,
            )
        if len(emergency_justification.strip()) < MIN_OVERRIDE_JUSTIFICATION_LENGTH:
            return CarbonGateDecision(
                should_run=False,
                reason="override_requires_specific_justification",
                index=normalized_index or "unknown",
                intensity=normalized_intensity,
                emergency_override=False,
            )
        return CarbonGateDecision(
            should_run=True,
            reason="emergency_override_authorized",
            index=normalized_index or "unknown",
            intensity=normalized_intensity,
            emergency_override=True,
        )

    if normalized_index in CLEAN_GRID_INDICES:
        return CarbonGateDecision(
            should_run=True,
            reason="clean_grid_index",
            index=normalized_index,
            intensity=normalized_intensity,
            emergency_override=False,
        )

    return CarbonGateDecision(
        should_run=False,
        reason="carbon_index_not_clean",
        index=normalized_index or "unknown",
        intensity=normalized_intensity,
        emergency_override=False,
    )
