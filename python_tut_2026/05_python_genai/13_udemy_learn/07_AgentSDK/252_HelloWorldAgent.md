# Hello World Agent — Agent + Runner

The OpenAI Agents SDK has four building blocks: **agents**, **handoffs**, **guardrails**
and **sessions**. A hello-world needs two classes: `Agent` (name + instructions) and
`Runner` (runs it). The while-loop, message history and tool-call handling you wrote by
hand in the weather agent are now inside `Runner.run_sync`.

---

## 1. What an agent is (again)

```text
   LLM  +  instructions  +  tools  (+ guardrails, history)  =  agent
```

You already built this by hand. Here's what that looked like vs now:

| By hand (weather agent) | With the SDK |
|---|---|
| system prompt string | `instructions=` |
| `while True:` loop | `Runner.run_sync()` |
| `messages = []` history you append to | handled inside the runner |
| parse JSON, `if step == "action": call tool` | `tools=[...]`, called automatically |
| `if step == "output": break` | `result.final_output` |

> **Key idea:** the SDK doesn't change what an agent is. It hides the plumbing.

---

## 2. Install

```bash
pip install openai-agents
pip freeze > requirements.txt
```

Several packages come with it. The one you import from is `agents`.

---

## 3. The code

`agent_sdk/hello.py`, with a `.env` next to it holding `OPENAI_API_KEY`:

```python
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

# 1. define the agent: a name + instructions (+ tools later)
hello_agent = Agent(
    name="Hello World Agent",
    instructions="You greet the user and answer using emojis, in a funny way.",
)

# 2. run it with an input
result = Runner.run_sync(hello_agent, "Hello, my name is Piyush")

# 3. read the final answer
print(result.final_output)
```

```bash
python agent_sdk/hello.py
```

```text
Hey Piyush! 🎉 Welcome to the fun zone 😄 Flash your best smile, you're about to have a blast! 🚀
```

| Line | Meaning |
|---|---|
| `Agent(name=..., instructions=...)` | create an agent. `name` is a label; `instructions` is the system prompt |
| `Runner.run_sync(agent, input)` | run the whole loop: LLM call → tool calls if any → repeat → stop at final answer |
| `result.final_output` | the text the agent ended with |

Three real lines. Everything else is import and setup.

---

## 4. What `run_sync` does for you

```text
   your old loop                         Runner.run_sync
   ┌──────────────────────────┐          ┌──────────────────────────┐
   │ while True:              │          │ (same loop, inside SDK)  │
   │   call LLM               │          │                          │
   │   if tool call: run it,  │   ──►    │  you see only:           │
   │     append result, loop  │          │  result.final_output     │
   │   if output: break       │          │                          │
   └──────────────────────────┘          └──────────────────────────┘
```

5 iterations or 10, 0 tool calls or 10, you don't care. You get the result.

---

## 5. What's coming

Same `Agent(...)` call, more arguments:

| Argument / feature | Lecture |
|---|---|
| `tools=[...]` | next: attach functions the agent can call |
| streaming | token-by-token output |
| MCP | plug in MCP servers as tools |
| handoffs | one agent passes the conversation to another |
| guardrails | check inputs and outputs |
| sessions | keep history across runs |

---

## Remember

| Term | One line |
|---|---|
| **`pip install openai-agents`** | the SDK; import from `agents` |
| **`Agent`** | name + instructions (+ tools, handoffs, guardrails) |
| **`Runner.run_sync(agent, input)`** | run the agent loop to completion |
| **`result.final_output`** | the answer |
| **abstraction** | the while-loop, history and tool dispatch live inside the runner |
| **4 primitives** | agents, handoffs, guardrails, sessions |

> **If someone asks in an interview:** "What does the OpenAI Agents SDK give you over a
> hand-written agent loop?" A small set of primitives (Agent, Runner, tools, handoffs,
> guardrails, sessions) that handle the LLM call loop, tool dispatch and history, so an
> agent is a declaration (name, instructions, tools) rather than orchestration code.
