# Turning an Existing Agent Into a Voice Agent

The payoff: a voice interface isn't a new agent - it's the *same* agent
from earlier in the course, with voice swapped in for its input and
output. The tool-calling, message history, and logic underneath don't change.

---

## 🟢 Beginner — only input and output swap

```text
   BEFORE (text agent)                AFTER (voice agent)

   user_query = input(...)            user_query = r.recognize_google(audio)
          │                                    │
          ▼                                    ▼
     agent loop                          agent loop
     (tool calls, message                (UNCHANGED)
      history, LLM call)                       │
          │                                    ▼
          ▼                            asyncio.run(tts(ai_response))
   print(ai_response)                  instead of print()
```

The existing weather/cursor agent (from the earlier tool-calling section)
already had everything it needed - tools, message history, the LLM loop.
Voice just changes how the human talks to it.

---

## 🟡 Intermediate — what's reused vs what's swapped

| Reused as-is | Swapped |
|---|---|
| tool-calling loop | input source: typed text → STT (`r.recognize(audio)`) |
| message/conversation history | output: printed text → spoken via the TTS function |
| any existing tools (e.g. file-writing) | nothing else - the tools themselves don't change |

Proof this actually works: spoken requests like *"create a black themed
todo application"* → the agent asks a clarifying follow-up **out loud**
(language/framework?) → spoken answer *"HTML, CSS, JavaScript"* → the
agent calls its existing file-writing tools and produces real
`index.html`, `style.css`, `script.js` on disk - the same tool-calling
capability the agent already had, just driven by voice instead of text.

---

## 🔴 Expert — two real gotchas worth internalizing

**1. Copy before you edit, don't modify the original in place.**
While adapting the agent, the wrong file got edited directly - the
original working agent was at risk of being changed. The fix: take a
backup, copy the agent's code into a **new** file (`cursor.py` in the
voice agent folder), and restore the original untouched. The generalizable
rule: when adapting someone else's (or your own earlier) script for a new
use case, copy it to a new file *first* - never edit the original in place.

**2. Don't trust a tool call's success message at face value.**
The agent reported `index.html` was created, but the file was initially
missing - it self-corrected on the next turn. Agentic tool-calling can
report success even when the actual filesystem result lags or fails -
verify the real outcome, don't just trust the agent's own claim.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Voice-wrapping an agent** | swap text input/output for STT/TTS - the agent's logic and tools stay unchanged |
| **Copy-before-edit** | adapt a working script in a new file, never modify the original in place |
| **Trust but verify** | a tool call reporting success doesn't guarantee the filesystem actually reflects it |
