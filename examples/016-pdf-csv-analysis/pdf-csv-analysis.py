# PDF and CSV data analysis and summarization
# This example demonstrates how to use the Gemini API to analyze data from PDF and CSV files.

# Import necessary libraries
from google import genai
from google.genai import types
import httpx
import os

# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# We start with the PDF analysis.
# Download the PDF file
pdf_url = "https://www.princexml.com/samples/invoice/invoicesample.pdf"
pdf_data = httpx.get(pdf_url).content

# Prompt to extract main players from the PDF
pdf_prompt = (
    "Identify the main companies or entities mentioned in this invoice. "
    "Summarize the data."
)

# Generate content with the PDF and the prompt
pdf_response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(data=pdf_data, mime_type="application/pdf"),
        pdf_prompt,
    ],
)

# Print the PDF analysis result
print("PDF Analysis Result:\n", pdf_response.text)

# Moving on to the CSV analysis now. You'll note that the process is very
# similar.
# You can also pass in code files, XML, RTF, Markdown, and more.
# We download the CSV file here.
csv_url = "https://gist.githubusercontent.com/suellenstringer-hye/f2231b3383538bcb1a5b051c7908f5b7/raw/0f4e0733a434733cda8e749bbbf33a93c2b5bbde/test.csv"
csv_data = httpx.get(csv_url).content

# Prompt to analyze the CSV data
csv_prompt = "Analyze this data and tell me about the contents. Summarize the data."

# Generate content with the CSV data and the prompt
csv_response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(
            data=csv_data,
            mime_type="text/csv",
        ),
        csv_prompt,
    ],
)

# Print the CSV analysis result
print("\nCSV Analysis Result:\n", csv_response.text)
