# Gemini by Example

A hands-on introduction to using the Google Gemini API through annotated example programs.

## Overview

Gemini by Example provides step-by-step tutorials for learning how to use the Gemini API in Python. The project features:

- Simple, commented examples that build from basic to advanced usage
- Side-by-side code and explanations
- Runnable shell commands with expected outputs
- Examples organized by category
- Support for images to illustrate concepts

## Project Structure

```
geminibyexample/
├── data/               # Processed data files
│   ├── examples.json   # Structured example data
│   └── sections.json   # Section definitions for organizing examples
├── examples/           # Source examples
│   ├── 001-basic-generation/
│   │   ├── basic-generation.py  # Python code with comments
│   │   ├── basic-generation.sh  # Shell commands and output
│   │   └── basic-generation.png # Optional example image
│   ├── 002-streaming-text/
│   └── ...
├── build_examples/     # Scripts to build data files
│   └── build_examples.py
├── build_static_site.py # Generate static HTML site
├── docs/               # Generated static site (GitHub Pages)
│   ├── llms.txt        # Simplified documentation with links
│   ├── llms-ctx.txt    # Comprehensive documentation with code
│   └── ...
├── templates/          # Site templates
└── static/             # Static assets
```

## Quickstart

To build and preview the site locally:

```bash
# One command to build both examples data and static site
python build_static_site.py

# Open the generated site
open docs/index.html
```

## Features

- **Organized Sections**: Examples are grouped into logical sections
- **Copy All Python**: Each example has a "Copy All Python" button to easily copy the complete code
- **Annotated Code**: Line-by-line explanations paired with code
- **Visual Examples**: Support for images to illustrate concepts
- **Shell Commands**: Example commands with expected output
- **AI-Ready Documentation**: Generated files (`llms.txt` and `llms-ctx.txt`) that can be used as context in AI coding tools
- **Keyboard Navigation**: Use arrow keys to move between examples

## Working with Examples

Examples are Python files with special comment formatting:

```python
# Title of the Example
# This is a description of what this example demonstrates.

# This is a comment that explains the next line of code
code_here()

# Another explanation
more_code()
```

- The first comment block becomes the title and description
- Each comment block explains the code that follows it
- Comments without following code create section headers

For detailed instructions on creating new examples, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Building the Site

Build both the examples data and static site with a single command:

```bash
python build_static_site.py
```

This will:
1. Process all examples and create `data/examples.json`
2. Generate the static site in the `docs/` directory
3. Copy all assets and images
4. Generate two documentation files:
   - `llms.txt`: A simplified summary with links to examples
   - `llms-ctx.txt`: Comprehensive documentation with full code examples

These text files are useful for context injection into AI tools like Cursor, Claude, or Gemini, allowing developers to ask questions about the Gemini API with these examples as context.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on how to:

- Add new examples
- Create example categories
- Include images
- Format your code and comments

## License

MIT