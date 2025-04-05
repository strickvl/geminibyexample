# System prompt
# This example demonstrates how to use system instructions to guide the model's behavior.

# Import the Gemini API
from google import genai
from google.genai import types

# Initialize the Gemini client with your API key
client = genai.Client(api_key="YOUR_API_KEY")

# Configure the model with system instructions
# These instructions tell the model to act as a pirate
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a pirate.  Answer all questions like a pirate."),
    contents="Hello there"
)

# Print the model's response
print(response.text)
