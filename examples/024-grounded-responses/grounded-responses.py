# Grounded Responses with Search Tool
# This example demonstrates how to use the Gemini API with the Search tool to get grounded responses.

# Import the Gemini API and necessary tools
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

# Initialize the Gemini client with your API key
client = genai.Client(api_key="YOUR_API_KEY")

# Specify the model to use (Gemini 2.0 models or later support search as a tool)
model_id = "gemini-2.0-flash"

# Configure the Google Search tool
google_search_tool = Tool(
    google_search = GoogleSearch()
)

# Craft your query.  This one asks for films in Delft cinemas on a specific date.
query = "What films are showing in Delft on October 27, 2024, particularly at Filmhuis Lumen and Pathe cinemas?"

# Call the API to generate content, including the search tool in the configuration
response = client.models.generate_content(
    model=model_id,
    contents=query,
    config=GenerateContentConfig(
        tools=[google_search_tool],
        response_modalities=["TEXT"],
    )
)

# Print the generated text response
for each in response.candidates[0].content.parts:
    print(each.text)

# Print the grounding metadata (web content used to ground the response).
print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)