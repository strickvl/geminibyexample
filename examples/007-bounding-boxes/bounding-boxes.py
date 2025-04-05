# Bounding boxes
# This example demonstrates how to use the Gemini API to detect an object (a cat) in an image and retrieve its bounding box coordinates.

# Import necessary libraries. Make sure Pillow is installed!
from google import genai
import requests
from PIL import Image
from io import BytesIO

# Initialize the Gemini client with your API key
client = genai.Client(api_key="YOUR_API_KEY")

# Specify the prompt, asking for a bounding box around the cat
prompt = (
    "Return a bounding box for the cat in this image "
    "in [ymin, xmin, ymax, xmax] format."
)

# Download the cat image from cataas.com
image_url = "https://cataas.com/cat"
response = requests.get(image_url)
cat_image = Image.open(BytesIO(response.content))

# Call the Gemini API to generate content with the image and prompt
response = client.models.generate_content(
    model="gemini-1.5-pro", contents=[cat_image, prompt]
)

# Print the response text, which will contain the bounding box coordinates
print(response.text)

#
# Normalize Coordinates
# The model returns bounding box coordinates in the format [y_min, x_min, y_max, x_max].
# To convert these normalized coordinates to the pixel coordinates of your original image, follow these steps:
# 1. Divide each output coordinate by 1000.
# 2. Multiply the x-coordinates by the original image width.
# 3. Multiply the y-coordinates by the original image height.
#
# Example Calculation (assuming the model returns [200, 300, 700, 800] and the image is 1000x800):
y_min = (200 / 1000) * 800  # 160
x_min = (300 / 1000) * 1000  # 300
y_max = (700 / 1000) * 800  # 560
x_max = (800 / 1000) * 1000  # 800
