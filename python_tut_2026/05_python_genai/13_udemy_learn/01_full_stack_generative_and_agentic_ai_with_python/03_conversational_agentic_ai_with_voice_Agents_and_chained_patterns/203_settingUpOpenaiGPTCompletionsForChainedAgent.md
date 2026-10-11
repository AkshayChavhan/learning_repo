# Step 2 — The LLM Call, Prompted for Voice

With STT done, the transcribed text goes to an ordinary chat completion -
same pattern used everywhere else in this course. The one thing that's
different: the system prompt has to know its output will be *spoken*.

---

## 🟢 Beginner — just a normal chat completion

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are an expert voice agent. You are given the transcript of what the
user said using voice. Respond as if you are a voice agent - whatever
you say will be converted back to audio using AI and played back to the
user.
"""

def main():
    # stt = ... (the transcribed text from the STT step)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": stt},
        ],
    )

    ai_response = response.choices[0].message.content
    print(ai_response)
```

Nothing new mechanically - `OpenAI()` client, `load_dotenv()`,
`.chat.completions.create(...)`, `.choices[0].message.content`. The STT
output just becomes the `user` message content.

---

## 🟡 Intermediate — still just text-to-text, still flexible

This is the payoff from the chained architecture lecture, in practice:
the model here can be swapped for Gemini, Claude, anything - "it's just
a text-to-text model." Nothing about the voice pipeline constrains the
model choice at this step.

**Practical setup tip:** reuse an existing `.env` from another project
folder (`cp` it over) instead of re-typing API keys for every new
project that needs the same ones.

---

## 🔴 Expert — why the system prompt matters here specifically

**The important part:** the system prompt explicitly tells the model
*"you are a voice agent, not a text agent"* - and that it's given the
transcript of what the user said, since its own reply will be converted
to audio and played back.

This matters because text written to be **read** and text written to be
**spoken** aren't the same. A model that doesn't know its output becomes
audio might reply with bullet points, markdown, or long visually-structured
text - fine on a screen, awkward or nonsensical when read aloud by TTS.
Telling the model the *context* its text will be used in changes the
style of what it generates, not just the content.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **This step** | an ordinary text-to-text chat completion - STT output becomes the user message |
| **Voice-aware system prompt** | tells the model its reply will be spoken, not read - shapes style, not just content |
| **Model flexibility** | any text-to-text model works here - no lock-in from the voice pipeline |
