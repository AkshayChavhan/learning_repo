# Image-to-text with a vision model
# REQUIRES: huggingface-cli login (for gated models)
# CPU speed: ~30-60 seconds per image

from transformers import pipeline
from PIL import Image
import requests

print("Loading vision model... (first time: downloads ~1.7 GB)")
print("This model is NOT gated, so no authentication needed.\n")

# Use a smaller vision model that works on CPU
# Salesforce BLIP: 990M params, ~30 sec per image on CPU
pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# Load an image from HuggingFace's example dataset
print("Downloading example image...")
url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"
image = Image.open(requests.get(url, stream=True).raw)

# Save it locally so we can see what we're analyzing
image.save("example_image.jpg")
print(f"Image saved as example_image.jpg ({image.size})\n")

# Generate a caption
print("Generating caption... (this takes ~30 seconds on CPU)\n")
result = pipe(image)

# Extract and display
caption = result[0]["generated_text"]
print(f"Caption: {caption}")
