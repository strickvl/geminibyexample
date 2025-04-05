# Image question answering
# This example demonstrates how to use the Gemini API to analyze or understand images of cats, including using image URLs and base64 encoding.

# Import necessary libraries
from google import genai
from google.genai import types
import requests
import base64

# Replace with your Gemini API key
client = genai.Client(api_key="YOUR_API_KEY")

# We'll start by using an image URL.
# Load an image of a cat from a URL
image_url = "https://cataas.com/cat"
image_response = requests.get(image_url)
image_content = image_response.content

# Ask Gemini about the cat in the image
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["What breed of cat is this?", types.Part.from_bytes(data=image_content, mime_type="image/jpeg")]
)

print("Response from URL Image:\n", response.text)

# Now we'll use a local image file.
# Load a local image of a cat and encode it as Base64
with open("cat.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

# Ensure the encoded string is a string
encoded_string = encoded_string.decode('utf-8')

# Ask Gemini a question about the cat, providing the image as a Base64 string
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Is this cat fluffy?", types.Part.from_bytes(data=base64.b64decode(encoded_string), mime_type="image/jpeg")]
)

print("\nResponse from Base64 Image:\n", response.text)
