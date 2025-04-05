# Streaming Text Generation
# This example demonstrates how to stream text when generating content using the Gemini API.
from google import genai

# Initialize the Gemini client with your API key
client = genai.Client(api_key="YOUR_API_KEY")

# Call the generate_content_stream method to get a stream of responses
response = client.models.generate_content_stream(
    model="gemini-2.0-flash", contents=["Explain how AI works"]
)

# Iterate over the stream and print each chunk of text as it arrives
for chunk in response:
    print(chunk.text, end="")
