#!/usr/bin/env python3
"""
Static Site Generator for Gemini by Example.

This script generates a complete static site from the examples.json file,
following the same layout and styling as the dynamic FastHTML application.
"""

import json
import logging
import os
import shutil
from pathlib import Path
from html import escape
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Site constants
SITE_TITLE = "Gemini by Example"
SITE_DESCRIPTION = "Learn the Gemini API through annotated examples"


def load_examples() -> List[Dict[str, Any]]:
    """Load examples from the JSON file."""
    try:
        data_file = Path(__file__).parent / "data" / "examples.json"
        logger.info("Loading examples from %s" % data_file)
        with open(data_file, "r") as f:
            data = json.load(f)

        examples = data.get("examples", [])
        logger.info("Loaded %d examples" % len(examples))
        return examples
    except Exception as e:
        logger.error("Error loading examples: %s" % e)
        return []


def find_next_example(examples: List[Dict[str, Any]], current_order: int) -> Optional[Dict[str, Any]]:
    """Find the next example based on order."""
    for example in examples:
        if example["order"] > current_order:
            return example
    return None


def generate_html_head(title: str, include_main_css: bool = True, base_url: str = ".") -> str:
    """Generate HTML head section.

    Args:
        title: The page title
        include_main_css: Whether to include CSS styles
        base_url: The base URL for relative links (default: "." for current directory)
    """
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <meta name="description" content="{escape(SITE_DESCRIPTION)}">
    <script defer data-domain="geminibyexample.com" src="https://plausible.io/js/script.js"></script>
"""
    if include_main_css:
        head += """    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.5;
            color: #222;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        header {
            border-bottom: 1px solid #eee;
            padding: 15px 0;
            margin-bottom: 20px;
        }
        .site-title {
            text-decoration: none;
            color: #375EAB;
            font-weight: 500;
            font-size: 20px;
        }
        main {
            padding-bottom: 40px;
        }
        footer {
            border-top: 1px solid #eee;
            padding: 15px 0;
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }
        h1 {
            font-size: 36px;
            font-weight: 500;
            margin: 0 0 25px 0;
            color: #333;
        }
        p {
            margin: 20px 0;
            color: #444;
            line-height: 1.6;
        }
        a {
            color: #375EAB;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .example-link {
            margin: 8px 0;
            line-height: 1.5;
        }
        .row {
            display: flex;
            width: 100%;
            margin-bottom: 30px;
            gap: 30px;
        }
        .docs {
            flex: 1;
            min-width: 0;
            color: #444;
            line-height: 1.6;
        }
        .code {
            flex: 2;
            min-width: 0;
            position: relative;
        }
        pre {
            margin: 0;
            padding: 16px;
            background-color: #f8f8f8;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
        }
        .leading {
            margin-bottom: 5px;
        }
        hr {
            border: none;
            border-top: 1px solid #eee;
            margin: 20px 0;
        }
        .buttons {
            position: absolute;
            top: 5px;
            right: 5px;
            z-index: 10;
        }
        .copy {
            cursor: pointer;
            width: 18px;
            height: 18px;
            opacity: 0.6;
            color: #666;
            background-color: #f8f8f8;
            border-radius: 3px;
            padding: 3px;
        }
        .copy:hover {
            opacity: 1;
            color: #375EAB;
        }
        .tooltip {
            position: absolute;
            background: #333;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            top: -25px;
            right: 0;
        }
        .command-prompt {
            color: #888;
        }
        .command-text {
            font-weight: bold;
        }
        .next {
            margin-top: 30px;
            font-weight: 500;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        @media (max-width: 768px) {
            .row {
                flex-direction: column;
            }
            .docs, .code {
                width: 100%;
            }
        }
    </style>
"""
    head += f"""</head>
<body>
    <div class="container">
        <header>
            <a href="{base_url}/" class="site-title">Gemini by Example</a>
        </header>
        <main>
"""
    return head


def generate_html_footer() -> str:
    """Generate HTML footer section."""
    return """        </main>
        <footer>
            <p>Gemini by Example | <a href="https://github.com/strickvl/geminibyexample">Source</a> | <a href="https://mlops.systems">Blog</a></p>
        </footer>
    </div>
    <script>
        // Function to copy code to clipboard
        function copyCode(button) {
            const codeBlock = button.closest('.code').querySelector('pre');
            const code = codeBlock.textContent;
            
            // For older browsers, fallback to textarea method
            if (!navigator.clipboard) {
                const textArea = document.createElement('textarea');
                textArea.value = code;
                textArea.style.position = 'fixed';  // Avoid scrolling to bottom
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                
                try {
                    document.execCommand('copy');
                    showTooltip(button, 'Copied!');
                } catch (err) {
                    console.error('Failed to copy text: ', err);
                    showTooltip(button, 'Error!');
                }
                
                document.body.removeChild(textArea);
                return;
            }
            
            // Use clipboard API if available
            navigator.clipboard.writeText(code).then(() => {
                showTooltip(button, 'Copied!');
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                showTooltip(button, 'Error!');
            });
        }
        
        // Helper to show tooltip
        function showTooltip(button, message) {
            // Remove any existing tooltips
            const oldTooltip = button.parentElement.querySelector('.tooltip');
            if (oldTooltip) {
                oldTooltip.remove();
            }
            
            // Create and append new tooltip
            const tooltip = document.createElement('span');
            tooltip.textContent = message;
            tooltip.className = 'tooltip';
            button.parentElement.appendChild(tooltip);
            
            // Remove tooltip after 1 second
            setTimeout(() => tooltip.remove(), 1000);
        }

        // Enable keyboard navigation between examples
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey || e.altKey || e.shiftKey || e.metaKey) {
                return;
            }
            
            if (e.key === 'ArrowRight') {
                const nextLink = document.querySelector('.next a');
                if (nextLink) {
                    window.location.href = nextLink.getAttribute('href');
                }
            }
            
            if (e.key === 'ArrowLeft') {
                // We could implement previous page navigation in the future
            }
        });
    </script>
</body>
</html>
"""


def generate_index_html(examples: List[Dict[str, Any]], output_dir: Path) -> None:
    """Generate index.html page."""
    logger.info("Generating index page with %d examples" % len(examples))

    output_file = output_dir / "index.html"
    with open(output_file, "w") as f:
        f.write(generate_html_head(SITE_TITLE, base_url="."))

        # Page content
        f.write(f"""            <h1>{SITE_TITLE}</h1>
            <p style="margin: 20px 0; color: #444; line-height: 1.6;">
                Gemini by Example is a hands-on introduction to [Google's Gemini
                SDK and API](https://ai.google.dev/gemini-api/docs)
                using annotated code examples.
            </p>
            <p style="margin: 20px 0; color: #444; line-height: 1.6;">
                Check out the <a href="{examples[0]["id"]}/index.html">first example</a> 
                or browse the full list below.
            </p>
            <p style="margin: 20px 0; color: #444; line-height: 1.6;">
                Examples here assume Python >=3.9.
            </p>
            <div style="margin-top: 30px;">
""")

        # Example links
        for example in examples:
            f.write(f"""                <div class="example-link">
                    <a href="{example["id"]}/">{example["title"]}</a>
                </div>
""")

        f.write("            </div>\n")
        f.write(generate_html_footer())

    logger.info("Generated index page at %s" % output_file)


def generate_example_html(example: Dict[str, Any], examples: List[Dict[str, Any]], output_dir: Path) -> None:
    """Generate an individual example page."""
    logger.info(
        "Generating page for example: %s - %s" % (example["id"], example["title"])
    )

    # Create directory for example
    example_dir = output_dir / example["id"]
    example_dir.mkdir(exist_ok=True, parents=True)

    # Create index.html in the example directory
    output_file = example_dir / "index.html"

    # Find the next example
    next_example = find_next_example(examples, example["order"])

    with open(output_file, "w") as f:
        f.write(generate_html_head(f"{example['title']} - {SITE_TITLE}", base_url=".."))

        # Page title
        f.write(f"""            <h1>{example["title"]}</h1>
""")

        # Description if available
        if example.get("description"):
            f.write(f"""            <p style="margin: 20px 0 40px 0; color: #444; line-height: 1.6; font-size: 1.1em;">
                {example["description"]}
            </p>
""")

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
                f.write("""            <hr>
""")

            # Process segments in this section
            for segment in section["segments"]:
                combined_annotation = ""
                if section["header"]:
                    combined_annotation += f"<div style='font-size: 0.9em; color: #666;'>{section['header']}</div>\n"

                annotation = segment.get("annotation", "")
                if annotation:
                    combined_annotation += annotation

                code_text = segment.get("display_code", "").strip()

                # If there's no code or annotation, skip
                if not code_text and not combined_annotation:
                    continue

                # Start row
                f.write("""            <div class="row">
""")

                # Left column (annotation)
                if combined_annotation:
                    f.write(f"""                <div class="docs">
                    {combined_annotation}
                </div>
""")

                # Right column (code)
                if code_text:
                    f.write(f"""                <div class="code">
                    <div class="buttons">
                        <svg class="copy" title="Copy code" onclick="copyCode(this)" width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M16 1H4C2.9 1 2 1.9 2 3V17H4V3H16V1ZM19 5H8C6.9 5 6 5.9 6 7V21C6 22.1 6.9 23 8 23H19C20.1 23 21 22.1 21 21V7C21 5.9 20.1 5 19 5ZM19 21H8V7H19V21Z" fill="currentColor"/>
                        </svg>
                    </div>
                    <pre><code>{escape(code_text)}</code></pre>
                </div>
""")

                # End row
                f.write("""            </div>
""")

        # Shell segments if available
        shell_segments = example.get("shell_segments", [])
        if shell_segments:
            f.write("""            <hr>
            <h2>Running the Example</h2>
""")

            for segment in shell_segments:
                explanation = segment.get("explanation", "")
                command = segment.get("command", "")
                output = segment.get("output", "")

                f.write("""            <div class="row">
""")

                # Left column (explanation)
                if explanation:
                    f.write(f"""                <div class="docs">
                    <p>{escape(explanation)}</p>
                </div>
""")

                # Right column (command + output)
                f.write(f"""                <div class="code">
                    <div class="buttons">
                        <svg class="copy" title="Copy command" onclick="copyCode(this)" width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M16 1H4C2.9 1 2 1.9 2 3V17H4V3H16V1ZM19 5H8C6.9 5 6 5.9 6 7V21C6 22.1 6.9 23 8 23H19C20.1 23 21 22.1 21 21V7C21 5.9 20.1 5 19 5ZM19 21H8V7H19V21Z" fill="currentColor"/>
                        </svg>
                    </div>
                    <pre><code><span><span class="command-prompt">$ </span><span class="command-text">{escape(command)}</span></span>
{escape(output)}</code></pre>
                </div>
""")

                f.write("""            </div>
""")

        # Next example link
        if next_example:
            f.write(f"""            <p class="next">
                Next example: <a href="../{next_example["id"]}/">{next_example["title"]}</a>
            </p>
""")

        f.write(generate_html_footer())

    logger.info("Generated example page at %s" % output_file)


def copy_static_files(source_dir: Path, output_dir: Path) -> None:
    """Copy static files to the output directory."""
    target_dir = output_dir / "static"

    # Create target directory
    target_dir.mkdir(exist_ok=True, parents=True)

    # Copy static files
    if source_dir.exists():
        logger.info("Copying static files from %s to %s" % (source_dir, target_dir))
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
    else:
        logger.warning("Static directory %s does not exist" % source_dir)


def generate_static_site() -> None:
    """Generate the complete static site."""
    examples = load_examples()
    if not examples:
        logger.error("No examples found. Exiting.")
        return

    script_dir = Path(__file__).parent
    output_dir = script_dir / "docs"
    static_dir = script_dir / "static"

    # Create output directory
    output_dir.mkdir(exist_ok=True, parents=True)
    logger.info("Generating static site in %s" % output_dir)

    # Copy static files
    copy_static_files(static_dir, output_dir)

    # Generate index page
    generate_index_html(examples, output_dir)

    # Generate example pages
    for example in examples:
        generate_example_html(example, examples, output_dir)

    logger.info(
        "Static site generation complete! The site is available at %s" % output_dir
    )


if __name__ == "__main__":
    generate_static_site()
