# Code execution
# This example demonstrates how to use the Gemini API to execute code
# (agent-style) and calculate the sum of the first 50 prime numbers.

# Import the necessary libraries. Make sure you have the rich library installed!
from google import genai
from google.genai import types
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel

# Initialize the rich console and the Gemini client
console = Console()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configure the model to use the code execution tool.
# Note that not all models support code execution.
# The code execution environment includes a number of popular libraries like
# sklearn, matplotlib, pandas, pdfminer and so on.
# You can't install your own libraries.
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="What is the sum of the first 50 prime numbers? "
    "Generate and run code for the calculation, and make sure you get all 50.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution)]
    ),
)


for part in response.candidates[0].content.parts:
    if part.text is not None:
        console.print(Markdown(part.text))

    if part.executable_code is not None:
        code = part.executable_code.code
        # Detect language (simple approach)
        language = (
            "python"
            if "def " in code or "import " in code or "print(" in code
            else "text"
        )
        console.print(
            Panel(
                Syntax(code, language, theme="monokai", line_numbers=True),
                title="Code",
                border_style="blue",
            )
        )

    if part.code_execution_result is not None:
        console.print(
            Panel(
                part.code_execution_result.output,
                title="Output",
                border_style="green",
            )
        )

    if part.inline_data is not None:
        console.print(
            "[yellow]Image data available but cannot be displayed in terminal[/yellow]"
        )

    console.print("---")
