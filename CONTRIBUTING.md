# Contributing to Gemini by Example

Thank you for your interest in contributing to Gemini by Example! This document provides guidelines and instructions for adding new examples and improving the project.

## Adding a New Example

### 1. Create a Directory

Create a new directory in `examples/` with a numeric prefix for ordering:

```
examples/003-your-example-name/
```

The numeric prefix determines the order of examples on the site.

### 2. Add Python File

Create a Python file (`.py`) within your example directory that demonstrates the feature:

```python
# Your Example Title
# This is a description of what this example demonstrates.
# This will appear at the top of the example page.

# This comment explains the next line of code
from google import genai

# Comments should explain each significant step
client = genai.Client(api_key="YOUR_API_KEY")

# Empty comment lines create section breaks
# This starts a new section of explanation

response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents="Your prompt here"
)
print(response.text)
```

#### Formatting Rules:

- The first comment block becomes the title and description
- Each comment block explains the code that follows it
- Comment blocks with no following code create section headings
- Comments must start with `#` at the beginning of the line

### 3. Add Shell Script

Create a shell script (`.sh`) showing how to run the example:

```bash
# First, install the Google Generative AI library
$ pip install google-generative-ai

# Then run the program with Python
$ python your-example.py
Expected output goes here...
```

#### Shell Script Format:

- Lines starting with `# ` are explanations
- Lines starting with `$ ` are commands to run
- Other lines are expected output
- Keep outputs concise and relevant

### 4. Add Images (Optional)

If you want to include images:

1. Add a single PNG file to your example directory
2. Use a meaningful filename with a numeric prefix, e.g., `01-result-image.png`
3. The part after the prefix will be used as the caption (e.g., "Result image")
4. Please compress images using [TinyPNG](https://tinypng.com/) before adding them

## Building and Testing

After creating your example:

1. Build the examples data:
   ```bash
   python build_static_site.py
   ```

   This runs both the example builder and static site generator in one step.

2. Open the generated HTML in the `docs/` directory to preview your example

## Example Organization

Examples are organized into sections using the `data/sections.json` file. To add your example to a section:

1. Find the appropriate section in `sections.json`
2. Add your example's directory name to the `examples` array

```json
{
  "sections": [
    {
      "id": "001-basic",
      "title": "Basic Examples",
      "description": "Getting started with Gemini API",
      "order": 1,
      "examples": ["001-basic-generation", "002-values", "003-your-example-name"]
    }
  ]
}
```

If you're creating a new section, add it to the array with a unique ID and order number.

## Style Guidelines

- Keep examples simple and focused on one concept
- Use clear, concise explanations
- Follow PEP 8 for Python code
- Avoid complex dependencies beyond the Google Generative AI library
- Make sure examples are runnable with just the instructions provided

## Submission Process

1. Fork the repository
2. Create a branch for your changes
3. Add your example and test it locally
4. Submit a pull request with a clear description of your example

Thank you for contributing to Gemini by Example!