# Code Execution: Sum of first 50 primes using HTTP API
# This example demonstrates how to use the Gemini API to execute code and calculate the sum of the first 50 prime numbers using the HTTP API.

import requests
import json
import os

# Set the API key and endpoint
api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key

# Set the request headers and payload
headers = {
    'Content-Type': 'application/json'
}
payload = {
    "tools": [{
        "code_execution": {}
    }],
    "contents": {
        "parts": {
            "text": "What is the sum of the first 50 prime numbers? Generate and run code for the calculation, and make sure you get all 50."
        }
    }
}

# Make the API request
response = requests.post(url, headers=headers, json=payload)

# Parse the JSON response
json_response = response.json()

# Extract the text from the response
text = json_response['candidates'][0]['content']['parts'][0]['text']

# Print the response
print(text)