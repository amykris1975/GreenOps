# Run GreenOps Locally

This folder contains the local GreenOps execution mode. It reads Gemini credentials from the runtime environment and **never prompts for or stores a key**.

## Prerequisites

1. Python 3.10+.
2. Dependencies installed from the repository root:

   ```bash
   pip install -r requirements.txt
   ```

3. A Gemini API key created in the appropriate Google AI Studio project. Enter the key only in your approved secret manager or local environment—not in source files, a `.env` committed to Git, a terminal transcript, or a pull request.

## Secure quick start

From the repository root:

```bash
# macOS/Linux
export GEMINI_API_KEY="<stored-in-your-shell-or-secret-manager>"
export GREENOPS_GEMINI_MODEL="gemini-2.5-flash"  # optional; use a model enabled for your project
python Local/greenops_local.py
```

```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="<stored-in-your-shell-or-secret-manager>"
$env:GREENOPS_GEMINI_MODEL="gemini-2.5-flash"   # optional
python Local/greenops_local.py
```

`GOOGLE_API_KEY` remains supported only for backward compatibility. When both are set, `GEMINI_API_KEY` takes precedence.

## Validate configuration behavior without a live request

```bash
python -m unittest discover -s tests -v
```

The tests check key precedence and malformed configuration without contacting Gemini or exposing a credential.

## What to expect

The script will:

1. Connect to the UK National Grid Carbon Intensity API.
2. Run three local scenarios (microservice, data migration, and security patch).
3. Use Gemini to reason about scheduling only after a key is available in the runtime environment.

## Troubleshooting

| Symptom | Action |
|---|---|
| `Gemini configuration error` | Confirm the secret store/runtime provides `GEMINI_API_KEY` and that it has no leading, trailing, or embedded whitespace. |
| Model request fails | Set `GREENOPS_GEMINI_MODEL` to a model enabled for the selected AI Studio project. |
| `429 Resource Exhausted` | Authentication worked; wait for quota availability or use a project with appropriate capacity. |
| Protobuf / SDK error | Upgrade the packages declared in `requirements.txt` in the local virtual environment. |
