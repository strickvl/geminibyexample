# Gemini by Example

A hands-on introduction to using the Google Gemini API through annotated example programs.

## Overview

Gemini by Example provides step-by-step tutorials for learning how to use the Gemini API in Python. The project features:

- Simple, commented examples that build from basic to advanced usage
- Side-by-side code and explanations
- Runnable shell commands with expected outputs

## Project Structure

```
geminibyexample/
├── data/               # Processed data (examples.json)
├── examples/           # Source examples (Python files with comments)
│   ├── 001-basic-generation/
│   ├── 002-values/
│   └── ...
├── build_examples/     # Scripts to build data files
│   └── build_examples.py
├── build_static_site.py # Generate static HTML site
├── main.py             # FastHTML dynamic site
├── templates/          # Site templates
├── static/             # Static assets
└── site/               # Generated static site (after running build_static_site.py)
```

## Working with Examples

### Adding a New Example

1. Create a new directory in `examples/` with a numeric prefix (e.g., `003-new-example/`)
2. Add a Python file with the example code and detailed comments
3. Add a shell script (`.sh`) with example commands to run the code

The first comment block in the Python file will be used as the title and description.

Example Python file format:
```python
# Title of the Example
# This is a description of what this example demonstrates.

# This is a comment that explains the next line of code
code_here()

# Another explanation
more_code()
```

### Building the Data

After adding or modifying examples, rebuild the data file:

```bash
python build_examples/build_examples.py
```

This processes all example directories and generates `data/examples.json` with the structured content.

## Running the Site

### Dynamic Site

Run the dynamic site with FastHTML:

```bash
python main.py
```

This starts a local server that renders the examples dynamically.

### Static Site Generation

To build a static version of the site:

```bash
python build_static_site.py
```

This generates a complete static site in the `site/` directory with:
- An index page listing all examples
- Individual pages for each example
- All necessary assets and styling

The static site can be hosted on any web server or static hosting service.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.