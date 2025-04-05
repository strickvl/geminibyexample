# YouTube video summarization
# This example demonstrates how to summarize a YouTube video using its URL.

# Import the Gemini API
from google import genai

# Initialize the Gemini client with your API key
client = genai.Client(api_key="YOUR_API_KEY")

# Construct the prompt with the YouTube video URL
youtube_url = "https://www.youtube.com/watch?v=tAP1eZYEuKA"
prompt = f"Summarize the content of this YouTube video: {youtube_url}"

# Call the API to generate content
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        {
            "parts": [
                {"text": "Can you summarize this video?"},
                {"file_data": {"file_uri": youtube_url}},
            ]
        }
    ],
)

# Print the generated summary
print(response.text)
