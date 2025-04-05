# Audio question answering
# This example demonstrates how to ask a question about the content of an audio file using the Gemini API.

# Import the necessary libraries
from google import genai
from google.genai import types
import requests
import os

# Replace with your actual API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define a descriptive User-Agent following Wikimedia's policy
user_agent = "GeminiByExample/1.0 (https://github.com/strickvl/geminibyexample; contact@example.org) python-requests/2.0"

# Download the audio file from the URL
url = "https://upload.wikimedia.org/wikipedia/commons/1/1f/%22DayBreak%22_with_Jay_Young_on_the_USA_Radio_Network.ogg"
headers = {"User-Agent": user_agent}
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an exception for bad status codes

# Save the content to a variable
# Note: If your audio file is larger than 20MB, you should use the File API to upload the file first.
# The File API allows you to upload larger files and then reference them in your requests.
audio_bytes = response.content

# You can now pass that audio file along with the prompt to Gemini
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "What is the main topic of this audio?",
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        ),
    ],
)

print(response.text)
