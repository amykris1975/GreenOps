# Gemini Integration Handoff for Caleb McCombs

> **Purpose:** A contributor-ready, secret-free handoff for reviewing or extending GreenOps' Gemini integration. Caleb McCombs is named here at the requester's direction; this document does **not** grant repository access, imply affiliation, or assign authority.

## What this pull request changes

- Adds a deterministic local configuration helper with `GEMINI_API_KEY` as the preferred environment variable and `GOOGLE_API_KEY` as a legacy fallback.
- Removes the interactive API-key prompt from local execution, so a key cannot be inadvertently entered into a terminal transcript.
- Adds a committed `.env.example`, a repository `.gitignore`, and unit tests that verify configuration behavior without contacting Gemini.
- Makes the Gemini model an explicit non-secret setting through `GREENOPS_GEMINI_MODEL`.

## Secure setup

1. Create or select the intended Google AI Studio project in the Google UI.
2. Enter the key **only** in the approved secret manager, CI secret store, or secure connector credential field.
3. Set exactly one preferred runtime variable: `GEMINI_API_KEY`. Do not commit a `.env` file, notebook output, screenshot that reveals a key, or copied terminal history.
4. Optionally set `GREENOPS_GEMINI_MODEL` to a model available to that project/key. The template defaults to `gemini-2.5-flash`; change it if the project does not expose that model.
5. Run the configuration tests before enabling live calls:

   ```bash
   python -m unittest discover -s tests -v
   ```

## Review boundaries

- This repository must not store an API key, key suffix, billing information, phone number, private message, or user contact information.
- A Gemini response is an operational recommendation, not an autonomous approval. Keep a named human owner responsible for deployment decisions and record exceptions.
- Do not infer an organizational relationship from an AI Studio project name or from this handoff document. Partner, contributor, repository, and reviewer permissions must be established separately through normal GitHub and contractual processes.

## Suggested reviewer checklist

- [ ] No key-shaped value, `.env`, or private screenshot is included in the diff.
- [ ] The secure secret store provides `GEMINI_API_KEY` in the intended runtime.
- [ ] The selected model is enabled for the intended project/key.
- [ ] Unit tests pass without a live Gemini request.
- [ ] Any production deployment path has a human escalation and rollback process.
