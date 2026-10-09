# Conversational AI & Voice Agents — What They Are

Until now every agent we built was **text in → LLM → text out**. A **voice agent** keeps the
same brain (the LLM) but changes the interface: the user **speaks**, the agent **speaks back**.
It feels like talking to a person, and your hands stay free.

---

## Topic at a glance

```text
        What we had                       Why voice
            \                                /
  text tokens in ──\          typing is slow ──/
                    \                        /
  GPT-4.1 / Gemini ──\      hands busy ─────/
                      ►   VOICE / CONVERSATIONAL AGENT
  audio in, audio out /     endless use cases ──\
                    /                            \
  same LLM brain ──/         assistants, support ──\
            /                                        \
        What changes                           What we'll build
```

---

## 🟢 Beginner — text agent vs voice agent

| | Text agent (so far) | Voice agent (this section) |
|---|---|---|
| **Input** | text tokens you type | your **voice** (audio) |
| **Brain** | LLM (GPT-4.1, Gemini) | same LLM |
| **Output** | text | spoken **audio** reply |
| **Tool calling / agents** | ✅ already built | ✅ still works, same idea |
| **Feels like** | chatting in a box | **talking** to someone |

```text
 TEXT AGENT                          VOICE AGENT

  "book a cab"  ──► [ LLM ] ──► "Done, cab at 5"     🎤 "book a cab" ──► [ LLM ] ──► 🔊 "Done, cab at 5"
   (typed)                        (text)              (spoken)                       (spoken)
```

> **Key idea:** the intelligence is unchanged. Only the **way you talk to it** changes:
> audio goes in, audio comes out.

---

## 🟡 Intermediate — why bother with voice?

People want the **easiest** way to get something done. Typing, even into ChatGPT, is friction.

| Situation | Typing | Voice |
|---|---|---|
| Driving | ❌ hands on wheel, eyes on road | ✅ just say it |
| Cooking / hands dirty | ❌ | ✅ |
| Long instruction | slow to type | fast to say |
| Accessibility (vision, motor) | hard | natural |
| Reply | you must **read** it | you **hear** it, keep working |

The result is a **hands-free, hassle-free** loop: command by voice → agent acts (tools,
APIs, memory) → agent answers by voice.

### Where this shows up

| Use case | What the voice agent does |
|---|---|
| Personal assistant | "remind me…", "what's on my calendar", "send a message" |
| Customer support / IVR | answers calls, looks up orders, books appointments |
| In-car / smart home | control devices without a screen |
| Sales / outbound calls | talks a script, logs the outcome |
| Tutoring, language practice | spoken conversation with feedback |

The ideas are endless: anything you can do with a text agent, you can now do by **talking**.

---

## 🔴 Expert — what actually sits under "audio in, audio out" (preview)

A voice agent is still a pipeline. Two ways to build it:

```text
 CHAINED PATTERN (3 models, we build this)

  🎤 audio ──► STT ──► text ──► [ LLM + tools + memory ] ──► text ──► TTS ──► 🔊 audio
             speech-to-text                                        text-to-speech

 SPEECH-TO-SPEECH (1 realtime model)

  🎤 audio ──────────────► [ realtime LLM ] ──────────────► 🔊 audio
```

| | Chained (STT → LLM → TTS) | Speech-to-speech |
|---|---|---|
| Parts | 3 separate models | 1 model handles audio directly |
| Reuse existing agent? | ✅ drop your text agent in the middle | needs an audio-native model |
| Control / debugging | ✅ you see the text at every step | harder, audio in / audio out |
| Latency | higher (3 hops) | lower |
| Tone, emotion, interruptions | lost at the STT step | preserved |
| Good first build | ✅ **yes** | later |

The chained pattern in plain Python shape (real STT/TTS come later in the section):

```python
def stt(audio: bytes) -> str:            # speech  -> text
    return "book a cab for 5 pm"

def agent(text: str) -> str:             # our existing text agent (LLM + tools)
    return "Done, your cab is booked for 5 pm."

def tts(text: str) -> bytes:             # text -> speech
    return f"<audio of: {text}>".encode()

reply_audio = tts(agent(stt(b"<mic input>")))
print(reply_audio.decode())
```

```text
<audio of: Done, your cab is booked for 5 pm.>
```

Everything we already know (tool calling, memory, graph memory) plugs into the **middle box**.

---

## Gotchas & things to keep in mind

- **Voice ≠ new brain.** Don't rebuild the agent. Wrap the one you have with STT and TTS.
- **Latency is the UX.** A 3-second pause feels broken in speech, fine in a chat box.
- **Turn-taking matters.** The agent must know when you've *stopped* talking and allow
  interruptions, or the conversation feels robotic.
- **STT errors propagate.** If "book a cab" is heard as "book a cap", every later step is wrong.
- **Spoken replies must be short.** A 300-word answer is fine to read, painful to listen to.

> **Interview angle:** *"What's the difference between a chatbot and a voice agent?"*
> Same LLM core; the voice agent adds **speech-to-text** on the way in and **text-to-speech**
> on the way out (chained pattern), or uses a **speech-to-speech** realtime model. The new
> problems are **latency**, **turn-taking / interruptions**, and **transcription errors**,
> not reasoning.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Conversational / voice agent** | an LLM agent you **talk** to and that **talks back** |
| **STT** | speech-to-text: audio → text |
| **TTS** | text-to-speech: text → audio |
| **Chained pattern** | STT → LLM (agent) → TTS, three models in a row |
| **Speech-to-speech** | one realtime model takes audio in and produces audio out |
| **Why voice** | hands-free, faster than typing, natural while driving / working |
