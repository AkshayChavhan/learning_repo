# Hosted Tools — Web Search Out of the Box

The SDK has **three kinds of tools**. This lecture uses the first: **hosted tools**, built
and run by OpenAI, like web search. You don't write any tool code. You import the tool,
put it in `tools=[...]`, and the runner calls it when the agent needs it.

---

## 1. Three kinds of tools

| Kind | Who writes it | Example | Lecture |
|---|---|---|---|
| **Hosted tool** | OpenAI | `WebSearchTool`, code interpreter, computer use | this one |
| **Function tool** | you, a plain Python function | `get_weather(city)` | next |
| **Agent as tool** | you, another agent | a physics agent calls a maths agent to calculate | later |

Same idea as always: a tool lets the agent **act** (fetch data, run code, call an API).

---

## 2. The code

Copy `hello.py`, add two things:

```python
from dotenv import load_dotenv
from agents import Agent, Runner
from agents import WebSearchTool            # ① import the hosted tool

load_dotenv()

agent = Agent(
    name="Hello World Agent",
    instructions="You greet the user and answer using emojis, in a funny way.",
    tools=[WebSearchTool()],                 # ② give it to the agent
)

result = Runner.run_sync(agent, "What is on piyushgarg.dev website?")
print(result.final_output)
```

```bash
python agent_sdk/agent_with_tool.py
```

```text
Hey there tech adventurer! 🚀 Peeking into piyushgarg.dev...
It's Piyush Garg's site: intro, courses, video content, links... 😄
```

| Line | Meaning |
|---|---|
| `from agents import WebSearchTool` | hosted tools are classes in the SDK |
| `tools=[WebSearchTool()]` | a **list**; add more tools with commas |
| nothing else | the runner decides when to search, searches, feeds the result back, loops |

---

## 3. What happened inside the loop

```text
   input: "What is on piyushgarg.dev?"
      │
      ▼
   LLM: "I need to look this up" ──► WebSearchTool runs (on OpenAI's side)
      │                                       │
      ◄──────────── search results ───────────┘
      ▼
   LLM: writes the final answer ──► result.final_output
```

Second test: *"Fetch the weather for Patiala, pin code …"* → the agent searched and
returned current weather, even history. All automatic.

---

## 4. Same question, tool removed

```python
    # tools=[WebSearchTool()],     # commented out
```

```text
Hey there! 🌦️ My weather wand only works for places I can see...
Open Google, type "Patiala weather" and you'll have it! 😅
```

No tool, no action. The LLM can only talk about what it already knows and tells **you**
to search. That's the whole difference a tool makes.

---

## 5. Hosted tools available (Nov 2025)

| Tool | What it does |
|---|---|
| `WebSearchTool` | search the internet |
| `FileSearchTool` | search files you've uploaded to OpenAI (vector store) |
| `CodeInterpreterTool` | run code in a sandbox |
| `ComputerTool` | control a computer / browser |
| `ImageGenerationTool` | generate images |
| `LocalShellTool` | run shell commands on **your** machine |

The list grows. Check the docs' *Tools → Hosted tools* page for the current set and each
tool's parameters. No need to implement them all, just know they exist.

---

## Remember

| Term | One line |
|---|---|
| **hosted tool** | a tool OpenAI builds and runs; you only import it |
| **`from agents import WebSearchTool`** | import |
| **`tools=[WebSearchTool()]`** | attach; a list, so several tools are fine |
| **automatic** | the runner calls the tool inside the loop when the LLM asks for it |
| **no tool = no action** | the model falls back to "go search it yourself" |
| **3 kinds** | hosted, function (next), agent-as-tool (later) |

> **If someone asks in an interview:** "What tool types does the OpenAI Agents SDK
> support?" Hosted tools run by OpenAI (web search, file search, code interpreter,
> computer use), function tools which are your own Python functions, and agents used as
> tools by other agents. All are passed in the agent's `tools` list and invoked by the
> runner automatically.
