# Streaming text
# This example demonstrates how to use the Gemini API to generate text content and stream the output.

# Import the Gemini API
from google import genai

# Initialize the Gemini client with your API key
client = genai.Client(api_key="YOUR_API_KEY")

# Call the API to generate content in streaming mode
response = client.models.generate_content_stream(
    model="gemini-2.0-flash",
    contents=["Explain how AI works"]
)

# Iterate over the stream of responses and print each chunk of text
for chunk in response:
    print(chunk.text, end="")
