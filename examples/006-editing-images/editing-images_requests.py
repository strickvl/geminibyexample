# Edit a cat image to add a hat using the HTTP API
# This example demonstrates how to edit an existing image of a cat to add a hat using the Gemini API via HTTP requests.

import requests
import json
import base64
import os

# Set your Gemini API key and the API endpoint
api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key=" + api_key

# Download the cat image from cataas.com
image_url = "https://cataas.com/cat"
response = requests.get(image_url)
image_data = response.content

# Encode the image to base64
image_base64 = base64.b64encode(image_data).decode("utf-8")

# Prepare the request payload
payload = json.dumps({
    "contents": [
        {
            "parts": [
                {"text": "Please add a stylish top hat to this cat."},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                }
            ]
        }
    ],
    "generationConfig": {"responseModalities": ["Text", "Image"]}
})

# Set the headers
headers = {
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(api_url, headers=headers, data=payload)

# Parse the JSON response
response_json = response.json()

# Extract the image data from the response
image_data_base64 = response_json['candidates'][0]['content']['parts'][0]['inline_data']['data']

# Decode the base64 image data
image_data = base64.b64decode(image_data_base64)

# Save the edited image to a file
with open("cat_with_hat_http.png", "wb") as f:
    f.write(image_data)

print("Image saved as cat_with_hat_http.png")