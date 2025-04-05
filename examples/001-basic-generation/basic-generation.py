# Simple text generation

# Our first example demonstrates how to use the Gemini API
# to generate content with a simple prompt.
from google import genai

# Best practice: store your API key in an environment variable
# and load it from there.
client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
