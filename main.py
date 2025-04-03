import json
import logging
from pathlib import Path
from fasthtml.common import *

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastHTML application
app, rt = fast_app(
    static_dir="static",
    title="Gemini by Example",
    description="Learn Python through annotated examples",
)


# Load example data from JSON file
def load_examples():
    try:
        data_file = Path(__file__).parent / "data" / "examples.json"
        logger.info(f"Loading examples from {data_file}")
        with open(data_file, "r") as f:
            data = json.load(f)

        examples = data.get("examples", [])
        logger.info(f"Loaded {len(examples)} examples")
        return examples
    except Exception as e:
        logger.error(f"Error loading examples: {e}")
        return []


# Load examples when the module is imported
examples = load_examples()


# Index page route
@rt("/")
def index():
    """Render the index page with a list of all examples."""
    logger.info(f"Rendering index page with {len(examples)} examples")

    # Create example links - simple list without numbering
    example_links = []
    for example in examples:
        example_links.append(
            Div(
                A(example["title"], href=f"/{example['id']}"),
                style="margin: 8px 0; line-height: 1.5;",
            )
        )

    # Create minimal page matching Go by Example style
    return Titled(
        "Gemini by Example",
        Div(
            P(
                "Gemini by Example is a hands-on introduction to Python using ",
                "annotated example programs. Check out the ",
                A("first example", href="/001-hello-world"),
                " or browse the full list below.",
                style="margin: 20px 0; color: #444; line-height: 1.6;",
            ),
            P(
                "Unless stated otherwise, examples here assume the latest Python version.",
                style="margin: 20px 0; color: #444; line-height: 1.6;",
            ),
            Div(*example_links, style="margin-top: 30px;"),
            style="max-width: 800px; margin: 40px 0 0 50px; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.5; color: #222;",
        ),
    )


# Helper function to find an example by ID
def find_example(example_id):
    for example in examples:
        if example["id"] == example_id:
            return example
    return None


# Helper function to find the next example
def find_next_example(current_order):
    for example in examples:
        if example["order"] > current_order:
            return example
    return None


# Example page route
@rt("/{example_id}")
def example_page(example_id: str):
    """Render an individual example page."""
    example = find_example(example_id)

    if not example:
        return Titled(
            "Example Not Found - Gemini by Example",
            Div(
                H1(
                    "Example Not Found",
                    style="font-size: 36px; font-weight: 500; margin-bottom: 20px; color: #333;",
                ),
                P(f"The example '{example_id}' was not found."),
                P(A("Back to index", href="/")),
                style="max-width: 800px; margin: 40px 0 0 50px; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.5; color: #222;",
            ),
        )

    # Find the next example for navigation
    next_example = find_next_example(example["order"])

    # Build page content
    content = [
        H1(
            example["title"],
            " - ",
            A(
                "Gemini by Example",
                href="/",
                style="text-decoration: none; color: #375EAB;",
            ),
            style="font-size: 36px; font-weight: 500; margin-bottom: 25px; color: #333;",
        )
    ]

    # Create table for code and annotations
    table = Div(
        style="display: table; width: 100%; border-collapse: collapse; border: 1px solid #e0e0e0; margin: 20px 0;"
    )

    # Add code segments
    for i, segment in enumerate(example["code_segments"]):
        is_last = i == len(example["code_segments"]) - 1
        border_style = "" if is_last else "border-bottom: 1px dashed #e0e0e0;"

        # Create a row
        row = Div(style="display: table-row;")

        # Left column (annotation)
        annotation = segment.get("annotation", "")
        row.children.append(
            Div(
                P(annotation) if annotation else "",
                style=f"display: table-cell; width: 55%; padding: 10px 15px; border-right: 1px solid #e0e0e0; {border_style} vertical-align: top; color: #444;",
            )
        )

        # Right column (code)
        code_text = segment.get("display_code", "").strip()
        row.children.append(
            Div(
                Pre(
                    Code(
                        code_text,
                        style="font-family: 'Menlo', 'Monaco', 'Consolas', monospace;",
                    )
                )
                if code_text
                else "",
                style=f"display: table-cell; width: 45%; padding: 10px; background-color: #f8f8f8; {border_style} vertical-align: top;",
            )
        )

        table.children.append(row)

    content.append(table)

    # Add shell commands if any
    if example["shell_segments"]:
        shell_table = Div(
            style="display: table; width: 100%; border-collapse: collapse; border: 1px solid #e0e0e0; margin: 20px 0;"
        )

        for i, segment in enumerate(example["shell_segments"]):
            is_last = i == len(example["shell_segments"]) - 1
            border_style = "" if is_last else "border-bottom: 1px dashed #e0e0e0;"

            # Create a row
            row = Div(style="display: table-row;")

            # Left column (explanation)
            explanation = segment.get("explanation", "")
            row.children.append(
                Div(
                    P(explanation) if explanation else "",
                    style=f"display: table-cell; width: 55%; padding: 10px 15px; border-right: 1px solid #e0e0e0; {border_style} vertical-align: top; color: #444;",
                )
            )

            # Right column (command and output)
            command = segment.get("command", "")
            output = segment.get("output", "")

            # Format command with special style for the prompt
            cmd_parts = []
            if command:
                cmd_parts.append(Span("$ ", style="color: #999; user-select: none;"))
                cmd_parts.append(Span(command, style="font-weight: normal;"))

            cmd_content = (
                Pre(
                    *cmd_parts,
                    "\n",
                    output,
                    style="font-family: 'Menlo', 'Monaco', 'Consolas', monospace; margin: 0;",
                )
                if command
                else ""
            )

            row.children.append(
                Div(
                    cmd_content,
                    style=f"display: table-cell; width: 45%; padding: 10px; background-color: #f8f8f8; {border_style} vertical-align: top;",
                )
            )

            shell_table.children.append(row)

        content.append(shell_table)

    # Add next example link if available
    if next_example:
        content.append(
            P(
                "Next example: ",
                A(
                    next_example["title"],
                    href=f"/{next_example['id']}",
                    style="color: #375EAB;",
                ),
                style="margin-top: 30px; font-weight: 500;",
            )
        )

    return Titled(
        f"{example['title']} - Gemini by Example",
        Div(
            *content,
            style="max-width: 800px; margin: 40px 0 0 50px; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.5; color: #222;",
        ),
    )


if __name__ == "__main__":
    serve()
