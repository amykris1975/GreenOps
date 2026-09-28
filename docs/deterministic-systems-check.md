# Deterministic Systems Check: GreenOps Agent Boundary

> **Control objective:** no system can promise perfection. GreenOps instead requires explicit, reproducible controls for every action with environmental, operational, or release impact.

## Decision boundary

| Function | Allowed implementation | Not allowed |
|---|---|---|
| Carbon execution gate | Deterministic code using a documented API response, a fixed clean-index allowlist, fail-closed parsing, and test coverage | A model response deciding whether compute may run |
| Emergency override | A human-triggered workflow requiring an independent systems-check attestation, a specific justification, and a change-record reference | An LLM-created override, silent bypass, or an unreviewed boolean flag |
| Model selection and API configuration | Runtime environment/secret manager plus explicit non-secret model setting | Hard-coded key, interactive terminal key prompt, committed `.env`, or opaque default project choice |
| AI assistance | Explanation, summarization, anomaly triage, or recommendations constrained by source evidence | Approving deployments, signing contracts, attesting compliance, creating insurance decisions, or asserting a human review occurred |
| Release approval | Named human/process controls in GitHub and deployment systems | A prompt, AI agent, or unverified text field acting as an identity check |

## Invariants checked in this PR

1. `GEMINI_API_KEY` wins over legacy `GOOGLE_API_KEY`; neither value is written to disk or logs.
2. Carbon decisions fail closed for missing, invalid, negative, non-finite, or non-clean readings.
3. The local Gemini tool list exposes a carbon-decision readout, **not** a deployment-execution tool.
4. The GitHub workflow verifies repository control invariants before evaluating the external carbon API.
5. An emergency bypass cannot run without `reviewed`, a meaningful justification, and a systems-check reference. This preserves an auditable statement, but it does not authenticate the human. Configure GitHub protected environments/reviewers after the exact account identity is confirmed.

## Systems check for Caleb McCombs

Caleb McCombs is named by the requester as the intended creator/system reviewer. Before representing this as Caleb's review or assigning a GitHub review request, confirm the exact GitHub handle and obtain the appropriate repository permission. Until then, use this checklist as a **proposed** independent systems check:

- [ ] Verify the PR contains no API key, partial key, private message, phone number, or customer data.
- [ ] Run `python3 tools/validate_deterministic_controls.py` and `python3 -m unittest discover -s tests -v`.
- [ ] Confirm that no AI-call path can set `should_run=true`, set an emergency override, or execute a deployment.
- [ ] Confirm the selected Gemini model exists for the intended secured project before a live run.
- [ ] Configure a protected GitHub environment and a named release reviewer for production; do not rely on a free-text workflow input for identity verification.
- [ ] Record the review decision and evidence in the PR or a linked change record.

`GreenOps@workforce.dev` is treated here as a label in the request. This PR does not create, access, or configure that domain or any external workforce service.
