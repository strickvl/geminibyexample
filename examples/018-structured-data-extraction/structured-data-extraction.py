# Extract structured data from a PDF invoice
# This example demonstrates how to extract structured data from a PDF invoice using the Gemini API and Pydantic.

# Import necessary libraries
import os
import requests
import json
from pydantic import BaseModel
from typing import List
from google import genai

# Define Pydantic models for structured data
class Item(BaseModel):
    name: str
    price_per_kg: float
    quantity_kg: float


class InvoiceContents(BaseModel):
    sender: str
    recipient: str
    address: str
    full_total: float
    subtotal: float
    GST: float
    items: List[Item]

# Load the PDF invoice from a URL
# For PDFs larger than 20MB, use the Files API for uploading
pdf_url = "https://www.princexml.com/samples/invoice/invoicesample.pdf"
response = requests.get(pdf_url)
response.raise_for_status()  # Ensure the download was successful
pdf_data = response.content

# Initialize the Gemini client with your API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"))

# Configure the model for structured output
model = 'gemini-2.5-pro-preview-03-25'

# Construct the prompt with instructions and schema information
prompt_text = f"""Extract the following information from the invoice: sender, recipient, address, full_total, subtotal, GST, and a list of items (name, price/kg, quantity (kg))."

# Call the Gemini API to extract structured data from the PDF
response = client.generate_content(
    model=model,
    contents=[pdf_data, prompt_text],
    generation_config=genai.GenerationConfig(temperature=0.0),
)

# Parse the JSON response into the Pydantic model
# Assuming the model returns a JSON string representation of the InvoiceContents
invoice_data = json.loads(response.text)
invoice = InvoiceContents(**invoice_data)

# Print the extracted data as a JSON string
print(invoice.model_dump_json(indent=2))
