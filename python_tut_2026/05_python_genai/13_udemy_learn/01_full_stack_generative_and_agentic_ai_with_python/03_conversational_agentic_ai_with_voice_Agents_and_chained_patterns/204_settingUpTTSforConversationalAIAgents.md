# Step 3 — TTS, Then Looping Into a Real Conversation

The last piece of the chain: turn the LLM's text reply into audio and
play it. Then wrap the whole STT → LLM → TTS pipeline in a loop with
memory, and it's a real conversational voice agent.

---

## 🟢 Beginner — what a TTS model is

A TTS (Text-to-Speech) model takes text in, returns audio out. OpenAI has
one; **ElevenLabs** is a common alternative, notable for voice cloning
(you can generate speech in your *own* voice). OpenAI's own **OpenAI.fm**
demo site lets you try different voices and styles (chill, professional,
"cowboy") on the same text before writing any code.

---

## 🟡 Intermediate — the async streaming TTS call

Verified against OpenAI's own docs:

```python
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

client = AsyncOpenAI()

async def tts(speech: str):
    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=speech,
        instructions="Speak in a cheerful manner, full of delight and happiness.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

asyncio.run(tts(ai_response))
```

| Part | Does |
|---|---|
| `AsyncOpenAI()` | a **different client class** from the sync `OpenAI()` used for the chat completion step |
| `voice="coral"` | one of several built-in voice presets |
| `instructions="..."` | the *tone* to speak in - separate from *what* to speak |
| `response_format="pcm"` | one of several audio formats (others: opus, aac, flac, wav) |
| `LocalAudioPlayer().play(response)` | plays the streamed audio directly on the machine - no file saved |

**Install gotcha:** `LocalAudioPlayer` needs an extra install beyond the base SDK:

```bash
pip install -U openai
pip install 'openai[voice_helpers]'
```

Missing this gives an error demanding the extra package - expected, not a sign of broken code.

---

## 🔴 Expert — looping it into a real conversation

Two changes turn the three one-shot steps into an actual back-and-forth agent:

**1. Wrap everything in `while True:`** - otherwise the program exits after a single exchange.

**2. Keep a running `messages` list instead of one system+user pair per turn:**

```python
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    stt = listen_and_transcribe()          # the STT step
    messages.append({"role": "user", "content": stt})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )
    ai_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_response})

    asyncio.run(tts(ai_response))          # the TTS step
```

This is the difference between a one-off Q&A and real memory. Appending
both the user's turn *and* the assistant's reply to `messages` is what let
the demo correctly answer "what is my name?" several turns after the user
first said it - the full history goes to the LLM every single call, not
just the latest sentence.

---

## The complete picture

```text
  mic ──► STT ──► text ──► messages.append ──► LLM (full history) ──► text
                                                                          │
                                                             messages.append
                                                                          │
                                                                          ▼
                                                    TTS (async, streamed) ──► speakers
                                                                          │
                                                                    loop back to mic
```

That's the full chained architecture: STT, a memory-aware LLM call, TTS,
on repeat.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **TTS** | text in, audio out - OpenAI's or alternatives like ElevenLabs (voice cloning) |
| **`AsyncOpenAI`** | the async client class, separate from the sync `OpenAI()` used earlier |
| **`LocalAudioPlayer`** | plays streamed audio directly - needs `pip install 'openai[voice_helpers]'` |
| **`instructions=`** | sets the *tone* of the spoken output, independent of the text content |
| **Running `messages` list** | what gives the agent real multi-turn memory, instead of one-shot replies |

---

## Sources

- [Text to speech — OpenAI developer docs](https://developers.openai.com/api/docs/guides/text-to-speech)
