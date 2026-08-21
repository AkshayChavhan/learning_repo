# Image-to-text with a vision LLM (image Q&A, not just captions)
# NOTE: original code used gemma-4-31B-it (31 billion params, 62 GB) — NOT runnable on CPU
# This version uses gemma-2-2b-it (2 billion params, ~5 GB) — slow but works on CPU
#
# REQUIRES: huggingface-cli login (this model is gated)
# SPEED: ~2–3 minutes per query on CPU (will be faster with GPU)

from transformers import pipeline
from PIL import Image
import requests

print("Authenticating and loading model...")
print("(First time: downloads ~5 GB, requires: huggingface-cli login)\n")

# Use gemma-2-2b instead of gemma-4-31b
# 2B = runnable on CPU; 31B = GPU only
pipe = pipeline("image-text-to-text", model="google/gemma-2-2b-it")

# Prepare the image and question
print("Downloading image...")
image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"
image = Image.open(requests.get(image_url, stream=True).raw)

# Format messages for vision-language chat
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": image_url},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]

print("Running inference... (this takes ~2–3 minutes on CPU)\n")
result = pipe(text=messages)

print(f"Answer: {result}")

# The response will look like:
# [{'generated_text': '... model\'s answer here ...'}]