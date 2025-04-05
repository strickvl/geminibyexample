# Video transcription
# This example demonstrates how to transcribe the content of a video using the Gemini API.
# Note: For videos larger than 20MB, you must use the File API for uploading.

# Import the Gemini API
from google import genai
from google.genai import types
import os
import requests

# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"

# Download the video file.
# Read the video file as bytes for inline upload.
response = requests.get(video_url)
video_bytes = response.content

# Define our prompt
prompt = (
    "Transcribe the audio from this video, giving timestamps for "
    "salient events in the video. Also provide visual descriptions."
)

# Create a Gemini request with the video and our prompt.
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=types.Content(
        parts=[
            types.Part(text=prompt),
            types.Part(inline_data=types.Blob(data=video_bytes, mime_type="video/mp4")),
        ]
    ),
)

# Print the model's response
print(response.text)
