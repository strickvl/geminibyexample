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
        style="max-width: 1200px; margin: 40px auto; padding: 0 20px 50px 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.5; color: #222;",
    )

    # Process code segments
    logger.info(f"Processing {len(example['code_segments'])} code segments")

    # We now rely on the build script to parse the first comment block
    # as the page intro text. So no need to remove the first code segment here.
    # Instead, we'll just check if example["description"] has content and render it.
    if example.get("description"):
        main_content.children = (
            *main_content.children,
            P(
                example["description"],
                style="margin: 20px 0 40px 0; color: #444; line-height: 1.6; font-size: 1.1em;",
            ),
        )

    # Create a container for the two-column layout
    content_container = Div(style="width: 100%;")
    main_content.children = (*main_content.children, content_container)

    # Group segments by section headers
    sections = []
    current_section = None
    current_segments = []

    for segment in example["code_segments"]:
        annotation = segment.get("annotation", "")
        code_text = segment.get("display_code", "").strip()

        # Skip completely empty segments
        if not annotation and not code_text:
            continue

        # If annotation with no code, it's a section header
        if annotation and not code_text:
            # Add previous section if exists
            if current_section:
                sections.append(
                    {"header": current_section, "segments": current_segments}
                )

            # Start a new section
            current_section = annotation
            current_segments = []
        else:
            # Add to current section
            current_segments.append(segment)

    # Add the final section
    if current_section and current_segments:
        sections.append({"header": current_section, "segments": current_segments})

    # Process each section
    for i, section in enumerate(sections):
        # Add divider if not first section
        if i > 0:
            content_container.children = (
                *content_container.children,
                Hr(style="border: none; border-top: 1px solid #eee; margin: 20px 0;"),
            )

        # We'll combine the header with the annotation for each segment
        for segment in section["segments"]:
            combined_annotation = ""
            if section["header"]:
                combined_annotation += f"{section['header']}\n"
            annotation = segment.get("annotation", "")
            if annotation:
                combined_annotation += annotation

            code_text = segment.get("display_code", "").strip()

            # If there's no code or annotation, skip
            if not code_text and not combined_annotation:
                continue

            # Create the row for two-column layout
            example_row = Div(
                style="display: flex; width: 100%; margin-bottom: 30px; gap: 30px;",
                class_="example-row",
            )

            # Left col is annotation
            if combined_annotation:
                left_col = Div(
                    NotStr(combined_annotation),
                    style="flex: 1; min-width: 0; color: #444; line-height: 1.6;",
                    class_="example-col",
                )
                example_row.children = (left_col,)

            # Right col is code
            if code_text:
                right_col = Div(
                    Pre(
                        Code(
                            code_text,
                            style="font-family: 'Menlo', 'Monaco', 'Consolas', monospace;",
                        ),
                        style="margin: 0; padding: 16px; background-color: #f8f8f8; border-radius: 5px; overflow-x: auto;",
                    ),
                    style="flex: 2; min-width: 0;",
                    class_="example-col",
                )
                if hasattr(example_row, "children"):
                    example_row.children = (*example_row.children, right_col)
                else:
                    example_row.children = (right_col,)

            content_container.children = (*content_container.children, example_row)

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
    # Add stylesheet for better two-column layout
    head_content = [
        Title(f"{example['title']} - Gemini by Example"),
        Style("""
            @media (max-width: 768px) {
                .example-row {
                    flex-direction: column !important;
                }
                .example-col {
                    width: 100% !important;
                }
            }
        """),
    ]

    # Return both head content and main content
    return head_content, main_content


if __name__ == "__main__":
    serve()