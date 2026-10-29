import os
import urllib.error
import core

key = os.getenv("MODEL_API_KEY", "")

def safe(text):
    text = str(text)
    return text.replace(key, "[API_KEY_HIDDEN]") if key else text

base = os.getenv("MODEL_BASE_URL", "").rstrip("/")

print("Model:", os.getenv("MODEL_NAME"))
print("Request URL:", base + "/chat/completions")
print("API key configured:", bool(key))

try:
    reply, metadata = core.model_call([
        {"role": "user", "content": "Reply OK only."}
    ])
    print("SUCCESS:", safe(reply))
    print("Returned model:", metadata.get("returned_model"))
except urllib.error.HTTPError as error:
    print("HTTP status:", error.code)
    body = error.read().decode("utf-8", errors="replace")
    print("Error details:", safe(body))
except Exception as error:
    print("Error:", safe(error))