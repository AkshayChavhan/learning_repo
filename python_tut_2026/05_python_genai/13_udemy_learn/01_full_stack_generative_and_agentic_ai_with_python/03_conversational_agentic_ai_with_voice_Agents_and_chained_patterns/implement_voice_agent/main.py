import os

import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()  # reads ./.env - the API keys live there, never in code

# TTS (gpt-4o-mini-tts) exists only on OpenAI, so it gets its own async
# client - created AFTER load_dotenv(), otherwise OPENAI_API_KEY isn't set
# yet and the constructor raises "Missing credentials" before anything runs.
tts_client = AsyncOpenAI()

# Chat LLM: OpenAI by default (what the course uses). If the OpenAI key has
# no credits (429 credit_balance_exhausted), set LLM_PROVIDER=groq in .env -
# the SAME OpenAI SDK then talks to Groq's OpenAI-compatible endpoint instead.
PROVIDER = os.getenv("LLM_PROVIDER", "openai")
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
    async with tts_client.audio.speech.with_streaming_response.create(
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
        r.adjust_for_ambient_noise(source)   # calibrate once, not on every turn
        print("Voice agent ready. Say 'exit' or press Ctrl+C to stop.")

        while True:                          # one iteration = one exchange
            print("\nSpeak something...")
            audio = r.listen(source)         # blocks until you pause (~2s of silence)
            print("Processing audio...")

            try:
                stt = r.recognize_google(audio)   # sends audio to Google's STT backend
            except sr.UnknownValueError:          # noise / mumble - nothing transcribed
                print("Didn't catch that, try again.")
                continue
            except sr.RequestError as e:          # Google STT unreachable
                print("STT request failed:", e)
                continue

            print("You said:", stt)
            if stt.strip().lower() in ("exit", "quit", "stop"):
                print("Bye.")
                break

            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": stt},
                    ],
                )
            except Exception as e:  # e.g. OpenAI 429 (no credits) - don't kill the loop
                print(f"LLM call failed ({PROVIDER}/{MODEL}):", str(e)[:160])
                continue
            ai_response = response.choices[0].message.content
            print("AI :->", ai_response)

            try:
                asyncio.run(tts(ai_response))
            except Exception as e:  # e.g. OpenAI 429 (no credits) - keep the loop alive
                print("TTS unavailable:", str(e)[:120])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")