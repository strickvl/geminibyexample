# Calculating multimodal input tokens
# This example demonstrates how to calculate input tokens for different data types when using the Gemini API, including images, video, and audio.

# Images are tokenized based on their dimensions.
# With Gemini 2.0, image inputs with both dimensions <=384 pixels are counted as 258 tokens.
# Images larger in one or both dimensions are cropped and scaled as needed into tiles of 768x768 pixels, each counted as 258 tokens.
def calculate_image_tokens(width, height):
    if width <= 384 and height <= 384:
        return 258
    else:
        tiles_width = (width + 767) // 768
        tiles_height = (height + 767) // 768
        return tiles_width * tiles_height * 258


# Video is tokenized at a fixed rate of 263 tokens per second.
def calculate_video_tokens(duration_seconds):
    return duration_seconds * 263


# Audio is tokenized at a fixed rate of 32 tokens per second.
def calculate_audio_tokens(duration_seconds):
    return duration_seconds * 32


# Example Usage
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
