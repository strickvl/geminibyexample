# Install the Google Generative AI library and Pydantic
$ pip install google-genai pydantic requests

# Then run the program with Python
$ python structured-data-extraction.py
{
  "sender": "SUNNY FARM",
  "recipient": "Denny Gunawan",
  "address": "221 Queen St\nMelbourne VIC 3000",
  "full_total": "$39.60",
  "subtotal": "$36.00",
  "gst_value": "$3.60",
  "items": [
    {
      "name": "Apple",
      "price_per_kg": "$5.00",
      "quantity_kg": 1
    },
    {
      "name": "Orange",
      "price_per_kg": "$1.99",
      "quantity_kg": 2
    },
    {
      "name": "Watermelon",
      "price_per_kg": "$1.69",
      "quantity_kg": 3
    },
    {
      "name": "Mango",
      "price_per_kg": "$9.56",
      "quantity_kg": 2
    },
    {
      "name": "Peach",
      "price_per_kg": "$2.99",
      "quantity_kg": 1
    }
  ]
}
