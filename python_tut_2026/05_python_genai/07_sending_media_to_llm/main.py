from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


openai_client = OpenAI()

response = openai_client.chat.completions.create(
    # gpt-4-vision-preview was RETIRED by OpenAI (404 model_not_found).
    # Modern gpt-4o / gpt-4.1 models accept images natively - no special model needed.
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate a caption for this image about 50 words."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)