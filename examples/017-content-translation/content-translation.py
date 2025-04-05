# Translate documents
# This example demonstrates how to load content from a URL and translate it into
# Chinese using the Gemini API.
# It's easy to do the same using PDF or Markdown files, though you might want to
# split it up into smaller chunks for better accuracy if your document is long.

# Import the necessary libraries
from google import genai
import requests
import os

# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define the URL of the content to be translated
url = "https://raw.githubusercontent.com/zenml-io/zenml/refs/heads/main/README.md"

# Fetch the content from the URL
response = requests.get(url)
text_content = response.text

# Define the prompt for translation
prompt = f"Translate the following English text to Chinese: {text_content}"

# Generate the translated content using the Gemini API.
# We're using the 2.0-flash-lite model here for speed, but you probably would
# want to use a more powerful model for better results.
model = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=prompt,
)

# Print the translated text
print(model.text)
