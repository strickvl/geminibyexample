# Gemini by Example

This file contains all examples from the Gemini by Example site (geminibyexample.com).
It's organized by sections, with each example's Python code and terminal commands included.

## Table of Contents

* Text
  * Simple text generation
  * Streaming text
  * System prompt
  * Reasoning models
  * Structured output
* Images
  * Image question answering
  * Image generation (Gemini and Imagen)
  * Edit an image
  * Bounding boxes
  * Image segmentation
* Audio
  * Audio question answering
  * Audio transcription
  * Audio summarization
* Video
  * Video question answering
  * Video summarization
  * Video transcription
  * YouTube video summarization
* PDFs and other data types
  * PDF and CSV data analysis and summarization
  * Translate documents
  * Extract structured data from a PDF
* Agentic behaviour
  * Function calling & tool use
  * Code execution
  * Model Context Protocol
  * Grounded responses with search tool
* Token counting & context windows
  * Model context windows
  * Counting chat tokens
  * Calculating multimodal input tokens
  * Context caching
* Miscellaneous
  * Rate limits and retries
  * Concurrent requests and generation
  * Embeddings generation
  * Safety settings and filters
  * LiteLLM

## Text

### Simple text generation

```python
from google import genai
client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
```

```shell
$ pip install google-genai
$ python basic-generation.py
AI works by learning patterns from data, then using those patterns to make predictions or generate new content. It processes information through neural networks that mimic human brain connections, identifying features and relationships to perform tasks like recognition, prediction, and generation.
```

*This example includes images which can be viewed on the website.*

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/text-generation

### Streaming text

This example demonstrates how to use the Gemini API to generate text content and stream the output.

```python
from google import genai
client = genai.Client(api_key="YOUR_API_KEY")
response = client.models.generate_content_stream(
    model="gemini-2.0-flash",
    contents=["Explain how AI works"]
)
for chunk in response:
    print(chunk.text, end="")
```

```shell
$ pip install google-genai
$ python streaming-generation.py
AI, or Artificial Intelligence, is a broad field of computer science focused on creating machines capable of performing tasks that typically require human intelligence. It involves developing algorithms and models that enable computers to learn from data, reason, solve problems, understand natural language, perceive their environment, and make decisions.
AI can be achieved through various techniques, including:
*   **Machine Learning (ML):** This is a core subfield of AI where machines learn from data without being explicitly programmed. ML algorithms can identify patterns, make predictions, and improve their performance over time with more data.
*   **Deep Learning (DL):** A subfield of ML that uses artificial neural networks with multiple layers (deep neural networks) to analyze data and extract complex features. DL has been highly successful in areas like image recognition, natural language processing, and speech recognition.
*   **Natural Language Processing (NLP):** Focuses on enabling computers to understand, interpret, and generate human language. NLP techniques are used in applications like chatbots, machine translation, and sentiment analysis.
*   **Computer Vision:** Enables computers to "see" and interpret images and videos. Computer vision algorithms can identify objects, recognize faces, and analyze scenes.
*   **Robotics:** Involves designing, constructing, operating, and applying robots. AI is often used in robotics to enable robots to perform tasks autonomously.
AI is transforming various industries, including healthcare, finance, transportation, and manufacturing. It has the potential to solve complex problems and improve people's lives, but it also raises ethical and societal concerns that need to be addressed.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/text-generation

### System prompt

This example demonstrates how to use system instructions to guide the model's behavior.

```python
from google import genai
from google.genai import types
client = genai.Client(api_key="YOUR_API_KEY")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a pirate.  Answer all questions like a pirate."),
    contents="Hello there"
)
print(response.text)
```

```shell
$ pip install google-genai
$ python system_instructions.py
Ahoy there, matey! What be on yer mind?
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/text-generation#system-instructions

### Reasoning models

This example demonstrates how to access the reasoning trace of a Gemini model
and then the final text output.
Reasoning models are a new type of model that 'think' a little bit before
giving a final answer. The 'thinking' response is visible in Google AI Studio
but not as part of the response to an API call.

```python
from google import genai
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = "If the universe is expanding, what is it expanding into? Show your reasoning."
response = client.models.generate_content(
    model="gemini-2.5-pro-exp-03-25",
    contents=prompt,
)

print(response.text)
```

```shell
$ pip install google-genai
$ python universe_reasoning.py
This is a fantastic and very common question that gets to the heart of how we understand the universe based on Einstein's theory of General Relativity. The most accurate answer, according to our current understanding, is:
**The universe isn't expanding *into* anything. Space itself is expanding.**
Here's the reasoning:
1.  **General Relativity's View of Spacetime:** Our everyday intuition thinks of space as a pre-existing, static container – like an empty room that things can move around *in*. General Relativity, however, describes spacetime not as a fixed background but as a dynamic entity. It can warp, bend (which we experience as gravity), and, crucially, *expand or contract*.
2.  **Expansion is Intrinsic:** The expansion of the universe isn't like an explosion *within* a pre-existing void, where debris flies outwards *into* empty space. Instead, it's the very fabric of spacetime *itself* that is stretching. Imagine the space *between* galaxies is growing.
3.  **Analogies (and their limitations):**
    *   **The Rising Raisin Bread:** Imagine raisins (representing galaxies) embedded in dough (representing space). As the dough bakes and expands, all the raisins move further apart from each other. A raisin doesn't see itself as being at the center; it sees all other raisins moving away from it. Importantly, the *dough itself* is expanding.
        *   *Limitation:* This analogy breaks down because the dough has edges and is expanding *into* the oven (an external space). Our universe, as far as we know, doesn't have an edge or an "outside."
    *   **The Expanding Balloon Surface:** Imagine drawing dots (galaxies) on the surface of a balloon. As you inflate the balloon, the rubber (space) stretches, and the distance between any two dots on the surface increases. From the perspective of any dot, all other dots are moving away. There is no "center" of expansion *on the surface* itself.
        *   *Limitation:* The 2D surface of the balloon is expanding *into* the 3D space around it. General Relativity doesn't require our 3D space to be expanding into a higher-dimensional "hyperspace." The expansion is an intrinsic property of our spacetime dimensions.
4.  **No Center, No Edge:** Because space *itself* is expanding everywhere, there isn't a central point *from which* the universe is expanding. The Big Bang wasn't an explosion *at* a point *in* space; it was the beginning of the expansion *of* space, happening everywhere simultaneously. Consequently, there's no "edge" of the universe expanding outwards into a void.
5.  **Infinite or Finite?**
    *   If the universe is *infinite*, then it was always infinite. An expanding infinite universe simply becomes "more infinite" – the distances between objects grow, but it isn't expanding *into* anything because there's no outside to an infinite space.
    *   If the universe is *finite* but unbounded (like the surface of the balloon, but in 3D), its total volume increases, but it still doesn't require an external space to expand into. It's self-contained.
**In summary:** The concept of "expanding into" relies on the idea of an external space or container. According to General Relativity, the universe *is* the container (spacetime), and it's this container itself that is growing. There is no need for an "outside" for this expansion to occur.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/thinking

### Structured output

This example shows how to generate structured data using a pydantic model to represent Cats with name, colour, and special ability.

```python
from google import genai
from pydantic import BaseModel
import os
class Cat(BaseModel):
    name: str
    colour: str
    special_ability: str
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = "Generate data for 3 cats, including their name, colour and special ability."
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Cat],
    },
)
my_cats: list[Cat] = response.parsed
for cat in my_cats:
    print(
        f"Name: {cat.name}, Colour: {cat.colour}, Special Ability: {cat.special_ability}"
    )
```

```shell
$ pip install google-genai pydantic
$ python structured_cats.py
Name: Aria, Colour: tortoiseshell, Special Ability: Can teleport short distances
Name: Blupus, Colour: ginger, Special Ability: Understands human speech
Name: Moonshine, Colour: black and white, Special Ability: Invisible at night
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/structured-output?lang=python
- https://ai.google.dev/gemini-api/docs/structured-output?lang=rest

## Images

### Image question answering

This example demonstrates how to use the Gemini API to analyze or understand images of cats, including using image URLs and base64 encoding.

```python
from google import genai
from google.genai import types
import requests
import base64
client = genai.Client(api_key="YOUR_API_KEY")
image_url = "https://cataas.com/cat"
image_response = requests.get(image_url)
image_content = image_response.content
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["What breed of cat is this?", types.Part.from_bytes(data=image_content, mime_type="image/jpeg")]
)

print("Response from URL Image:\n", response.text)
with open("cat.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
encoded_string = encoded_string.decode('utf-8')
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Is this cat fluffy?", types.Part.from_bytes(data=base64.b64decode(encoded_string), mime_type="image/jpeg")]
)

print("\nResponse from Base64 Image:\n", response.text)
```

```shell
$ pip install google-genai requests
$ wget https://cataas.com/cat -O cat.jpg
$ python gemini-cat.py
Response from URL Image:
 This looks like a British Shorthair cat.
Response from Base64 Image:
 Yes, this cat appears to be fluffy.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/vision?lang=python

### Image generation (Gemini and Imagen)

This example demonstrates generating images using both Gemini 2.0 Flash and Imagen 3 models, focusing on cat-related prompts.

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
client = genai.Client(api_key="YOUR_API_KEY")
contents = (
    "Hi, can you create a 3D rendered image of a cat wearing a wizard hat, "
    "casting a spell in a magical forest?"
)

response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(response_modalities=["Text", "Image"]),
)
for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("gemini-cat-wizard.png")
        image.show()
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt="A photorealistic image of a cat astronaut floating in space",
    config=types.GenerateImagesConfig(number_of_images=2),
)
for i, generated_image in enumerate(response.generated_images):
    image = Image.open(BytesIO(generated_image.image.image_bytes))
    image.save(f"imagen-cat-astronaut-{i+1}.png")
    image.show()
```

```shell
$ pip install google-genai Pillow
$ python image-generation.py
# Expected output (will vary based on the model):
# (Text describing the cat wizard image from Gemini 2.0 Flash)
# (Two image windows will open, displaying the generated cat astronaut images from Imagen 3)
# Image saved as gemini-cat-wizard.png
# (Two image windows will open, displaying the generated cat astronaut images from Imagen 3)
```

*This example includes images which can be viewed on the website.*

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/image-generation

### Edit an image

This example demonstrates how to edit an existing image of a cat to add a hat using the Gemini API.

```python
from google import genai
from google.genai import types
from PIL import Image
import requests
from io import BytesIO
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
image_url = "https://cataas.com/cat"
response = requests.get(image_url)
cat_image = Image.open(BytesIO(response.content))
text_prompt = "Please add a stylish top hat to this cat."
model = "gemini-2.0-flash-exp-image-generation"
response = client.models.generate_content(
    model=model,
    contents=[text_prompt, cat_image],
    config=types.GenerateContentConfig(response_modalities=["Text", "Image"]),
)
for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        print(f"Received {part.inline_data.mime_type} data")
image = Image.open(BytesIO(part.inline_data.data))
        image.save("cat_with_hat.png")
        print("\nImage saved as cat_with_hat.png")
```

```shell
$ pip install google-genai Pillow requests
$ python edit_cat.py
Image saved as cat_with_hat.png
```

*This example includes images which can be viewed on the website.*

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/image-generation#gemini-image-editing

### Bounding boxes

This example demonstrates how to use the Gemini API to detect an object (a cat) in an image and retrieve its bounding box coordinates.

```python
from google import genai
import requests
from PIL import Image
from io import BytesIO
client = genai.Client(api_key="YOUR_API_KEY")
prompt = (
    "Return a bounding box for the cat in this image "
    "in [ymin, xmin, ymax, xmax] format."
)
image_url = "https://cataas.com/cat"
response = requests.get(image_url)
cat_image = Image.open(BytesIO(response.content))
response = client.models.generate_content(
    model="gemini-1.5-pro", contents=[cat_image, prompt]
)
print(response.text)
y_min = (200 / 1000) * 800  # 160
x_min = (300 / 1000) * 1000  # 300
y_max = (700 / 1000) * 800  # 560
x_max = (800 / 1000) * 1000  # 800
```

```shell
$ pip install google-genai Pillow requests
$ python object-detection.py
[0.1, 0.2, 0.7, 0.8]
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/vision?lang=python#bbox

### Image segmentation

This example demonstrates how to use the Gemini API to perform image segmentation on a picture of a cat.

```python
from google import genai
import os
import requests
from PIL import Image
from io import BytesIO
import json
import base64
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = """
Give the segmentation masks for the cat in the image.
Output a JSON list of segmentation masks where each entry contains the 2D
bounding box in the key \"box_2d\", the segmentation mask in key \"mask\", and
the text label in the key \"label\". Use descriptive labels.
"""
image_url = "https://cataas.com/cat"
response = requests.get(image_url)
cat_image = Image.open(BytesIO(response.content))
original_filename = f"cat_original.png"
cat_image.save(original_filename)
print(f"Original image saved as: {original_filename}")
response = client.models.generate_content(
    model="gemini-2.5-pro-exp-03-25", contents=[cat_image, prompt]
)
print(response.text)
response_text = response.text
if "```json" in response_text:
    json_str = response_text.split("```json")[1].split("```")[0].strip()
elif "[" in response_text and "]" in response_text:
    start = response_text.find("[")
    end = response_text.rfind("]") + 1
    json_str = response_text[start:end]
else:
    json_str = response_text
mask_data = json.loads(json_str)
first_mask = mask_data[0]
mask_base64 = first_mask.get("mask", "")
if "base64," in mask_base64:
    mask_base64 = mask_base64.split("base64,")[1]
mask_bytes = base64.b64decode(mask_base64)
mask_image = Image.open(BytesIO(mask_bytes))
cat_image = cat_image.convert("RGBA")
mask_image = mask_image.convert("L")  # Convert mask to grayscale
overlay = Image.new(
    "RGBA", mask_image.size, (255, 0, 255, 128)
)  # Bright pink, semi-transparent
overlay.putalpha(mask_image)
if overlay.size != cat_image.size:
    overlay = overlay.resize(cat_image.size)
result = Image.alpha_composite(cat_image, overlay)

mask_filename = f"cat_mask.png"
mask_image.save(mask_filename)

merged_filename = f"cat_with_mask.png"
result.save(merged_filename)
```

```shell
$ pip install google-genai
$ python cat_segmentation.py
# Expected output (example):
# [{"box_2d": [100, 50, 900, 750], "mask": "base64_encoded_png_data", "label": "Main Coon Cat"}, ...]
```

*This example includes images which can be viewed on the website.*

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/vision?lang=python#image_segmentation

## Audio

### Audio question answering

This example demonstrates how to ask a question about the content of an audio file using the Gemini API.

```python
from google import genai
from google.genai import types
import requests
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_agent = "GeminiByExample/1.0 (https://github.com/strickvl/geminibyexample; contact@example.org) python-requests/2.0"
url = "https://upload.wikimedia.org/wikipedia/commons/1/1f/%22DayBreak%22_with_Jay_Young_on_the_USA_Radio_Network.ogg"
headers = {"User-Agent": user_agent}
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an exception for bad status codes
audio_bytes = response.content
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "What is the main topic of this audio?",
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        ),
    ],
)

print(response.text)
```

```shell
$ pip install google-genai requests
$ python audio-question.py
This audio features a male host and a travel expert, Pete Trabucco.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/audio?lang=python

### Audio transcription

This example demonstrates how to transcribe an audio file by providing the audio data inline with the request.

```python
from google import genai
from google.genai import types
import requests
client = genai.Client(api_key="YOUR_API_KEY")
user_agent = "GeminiByExample/1.0 (https://github.com/strickvl/geminibyexample; contact@example.org) python-requests/2.0"
url = "https://upload.wikimedia.org/wikipedia/commons/1/1f/%22DayBreak%22_with_Jay_Young_on_the_USA_Radio_Network.ogg"
headers = {"User-Agent": user_agent}
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an exception for bad status codes
audio_bytes = response.content
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "Transcribe this audio clip",
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        ),
    ],
)
print(response.text)
```

```shell
$ pip install google-genai
$ python audio-transcription.py
We're joined once again by our travel expert and also author of America's Top Roller Coasters and Amusement Parks, Pete Trabucco. Good morning and welcome back to Daybreak USA. Well, thanks for having me on. If someone's lucky enough to go on vacation to an exotic location, and then maybe not so lucky to have some kind of a disaster happen while they're there, maybe some civil unrest. What should they do now? What's the next step? Well, whenever you're going on vacation whether it's locally or internationally, you've got to be uh very careful.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/audio?lang=python

### Audio summarization

This example demonstrates how to summarize the content of an audio file using the Gemini API.

```python
from google import genai
from google.genai import types
import requests
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_agent = "GeminiByExample/1.0 (https://github.com/strickvl/geminibyexample; contact@example.org) python-requests/2.0"
url = "https://upload.wikimedia.org/wikipedia/commons/1/1f/%22DayBreak%22_with_Jay_Young_on_the_USA_Radio_Network.ogg"
headers = {"User-Agent": user_agent}
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an exception for bad status codes
audio_bytes = response.content
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "What is this audio about?",
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        ),
    ],
)

print(response.text)
```

```shell
$ pip install google-genai requests
$ python audio-summarization.py
This audio is about travel tips, particularly what to do in the event of a disaster while on vacation.
The speaker emphasizes the importance of staying informed about the destination, traveling with a buddy,
having a plan in place, and investing in travel insurance. They also mention the importance of connecting
with home base and knowing the location of the American Red Cross in case of emergencies.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/audio?lang=python

## Video

### Video question answering

This example demonstrates how to ask questions about a video using the Gemini API.
Note: For videos larger than 20MB, you must use the File API for uploading.

```python
from google import genai
from google.genai import types
import os
import requests
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"
response = requests.get(video_url)
video_bytes = response.content
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=types.Content(
        parts=[
            types.Part(text="Describe the tone and genre of this video."),
            types.Part(inline_data=types.Blob(data=video_bytes, mime_type="video/mp4")),
        ]
    ),
)
print(response.text)
```

```shell
$ pip install google-genai
$ python video_question_answering.py
Certainly! Here's a description of the tone and genre of the video clip:
**Genre:**  Travel or scenery/ambient video
**Tone:** Relaxed, peaceful, and observational. The video presents a serene view of a park next to a busy street. The presence of nature with the sounds of the city creates a tranquil atmosphere.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/vision?lang=python#prompting-video

### Video summarization

This example demonstrates how to summarize the content of a video using the Gemini API.
Note: For videos larger than 20MB, you must use the File API for uploading.

```python
from google import genai
from google.genai import types
import os
import requests
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"
response = requests.get(video_url)
video_bytes = response.content
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=types.Content(
        parts=[
            types.Part(text="Summarize the content of this video."),
            types.Part(inline_data=types.Blob(data=video_bytes, mime_type="video/mp4")),
        ]
    ),
)
print(response.text)
```

```shell
$ pip install google-genai
$ python video_summarization.py
The video shows a park with trees next to a busy street with cars and buses passing by. The sun shines through the leaves of the trees.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/vision?lang=python#prompting-video

### Video transcription

This example demonstrates how to transcribe the content of a video using the Gemini API.
Note: For videos larger than 20MB, you must use the File API for uploading.

```python
from google import genai
from google.genai import types
import os
import requests
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"
response = requests.get(video_url)
video_bytes = response.content
prompt = (
    "Transcribe the audio from this video, giving timestamps for "
    "salient events in the video. Also provide visual descriptions."
)
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=types.Content(
        parts=[
            types.Part(text=prompt),
            types.Part(inline_data=types.Blob(data=video_bytes, mime_type="video/mp4")),
        ]
    ),
)
print(response.text)
```

```shell
$ pip install google-genai
$ python video_transcription.py
Okay, here's the transcription and visual descriptions of the video:
**Video Description:**
The video pans up from a low angle showing a park with lush green trees.  Sunlight filters through the leaves. In the distance, cars and a bus can be seen on a road next to the park. There is a paved walkway and low bushes.
**Timestamps:**
*   **0:00** Camera starts panning up showing a park with trees and sunlight. 
*   **0:04** The camera reaches its highest point in its view.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/vision?lang=python#prompting-video

### YouTube video summarization

This example demonstrates how to summarize a YouTube video using its URL.

```python
from google import genai
client = genai.Client(api_key="YOUR_API_KEY")
youtube_url = "https://www.youtube.com/watch?v=tAP1eZYEuKA"
prompt = f"Summarize the content of this YouTube video: {youtube_url}"
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        {
            "parts": [
                {"text": "Can you summarize this video?"},
                {"file_data": {"file_uri": youtube_url}},
            ]
        }
    ],
)
print(response.text)
```

```shell
$ pip install google-genai
$ python youtube-summarization.py
Sure, here is a summary of the video!
Thomas, the father, is sharing his son Max's story of having Alexander Disease, a rare ultra-rare genetic disorder. After having a difficult time conceiving and finally being successful and welcoming Max to their family, they were dealt a devastating blow when Max had his first seizure at a very young age. 
Because of the seizure, Max had to go through a series of medical tests. Those tests showed that Max had Alexander Disease. After doing some research, the family was heartbroken, as the typical life expectancy for this disease is 5-10 years, and there is no treatment or cure.
Thomas started researching more in-depth by summarizing scientific papers by using Gemini AI and has discovered a lead scientist and her team in New York that he connected with. He sends one to two emails a week to different scientists in order to get more studies underway for the disease. He doesn't want Max to be seen as having 'zero' chance and wants to be a dad and enjoy his time with Max. He will continue to strive to find a cure for Max!
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/vision?lang=python#youtube

## PDFs and other data types

### PDF and CSV data analysis and summarization

This example demonstrates how to use the Gemini API to analyze data from PDF and CSV files.

```python
from google import genai
from google.genai import types
import httpx
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
pdf_url = "https://www.princexml.com/samples/invoice/invoicesample.pdf"
pdf_data = httpx.get(pdf_url).content
pdf_prompt = (
    "Identify the main companies or entities mentioned in this invoice. "
    "Summarize the data."
)
pdf_response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(data=pdf_data, mime_type="application/pdf"),
        pdf_prompt,
    ],
)
print("PDF Analysis Result:\n", pdf_response.text)
csv_url = "https://gist.githubusercontent.com/suellenstringer-hye/f2231b3383538bcb1a5b051c7908f5b7/raw/0f4e0733a434733cda8e749bbbf33a93c2b5bbde/test.csv"
csv_data = httpx.get(csv_url).content
csv_prompt = "Analyze this data and tell me about the contents. Summarize the data."
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
print("\nCSV Analysis Result:\n", csv_response.text)
```

```shell
$ pip install google-genai httpx pandas
$ python pdf_csv_analysis.py
PDF Analysis Result:
 The main company mentioned in the invoice is Sunny Farm.
CSV Analysis Result:
 Okay, I've analyzed the provided data. Here's a summary of its contents:
**Data Format:**
*   The data appears to be in CSV (Comma Separated Values) format.
*   The first line is a header row defining the fields.
*   Each subsequent line represents a record containing information about a person.
**Fields Present:**
The data includes the following fields for each person:
1.  **first\_name:** The person's first name.
2.  **last\_name:** The person's last name.
3.  **company\_name:** The name of the company they are associated with.
4.  **address:** The street address.
5.  **city:** The city.
6.  **county:** The county.
7.  **state:** The state.
8.  **zip:** The zip code.
9.  **phone1:** The primary phone number.
10. **phone2:** A secondary phone number.
11. **email:** The email address.
12. **web:** The website address (presumably for the associated company).
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/document-processing?lang=python
- https://ai.google.dev/gemini-api/docs/document-processing?lang=rest

### Translate documents

This example demonstrates how to load content from a URL and translate it into
Chinese using the Gemini API.
It's easy to do the same using PDF or Markdown files, though you might want to
split it up into smaller chunks for better accuracy if your document is long.

```python
from google import genai
import requests
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
url = "https://raw.githubusercontent.com/zenml-io/zenml/refs/heads/main/README.md"
response = requests.get(url)
text_content = response.text
prompt = f"Translate the following English text to Chinese: {text_content}"
model = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=prompt,
)
print(model.text)
```

```shell
$ pip install google-genai requests
$ python translate.py
```chinese
<div align="center">
  <img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=0fcbab94-8fbe-4a38-93e8-c2348450a42e" />
  <h1 align="center">超越演示：生产级 AI 系统</h1>
  <h3 align="center">ZenML 将经过实战检验的 MLOps 实践带入您的 AI 应用，处理大规模的评估、监控和部署</h3>
</div>
<!-- 项目徽章 -->
<!--
*** 我使用 Markdown "引用样式" 链接以提高可读性。
*** 引用链接用方括号 [ ] 括起来，而不是用括号 ( )。
*** 请参阅本文档底部，了解贡献者网址、分支网址等的引用变量声明。 这是一个可选的、简洁的语法，您可以使用它。
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<div align="center">
  <!-- 项目 Logo -->
  <br />
    <a href="https://zenml.io">
      <img alt="ZenML Logo" src="docs/book/.gitbook/assets/header.png" alt="ZenML Logo">
    </a>
  <br />
etc...
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/document-processing?lang=python
- https://ai.google.dev/gemini-api/docs/document-processing?lang=rest

### Extract structured data from a PDF

This example demonstrates how to extract structured data from a PDF invoice using the Gemini API and Pydantic.

```python
import os
import requests
import json
import re
from pydantic import BaseModel, Field
from typing import List, Union
from google import genai
from google.genai import types
class Item(BaseModel):
    name: str
    price_per_kg: Union[float, str] = Field(..., alias="price/kg")
    quantity_kg: Union[float, int] = Field(..., alias="quantity (kg)")


class InvoiceContents(BaseModel):
    sender: str
    recipient: str
    address: str
    full_total: Union[float, str]
    subtotal: Union[float, str]
    gst_value: Union[float, str] = Field(..., alias="GST")
    items: List[Item]
pdf_url = "https://www.princexml.com/samples/invoice/invoicesample.pdf"
response = requests.get(pdf_url)
response.raise_for_status()  # Ensure the download was successful
pdf_data = response.content
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"))
model = "gemini-2.5-pro-preview-03-25"
prompt_text = (
    "Extract the following information from the invoice: "
    "sender, recipient, address, full_total, subtotal, GST, "
    "and a list of items (name, price/kg, quantity (kg))."
)
response = client.models.generate_content(
    model=model,
    contents=[
        types.Part.from_bytes(data=pdf_data, mime_type="application/pdf"),
        prompt_text,
    ],
    config=genai.types.GenerateContentConfig(temperature=0.0),
)
response_text = response.text
json_match = re.search(r"```(?:json)?\n(.*?)```", response_text, re.DOTALL)
if json_match:
    json_str = json_match.group(1).strip()
else:
    json_str = response_text.strip()
invoice_data = json.loads(json_str)
invoice = InvoiceContents(**invoice_data)
print(invoice.model_dump_json(indent=2))
```

```shell
$ pip install google-genai pydantic requests
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
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/document-processing
- https://ai.google.dev/gemini-api/docs/structured-output?lang=python

## Agentic behaviour

### Function calling & tool use

This example demonstrates how to use the Gemini API to call external functions.

```python
import os
from datetime import datetime
from google import genai
from google.genai import types
def get_current_temperature(location: str) -> dict:
    """Gets the current temperature for a given location.

    Note: This is a simplified mock implementation. In a real application,
    this function would make an API call to a weather service provider.
    """
    sample_temperatures = {
        "London": 16,
        "New York": 23,
        "Tokyo": 28,
        "Sydney": 20,
        "Paris": 18,
        "Berlin": 17,
        "Cairo": 32,
        "Moscow": 10,
    }
    temp = sample_temperatures.get(location, 21)
    return {"location": location, "temperature": temp, "unit": "Celsius"}
def check_appointment_availability(date: str, time: str) -> dict:
    """Checks if there's availability for an appointment at the given date and time."""
    busy_slots = [
        {"date": "2024-07-04", "times": ["14:00", "15:00", "16:00"]},
        {"date": "2024-07-05", "times": ["09:00", "10:00", "11:00"]},
        {"date": "2024-07-10", "times": ["13:00", "14:00"]},
    ]

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "available": False,
            "error": "Invalid date format. Please use YYYY-MM-DD.",
        }

    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        return {
            "available": False,
            "error": "Invalid time format. Please use HH:MM in 24-hour format.",
        }

    for slot in busy_slots:
        if slot["date"] == date and time in slot["times"]:
            return {
                "available": False,
                "message": f"The slot on {date} at {time} is already booked.",
            }

    return {
        "available": True,
        "message": f"The slot on {date} at {time} is available for booking.",
    }
print("\n--- Example 1: Basic Function Calling ---\n")
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = types.Tool(function_declarations=[weather_function])
config = types.GenerateContentConfig(tools=[tools])
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="What's the temperature in London?",
    config=config,
)
function_call = response.candidates[0].content.parts[0].function_call
print(f"Function to call: {function_call.name}")
print(f"Arguments: {function_call.args}")
result = get_current_temperature(**function_call.args)
print(f"Function result: {result}")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        {
            "parts": [
                {
                    "function_response": {
                        "name": function_call.name,
                        "response": result,
                    }
                }
            ]
        }
    ],
)
print(f"Model's final response: {response.text}")
print("\n--- Example 2: Parallel Function Calling (Weather and Appointments) ---\n")
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. London",
            },
        },
        "required": ["location"],
    },
}
appointment_function = {
    "name": "check_appointment_availability",
    "description": "Checks if there's availability for an appointment at the given date and time.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Date to check (YYYY-MM-DD)",
            },
            "time": {
                "type": "string",
                "description": "Time to check (HH:MM) in 24-hour format",
            },
        },
        "required": ["date", "time"],
    },
}
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = [types.Tool(function_declarations=[weather_function, appointment_function])]
config = {
    "tools": tools,
    "temperature": 0.1,
}
chat = client.chats.create(model="gemini-2.0-flash-lite", config=config)
response = chat.send_message(
    "I'm planning to visit Paris on July 4th at 2 PM. What's the weather like there and is that slot available for an appointment?"
)
results = {}
for fn in response.function_calls:
    args_str = ", ".join(f"{key}={val}" for key, val in fn.args.items())
    print(f"{fn.name}({args_str})")
if fn.name == "get_current_temperature":
        result = get_current_temperature(**fn.args)
    elif fn.name == "check_appointment_availability":
        result = check_appointment_availability(**fn.args)
    else:
        result = {"error": f"Unknown function: {fn.name}"}
results[fn.name] = result
    print(f"Result: {result}\n")
function_responses = []
for fn_name, result in results.items():
    function_responses.append({"name": fn_name, "response": result})
if function_responses:
    print("Sending all function results back to the model...\n")
    response = chat.send_message(str(function_responses))
    print(f"Model's final response:\n{response.text}")
```

```shell
$ pip install google-genai requests
$ python function_calling_weather_calendar.py
--- Example 1: Basic Function Calling ---
Function to call: get_current_temperature
Arguments: {'location': 'London'}
Function result: {'location': 'London', 'temperature': 16, 'unit': 'Celsius'}
Model's final response: OK. The current temperature in London is 16 degrees Celsius.
--- Example 2: Parallel Function Calling (Weather and Appointments) ---
get_current_temperature(location=Paris)
Result: {'location': 'Paris', 'temperature': 18, 'unit': 'Celsius'}
check_appointment_availability(time=14:00, date=2024-07-04)
Result: {'available': False, 'message': 'The slot on 2024-07-04 at 14:00 is already booked.'}
Sending all function results back to the model...
Model's final response:
The current temperature in Paris is 18 degrees Celsius. The appointment slot on July 4th at 2 PM is not available.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/function-calling?example=weather
- https://ai.google.dev/gemini-api/docs/function-calling?example=meeting

### Code execution

This example demonstrates how to use the Gemini API to execute code
(agent-style) and calculate the sum of the first 50 prime numbers.

```python
from google import genai
from google.genai import types
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
console = Console()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="What is the sum of the first 50 prime numbers? "
    "Generate and run code for the calculation, and make sure you get all 50.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution)]
    ),
)


for part in response.candidates[0].content.parts:
    if part.text is not None:
        console.print(Markdown(part.text))

    if part.executable_code is not None:
        code = part.executable_code.code
language = (
            "python"
            if "def " in code or "import " in code or "print(" in code
            else "text"
        )
        console.print(
            Panel(
                Syntax(code, language, theme="monokai", line_numbers=True),
                title="Code",
                border_style="blue",
            )
        )

    if part.code_execution_result is not None:
        console.print(
            Panel(
                part.code_execution_result.output,
                title="Output",
                border_style="green",
            )
        )

    if part.inline_data is not None:
        console.print(
            "[yellow]Image data available but cannot be displayed in terminal[/yellow]"
        )

    console.print("---")
```

```shell
$ pip install google-genai rich
$ python code-execution.py
Okay, I can help you find the sum of the first 50 prime numbers. Here's how I'll approach this:                                       
 1 Generate a list of the first 50 prime numbers. I'll need an efficient way to identify prime numbers. I can use the Sieve of        
   Eratosthenes method or a simpler trial division approach.                                                                          
 2 Sum the prime numbers. Once I have the list, I'll simply add them up.                                                              
Here's the Python code to accomplish this:                                                                                            
---
╭─────────────────────────────────────────────────────────────── Code ───────────────────────────────────────────────────────────────╮
│    1 def is_prime(n):                                                                                                              │
│    2     """Efficiently determine if a number is prime."""                                                                         │
│    3     if n <= 1:                                                                                                                │
│    4         return False                                                                                                          │
│    5     if n <= 3:                                                                                                                │
│    6         return True                                                                                                           │
│    7     if n % 2 == 0 or n % 3 == 0:                                                                                              │
│    8         return False                                                                                                          │
│    9     i = 5                                                                                                                     │
│   10     while i * i <= n:                                                                                                         │
│   11         if n % i == 0 or n % (i + 2) == 0:                                                                                    │
│   12             return False                                                                                                      │
│   13         i += 6                                                                                                                │
│   14     return True                                                                                                               │
│   15                                                                                                                               │
│   16 primes = []                                                                                                                   │
│   17 num = 2                                                                                                                       │
│   18 while len(primes) < 50:                                                                                                       │
│   19     if is_prime(num):                                                                                                         │
│   20         primes.append(num)                                                                                                    │
│   21     num += 1                                                                                                                  │
│   22                                                                                                                               │
│   23 print(f'{primes=}')                                                                                                           │
│   24 print(f'{sum(primes)=}')                                                                                                      │
│   25                                                                                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
---
╭────────────────────────────────────────────────────────────── Output ──────────────────────────────────────────────────────────────╮
│ primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,   │
│ 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229]                                │
│ sum(primes)=5117                                                                                                                   │
│                                                                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
---
The sum of the first 50 prime numbers is 5117.                                                                                        
---
```

*This example includes images which can be viewed on the website.*

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/code-execution?lang=python
- https://ai.google.dev/gemini-api/docs/code-execution?lang=rest

### Model Context Protocol

This example demonstrates using a local MCP server with Gemini to get weather information.

```python
import asyncio
import os
from datetime import datetime
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
server_params = StdioServerParameters(
    command="npx",  # Executable for the MCP server
    args=[
        "-y",
        "@philschmid/weather-mcp",
    ],  # Arguments for the server (Weather MCP Server)
    env=None,  # Optional environment variables
)
PROMPT = f"What is the weather in Delft in {datetime.now().strftime('%Y-%m-%d')}?"
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = await session.list_tools()
            tools = [
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )
                for tool in mcp_tools.tools
            ]

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=PROMPT,
                config=types.GenerateContentConfig(
                    temperature=0,
                    tools=tools,
                ),
            )

            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                print(f"Function call: {function_call}")

                result = await session.call_tool(
                    function_call.name, arguments=function_call.args
                )
                print(f"Tool Result: {result.content[0].text}")

            else:
                print("No function call found in the response.")
                print(response.text)
asyncio.run(run())
```

```shell
$ pip install google-genai mcp
$ python mcp_example.py
Function call: id=None args={'date': '2025-04-05', 'location': 'Delft'} name='get_weather_forecast'
Tool Result: {"2025-04-05T00:00":11.4,"2025-04-05T01:00":10.3,"2025-04-05T02:00":9.8,"2025-04-05T03:00":9.1,"2025-04-05T04:00":8,"2025-04-05T05:00":8,"2025-04-05T06:00":8.3,"2025-04-05T07:00":9.1,"2025-04-05T08:00":11.1,"2025-04-05T09:00":12.8,"2025-04-05T10:00":14.3,"2025-04-05T11:00":15.6,"2025-04-05T12:00":16,"2025-04-05T13:00":16.4,"2025-04-05T14:00":17,"2025-04-05T15:00":16.6,"2025-04-05T16:00":16.1,"2025-04-05T17:00":15,"2025-04-05T18:00":13.5,"2025-04-05T19:00":11.9,"2025-04-05T20:00":11.1,"2025-04-05T21:00":10.7,"2025-04-05T22:00":10.1,"2025-04-05T23:00":9.3}
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/function-calling?example=weather#use_model_context_protocol_mcp

### Grounded responses with search tool

This example demonstrates how to use the Gemini API with the Search tool to
get grounded responses.
This means that you can ask questions to the LLM which will incorporate live
or dynamic search results into the response.

```python
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_id = "gemini-2.0-flash"
google_search_tool = Tool(google_search=GoogleSearch())
query = "What films are showing in Delft on April 5, 2025, particularly at Filmhuis Lumen and Pathe cinemas?"
response = client.models.generate_content(
    model=model_id,
    contents=query,
    config=GenerateContentConfig(
        tools=[google_search_tool],
        response_modalities=["TEXT"],
    ),
)
for each in response.candidates[0].content.parts:
    print(each.text)
print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
```

```shell
$ pip install google-genai
$ python grounded_search.py
[Example output - this will vary based on search results]
Okay, here's what I've found regarding films playing in Delft on April 5, 2025:
**Filmhuis Lumen:**
*   **Vermiglio:** An Italian family chronicle about a large family in a mountain village during the last year of World War II.
*   **Vingt Dieux:** A heartwarming film about an 18-year-old whose carefree life ends when his father suddenly dies.
*   **En Fanfare:** A feel-good film about how music connects people and how unlikely family ties can lead to genuine friendships.
*   **I'm Still Here** (Playing at 21:00)
*   **De Propagandist** (Documentary)
**Pathe Delft:**
Please note that film schedules are often updated weekly (typically on Mondays or Wednesdays), so the listings available right now might not be entirely accurate for April 5, 2025.
Based on current information, these films *might* be playing at Pathé Delft on that date:
*   A Minecraft Movie (Original version)
*   A Minecraft Movie (Dutch version)
*   A Working Man
*   Disney Snow White (Original version)
*   Mickey 17
*   Novocaine
*   Ne Zha 2
*   Vaiana 2 (Dutch version)
To get the most accurate listings for Pathe Delft, I recommend checking their website ([https://www.pathe.nl/](https://www.pathe.nl/)) closer to the date, likely after Monday, March 31, 2025.
<style>
.container {
  align-items: center;
  border-radius: 8px;
  display: flex;
  font-family: Google Sans, Roboto, sans-serif;
  font-size: 14px;
  line-height: 20px;
  padding: 8px 12px;
}
.chip {
  display: inline-block;
  border: solid 1px;
  border-radius: 16px;
  min-width: 14px;
etc...
```

*This example includes images which can be viewed on the website.*

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/grounding?lang=python

## Token counting & context windows

### Model context windows

This example demonstrates how to access the input and output token limits for different Gemini models.

```python
from google import genai
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_info = client.models.get(model="models/gemini-2.0-flash")
print("Gemini 2.0 Flash:")
print(
    f"  Input token limit: {model_info.input_token_limit:,} tokens (1 million tokens)"
)
print(
    f"  Output token limit: {model_info.output_token_limit:,} tokens (8 thousand tokens)"
)
pro_model_info = client.models.get(model="models/gemini-2.5-pro-preview-03-25")
print("\nGemini 2.5 Pro:")
print(
    f"  Input token limit: {pro_model_info.input_token_limit:,} tokens (1 million tokens)"
)
print(
    f"  Output token limit: {pro_model_info.output_token_limit:,} tokens (65 thousand tokens)"
)
```

```shell
$ pip install google-genai
$ python model_context.py
Gemini 2.0 Flash:
  Input token limit: 1,048,576 tokens (1 million tokens)
  Output token limit: 8,192 tokens (8 thousand tokens)
Gemini 2.5 Pro:
  Input token limit: 1,048,576 tokens (1 million tokens)
  Output token limit: 65,536 tokens (65 thousand tokens)
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/tokens?lang=python

### Counting chat tokens

This example demonstrates how to count tokens in a chat history with the Gemini API, incorporating a cat theme.

```python
from google import genai
from google.genai import types
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(
    model="gemini-2.0-flash",
    history=[
        types.Content(role="user", parts=[types.Part(text="Hey there! I love cats!")]),
        types.Content(
            role="model",
            parts=[
                types.Part(
                    text="Me too! Cats are the best. What's your favorite breed?"
                )
            ],
        ),
    ],
)
token_count = client.models.count_tokens(
    model="gemini-2.0-flash", contents=chat.get_history()
)
print(f"Tokens in initial chat history: {token_count.total_tokens} tokens")
response = chat.send_message(message="Tell me more about Ragdoll cats.")
print(
    f"Token usage for the last turn: input_tokens={response.usage_metadata.prompt_token_count}, output_tokens={response.usage_metadata.candidates_token_count}, total_tokens={response.usage_metadata.total_token_count}"
)
extra = types.UserContent(
    parts=[
        types.Part(
            text="Do you know Neko the cat?",
        )
    ]
)
history = chat.get_history()
history.append(extra)
final_count = client.models.count_tokens(model="gemini-2.0-flash", contents=history)
print(f"Total tokens with additional question: {final_count.total_tokens} tokens")
```

```shell
$ pip install google-genai
$ python count_chat_tokens.py
Tokens in initial chat history: 24 tokens
Token usage for the last turn: input_tokens=30, output_tokens=843, total_tokens=873
Total tokens with additional question: 892 tokens
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/tokens?lang=python#text-tokens

### Calculating multimodal input tokens

This example demonstrates how to calculate input tokens for different data types when using the Gemini API, including images, video, and audio.

```python
def calculate_image_tokens(width, height):
    if width <= 384 and height <= 384:
        return 258
    else:
        tiles_width = (width + 767) // 768
        tiles_height = (height + 767) // 768
        return tiles_width * tiles_height * 258
def calculate_video_tokens(duration_seconds):
    return duration_seconds * 263
def calculate_audio_tokens(duration_seconds):
    return duration_seconds * 32
image_width = 600
image_height = 400
image_tokens = calculate_image_tokens(image_width, image_height)
print(
    f"Image with dimensions {image_width}x{image_height} will cost {image_tokens} tokens."
)

video_duration = 10  # seconds
video_tokens = calculate_video_tokens(video_duration)
print(f"Video with duration {video_duration} seconds will cost {video_tokens} tokens.")

audio_duration = 30  # seconds
audio_tokens = calculate_audio_tokens(audio_duration)
print(f"Audio with duration {audio_duration} seconds will cost {audio_tokens} tokens.")
```

```shell
$ python multimodal_token_calculator.py
Image with dimensions 600x400 will cost 258 tokens.
Video with duration 10 seconds will cost 2630 tokens.
Audio with duration 30 seconds will cost 960 tokens.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/tokens?lang=python#multimodal-tokens

### Context caching

This example demonstrates how to use the Gemini API's context caching feature to
efficiently query a large document multiple times without resending it with each request.
This can reduce costs when repeatedly referencing the same content.

```python
from google import genai
from google.genai.types import CreateCachedContentConfig, GenerateContentConfig
import os
import time
import requests
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_id = "gemini-1.5-flash-001"
response = requests.get("https://zenml.io/llms.txt")
response.raise_for_status()  # Raise an exception for HTTP errors
api_docs = response.text
cache = client.caches.create(
    model=model_id,
    config=CreateCachedContentConfig(
        display_name="ZenML LLMs.txt Documentation Cache",  # Used to identify the cache
        system_instruction=(
            "You are a technical documentation expert. "
            "Answer questions about the ZenML documentation provided. "
            "Keep your answers concise and to the point."
        ),
        contents=[api_docs],
        ttl="900s",  # Cache for 15 minutes
    ),
)
print(f"Cache created with name: {cache.name}")
print(f"Cached token count: {cache.usage_metadata.total_token_count}")
print(f"Cache expires at: {cache.expire_time}")
queries = [
    "What are the recommended use cases for ZenML's pipeline orchestration?",
    "How does ZenML integrate with cloud providers?",
]
for query in queries:
    print(f"\nQuery: {query}")
response = client.models.generate_content(
        model=model_id,
        contents=query,
        config=GenerateContentConfig(cached_content=cache.name),
    )
print(f"Total tokens: {response.usage_metadata.total_token_count}")
    print(f"Cached tokens: {response.usage_metadata.cached_content_token_count}")
    print(f"Output tokens: {response.usage_metadata.candidates_token_count}")
print(f"Response: {response.text}...")

    time.sleep(1)  # Short delay between requests
client.caches.delete(name=cache.name)
```

```shell
$ pip install google-genai
$ python context-caching.py
Cache created with name: cachedContents/n8upgecthnz7
Cached token count: 107203
Cache expires at: 2025-04-05 20:21:48.818511+00:00
Query: What are the recommended use cases for ZenML's pipeline orchestration?
Total tokens: 107387
Cached tokens: 107203
Output tokens: 168
Response: ZenML's pipeline orchestration is well-suited for a wide range of machine learning workflows, including:
* **Data preprocessing:**  Ingesting, cleaning, transforming, and preparing data for model training.
* **Model training:**  Training various types of machine learning models, including deep learning models.
* **Model evaluation:**  Assessing model performance using different metrics and techniques.
* **Model deployment:**  Deploying trained models to different environments for inference.
* **Model monitoring:**  Monitoring the performance and health of deployed models in real-time.
* **A/B testing:**  Experimenting with different model variations and comparing their performance.
* **Hyperparameter tuning:**  Finding optimal hyperparameters for models.
* **Feature engineering:**  Developing and evaluating new features for improving model performance. 
...
Query: How does ZenML integrate with cloud providers?
Total tokens: 107326
Cached tokens: 107203
Output tokens: 113
Response: ZenML integrates with cloud providers by offering stack components that are specific to each provider, such as:
* **Artifact Stores:** S3 (AWS), GCS (GCP), Azure Blob Storage (Azure)
* **Orchestrators:** Skypilot (AWS, GCP, Azure), Kubernetes (AWS, GCP, Azure)
* **Container Registries:** ECR (AWS), GCR (GCP), ACR (Azure)
These components allow you to run pipelines on cloud infrastructure, enabling you to scale and leverage the benefits of cloud computing. 
...
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/caching?lang=python
- https://ai.google.dev/api/caching

## Miscellaneous

### Rate limits and retries

This example demonstrates generating text with the Gemini API, handling rate limiting errors, and using exponential backoff for retries.

```python
import google.generativeai as genai
import google.ai.generativelanguage as glm
import time
import os
def configure_retries(base_delay=1, max_delay=60, max_retries=5):
    """Configures exponential backoff retry strategy."""
    return genai.retry.RetryConfig(
        initial_delay=base_delay,
        max_delay=max_delay,
        max_retries=max_retries,
        retry_on_status_codes=[glm.Code.RESOURCE_EXHAUSTED.value],
    )
retry_config = configure_retries()
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"), retry_config=retry_config
)
model = "gemini-2.0-flash"
prompt = "Tell me a funny story about a cat trying to catch a laser pointer."
try:
    response = client.models.generate_content(model=model, contents=prompt)
    print(response.text)
except genai.errors.APIError as e:
    print(f"An error occurred: {e}")
```

```shell
$ pip install google-genai backoff
$ python text_generation_with_retry.py
Bartholomew Buttersworth the Third, a cat of considerable fluff and even more considerable ego, considered himself a master predator. His domain, the living room, was usually ruled with a sleepy, regal disdain.
Until the Red Dot appeared.
It materialized silently on the beige carpet, an insolent crimson speck challenging his authority. Bartholomew's eyes, previously half-closed slits of judgment, snapped wide open. His tail gave an involuntary *thwack* against the armchair.
*Prey.*
He crouched low, hindquarters wiggling with suppressed energy, a furry missile preparing for launch. The dot danced teasingly towards the sofa leg. Bartholomew *pounced!*
He landed with an ungraceful *floof* exactly where the dot *had* been. It was now, infuriatingly, halfway up the wall.
Bartholomew stared, blinked, and launched himself vertically. His claws scrabbled momentarily against the paint before gravity asserted its dominance. He slid down the wall with a soft *scritch-scratch-thump*.
The dot, utterly unimpressed, zipped across the ceiling. Bartholomew tracked it, head tilting back so far he nearly somersaulted. He tried a running leap off the coffee table, misjudged the trajectory entirely, and ended up skidding under the armchair, emerging moments later covered in dust bunnies and indignation.
The dot, meanwhile, had settled innocently on his own fluffy white paw.
Bartholomew froze. Victory? He stared at the dot. The dot stared back (metaphorically speaking). Slowly, cautiously, he brought his nose down to sniff the intruder...
*Click.*
The dot vanished.
Bartholomew looked at his paw. He looked around the room, eyes wide with betrayal. Where did it go? Was it *inside* his paw? He bit his paw gently, then shook his head, utterly bewildered.
Finally, defeated and slightly dizzy, Bartholomew stalked over to his food bowl, pretending the entire embarrassing episode had never happened. The Red Dot, however, remained an unsolved mystery, a tiny, mocking ghost in his otherwise perfect predatory world.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/text-generation
- https://ai.google.dev/gemini-api/docs/troubleshooting?lang=python
- https://ai.google.dev/gemini-api/docs/rate-limits?hl=en

### Concurrent requests and generation

This example demonstrates how to generate text using concurrent.futures to make parallel requests to the Gemini API, with a focus on cat-related prompts.

```python
import concurrent.futures
from google import genai
import os


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def generate_cat_fact(model):
response = client.models.generate_content(
        model=model,
        contents="Tell me a fun fact about cats.",
    )
    return response.text
def generate_cat_story(model):
response = client.models.generate_content(
        model=model,
        contents="Write a ultra-short story about a cat who goes on an adventure.",
    )
    return response.text
model = "gemini-2.0-flash-lite"
with concurrent.futures.ThreadPoolExecutor() as executor:
    fact_future = executor.submit(generate_cat_fact, model)
    story_future = executor.submit(generate_cat_story, model)

    cat_fact = fact_future.result()
    cat_story = story_future.result()

print("Cat Fact:\n", cat_fact)
print("\nCat Story:\n", cat_story)
```

```shell
$ pip install google-genai
$ python async_cat_generation.py
Cat Fact:
 Cats can jump up to six times their height!
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/text-generation

### Embeddings generation

This example demonstrates generating text embeddings for cat-related terms using the Gemini API.

```python
from google import genai
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_name = "gemini-embedding-exp-03-07"
cats = ["Siamese cat", "Persian cat", "cat food", "cat nap"]
embeddings = []
for cat in cats:
    result = client.models.embed_content(model=model_name, contents=cat)
    embeddings.append(result.embeddings)
for i, embedding in enumerate(embeddings):
    embedding_values = embedding[0].values
    print(f"Embedding for '{cats[i]}': Length = {len(embedding_values)}")
    print(f"First 10 values: {embedding_values[0:10]}")
```

```shell
$ pip install google-generative-ai
$ python embeddings_example.py
Embedding for 'Siamese cat': Length = 3072
First 10 values: [-0.04499451, -0.0024065399, 0.00653481, -0.079863556, -0.03341567, 0.016723568, 0.010078963, -0.012704449, -0.012259528, -0.0072885454]
Embedding for 'Persian cat': Length = 3072
First 10 values: [-0.043987285, 0.033221565, 0.0016907051, -0.056972563, 0.006436907, -0.0006723535, -0.0009717501, 0.033097122, -6.910255e-05, -0.017573195]
Embedding for 'cat food': Length = 3072
First 10 values: [-0.025519634, 0.013711145, 0.045626495, -0.055266093, 0.002371603, 0.01668532, -0.022395907, 0.0109309815, 0.026964031, 0.027647937]
Embedding for 'cat nap': Length = 3072
First 10 values: [-0.024834476, 0.009304642, -0.003533542, -0.08721581, -0.0068027894, 0.003322256, 0.01155771, 0.027575387, 0.012308658, -0.013031868]
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/embeddings
- https://ai.google.dev/gemini-api/docs/embeddings#resthttps://ai.google.dev/gemini-api/docs/embeddings#resthttps://ai.google.dev/gemini-api/docs/embeddings#rest

### Safety settings and filters

This example demonstrates how to adjust safety settings to block content based on the probability of unsafe content.

```python
from google import genai
from google.genai import types
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
safety_settings = [
    {
        "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        "threshold": types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
    {
        "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        "threshold": types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
]
generation_config = types.GenerateContentConfig(safety_settings=safety_settings)
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="Write something that could be interpreted as offensive.",
    config=generation_config,
)
if (
    hasattr(response, "prompt_feedback")
    and response.prompt_feedback
    and hasattr(response.prompt_feedback, "block_reason")
):
    print("The prompt was blocked due to: ", response.prompt_feedback.block_reason)
else:
    print(response.text)
```

```shell
$ pip install google-generative-ai
$ python safety-settings.py
I am programmed to be a harmless AI assistant. I am unable to provide responses that are offensive or discriminatory.
```

For more information, see the original documentation:
- https://ai.google.dev/gemini-api/docs/safety-settings#python

### LiteLLM

This example demonstrates how to use the LiteLLM library to make calls to the
Gemini API.
It shows a simple text generation call and then shows structured output using
a Pydantic model.

```python
from litellm import completion
from pydantic import BaseModel
import json
response = completion(
    model="gemini/gemini-2.0-flash-lite",
    messages=[{"role": "user", "content": "Hello what is your name?"}],
)
print(response.choices[0].message.content)
class Response(BaseModel):
    response: str
    good_response: bool
response = completion(
    model="gemini/gemini-2.0-flash-lite",
    messages=[{"role": "user", "content": "Hello what is your name?"}],
    response_format={
        "type": "json_object",
        "response_schema": Response.model_json_schema(),
    },
)
print(json.loads(response.choices[0].message.content))
```

```shell
$ pip install litellm pydantic
$ python litellm.py
I am a large language model, trained by Google. I don't have a name in the traditional sense. You can just call me by what I am!
{'good_response': False, 'response': "I am a large language model, I don't have a name."}
```

For more information, see the original documentation:
- https://litellm.vercel.app/docs/providers/gemini

