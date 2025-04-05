# Structured output
# This example shows how to generate structured data using a pydantic model to represent Cats with name, colour, and special ability.

# Import the Gemini API and pydantic
from google import genai
from pydantic import BaseModel
import os


# Define a Pydantic model for a Cat
class Cat(BaseModel):
    name: str
    colour: str
    special_ability: str


# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define the prompt. Note: It asks for 3 cats
prompt = "Generate data for 3 cats, including their name, colour and special ability."

# Call the API to generate content, specifying the response schema.
# Note that it expects a `list` and not a `typing.List` object.
# For some reason Gemini models are finicky about that.
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Cat],
    },
)

# Parse the json response to a list of Cat objects
my_cats: list[Cat] = response.parsed

# Print the generated cat data
for cat in my_cats:
    print(
        f"Name: {cat.name}, Colour: {cat.colour}, Special Ability: {cat.special_ability}"
    )
