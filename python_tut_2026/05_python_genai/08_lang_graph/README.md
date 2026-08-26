# 08 — LangGraph

Two graphs, building up from a straight line to a branch. LangGraph runs your
code as a **graph of nodes** instead of top-to-bottom statements: each node is a
plain function that takes the state and returns the parts it wants to change.
LangGraph merges those changes and follows the edges.

---

## The two files

### `chat.py` — a fixed line

```text
START ──► chatbot ──► sampleNode ──► END
```

Nodes, edges, `.compile()`. Nothing runs until you compile — that step validates
that every node is reachable and no edge dangles.

### `chat2.py` — a branch

```text
START ──► chatbot ──► evaluate ──► evaluate_response (router)
                                          │
                        is_good True  ────┼──► endnode ──────────────────► END
                        is_good False ────┴──► chatbot_gemini ──► endnode ─► END
```

The **conditional edge** is the reason to reach for LangGraph at all: a router
function inspects the state and names the next node. A plain `while` loop can
do a lot, but not this cleanly once the branching grows.

---

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate     # or: uv venv --python 3.12
pip install -r requirements.txt
```

### Environment

| Variable | Where |
|---|---|
| `OPENAI_API_KEY` | `.env` in this folder |

```bash
# from the repo root
export OPENAI_API_KEY='sk-proj-...'
./scripts/setup_env.sh
```

Both files call `load_dotenv()`, so the `.env` is read automatically.

---

## Run

```bash
python chat.py            # after activating
python chat2.py
./.venv/bin/python chat.py     # without activating
```

Every node prints its name and the state as it passes through, so you can watch
the graph execute.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`python-dotenv`, not `dotenv`** | `pip install dotenv` is a deprecated stub. Both import as `from dotenv import load_dotenv`, so the wrong one fails invisibly |
| **`chatbot_gemini` does not use Gemini** | Despite the name it calls `gpt-4.1-mini` through the same OpenAI client. No Google key needed |
| **Its docstring is stale** | `chatbot_gemini` says it is "currently unreachable". It is not — `evaluate` returns `is_good=False` for an empty answer and whenever the judge does not reply `GOOD`, and the router branches on exactly that. The fallback does run |
| **`evaluate` must be a node, not the router** | LangGraph keeps only what a *node* returns. State written inside a router is discarded, so `is_good` would silently stay `None` |
| **Router strings are load-bearing** | The literal a router returns must match an `add_node()` name exactly, or the graph fails at run time |
| **`pip freeze` inside the venv** | Outside it you capture every system package and the requirements file stops working elsewhere |

## Next

Project [09](../09_langgraph_checkpoints/) adds a **checkpointer**, so the graph
remembers the conversation between runs instead of starting empty each time.
