# Chained Architecture — STT → LLM → TTS

Chained architecture builds a voice agent out of three ordinary steps
wired in sequence: transcribe the audio, run a normal text-to-text LLM
call, then speak the reply back.

---

## 🟢 Beginner — the three steps

```text
  User's voice ──► STT ──► text ──► LLM (text-to-text) ──► text ──► TTS ──► audio out
                   │                                                  │
            Speech-to-Text                                      Text-to-Speech
```

| Step | Name | What it does |
|---|---|---|
| 1 | **STT** (Speech-to-Text) | transcribes spoken audio into text - like live subtitles |
| 2 | **LLM** | ordinary text-to-text call - same as every other model used so far |
| 3 | **TTS** (Text-to-Speech) | converts the LLM's text reply back into playable audio |

"Chained" because it's literally a sequence of transformations - voice to
text to text to voice.

---

## 🟡 Intermediate — why this is the flexible choice

Because step 2 is a plain text-to-text LLM call, everything already
covered in this course plugs straight in:

| You get, because the middle is plain text | Why it matters |
|---|---|
| **Any LLM** - Gemini, Claude, GPT, anything | not locked to a provider that natively supports speech |
| **Tool calling** | the LLM step can call tools exactly like before |
| **LangGraph / LangChain orchestration** | the whole rest of this course applies unchanged |

The middle step doesn't know or care that it's part of a voice pipeline -
that's the whole payoff of this architecture.

---

## 🔴 Expert — chained vs S2S, the real trade-off

| | Chained | S2S (Speech-to-Speech) |
|---|---|---|
| Model choice | any LLM | locked to a model that natively supports S2S - currently essentially only OpenAI's realtime model |
| Intelligence | high - use the biggest/best model available | lower - tuned for natural conversation, not peak reasoning |
| Cost | - | expensive |
| Latency | **higher** - three sequential steps each add delay | **lower** - fewer steps, more direct |
| Provider support | universal | currently OpenAI-only |

**Instructor's stated opinion, not confirmed fact:** S2S models likely do
the same voice-to-text-to-text-to-voice conversion internally anyway -
just hidden from the caller, optimized for low latency at the cost of
flexibility and raw intelligence.

**Course direction:** chained gets coded first - more widely used, more
flexible. S2S comes later via a documentation walkthrough - despite the
architectural limits, it's easy to code.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **STT** | Speech-to-Text - transcribes voice input |
| **TTS** | Text-to-Speech - converts the reply back to audio |
| **Chained architecture** | STT -> text LLM -> TTS, any model, full tool/orchestration support |
| **S2S** | a model that handles speech directly - less flexible, lower intelligence, lower latency |
