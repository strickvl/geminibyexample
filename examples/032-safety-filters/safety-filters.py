# Safety settings and filters
# This example demonstrates how to adjust safety settings to block content based on the probability of unsafe content.

# Import the Gemini API and required types
from google import genai
from google.genai import types
import os

# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define safety settings to block low and above probability for harassment and
# hate speech.
# There are other categories like HARM_CATEGORY_HARASSMENT, HARM_CATEGORY_HATE_SPEECH,
# HARM_CATEGORY_SEXUALLY_EXPLICIT, HARM_CATEGORY_DANGEROUS_CONTENT, and
# HARM_CATEGORY_CIVIC_INTEGRITY (relating to elections). These categories are defined in HarmCategory. The Gemini
# models only support these specific harm categories.
safety_settings = [
    {
        "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        "threshold": types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
    {
        "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        "threshold": types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
]

# Configure the generation with the defined safety settings
generation_config = types.GenerateContentConfig(safety_settings=safety_settings)

# Generate content with the specified safety settings
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="Write something that could be interpreted as offensive.",
    config=generation_config,
)

# Print the generated text (if not blocked by safety settings).
# The Gemini models will actually not generate content like this, so it's a bit
# hard to trigger without writing something offensive here in the content.
# I hope you get the idea, though, about how to use this.
if (
    hasattr(response, "prompt_feedback")
    and response.prompt_feedback
    and hasattr(response.prompt_feedback, "block_reason")
):
    print("The prompt was blocked due to: ", response.prompt_feedback.block_reason)
else:
    print(response.text)
