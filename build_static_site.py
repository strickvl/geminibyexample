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
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Site constants
SITE_TITLE = "Gemini by Example"
SITE_DESCRIPTION = "Learn the Gemini API through annotated examples"


def load_examples_data() -> Dict[str, Any]:
    """Load examples and sections from the JSON file."""
    try:
        data_file = Path(__file__).parent / "data" / "examples.json"
        logger.info("Loading examples from %s" % data_file)
        with open(data_file, "r") as f:
            data = json.load(f)

        examples = data.get("examples", [])
        sections = data.get("sections", [])
        logger.info(
            "Loaded %d examples and %d sections" % (len(examples), len(sections))
        )
        return {"examples": examples, "sections": sections}
    except Exception as e:
        logger.error("Error loading examples: %s" % e)
        return {"examples": [], "sections": []}


def load_examples() -> List[Dict[str, Any]]:
    """Load examples from the JSON file (backward compatibility)."""
    return load_examples_data().get("examples", [])


def find_next_example(
    examples: List[Dict[str, Any]], current_example: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Find the next example based on the example order and section.
    This function respects section organization, continuing to the next section when needed.

    Args:
        examples: List of all examples
        current_example: The current example

    Returns:
        The next example or None if there is no next example
    """
    current_order = current_example["order"]
    current_section_id = current_example.get("section_id")

    # First, try to find the next example in the same section
    if current_section_id:
        same_section_examples = [
            e for e in examples if e.get("section_id") == current_section_id
        ]
        for example in sorted(same_section_examples, key=lambda e: e["order"]):
            if example["order"] > current_order:
                return example

    # If we're at the end of a section or there's no section info,
    # find the next example in any section
    for example in sorted(examples, key=lambda e: e["order"]):
        if example["order"] > current_order:
            return example

    return None


def generate_html_head(
    title: str, include_main_css: bool = True, base_url: str = "."
) -> str:
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
            max-width: 900px;
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
    """Generate HTML footer section with current date."""
    from datetime import datetime

    current_date = datetime.now().strftime("%B %d, %Y")

    return (
        """        </main>
        <footer>
            <p>by <a href="https://linkedin.com/in/strickvl">Alex Strick van Linschoten</a> | <a href="https://mlops.systems">Blog</a> | <a href="https://github.com/strickvl/geminibyexample">Source</a> | <span style="color: #888; font-size: 0.9em;">Last updated: """
        + current_date
        + """</span></p>
        </footer>
    </div>
    <script>
        // Function to copy code to clipboard
        function copyCode(button) {
            const codeBlock = button.closest('.code').querySelector('pre');
            const code = codeBlock.textContent;
            copyToClipboard(code, button);
        }
        
        // Function to copy all Python code
        document.addEventListener('DOMContentLoaded', function() {
            const copyAllButton = document.getElementById('copy-all-python');
            if (copyAllButton) {
                copyAllButton.addEventListener('click', function() {
                    const allCodeElement = document.getElementById('all-python-code');
                    const code = allCodeElement.textContent;
                    copyToClipboard(code, copyAllButton);
                });
            }
        });
        
        // Shared function to copy text and show tooltip
        function copyToClipboard(text, element) {
            // For older browsers, fallback to textarea method
            if (!navigator.clipboard) {
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';  // Avoid scrolling to bottom
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                
                try {
                    document.execCommand('copy');
                    showTooltip(element, 'Copied!');
                } catch (err) {
                    console.error('Failed to copy text: ', err);
                    showTooltip(element, 'Error!');
                }
                
                document.body.removeChild(textArea);
                return;
            }
            
            // Use clipboard API if available
            navigator.clipboard.writeText(text).then(() => {
                showTooltip(element, 'Copied!');
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                showTooltip(element, 'Error!');
            });
        }
        
        // Helper to show tooltip
        function showTooltip(element, message) {
            // Check if there's already a tooltip
            let tooltip = element.parentElement.querySelector('.tooltip');
            if (tooltip) {
                tooltip.textContent = message;
            } else {
                // Create and append new tooltip
                tooltip = document.createElement('span');
                tooltip.textContent = message;
                tooltip.className = 'tooltip';
                tooltip.style.position = 'absolute';
                tooltip.style.background = '#333';
                tooltip.style.color = 'white';
                tooltip.style.padding = '2px 8px';
                tooltip.style.borderRadius = '4px';
                tooltip.style.fontSize = '12px';
                tooltip.style.top = '-25px';
                tooltip.style.right = '0';
                
                // Make sure the parent has position relative for tooltip positioning
                if (getComputedStyle(element.parentElement).position === 'static') {
                    element.parentElement.style.position = 'relative';
                }
                
                element.parentElement.appendChild(tooltip);
            }
            
            // Remove tooltip after 1.5 seconds
            setTimeout(() => tooltip.remove(), 1500);
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
                const prevLink = document.querySelector('.prev a');
                if (prevLink) {
                    window.location.href = prevLink.getAttribute('href');
                }
            }
        });
    </script>
</body>
</html>
"""
    )


def generate_index_html(
    examples: List[Dict[str, Any]], sections: List[Dict[str, Any]], output_dir: Path
) -> None:
    """Generate index.html page with section grouping."""
    logger.info(
        "Generating index page with %d examples and %d sections"
        % (len(examples), len(sections))
    )

    output_file = output_dir / "index.html"
    with open(output_file, "w") as f:
        f.write(generate_html_head(SITE_TITLE, base_url="."))

        # Page content
        f.write(f"""            <h1>{SITE_TITLE}</h1>
            <p style="margin: 20px 0; color: #444; line-height: 1.6;">
                Gemini is Google's most capable AI model for generating text, code, images, and more. Please visit the <a href="https://ai.google.dev/gemini-api/docs" target="_blank">official documentation</a> to learn more.
            </p>
            <p style="margin: 20px 0; color: #444; line-height: 1.6;">
                Gemini by Example is a hands-on introduction to Google's Gemini SDK and API using annotated code examples. Check out the <a href="{examples[0]["id"]}/">first example</a> 
                or browse the full list of sections below.
            </p>
            <p style="margin: 20px 0; color: #444; line-height: 1.6;">
                Examples here assume Python <code>&gt;=3.9</code> and
                the latest version of the Gemini SDK/API (the <a href="https://pypi.org/project/google-genai/" target="_blank"><code>google-genai</code></a> package).
                Try to upgrade to the latest versions if something isn't working.
            </p>
            <div style="margin-top: 30px;">
""")

        # If we have sections defined, group examples by section
        if sections:
            # Group examples by section_id
            examples_by_section = {}
            for example in examples:
                section_id = example.get("section_id", "999-misc")
                if section_id not in examples_by_section:
                    examples_by_section[section_id] = []
                examples_by_section[section_id].append(example)

            # Display sections and their examples
            for section in sorted(sections, key=lambda s: s["order"]):
                section_examples = examples_by_section.get(section["id"], [])
                if not section_examples:
                    continue

                # Section header
                f.write(f"""                <h2 style="margin-top: 40px; margin-bottom: 15px; color: #333;">{section["title"]}</h2>
""")
                # Only include description paragraph if it's not empty
                description = section.get("description", "")
                if description:
                    f.write(f"""                <p style="margin: 0 0 20px 0; color: #555;">{description}</p>
""")

                # Example links for this section
                for example in sorted(section_examples, key=lambda e: e["order"]):
                    f.write(f"""                <div class="example-link">
                        <a href="{example["id"]}/">{example["title"]}</a>
                    </div>
""")
        else:
            # Fallback to flat list if no sections
            for example in examples:
                f.write(f"""                <div class="example-link">
                        <a href="{example["id"]}/">{example["title"]}</a>
                    </div>
""")

        f.write("            </div>\n")
        f.write(generate_html_footer())

    logger.info("Generated index page at %s" % output_file)


def copy_example_images(
    example: Dict[str, Any], project_root: Path, output_dir: Path
) -> None:
    """
    Copy images from the example directory to the output directory.

    Args:
        example: The example data
        project_root: Project root path
        output_dir: Output directory for the example
    """
    image_data = example.get("image_data", [])
    if not image_data:
        return

    # Create images directory in the example output directory
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True, parents=True)

    # Copy each image
    for image in image_data:
        src_path = project_root / image["path"]
        dst_path = images_dir / image["filename"]

        if src_path.exists():
            try:
                shutil.copy2(src_path, dst_path)
                logger.info(f"Copied image {src_path} to {dst_path}")
            except Exception as e:
                logger.error(f"Failed to copy image {src_path}: {e}")
        else:
            logger.warning(f"Image file not found: {src_path}")


def generate_example_html(
    example: Dict[str, Any], examples: List[Dict[str, Any]], output_dir: Path
) -> None:
    """Generate an individual example page."""
    logger.info(
        "Generating page for example: %s - %s" % (example["id"], example["title"])
    )

    # Create directory for example
    example_dir = output_dir / example["id"]
    example_dir.mkdir(exist_ok=True, parents=True)

    # Copy images if any
    script_dir = Path(__file__).parent
    copy_example_images(example, script_dir, example_dir)

    # Create index.html in the example directory
    output_file = example_dir / "index.html"

    # Find the next example
    next_example = find_next_example(examples, example)

    with open(output_file, "w") as f:
        f.write(generate_html_head(f"{example['title']} - {SITE_TITLE}", base_url=".."))

        # Collect all Python code for the "Copy All" button first
        all_python_code = ""
        for segment in example["code_segments"]:
            code_text = segment.get("display_code", "").strip()
            if code_text:
                all_python_code += code_text + "\n"

        # Section and page title with "Copy All" button
        section_title = example.get("section_title", "")

        # Header container with flexbox to position title and button
        f.write("""            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <div>
""")

        # Title part
        if section_title:
            f.write(f"""                    <div style="margin-bottom: 10px; color: #666; font-size: 0.9em;">
                        <a href="../" style="text-decoration: none; color: #666;">{section_title}</a>
                    </div>
                    <h1 style="margin: 0; margin-bottom: 10px;">{example["title"]}</h1>
""")
        else:
            f.write(f"""                    <h1 style="margin: 0; margin-bottom: 10px;">{example["title"]}</h1>
""")

        f.write("""                </div>
""")

        # Button part (if we have Python code)
        if all_python_code:
            f.write("""                <div style="position: relative; margin-top: 10px;">
                    <button id="copy-all-python" style="background-color: #f1f8ff; border: 1px solid #c8e1ff; border-radius: 6px; padding: 6px 12px; font-size: 14px; color: #0366d6; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M16 1H4C2.9 1 2 1.9 2 3V17H4V3H16V1ZM19 5H8C6.9 5 6 5.9 6 7V21C6 22.1 6.9 23 8 23H19C20.1 23 21 22.1 21 21V7C21 5.9 20.1 5 19 5ZM19 21H8V7H19V21Z" fill="currentColor"/>
                        </svg>
                        Copy All Python
                    </button>
                    <div id="all-python-code" style="display: none;">{escape(all_python_code)}</div>
                </div>
""")

        # Close header container
        f.write("""            </div>
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

                # Right column (code) - without individual copy buttons
                if code_text:
                    f.write(f"""                <div class="code">
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

        # Images section if available
        image_data = example.get("image_data", [])
        if image_data:
            f.write("""            <hr>
""")

            for image in image_data:
                filename = image.get("filename", "")

                # Create a figure with the image
                f.write(f"""            <div style="margin: 30px 0; text-align: center;">
                <figure>
                    <img src="images/{filename}" alt="An illustration or output
                    from the example code" style="max-width: 100%; border: 1px solid #eee;
                    border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <figcaption style="margin-top: 10px; color: #666; font-style: italic;"></figcaption>
                </figure>
            </div>
""")

        # Documentation links section if available
        documentation_links = example.get("documentation_links", [])
        if documentation_links:
            f.write("""            <hr>
            <h3>For More Information</h3>
            <p>See the original documentation:</p>
            <ul>
""")
            for link in documentation_links:
                f.write(f"""                <li><a href="{link}" target="_blank">{link}</a></li>
""")
            f.write("""            </ul>
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


def extract_code_from_example(example: Dict[str, Any]) -> str:
    """Extract all Python code from an example's code segments."""
    code = ""
    for segment in example.get("code_segments", []):
        if segment.get("display_code", "").strip():
            code += segment.get("display_code", "").strip() + "\n"
    return code.strip()


def extract_shell_from_example(example: Dict[str, Any]) -> str:
    """Extract shell commands and outputs from an example."""
    shell = ""
    for segment in example.get("shell_segments", []):
        cmd = segment.get("command", "").strip()
        out = segment.get("output", "").strip()
        if cmd:
            shell += f"$ {cmd}\n"
            if out:
                shell += f"{out}\n"
    return shell.strip()


def generate_llms_txt(
    examples: List[Dict[str, Any]], sections: List[Dict[str, Any]], output_dir: Path
) -> None:
    """Generate llms.txt file with organized headers and full example code."""
    logger.info("Generating llms.txt")

    output_file = output_dir / "llms.txt"

    # Group examples by section
    examples_by_section = {}
    for example in examples:
        section_id = example.get("section_id", "999-misc")
        if section_id not in examples_by_section:
            examples_by_section[section_id] = []
        examples_by_section[section_id].append(example)

    with open(output_file, "w") as f:
        # Main heading and introduction
        f.write("# Gemini by Example\n\n")
        f.write(
            "This file contains all examples from the Gemini by Example site (geminibyexample.com).\n"
        )
        f.write(
            "It's organized by sections, with each example's Python code and terminal commands included.\n\n"
        )

        # Table of contents
        f.write("## Table of Contents\n\n")
        for section in sorted(sections, key=lambda s: s["order"]):
            section_examples = examples_by_section.get(section["id"], [])
            if not section_examples:
                continue

            f.write(f"* {section['title']}\n")
            for example in sorted(section_examples, key=lambda e: e["order"]):
                f.write(f"  * {example['title']}\n")
        f.write("\n")

        # Each section with its examples
        for section in sorted(sections, key=lambda s: s["order"]):
            section_examples = examples_by_section.get(section["id"], [])
            if not section_examples:
                continue

            # Section heading
            f.write(f"## {section['title']}\n\n")

            # Section description if available
            if section.get("description"):
                f.write(f"{section['description']}\n\n")

            # Each example in the section
            for example in sorted(section_examples, key=lambda e: e["order"]):
                # Example heading
                f.write(f"### {example['title']}\n\n")

                # Example description if available
                if example.get("description"):
                    f.write(f"{example['description']}\n\n")

                # Python code
                python_code = extract_code_from_example(example)
                if python_code:
                    f.write("```python\n")
                    f.write(python_code)
                    f.write("\n```\n\n")

                # Shell commands and output
                shell_code = extract_shell_from_example(example)
                if shell_code:
                    f.write("```shell\n")
                    f.write(shell_code)
                    f.write("\n```\n\n")

                # Image references if any
                if example.get("image_data"):
                    f.write(
                        "*This example includes images which can be viewed on the website.*\n\n"
                    )
                
                # Documentation links if any
                documentation_links = example.get("documentation_links", [])
                if documentation_links:
                    f.write("For more information, see the original documentation:\n")
                    for link in documentation_links:
                        f.write(f"- {link}\n")
                    f.write("\n")

    logger.info(f"Generated llms.txt at {output_file}")


def clean_docs_directory(output_dir: Path) -> None:
    """
    Clean up old files and example directories in the docs directory.

    Preserves important files like CNAME, .nojekyll, etc.

    Args:
        output_dir: Path to the docs directory
    """
    logger.info("Cleaning up old example directories and files in %s" % output_dir)

    # Files to preserve (never delete these)
    preserve_files = {
        "CNAME",  # Custom domain configuration
        ".nojekyll",  # GitHub Pages configuration
        ".gitignore",  # Git ignore file
    }

    # Directories to preserve (never delete these)
    preserve_dirs = {
        "static"  # Static assets directory
    }

    # Remove index.html
    index_file = output_dir / "index.html"
    if index_file.exists():
        index_file.unlink()
        logger.info("Removed %s" % index_file)

    # Remove llms.txt
    llms_file = output_dir / "llms.txt"
    if llms_file.exists():
        llms_file.unlink()
        logger.info("Removed %s" % llms_file)

    # Remove all example directories (folders that match the pattern \d{3}-*)
    for item in output_dir.iterdir():
        if item.is_dir() and item.name not in preserve_dirs:
            # Check if it's an example directory (matches pattern 001-*, 002-*, etc.)
            if re.match(r"^\d{3}-", item.name):
                shutil.rmtree(item)
                logger.info("Removed directory %s" % item)


def generate_static_site() -> None:
    """Generate the complete static site."""
    data = load_examples_data()
    examples = data.get("examples", [])
    sections = data.get("sections", [])

    if not examples:
        logger.error("No examples found. Exiting.")
        return

    script_dir = Path(__file__).parent
    output_dir = script_dir / "docs"
    static_dir = script_dir / "static"

    # Create output directory
    output_dir.mkdir(exist_ok=True, parents=True)
    logger.info("Generating static site in %s" % output_dir)

    # Clean up old files and directories
    clean_docs_directory(output_dir)

    # Copy static files
    copy_static_files(static_dir, output_dir)

    # Generate llms.txt file
    generate_llms_txt(examples, sections, output_dir)

    # Generate index page
    generate_index_html(examples, sections, output_dir)

    # Generate example pages
    for example in examples:
        generate_example_html(example, examples, output_dir)

    logger.info(
        "Static site generation complete! The site is available at %s" % output_dir
    )


if __name__ == "__main__":
    # First run the examples builder by importing it directly
    logger.info("Running examples builder first...")
    import sys

    # Add the build_examples directory to sys.path if needed
    build_examples_dir = Path(__file__).parent / "build_examples"
    if str(build_examples_dir) not in sys.path:
        sys.path.append(str(build_examples_dir))

    # Import and run the main function from build_examples
    from build_examples import main as build_examples_main

    build_examples_main()

    # Then generate the static site
    generate_static_site()
