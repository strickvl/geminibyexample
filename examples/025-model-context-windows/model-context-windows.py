# Model context windows
# This example demonstrates how to access the input and output token limits for different Gemini models.

# Import the Gemini API
from google import genai
import os

# Configure the client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Get information about the gemini-2.0-flash model
model_info = client.models.get(model="models/gemini-2.0-flash")

# Print the input and output token limits for gemini-2.0-flash
print("Gemini 2.0 Flash:")
print(
    f"  Input token limit: {model_info.input_token_limit:,} tokens (1 million tokens)"
)
print(
    f"  Output token limit: {model_info.output_token_limit:,} tokens (8 thousand tokens)"
)

# Get information about the gemini-2.5-pro-preview-03-25 model
pro_model_info = client.models.get(model="models/gemini-2.5-pro-preview-03-25")

# Print the input and output token limits for gemini-2.5-pro-preview-03-25
print("\nGemini 2.5 Pro:")
print(
    f"  Input token limit: {pro_model_info.input_token_limit:,} tokens (1 million tokens)"
)
print(
    f"  Output token limit: {pro_model_info.output_token_limit:,} tokens (65 thousand tokens)"
)
