import os

import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
client = AsyncOpenAI()


load_dotenv()  # reads ./.env - the API keys live there, never in code

# The OpenAI key on this machine has no credits (429 credit_balance_exhausted),
# so by default the SAME OpenAI SDK is pointed at Groq's OpenAI-compatible
# endpoint. After topping up, set LLM_PROVIDER=openai in .env to switch back.
PROVIDER = os.getenv("LLM_PROVIDER", "groq")
if PROVIDER == "groq":
    client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
    MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
else:
    client = OpenAI()  # picks up OPENAI_API_KEY from the environment
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = """
You are an expert voice agent. You are given the transcript of what the
user said using voice. Respond as if you are a voice agent - whatever
you say will be converted back to audio using AI and played back to the
user.
"""

async def tts(speech: str):
    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=speech,
        instructions="Speak in a cheerful manner, full of delight and happiness.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)   # noise cancellation
        print("Speak something...")

        audio = r.listen(source)             # blocks until you pause (~2s of silence)
        print("Processing audio...")

        stt = r.recognize_google(audio)      # sends audio to Google's STT backend
        print("You said:", stt)      
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": stt},
            ],
        )

        ai_response = response.choices[0].message.content
        print(ai_response)


if __name__ == "__main__":
    main()