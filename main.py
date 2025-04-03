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
            style="max-width: 800px; margin: 40px 0 0 50px; padding: 0 0 50px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.5; color: #222;",
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
    logger.info(f"Loading example page for ID: {example_id}")
    example = find_example(example_id)

    if not example:
        logger.warning(f"Example not found: {example_id}")
        return Titled(
            "Example Not Found - Gemini by Example",
            Div(
                # Navigation header with site title
                Div(
                    Div(
                        A(
                            "Gemini by Example",
                            href="/",
                            style="text-decoration: none; color: #375EAB; font-weight: 500; font-size: 20px;",
                        ),
                        style="margin-bottom: 10px;",
                    ),
                    H1(
                        "Example Not Found",
                        style="font-size: 36px; font-weight: 500; margin: 15px 0 25px 0; color: #333;",
                    ),
                    style="border-bottom: 1px solid #eee; padding-bottom: 15px; margin-bottom: 25px;",
                ),
                P(f"The example '{example_id}' was not found."),
                P(A("Back to index", href="/")),
                style="max-width: 800px; margin: 40px 0 0 50px; padding: 0 0 50px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.5; color: #222;",
            ),
        )

    logger.info(f"Example found: {example['title']} (Order: {example['order']})")

    # Find the next example for navigation
    next_example = find_next_example(example["order"])
    if next_example:
        logger.info(f"Next example: {next_example['title']}")
    else:
        logger.info("No next example found")

    # Build page content
    logger.info("Building page content")

    # Main content wrapper
    main_content = Div(
        # Navigation header
        Div(
            A(
                "Gemini by Example",
                href="/",
                style="text-decoration: none; color: #375EAB; font-weight: 500; font-size: 20px;",
            ),
            style="margin-bottom: 10px;",
        ),
        # Main title
        H1(
            example["title"],
            style="font-size: 36px; font-weight: 500; margin: 0 0 25px 0; color: #333;",
        ),
        style="max-width: 800px; margin: 40px 0 0 50px; padding: 0 0 50px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.5; color: #222;",
    )

    # Process code segments
    logger.info(f"Processing {len(example['code_segments'])} code segments")
    code_blocks = []

    # Build content sections
    for i, segment in enumerate(example["code_segments"]):
        annotation = segment.get("annotation", "")
        code_text = segment.get("display_code", "").strip()

        # Skip completely empty rows
        if not annotation and not code_text:
            logger.debug(f"Skipping empty segment {i+1}")
            continue

        is_annotation_only = bool(annotation and not code_text)

        if is_annotation_only:
            # For annotation-only segments, add a regular paragraph
            code_blocks.append(
                P(annotation, style="margin: 20px 0; color: #444; line-height: 1.6;")
            )
        else:
            # For code segments, create a two-column layout
            code_blocks.append(
                Div(
                    # Left column - explanation
                    Div(
                        P(annotation) if annotation else "",
                        style="width: 55%; padding-right: 20px; vertical-align: top; display: table-cell; color: #444; line-height: 1.6;",
                    ),
                    # Right column - code
                    Div(
                        Pre(
                            Code(
                                code_text,
                                style="font-family: 'Menlo', 'Monaco', 'Consolas', monospace;",
                            ),
                            style="margin: 0; padding: 10px; background-color: #f8f8f8; border-radius: 5px;",
                        ),
                        style="width: 45%; display: table-cell; vertical-align: top;",
                    ),
                    style="display: table; width: 100%; margin: 15px 0; border-top: 1px solid #eee; padding-top: 15px;",
                )
            )

    # Add code blocks to content
    for block in code_blocks:
        main_content.children = (*main_content.children, block)

    # Process shell segments if any
    shell_segments = example.get("shell_segments", [])
    if shell_segments:
        logger.info(f"Processing {len(shell_segments)} shell segments")

        for i, segment in enumerate(shell_segments):
            explanation = segment.get("explanation", "")
            command = segment.get("command", "")
            output = segment.get("output", "")

            # Format shell section
            shell_block = Div(
                # Left column - explanation
                Div(
                    P(explanation) if explanation else "",
                    style="width: 55%; padding-right: 20px; vertical-align: top; display: table-cell; color: #444; line-height: 1.6;",
                ),
                # Right column - command and output
                Div(
                    Pre(
                        Span("$ ", style="color: #999; user-select: none;"),
                        Span(command, style="font-weight: normal;") if command else "",
                        "\n" if command and output else "",
                        output,
                        style="margin: 0; padding: 10px; background-color: #f8f8f8; border-radius: 5px; font-family: 'Menlo', 'Monaco', 'Consolas', monospace;",
                    ),
                    style="width: 45%; display: table-cell; vertical-align: top;",
                ),
                style="display: table; width: 100%; margin: 15px 0; border-top: 1px solid #eee; padding-top: 15px;",
            )

            main_content.children = (*main_content.children, shell_block)

    # Add next example link if available
    if next_example:
        logger.info("Adding next example link")
        main_content.children = (
            *main_content.children,
            P(
                "Next example: ",
                A(
                    next_example["title"],
                    href=f"/{next_example['id']}",
                    style="color: #375EAB;",
                ),
                style="margin-top: 30px; font-weight: 500; padding-top: 15px; border-top: 1px solid #eee;",
            ),
        )

    logger.info("Returning final page content")
    # Set the browser title but don't duplicate the H1 on the page
    return Title(f"{example['title']} - Gemini by Example"), main_content


if __name__ == "__main__":
    serve()
