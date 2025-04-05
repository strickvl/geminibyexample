# Model Context Protocol
# This example demonstrates using a local MCP server with Gemini to get weather information.

# Import necessary libraries. Make you have mcp installed.
import asyncio
import os
from datetime import datetime
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define server parameters for the MCP server
server_params = StdioServerParameters(
    command="npx",  # Executable for the MCP server
    args=[
        "-y",
        "@philschmid/weather-mcp",
    ],  # Arguments for the server (Weather MCP Server)
    env=None,  # Optional environment variables
)

# Define the prompt to get the weather for the current day in Delft
PROMPT = f"What is the weather in Delft in {datetime.now().strftime('%Y-%m-%d')}?"


# Define an asynchronous function to run the MCP client and interact with
# Gemini.
# We retrieve tools from the MCP session and convert them to Gemini Tool objects
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = await session.list_tools()
            tools = [
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )
                for tool in mcp_tools.tools
            ]

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=PROMPT,
                config=types.GenerateContentConfig(
                    temperature=0,
                    tools=tools,
                ),
            )

            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                print(f"Function call: {function_call}")

                result = await session.call_tool(
                    function_call.name, arguments=function_call.args
                )
                print(f"Tool Result: {result.content[0].text}")

            else:
                print("No function call found in the response.")
                print(response.text)


# Run the asynchronous function
asyncio.run(run())
