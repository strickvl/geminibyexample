# Concurrent requests and generation
# This example demonstrates how to generate text using concurrent.futures to make parallel requests to the Gemini API, with a focus on cat-related prompts.

# Import the necessary libraries
import concurrent.futures
from google import genai
import os


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# A function to generate a fun fact about cats.
def generate_cat_fact(model):
    # Generates a fun fact about cats.
    response = client.models.generate_content(
        model=model,
        contents="Tell me a fun fact about cats.",
    )
    return response.text


# A function to generate a short story about a cat.
def generate_cat_story(model):
    # Generates a short story about a cat.
    response = client.models.generate_content(
        model=model,
        contents="Write a ultra-short story about a cat who goes on an adventure.",
    )
    return response.text


# The model to use for the requests.
model = "gemini-2.0-flash-lite"

# Use ThreadPoolExecutor to run the requests concurrently.
# We submit the tasks to the executor and then get the results.
with concurrent.futures.ThreadPoolExecutor() as executor:
    fact_future = executor.submit(generate_cat_fact, model)
    story_future = executor.submit(generate_cat_story, model)

    cat_fact = fact_future.result()
    cat_story = story_future.result()

print("Cat Fact:\n", cat_fact)
print("\nCat Story:\n", cat_story)
