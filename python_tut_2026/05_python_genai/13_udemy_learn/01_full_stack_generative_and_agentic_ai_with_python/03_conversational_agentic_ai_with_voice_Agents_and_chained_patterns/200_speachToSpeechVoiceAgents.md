# Speech-to-Speech (S2S) Voice Agents

The OpenAI voice-agent docs start with **"choose the right architecture"** and list two:
**speech-to-speech** and **chained**. S2S is the simpler one to describe: **voice in,
voice out, nothing else**. The model handles audio **natively**.

---

## Topic at a glance

```text
        What it is                          Pros
            \                                /
  native audio ──\           low latency ──/
                  \                        /
  voice in/out ───\       real time ─────/
                    ►   S2S VOICE AGENT
  tools, search ──/        very expensive ──\
                  /                          \
  handoff ───────/      scoped to ONE job ────\
            /                                  \
     Still an agent                          Cons
```

---

## 🟢 Beginner — "native audio handling"

```text
  🎤 user audio ──► [ S2S model ] ──► 🔊 agent audio
                     (one API call)
```

| Word in the docs | What it means for you |
|---|---|
| **Speech-to-speech** | input is speech, output is speech |
| **Native audio handling** | you send the **raw voice** to the model. No text step on your side |
| **Real time** | the reply starts coming back while the user is still being processed |

> **Key idea:** you never see text. Voice goes to the API, voice comes back.

---

## 🟡 Intermediate — it is still an agent

S2S is not just a talking box. Inside the agent you can bind the same things as before:

```text
                  ┌────────────────────────────┐
  🎤 audio ──────►│  S2S model                  │──────► 🔊 audio
                  │   • tool calling            │
                  │   • search                  │
                  │   • handoff to another agent│
                  └────────────────────────────┘
```

| Capability | S2S agent |
|---|---|
| Tool calling | ✅ |
| Search | ✅ |
| Handoff | ✅ |
| Memory / graph memory (earlier sections) | ✅ plugs in as a tool |
| Structured, multi-step conversation flow | ❌ (see cons) |

### Pros vs cons (straight from the lecture)

| ✅ Pros | ❌ Cons |
|---|---|
| **Low latency**: one hop, no STT / TTS in between | **Very expensive**: audio in + audio out via API |
| **Real time**: feels like a live call | **Scoped to one thing**: one agent = one specific job |
| **Natural** conversation, no robotic pauses | **No structured conversation**: it flows freely, you can't script steps |
| Simple wiring: audio → API → audio | Hard to debug: no text to inspect in the middle |

### What "scoped to one thing" means

| You can build | You can't easily build |
|---|---|
| a customer-support agent | one agent that does support **and** sales **and** booking in a scripted flow |
| a sales-call agent | a step-by-step form-filling conversation (ask A, then B, then C) |

One S2S agent = **one specific persona for one specific task**. Need more? Use **handoff**
to another agent rather than stuffing it all into one.

---

## 🔴 Expert — why it costs more, and what's really inside

### Where the cost comes from

```text
  TEXT agent:   cheap tokens in ──► cheap tokens out
  S2S agent:    AUDIO tokens in ──► AUDIO tokens out      ← audio tokens are far pricier,
                                                            and a call runs for minutes
```

Audio is streamed **both ways for the whole call**, and audio tokens are billed at a much
higher rate than text. A 10-minute support call is a lot of audio.

### S2S is a chain under the hood

The lecture's closing point: internally S2S **works like a chained model**. The provider
hides the pieces from you, but the audio still gets turned into something token-like,
reasoned over, and turned back into audio. That is why the course teaches **chained first**:
understand the chain and S2S stops being magic.

```text
  what you see:    🎤 ──► [   S2S   ] ──► 🔊
  what happens:    🎤 ──► [ audio→tokens → LLM → tokens→audio ] ──► 🔊
                            (hidden inside the provider)
```

### When to pick S2S

| Pick S2S when | Pick chained when |
|---|---|
| latency is the product (live calls) | you need control, logging, step-by-step flows |
| one narrow job, natural chat | many jobs, structured conversation |
| budget allows audio pricing | cost matters |
| you don't need the transcript | you need the text at every step |

---

## Gotchas & best practices

- **Don't put everything in one S2S agent.** It's good at one job. Split jobs and use handoff.
- **Budget before you build.** Audio tokens both ways, for minutes at a time, add up fast.
- **No text in the middle** means no cheap logging or guardrails on what was said. Plan for it.
- **S2S ≠ magic.** It's a chain the provider runs for you. Learn chained first (next lecture).

> **Interview angle:** *"Why would you choose S2S over a chained voice pipeline?"*
> **Latency and naturalness**: one real-time hop instead of STT → LLM → TTS. You pay for it
> with **cost**, **less control** (no text to inspect), and **narrow scope** (one agent, one
> job, no structured flow).

---

## Quick recap

| Term | One-line definition |
|---|---|
| **S2S (speech-to-speech)** | voice agent that takes audio in and returns audio out in one call |
| **Native audio handling** | the model accepts raw speech, no STT/TTS on your side |
| **Pros** | low latency, real time, natural conversation, tools/search/handoff still work |
| **Cons** | very expensive, scoped to one job, no structured conversations |
| **Under the hood** | still a chained pipeline, hidden by the provider |
| **Next** | chained architecture, the foundation S2S is built on |
