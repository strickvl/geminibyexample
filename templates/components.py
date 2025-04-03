from fasthtml.common import *
from typing import List, Dict, Any, Optional


def example_link(example: Dict[str, Any]) -> Div:
    """
    Create a link to an example for the index page.

    Args:
        example: Dictionary containing example data

    Returns:
        FastHTML Div component with the example link
    """
    return Div(
        class_="example-link", children=[A(example["title"], href=f"/{example['id']}")]
    )


def code_segment(segment: Dict[str, Any], is_last: bool = False) -> Div:
    """
    Create a code segment row with annotation and code.

    Args:
        segment: Dictionary containing segment data
        is_last: Whether this is the last segment in a container

    Returns:
        FastHTML Div component with the segment row
    """
    # Create the annotation section (left column)
    annotation = segment.get("annotation", "")
    docs_div = Div(class_="docs")
    if annotation:
        docs_div.children.append(P(annotation))

    # Create the code section (right column)
    code_text = segment.get("display_code", "").strip()
    code_class = "code" + ("" if is_last else " leading")

    code_children = []
    if code_text:
        code_children.append(
            Div(
                class_="buttons",
                children=[
                    Img(
                        class_="copy",
                        title="Copy code",
                        src="/static/img/clipboard.png",
                        onclick="copyCode(this)",
                    )
                ],
            )
        )
        code_children.append(Pre(Code(code_text)))

    code_div = Div(class_=code_class, children=code_children)

    # Combine into a row
    return Div(class_="row", children=[docs_div, code_div])


def shell_segment(segment: Dict[str, Any], is_last: bool = False) -> Div:
    """
    Create a shell command segment row with command and output.

    Args:
        segment: Dictionary containing shell segment data
        is_last: Whether this is the last segment in a container

    Returns:
        FastHTML Div component with the shell segment row
    """
    # Create the explanation section (left column)
    explanation = segment.get("explanation", "")
    docs_div = Div(class_="docs")
    if explanation:
        docs_div.children.append(P(explanation))

    # Create the command+output section (right column)
    command = segment.get("command", "")
    output = segment.get("output", "")

    # Format command with a prompt and style
    formatted_command = Span(
        children=[
            Span("$ ", class_="command-prompt"),
            Span(command, class_="command-text"),
        ]
    )

    # Create the full code block with command and output
    code_content = Pre(Code(children=[formatted_command, "\n", output]))

    code_div = Div(
        class_="code" + ("" if is_last else " leading"),
        children=[
            Div(
                class_="buttons",
                children=[
                    Img(
                        class_="copy",
                        title="Copy command",
                        src="/static/img/clipboard.png",
                        onclick="copyCode(this)",
                    )
                ],
            ),
            code_content,
        ],
    )

    # Combine into a row
    return Div(class_="row", children=[docs_div, code_div])
