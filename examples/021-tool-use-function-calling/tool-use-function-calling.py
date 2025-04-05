# Function calling & tool use
# This example demonstrates how to use the Gemini API to call external functions.

# Import necessary libraries
import os
from datetime import datetime
from google import genai
from google.genai import types


# Define the function to get temperature for a location.
# In a real application, this would call a weather API service like OpenWeatherMap or WeatherAPI
def get_current_temperature(location: str) -> dict:
    """Gets the current temperature for a given location.

    Note: This is a simplified mock implementation. In a real application,
    this function would make an API call to a weather service provider.
    """
    sample_temperatures = {
        "London": 16,
        "New York": 23,
        "Tokyo": 28,
        "Sydney": 20,
        "Paris": 18,
        "Berlin": 17,
        "Cairo": 32,
        "Moscow": 10,
    }
    temp = sample_temperatures.get(location, 21)
    return {"location": location, "temperature": temp, "unit": "Celsius"}


# Define the function to check appointment availability.
# In a real application, this would query a calendar API like Google Calendar or
# a booking system.
# For this example, we're using hard-coded busy slots.
def check_appointment_availability(date: str, time: str) -> dict:
    """Checks if there's availability for an appointment at the given date and time."""
    busy_slots = [
        {"date": "2024-07-04", "times": ["14:00", "15:00", "16:00"]},
        {"date": "2024-07-05", "times": ["09:00", "10:00", "11:00"]},
        {"date": "2024-07-10", "times": ["13:00", "14:00"]},
    ]

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "available": False,
            "error": "Invalid date format. Please use YYYY-MM-DD.",
        }

    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        return {
            "available": False,
            "error": "Invalid time format. Please use HH:MM in 24-hour format.",
        }

    for slot in busy_slots:
        if slot["date"] == date and time in slot["times"]:
            return {
                "available": False,
                "message": f"The slot on {date} at {time} is already booked.",
            }

    return {
        "available": True,
        "message": f"The slot on {date} at {time} is available for booking.",
    }


# For Example 1, we will call a single function with Gemini.
print("\n--- Example 1: Basic Function Calling ---\n")

# First, we define the function declaration that will be provided to the model.
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

# Create a client and configure it with the function declaration
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = types.Tool(function_declarations=[weather_function])
config = types.GenerateContentConfig(tools=[tools])

# Send a request to Gemini that will likely trigger the function
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="What's the temperature in London?",
    config=config,
)

# Check if Gemini responded with a function call
# Assumes Gemini will always respond with a function call.
function_call = response.candidates[0].content.parts[0].function_call
print(f"Function to call: {function_call.name}")
print(f"Arguments: {function_call.args}")

# Execute the function with the arguments Gemini provided
result = get_current_temperature(**function_call.args)
print(f"Function result: {result}")

# Send the function result back to Gemini for a final response
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        {
            "parts": [
                {
                    "function_response": {
                        "name": function_call.name,
                        "response": result,
                    }
                }
            ]
        }
    ],
)
print(f"Model's final response: {response.text}")


# Example 2 shows how to use multiple functions simultaneously.
print("\n--- Example 2: Parallel Function Calling (Weather and Appointments) ---\n")

# Define the weather function declaration
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. London",
            },
        },
        "required": ["location"],
    },
}

# Define the appointment function declaration
appointment_function = {
    "name": "check_appointment_availability",
    "description": "Checks if there's availability for an appointment at the given date and time.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Date to check (YYYY-MM-DD)",
            },
            "time": {
                "type": "string",
                "description": "Time to check (HH:MM) in 24-hour format",
            },
        },
        "required": ["date", "time"],
    },
}

# Create a client and configure it with both function declarations
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = [types.Tool(function_declarations=[weather_function, appointment_function])]

# Set a lower temperature for more predictable function calling
config = {
    "tools": tools,
    "temperature": 0.1,
}

# Start a chat and send a message that should trigger both functions
chat = client.chats.create(model="gemini-2.0-flash-lite", config=config)
response = chat.send_message(
    "I'm planning to visit Paris on July 4th at 2 PM. What's the weather like there and is that slot available for an appointment?"
)

# Store the results from each function call
results = {}

# Process each function call Gemini requests
# Assumes Gemini will always respond with function calls.
for fn in response.function_calls:
    args_str = ", ".join(f"{key}={val}" for key, val in fn.args.items())
    print(f"{fn.name}({args_str})")

    # Call the appropriate function based on name
    if fn.name == "get_current_temperature":
        result = get_current_temperature(**fn.args)
    elif fn.name == "check_appointment_availability":
        result = check_appointment_availability(**fn.args)
    else:
        result = {"error": f"Unknown function: {fn.name}"}

    # Store each result for later use
    results[fn.name] = result
    print(f"Result: {result}\n")

# Prepare all function responses to send back to Gemini
function_responses = []
for fn_name, result in results.items():
    function_responses.append({"name": fn_name, "response": result})

# Send all results back to Gemini in a single message
if function_responses:
    print("Sending all function results back to the model...\n")
    response = chat.send_message(str(function_responses))
    print(f"Model's final response:\n{response.text}")
