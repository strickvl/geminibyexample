# Context caching
# This example demonstrates how to use the Gemini API's context caching feature to
# efficiently query a large document multiple times without resending it with each request.
# This can reduce costs when repeatedly referencing the same content.

from google import genai
from google.genai.types import CreateCachedContentConfig, GenerateContentConfig
import os
import time
import requests

# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Specify a versioned model that supports context caching
# Note: Must use explicit version suffix (-001) for caching
model_id = "gemini-1.5-flash-001"

# Load a large document (e.g., technical documentation).
# For this example, we assume the document is in markdown format.
response = requests.get("https://zenml.io/llms.txt")
response.raise_for_status()  # Raise an exception for HTTP errors
api_docs = response.text

# Create a cache with the document and system instructions
cache = client.caches.create(
    model=model_id,
    config=CreateCachedContentConfig(
        display_name="ZenML LLMs.txt Documentation Cache",  # Used to identify the cache
        system_instruction=(
            "You are a technical documentation expert. "
            "Answer questions about the ZenML documentation provided. "
            "Keep your answers concise and to the point."
        ),
        contents=[api_docs],
        ttl="900s",  # Cache for 15 minutes
    ),
)

# Display cache information
print(f"Cache created with name: {cache.name}")
print(f"Cached token count: {cache.usage_metadata.total_token_count}")
print(f"Cache expires at: {cache.expire_time}")

# Define multiple queries to demonstrate reuse of cached content
queries = [
    "What are the recommended use cases for ZenML's pipeline orchestration?",
    "How does ZenML integrate with cloud providers?",
]

# Run multiple queries using the same cached content
for query in queries:
    print(f"\nQuery: {query}")

    # Generate response using the cached content
    response = client.models.generate_content(
        model=model_id,
        contents=query,
        config=GenerateContentConfig(cached_content=cache.name),
    )

    # Print token usage statistics to demonstrate savings
    print(f"Total tokens: {response.usage_metadata.total_token_count}")
    print(f"Cached tokens: {response.usage_metadata.cached_content_token_count}")
    print(f"Output tokens: {response.usage_metadata.candidates_token_count}")

    # Print the response (truncated for brevity)
    print(f"Response: {response.text}...")

    time.sleep(1)  # Short delay between requests

# When done with the cache, you can delete it to free up resources
client.caches.delete(name=cache.name)
