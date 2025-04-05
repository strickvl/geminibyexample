# Reasoning models
# This example demonstrates how to access the reasoning trace of a Gemini model
# and then the final text output.
# Reasoning models are a new type of model that 'think' a little bit before
# giving a final answer. The 'thinking' response is visible in Google AI Studio
# but not as part of the response to an API call.

# Import the Gemini API
from google import genai
import os

# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define a profound question about the universe
prompt = "If the universe is expanding, what is it expanding into? Show your reasoning."

# Generate content with the Gemini model
response = client.models.generate_content(
    model="gemini-2.5-pro-exp-03-25",
    contents=prompt,
)

print(response.text)
