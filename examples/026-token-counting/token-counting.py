# Counting chat tokens
# This example demonstrates how to count tokens in a chat history with the Gemini API, incorporating a cat theme.

# Import the Gemini API
from google import genai
from google.genai import types
import os

# Configure the Gemini API with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Start a chat session with a cat-related history
chat = client.chats.create(
    model="gemini-2.0-flash",
    history=[
        types.Content(role="user", parts=[types.Part(text="Hey there! I love cats!")]),
        types.Content(
            role="model",
            parts=[
                types.Part(
                    text="Me too! Cats are the best. What's your favorite breed?"
                )
            ],
        ),
    ],
)

# Count the tokens in the initial chat history
token_count = client.models.count_tokens(
    model="gemini-2.0-flash", contents=chat.get_history()
)
print(f"Tokens in initial chat history: {token_count.total_tokens} tokens")

# Send a new message to the chat, asking about cat breeds
response = chat.send_message(message="Tell me more about Ragdoll cats.")

# Print the token usage metadata from the response
print(
    f"Token usage for the last turn: input_tokens={response.usage_metadata.prompt_token_count}, output_tokens={response.usage_metadata.candidates_token_count}, total_tokens={response.usage_metadata.total_token_count}"
)

# Count tokens including next turn question
extra = types.UserContent(
    parts=[
        types.Part(
            text="Do you know Neko the cat?",
        )
    ]
)
history = chat.get_history()
history.append(extra)
final_count = client.models.count_tokens(model="gemini-2.0-flash", contents=history)
print(f"Total tokens with additional question: {final_count.total_tokens} tokens")
