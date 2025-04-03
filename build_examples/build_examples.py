#!/usr/bin/env python3
"""
Build script for Gemini by Example.

This script processes example directories containing source files (Python code,
shell commands, annotations) and compiles them into an optimised data format (JSON).
"""

import os
import json
import re
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def scan_examples_directory(examples_dir: Path) -> List[Path]:
    """
    Scan the examples directory for example folders.

    Args:
        examples_dir: Path to the examples directory

    Returns:
        List of paths to example directories
    """
    example_dirs = []
    for item in os.listdir(examples_dir):
        item_path = examples_dir / item
        if item_path.is_dir() and re.match(r"^\d+", item):
            example_dirs.append(item_path)

    # Sort by the numeric prefix
    example_dirs.sort(key=lambda p: int(p.name.split("-")[0]))
    return example_dirs


def extract_python_segments(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract code segments and annotations from a Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        List of dictionaries containing segment data
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    segments = []
    current_segment = None
    line_number = 1

    # Process each line
    for i, line in enumerate(lines):
        stripped = line.rstrip()

        # Check if this is a comment line
        is_comment = stripped.lstrip().startswith("#")

        # Start a new segment if necessary
        if current_segment is None or current_segment["is_comment"] != is_comment:
            # Save the current segment if it exists
            if current_segment is not None:
                current_segment["line_range"] = (
                    current_segment["start_line"],
                    line_number - 1,
                )
                segments.append(current_segment)

            # Start a new segment
            current_segment = {
                "code": line,
                "display_code": "" if is_comment else line,
                "annotation": stripped.lstrip("# ") if is_comment else "",
                "is_comment": is_comment,
                "start_line": line_number,
            }
        else:
            # Continue the current segment
            current_segment["code"] += line
            if not is_comment:
                current_segment["display_code"] += line
            elif stripped.lstrip().startswith("#"):
                # Append to annotation for multi-line comments
                if current_segment["annotation"]:
                    current_segment["annotation"] += "\n"
                current_segment["annotation"] += stripped.lstrip("# ")

        line_number += 1

    # Add the last segment
    if current_segment is not None:
        current_segment["line_range"] = (current_segment["start_line"], line_number - 1)
        segments.append(current_segment)

    # Map comments to code
    map_comments_to_code(segments)

    return segments


def map_comments_to_code(segments: List[Dict[str, Any]]) -> None:
    """
    Determine which code blocks each comment should align with.
    Modifies the segments list in place.

    Args:
        segments: List of segment dictionaries
    """
    for i, segment in enumerate(segments):
        if segment["is_comment"]:
            # Look for the next code segment
            next_code_index = None
            for j in range(i + 1, len(segments)):
                if not segments[j]["is_comment"]:
                    next_code_index = j
                    break

            if next_code_index is not None:
                # Found a code segment after this comment
                next_code = segments[next_code_index]
                segment["target_line_range"] = next_code["line_range"]
            elif i > 0 and not segments[i - 1]["is_comment"]:
                # No code after, but there's code before
                segment["target_line_range"] = segments[i - 1]["line_range"]
            else:
                # No related code found
                segment["target_line_range"] = segment["line_range"]


def extract_shell_segments(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract command and output segments from a shell file.

    Args:
        file_path: Path to the shell file

    Returns:
        List of dictionaries containing shell segment data
    """
    with open(file_path, "r") as f:
        content = f.read()

    segments = []

    # Extract commands and their outputs
    # Format is typically:
    # $ command
    # output
    pattern = (
        r"(?:^|\n)(?:# (.+?)(?:\n|$))?(?:\$ (.+?)(?:\n|$))((?:(?!\n\$|\n#).+?\n?)*)"
    )
    matches = re.finditer(pattern, content, re.MULTILINE)

    for match in matches:
        explanation = match.group(1) or ""
        command = match.group(2).strip()
        output = match.group(3).strip()

        segments.append(
            {"explanation": explanation, "command": command, "output": output}
        )

    return segments


def extract_title_and_description(segments: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Extract title and description from the first comment segment.

    Args:
        segments: List of segment dictionaries

    Returns:
        Tuple containing (title, description)
    """
    if segments and segments[0]["is_comment"]:
        lines = segments[0]["annotation"].split("\n")
        # First line is title
        title = lines[0].strip()
        # The rest is the intro paragraph/description
        description = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

        # Remove this entire segment from the list so it doesn't
        # show up as a code/comment block later
        segments.pop(0)

        return title, description

    return "Untitled Example", ""


def process_example_directory(example_dir: Path) -> Dict[str, Any]:
    """
    Process a single example directory and compile its data.

    Args:
        example_dir: Path to the example directory

    Returns:
        Dictionary containing compiled example data
    """
    example_id = example_dir.name
    order = int(example_id.split("-")[0])

    # Find Python and shell files
    python_files = list(example_dir.glob("*.py"))
    shell_files = list(example_dir.glob("*.sh"))

    if not python_files:
        logger.warning(f"No Python files found in {example_dir}")
        return None

    # Process the first Python file
    main_python_file = python_files[0]
    code_segments = extract_python_segments(main_python_file)

    # Extract title and description
    title, description = extract_title_and_description(code_segments)

    # Process the first shell file (if any)
    shell_segments = []
    if shell_files:
        shell_segments = extract_shell_segments(shell_files[0])

    # Compile the example data
    example_data = {
        "id": example_id,
        "title": title,
        "description": description,
        "order": order,
        "code_segments": code_segments,
        "shell_segments": shell_segments,
    }

    return example_data


def process_examples(example_dirs: List[Path]) -> Dict[str, Any]:
    """
    Process all example directories and compile them into a JSON structure.

    Args:
        example_dirs: List of paths to example directories

    Returns:
        Dictionary representing the compiled examples data
    """
    examples = []

    for example_dir in example_dirs:
        logger.info(f"Processing example: {example_dir.name}")
        example_data = process_example_directory(example_dir)
        if example_data:
            examples.append(example_data)

    # Sort examples by order
    examples.sort(key=lambda e: e["order"])

    return {"examples": examples}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Build Gemini by Example website data")
    parser.add_argument("--examples-dir", type=str, help="Path to examples directory")
    parser.add_argument("--output", type=str, help="Path to output JSON file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def main():
    """Main entry point for the build script."""
    args = parse_args()

    # Set verbose logging if requested
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Use command-line arguments if provided, otherwise use defaults
    examples_dir = (
        Path(args.examples_dir) if args.examples_dir else project_root / "examples"
    )
    output_file = (
        Path(args.output) if args.output else project_root / "data" / "examples.json"
    )

    logger.info(f"Scanning examples directory: {examples_dir}")
    example_dirs = scan_examples_directory(examples_dir)
    logger.info(f"Found {len(example_dirs)} example directories")

    logger.info("Processing examples...")
    data = process_examples(example_dirs)

    logger.info(f"Writing output to {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    logger.info("Build complete!")


if __name__ == "__main__":
    main()
