import requests
import os
import json

# Set your API key
api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")

# Gemini 2.0 Flash Image Generation (Replicating curl example)
url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={api_key}"

payload_gemini = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Hi, can you create a 3d rendered image of a cat with wings and a top hat flying over a happy futuristic scifi city with lots of greenery?"
                }
            ]
        }
    ],
    "generationConfig": {"responseModalities": ["Text", "Image"]},
}

response_gemini = requests.post(url_gemini, json=payload_gemini)
response_gemini.raise_for_status()

# Extract the image data from the response
data_gemini = response_gemini.text

data_start = data_gemini.find('"data": "') + len('"data": "')
data_end = data_gemini.find('"', data_start)
image_data = data_gemini[data_start:data_end]

# Decode the base64 image data
import base64

with open("gemini-cat-image.png", "wb") as fh:
    fh.write(base64.b64decode(image_data))

print("Gemini cat image saved to gemini-cat-image.png")

# Imagen 3 Image Generation (Replicating curl example)
url_imagen = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"

payload_imagen = {
    "instances": [
        {
            "prompt": "A tabby cat wearing a space helmet"
        }
    ],
    "parameters": {
        "sampleCount": 2
    }
}

response_imagen = requests.post(url_imagen, json=payload_imagen)
response_imagen.raise_for_status()

# Extract image data and write to file for each generated image
image_data_imagen = response_imagen.json()

for i, prediction in enumerate(image_data_imagen["predictions"]):
    image_bytes = base64.b64decode(prediction["bytesBase64Encoded"])

    with open(f"imagen_cat_{i + 1}.png", "wb") as f:
        f.write(image_bytes)
    print(f"Imagen cat image {i + 1} saved to imagen_cat_{i + 1}.png")
