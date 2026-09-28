# 12 — LangGraph Basics

Notes-first fundamentals for LangGraph — the ideas explained slowly, before you
meet them as running code. LangGraph runs your program as a **graph**: state
flows through a series of **nodes** connected by **edges**, instead of
top-to-bottom statements.

---

## What's here

This is the concepts-first companion to the working examples elsewhere in
this repo. Read it before `08` and `09` if those feel like they start moving
too fast.

| Path | Has |
|---|---|
| `README.md` | this page — concepts, then setup |
| `implementation/chat.py` | empty for now — code lands here as later topics add it |
| [`../08_lang_graph/`](../08_lang_graph/) | two runnable graphs — a straight line, then a branch |
| [`../09_langgraph_checkpoints/`](../09_langgraph_checkpoints/) | a graph that remembers state between runs |

---

## Topic 1 — Introduction to LangGraph

### Quick definitions

| Term | Meaning |
|---|---|
| **Graph** | The whole flow — nodes plus edges — built with `StateGraph(State)` |
| **State** | One shared dictionary every node reads from and writes to |
| **Node** | A plain Python function: state in, a dict of *changes* out |
| **Edge** | A connection between two nodes — defines what runs next |
| **START / END** | Built-in markers for where the graph begins and finishes |
| **`.compile()`** | Checks the graph is valid (every node reachable, no dangling edges) and returns something runnable |
| **`.invoke(state)`** | Runs the whole graph once, start to finish, and returns the final state |

### What is a Node?

A **node** is just a function. It receives the current state and returns a
dict containing only the pieces it wants to change — not the whole state.

```python
def classify_ticket(state: State) -> dict:
    category = "billing" if "invoice" in state["ticket"].lower() else "general"
    return {"category": category}          # only the NEW/CHANGED part
```

You register it on the graph with a name, and that name is what edges use to
refer to it:

```python
graph_builder.add_node("classify_ticket", classify_ticket)
```

LangGraph takes whatever a node returns and **merges** it into the existing
state for you — a node never has to know or repeat the rest of the state.

### What is an Edge?

An **edge** is the arrow between two nodes. It says "once this node finishes,
run that one next."

```python
graph_builder.add_edge("classify_ticket", "draft_reply")
```

Most edges are fixed like that. LangGraph also has a **conditional edge**,
where a router function looks at the state and decides the next node by name
instead of it being fixed in advance — that's how branching happens. It's
covered hands-on in [`08_lang_graph/`](../08_lang_graph/); this page sticks to
plain edges.

### What is State?

**State** is the one shared place every node reads from and writes to — usually
defined as a `TypedDict`:

```python
class State(TypedDict):
    ticket: str
    category: str
    reply: str
```

The part that trips people up: a node's return value doesn't *become* the new
state, it gets **merged** into it.

- A key that doesn't exist yet in the state → **added**.
- A key that already exists → **replaced** with the new value, by default.

(A field can opt into a different merge rule — accumulate instead of replace —
but that's a step past "basic," and shown in `08_lang_graph/`.)

---

## A small AI flow

A 3-node support-ticket assistant: classify the ticket, draft a reply, then
sign it off.

```text
START
  │
  │   you provide the initial state:
  │   {"ticket": "My invoice amount looks wrong this month."}
  ▼
┌───────────────────┐
│  classify_ticket   │   reads:  ticket
│                    │   writes: category
└───────────────────┘
  │
  │   state now: {ticket, category}
  ▼
┌───────────────────┐
│   draft_reply      │   reads:  ticket, category
│                    │   writes: reply
└───────────────────┘
  │
  │   state now: {ticket, category, reply}
  ▼
┌───────────────────┐
│   add_signoff      │   reads:  reply
│                    │   writes: reply   (replaces it)
└───────────────────┘
  │
  │   state now: {ticket, category, reply}   ← reply has changed again
  ▼
 END
```

### How the state changes, step by step

| After | Node that ran | It returned | State afterwards |
|---|---|---|---|
| start | — (you called `.invoke()`) | — | `{"ticket": "My invoice amount looks wrong this month."}` |
| 1 | `classify_ticket` | `{"category": "billing"}` | `{"ticket": "...", "category": "billing"}` |
| 2 | `draft_reply` | `{"reply": "Thanks for flagging this — we'll review your invoice within 24 hours."}` | adds `reply` — now 3 keys |
| 3 | `add_signoff` | `{"reply": "Thanks for flagging this — we'll review your invoice within 24 hours.\n\n– Support Bot"}` | `reply` is **replaced**, not appended — still 3 keys |

Two things worth noticing:

- **`ticket` never changes.** No node returns it, so it just rides along
  unchanged for the whole graph — that's what "shared state" means.
- **`reply` is overwritten at step 3, not extended.** By default, returning a
  key that already exists replaces its value. If you wanted step 3 to *append*
  a signature onto a running list instead of replacing a string, that needs the
  reducer LangGraph supports for exactly that case — see `08_lang_graph/` for
  it in action.

---

### Gotchas

| Gotcha | Detail |
|---|---|
| **A node returns changes, not the whole state** | Return only the keys you're updating — LangGraph merges them in for you |
| **A returned key must exist in your `State` type** | Otherwise it's silently dropped — no warning, no error. The most common LangGraph bug |
| **Returning an existing key replaces it, by default** | Accumulating instead (like chat history) needs an explicit reducer |
| **A router does no state-changing work** | Anything it writes to state is thrown away — its only job is to name the next node |
| **Nothing runs until `.compile()`** | That's also when the graph gets validated |
| **Router return values must match a node name exactly** | A typo there fails at run time, not at compile time |

---

## Topic 2 — Installation and Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv && source .venv/bin/activate     # or: uv venv --python 3.12
```

Everything below runs *inside* this environment. If a command later fails with
"module not found," the first thing to check is whether the venv is active —
your prompt should show `(.venv)`.

### 2. Install the packages

At minimum you need LangGraph itself, a chat model client, and a way to load
`.env` files. `implementation/chat.py` connects to **Gemini**, so that's the
provider package below:

```bash
pip install langgraph langchain langchain-google-genai python-dotenv
```

| Package | Verified version | What it's for |
|---|---|---|
| `langgraph` | `1.2.11` | the graph engine — `StateGraph`, `START`, `END` |
| `langchain` | `1.3.16` | `init_chat_model` and the rest of the chat-model layer |
| `langchain-google-genai` | `4.4.0` | the Gemini client `init_chat_model` builds when you pass `model_provider="google_genai"` |
| `python-dotenv` | `1.2.3` | reads `.env` into environment variables via `load_dotenv()` |

`08_lang_graph/` and `09_langgraph_checkpoints/` use `langchain-openai`
instead — same idea, different provider package. `init_chat_model` is what
lets the rest of your code stay identical either way.

Once your code runs, pin exactly what you installed so setup is repeatable:

```bash
pip freeze > requirements.txt        # run this INSIDE the venv, not outside it
pip install -r requirements.txt      # rebuild the same environment later
```

### 3. Add your API key

Create a `.env` file next to your code (e.g. in `implementation/`) — never
commit it, the repo's `.gitignore` already excludes `.env`:

```text
GOOGLE_API_KEY=AI...
```

Then read it at the top of your script, before building anything that needs
the key:

```python
from dotenv import load_dotenv

load_dotenv()          # pulls .env into environment variables
```

`init_chat_model(model_provider="google_genai", ...)` looks for
`GOOGLE_API_KEY` by that exact name — nothing to pass in by hand. (For OpenAI
instead, it's `OPENAI_API_KEY` — the key name follows the provider.)

### 4. Verify the install

```bash
pip show langgraph
```

If that prints a `Version:` line, the environment is ready. No output, or a
"package not found" — the venv isn't active, or step 2 didn't run inside it.

### Gotchas

| Gotcha | Detail |
|---|---|
| **`python-dotenv`, not `dotenv`** | `pip install dotenv` installs a deprecated, unrelated stub. Both are imported the same way — `from dotenv import load_dotenv` — so installing the wrong one fails silently until `load_dotenv()` doesn't actually load anything |
| **`pip freeze` outside the venv captures everything** | every package on the machine, system libraries included — always run it with the venv active |
| **The `.env` key name must match exactly** | `GOOGLE_API_KEY` for Gemini, `OPENAI_API_KEY` for OpenAI — a typo or the wrong provider's name and the client raises "no API key found," not "wrong key name" |
| **`load_dotenv()` must run before you build the model** | calling `init_chat_model(...)` first, then `load_dotenv()` after, means the key was never in the environment when it was needed |
| **`.env` is gitignored on purpose** | if `pip show` or your script works locally but a teammate's setup can't find the key, they need their own `.env` — it never gets committed |

---

## Next

- [`08_lang_graph/`](../08_lang_graph/) — these same ideas as real, running code: a straight-line graph, then one with a conditional edge
- [`09_langgraph_checkpoints/`](../09_langgraph_checkpoints/) — add a checkpointer so state survives between runs instead of starting empty each time
