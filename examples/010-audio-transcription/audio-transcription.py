# Audio transcription
# This example demonstrates how to transcribe an audio file by providing the audio data inline with the request.

# Import the necessary modules
from google import genai
from google.genai import types
import requests

# Initialize the Gemini client with your API key
client = genai.Client(api_key="YOUR_API_KEY")

# Define a descriptive User-Agent following Wikimedia's policy
user_agent = "GeminiByExample/1.0 (https://github.com/strickvl/geminibyexample; contact@example.org) python-requests/2.0"

# Download the audio file from the URL
url = "https://upload.wikimedia.org/wikipedia/commons/1/1f/%22DayBreak%22_with_Jay_Young_on_the_USA_Radio_Network.ogg"
headers = {"User-Agent": user_agent}
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an exception for bad status codes

# Read the audio file as bytes
# Note: If your audio file is larger than 20MB, you should use the File API to upload the file first.
# The File API allows you to upload larger files and then reference them in your requests.
audio_bytes = response.content

# Call the API to generate a transcription of the audio clip
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "Transcribe this audio clip",
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        ),
    ],
)

# Print the transcribed text
print(response.text)
