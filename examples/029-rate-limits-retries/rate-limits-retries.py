# Rate limits and retries
# This example demonstrates generating text with the Gemini API, handling rate limiting errors, and using exponential backoff for retries.

import google.generativeai as genai
import google.ai.generativelanguage as glm
import time
import os


# Configure the retry strategy
def configure_retries(base_delay=1, max_delay=60, max_retries=5):
    """Configures exponential backoff retry strategy."""
    return genai.retry.RetryConfig(
        initial_delay=base_delay,
        max_delay=max_delay,
        max_retries=max_retries,
        retry_on_status_codes=[glm.Code.RESOURCE_EXHAUSTED.value],
    )


# Set the retry configuration
retry_config = configure_retries()

# Initialize the Gemini client with your API key
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"), retry_config=retry_config
)

# Select the model
model = "gemini-2.0-flash"

# Construct the prompt
prompt = "Tell me a funny story about a cat trying to catch a laser pointer."

#
# Attempt text generation with retry logic
#
try:
    response = client.models.generate_content(model=model, contents=prompt)
    print(response.text)
except genai.errors.APIError as e:
    print(f"An error occurred: {e}")
