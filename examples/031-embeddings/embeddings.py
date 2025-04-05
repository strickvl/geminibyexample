# Embeddings generation
# This example demonstrates generating text embeddings for cat-related terms using the Gemini API.

# Import the Gemini API
from google import genai
import os

# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Specify the embedding model to use
model_name = "gemini-embedding-exp-03-07"

# Define some cat-related terms
cats = ["Siamese cat", "Persian cat", "cat food", "cat nap"]

# Generate embeddings for each term
embeddings = []
for cat in cats:
    result = client.models.embed_content(model=model_name, contents=cat)
    embeddings.append(result.embeddings)

# Print the embeddings (for demonstration purposes, showing the length)
for i, embedding in enumerate(embeddings):
    embedding_values = embedding[0].values
    print(f"Embedding for '{cats[i]}': Length = {len(embedding_values)}")
    print(f"First 10 values: {embedding_values[0:10]}")
