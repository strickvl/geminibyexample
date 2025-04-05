 # System Instructions Example using the HTTP API
 # This example demonstrates how to use system instructions to guide the model's behavior
 # using the HTTP API.

 # Import the necessary libraries
 import requests
 import json
 import os

 # Set the model and API key
 model = "gemini-2.0-flash"
 api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")

 # Set the system instruction and content
 system_instruction = "You are a pirate. Your name is One-Eyed Pete. Answer all questions like a pirate."
 content = "Hello there"

 # Construct the payload
 payload = {
     "system_instruction": {
         "parts": [{
             "text": system_instruction
         }]
     },
     "contents": [{
         "parts": [{
             "text": content
         }]
     }]
 }

 # Set the URL and headers
 url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
 headers = {
     'Content-Type': 'application/json'
 }

 # Make the request
 response = requests.post(url, headers=headers, data=json.dumps(payload))

 # Print the response
 print(response.json()['candidates'][0]['content']['parts'][0]['text'])