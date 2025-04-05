from pydantic import BaseModel, Field
from google import genai
import os
from rich import print as rprint
from rich.prompt import Prompt
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-pro-preview-03-25"


class GeminiExample(BaseModel):
    """Represents a code example for the Gemini by Example site."""

    python_code: str = Field(description="The Python code to be displayed and executed")
    shell_code: str = Field(
        description="Shell commands to run the Python code and sample outputs"
    )
    requests_code: str = Field(
        description="Python code using the requests library that replicates any curl examples in the documentation",
        default=None,
    )
    requires_image: bool = Field(
        description="Whether this example needs an image to be displayed (i.e. if it involves image generation)",
    )


def fetch_url_content(url: str) -> str:
    """Fetch and parse content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        return soup.get_text()
    except Exception as e:
        rprint(f"[bold red]Error fetching {url}: {e}[/bold red]")
        return ""


def get_example_files_content():
    """Get content from example files."""
    python_example = Path("examples/002-streaming-text/streaming-text.py").read_text()
    shell_example = Path("examples/002-streaming-text/streaming-text.sh").read_text()
    requests_example = Path(
        "examples/002-streaming-text/streaming-text_requests.py"
    ).read_text()
    return python_example, shell_example, requests_example


def get_contributing_guidelines():
    """Extract formatting guidelines from CONTRIBUTING.md."""
    contributing_text = Path("CONTRIBUTING.md").read_text()

    # Extract formatting sections
    python_format = re.search(
        r"### 2\. Add Python File.*?```python(.*?)```", contributing_text, re.DOTALL
    ).group(1)

    shell_format = re.search(
        r"### 3\. Add Shell Script.*?```bash(.*?)```", contributing_text, re.DOTALL
    ).group(1)

    formatting_rules = re.search(
        r"#### Formatting Rules:(.*?)###", contributing_text, re.DOTALL
    ).group(1)

    shell_format_rules = re.search(
        r"#### Shell Script Format:(.*?)###", contributing_text, re.DOTALL
    ).group(1)

    return python_format, shell_format, formatting_rules, shell_format_rules


def generate_example(prompt: str) -> GeminiExample:
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": GeminiExample,
        },
    )

    return response.parsed


def main():
    rprint("[bold blue]Welcome to the Gemini Example Generator![/bold blue]")

    # Ask for folder name
    folder_name = Prompt.ask(
        "[yellow]Enter the folder name for this example[/yellow] (e.g., 003-hello-world)"
    )

    # Validate folder name format (should be like 003-hello-world)
    while not re.match(r"^\d{3}-[a-z0-9-]+$", folder_name):
        rprint("[bold red]Folder name should be in format '003-hello-world'[/bold red]")
        folder_name = Prompt.ask(
            "[yellow]Enter the folder name for this example[/yellow] (e.g., 003-hello-world)"
        )

    # Ask for focus area
    focus = Prompt.ask(
        "[yellow]What specific aspect should this example focus on?[/yellow] (e.g., streaming text, multi-turn chat, etc.)"
    )

    # Ask for topical theme
    theme = Prompt.ask(
        "[yellow]Do you want a specific topical theme for this example?[/yellow] (e.g., cats, astronomy, cooking, etc. Leave blank for no theme)",
        default=""
    )

    # Ask for documentation URLs
    urls = []
    rprint(
        "[yellow]Enter documentation URLs related to this example (press Enter when done)[/yellow]"
    )
    while True:
        url = Prompt.ask("URL", default="")
        if not url:
            break
        urls.append(url)

    if not urls:
        rprint("[bold red]No URLs provided. At least one URL is required.[/bold red]")
        return

    # Fetch content from URLs
    rprint("\n[blue]Fetching content from URLs...[/blue]")
    docs_content = ""
    for url in urls:
        content = fetch_url_content(url)
        if content:
            docs_content += f"\n\n--- Content from {url} ---\n\n{content}"

    # Get example files and contributing guidelines
    python_example, shell_example, requests_example = get_example_files_content()
    python_format, shell_format, formatting_rules, shell_format_rules = (
        get_contributing_guidelines()
    )

    # Create the prompt
    prompt = f"""
You are an expert devrel with years of experience in creating code examples that help developers learn new technologies.

Your task today is to take some documentation from the Google Gemini SDK docs and turn it into a simple illustrative example using code.

## Focus Area
This example should specifically focus on: {focus}

{f'## Topical Theme\nThis example should incorporate the thematic elements of: {theme}' if theme else ''}

## Documentation Content
{docs_content}

## Formatting / Output rules
You will output the following:

- Python code formatted according to the guidelines below
- Shell code/output formatted according to the guidelines below
- Python requests code that replicates any curl examples found in the documentation, using the requests library (only if curl examples are present in the documentation). Note: This is stored in a separate file and is not used in the site build.
- A boolean as to whether you think it needs an image to illustrate the output (i.e., if image generation or editing is involved)

### Python File Format:
{python_format}

Python Formatting Rules:
{formatting_rules}

### Shell Script Format:
{shell_format}

Shell Script Formatting Rules:
{shell_format_rules}

## Examples
Here's an example of the Python code format:

```python
{python_example}
```

Here's an example of the shell code format:

```bash
{shell_example}
```

Here's an example of the requests code format:

```python
{requests_example}
```

Based on the documentation provided, please generate a concise, illustrative example that demonstrates the key concepts clearly, focusing specifically on {focus}. If the documentation contains multiple examples or topics, prioritize content related to {focus} and ignore unrelated sections.
{f"Try to incorporate elements of the theme: {theme} in your example where it makes sense, such as in prompts, variables, or example text." if theme else ""}

For the requests_code, ONLY include this if you find actual curl examples in the documentation. If curl examples exist, translate them to Python code using the requests library. Do NOT create requests code if there are no curl examples in the documentation.
"""

    # Generate the example
    rprint("\n[blue]Generating example using Gemini...[/blue]")
    try:
        result = generate_example(prompt)

        # Create the directory structure
        example_dir = Path("examples") / folder_name
        example_dir.mkdir(parents=True, exist_ok=True)

        # Extract the example name from the folder (e.g., "basic-generation" from "001-basic-generation")
        example_name = folder_name.split("-", 1)[1]

        # Save Python file
        python_file = example_dir / f"{example_name}.py"
        python_file.write_text(result.python_code)

        # Save Shell file
        shell_file = example_dir / f"{example_name}.sh"
        shell_file.write_text(result.shell_code)

        # Save Requests file if curl examples were found
        if result.requests_code:
            requests_file = example_dir / f"{example_name}_requests.py"
            requests_file.write_text(result.requests_code)

        # Save documentation URLs to a text file
        if urls:
            docs_file = example_dir / f"{example_name}_links.txt"
            docs_file.write_text("\n".join(urls))
            rprint(f"[blue]Saved documentation links to {docs_file}[/blue]")

        rprint(
            f"\n[bold green]Successfully created example in {example_dir}[/bold green]"
        )

        # Notify if an image is needed
        if result.requires_image:
            rprint(
                f"\n[bold red]NOTE: This example requires an image named '{example_name}.png' in the example directory.[/bold red]"
            )

    except Exception as e:
        rprint(f"[bold red]Error generating example: {e}[/bold red]")


if __name__ == "__main__":
    main()
