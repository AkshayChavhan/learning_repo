# 05 — Memory

**Models are stateless.** They remember nothing between calls. "Memory" is only
text you resend with the next request — and every strategy here is a different
answer to *how much* of it to resend.

---

## The files

Read them in order — each bounds the history a little more cleverly.

| # | File | Strategy | Cost of the strategy |
|---|---|---|---|
| 1 | `01_chat_history.py` | store messages, replay all | none — this is the raw substrate |
| 2 | `02_conversation_buffer_memory.py` | replay **everything** | tokens grow forever |
| 3 | `03_conversation_buffer_window.py` | replay last **k exchanges** | older turns are invisible |
| 4 | `04_conversation_token_buffer.py` | replay under a **token budget** | older turns are invisible |
| 5 | `05_conversation_summary_memory.py` | replay an **LLM summary** | an extra call, and lossy |

Files 2–5 all come from `langchain_classic.memory`, not `langchain`.

---

## The core idea

```text
   turn 1        turn 2        turn 3
     │             │             │
     ▼             ▼             ▼
 ┌───────┐     ┌───────┐     ┌───────┐
 │ model │     │ model │     │ model │      the model is the SAME every time
 └───────┘     └───────┘     └───────┘      and remembers NOTHING
     ▲             ▲             ▲
     │             │             │
   prompt      prompt +      prompt +
              history 1     history 1,2     ← memory just grows this
```

Memory is not a feature of the model. It is text you prepend.

---

## Choosing between them

```text
              everything            a token budget
                   \                    /
     perfect ───────\                  /────── honest about cost
     recall          \                /
                      ►   HISTORY    ◄
     unbounded ──────/                \────── needs an extra LLM call
     tokens         /                  \
                   /                    \
              last k turns          an LLM summary
```

| Memory | Keeps | Bounded? | Extra LLM call |
|---|---|---|---|
| Buffer | every message | ❌ no | no |
| Window | last `k` exchanges | ✅ by count | no |
| Token buffer | as much as fits | ✅ by tokens | no (counts only) |
| Summary | a rewritten gist of **all** of it | ✅ | **yes, per save** |

**Only summary keeps information from the whole conversation.** The window and
token buffer simply discard old turns — ask on turn 20 about turn 1 and it is
gone. Summary compresses instead of dropping, which is why it costs a call.

---

## `k` bounds what the model SEES, not what is stored

The most common misreading. With `k=2` and 9 exchanges saved:

```text
  buffer  returned: 18 messages
  window  returned:  4 messages   (k=2 → 2 pairs)
  window  STORED  : 18 messages   ← nothing was deleted
```

`save_context()` appends every message. The window is a **slice taken on the
way out** — `chat_memory.messages[-k*2:]`. So `k` bounds your token bill, not
your storage. All 18 are still reachable via `memory.chat_memory.messages`.

---

## `load_memory_variables({})`

Every file calls it with an empty dict:

```python
history = memory.load_memory_variables({})
```

The argument is **the chain's current inputs**, and it is required by the
interface. Buffer, window and token buffer ignore it entirely. It exists for
memories that need the current question to decide what to pull back — the
retrieval-backed ones.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **These live in `langchain_classic`** | `from langchain_classic.memory import …` — not `langchain.memory` |
| **`k` does not delete anything** | It slices on read. Storage keeps growing |
| **`max_token_limit` is easy to misspell** | Pydantic drops unknown kwargs **silently**, so `maxTokens=100` gives you the 2000 default with no error |
| **Token buffer's `llm=` is a counter** | It is used to count tokens, not to generate. No request is sent |
| **Summary returns one `SystemMessage`** | Not the original turns — the transcript is gone, replaced by a gist |
| **`return_messages=True` matters** | Without it you get a formatted string instead of Message objects |
