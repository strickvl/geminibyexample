from fasthtml.common import *


def layout(title, content):
    """
    Main layout template for Gemini by Example.

    Args:
        title: Page title
        content: Main content for the page

    Returns:
        FastHTML Titled component with the complete page layout
    """
    return Titled(
        title,
        Div(
            children=[
                # Header
                Header(A("Gemini by Example", class_="site-title", href="/")),
                # Main content
                Main(content),
                # Footer
                Footer(
                    P(
                        "Gemini by Example | ",
                        A(
                            "Source",
                            href="https://github.com/yourusername/geminibyexample",
                        ),
                        " | ",
                        A("License", href="#license"),
                    )
                ),
                # Links to CSS and JavaScript
                Link(rel="stylesheet", href="/static/css/style.css"),
                Script(src="/static/js/script.js"),
            ],
            class_="container",
        ),
    )
