# Cell 2: Configure Gemini API
from kaggle_secrets import UserSecretsClient

try:
    user_secrets = UserSecretsClient()
    # Prefer GEMINI_API_KEY. GOOGLE_API_KEY remains a backwards-compatible fallback.
    try:
        api_key = user_secrets.get_secret("GEMINI_API_KEY")
    except:
        api_key = user_secrets.get_secret("GOOGLE_API_KEY")

    if not api_key or api_key != api_key.strip() or any(char.isspace() for char in api_key):
        raise ValueError("Gemini secret is missing or malformed")

    genai.configure(api_key=api_key)
    print("✅ Gemini API Configured Successfully.")
except Exception:
    print("❌ Gemini was not configured. Add GEMINI_API_KEY in the notebook secret manager and retry.")
