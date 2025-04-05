# Streaming Text Generation using the HTTP API
# This example demonstrates how to use the Gemini API to generate text content
# and stream the output using the HTTP API.

# Import the necessary libraries
import requests
import json
import os

# Set the model and API key
model = "gemini-2.0-flash"
api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
prompt = "Explain how AI works"

# Set up the API request
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent"
params = {"alt": "sse", "key": api_key}
payload = {"contents": [{"parts": [{"text": prompt}]}]}

# Make the streaming request and process the response
with requests.post(url, json=payload, params=params, stream=True) as r:
    for line in r.iter_lines():
        if line and line.startswith(b"data: ") and not line.endswith(b"[DONE]"):
            try:
                data = json.loads(line[6:])
                if "candidates" in data and data["candidates"]:
                    text = data["candidates"][0]["content"]["parts"][0].get("text", "")
                    print(text, end="")
            except:
                pass
