# Hosted Tools — web search out of the box

A **hosted tool** is a tool the provider builds *and runs*. You write no tool code: import it,
put it in `tools=[...]`, and the runner calls it when the agent decides it needs it. This folder
is `hello.py` from lecture 252 plus two lines, and a `--no-tool` switch to see the difference a
tool makes.

```text
   "What is the weather in Patiala right now?"
          │
          ▼
   LLM: "I need to look this up" ──► hosted web search runs ON THE PROVIDER'S SERVERS
          │                                        │
          ◄──────────────── results ───────────────┘
          ▼
   LLM writes the answer ──► result.final_output
```

---

## 1. Setup

```bash
cd python_tut_2026/05_python_genai/13_udemy_learn/07_AgentSDK/253_implementHostedtOOLSinAgentSDK
source ../../../../../.venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # keys go here (gitignored)
```

---

## 2. Run

```bash
python agent_with_tool.py                                   # WITH the tool
python agent_with_tool.py --no-tool                         # same question, tool removed
python agent_with_tool.py "What is on piyushgarg.dev website?"
```

### With the tool

```text
Hey hey! 👋🌞 I just did a quick web‑hunt 🕵️‍♀️ (yes, I searched the internet) and here's the scoop on Patiala, Punjab right now:
- Condition: Clear sky 🌤️
- Temperature: 74 °F (23.6 °C) – feels like a toasty 81 °F! 🔥
- Humidity: 82 % (a bit muggy) 💧
- Wind: Gentle 2 mph from ENE 🌬️
```

### Same question, tool removed (`--no-tool`)

```text
👋 Hey there, weather‑wonderer! 🌦️
I'm not a live‑feed crystal ball 🧙‍♂️, so I can't peek at the exact sky‑status over Patiala right this second.
… For the freshest forecast, grab a trusty weather app or website. 😎☂️
```

**No tool = no action.** The model can only talk about what it already knows and tells *you* to
go search. That's the whole difference a tool makes.

---

## 3. The two lines (the lecture's code)

```python
from agents import WebSearchTool            # (1) import the hosted tool

agent = Agent(
    name="Hello World Agent",
    instructions="You greet the user and answer using emojis, in a funny way.",
    tools=[WebSearchTool()],                 # (2) give it to the agent - a list, add more with commas
)
result = Runner.run_sync(agent, "What is on piyushgarg.dev website?")
```

| Line | Meaning |
|---|---|
| `from agents import WebSearchTool` | hosted tools are classes in the SDK |
| `tools=[WebSearchTool()]` | attach it; the runner decides **when** to search |
| nothing else | search → results fed back → loop → final answer, all inside `Runner` |

---

## 4. Which provider runs the search

`WebSearchTool` is **OpenAI's** hosted tool: it executes on OpenAI's servers via the Responses
API, so it needs an OpenAI key with credits and cannot be served by another provider.
[agent_with_tool.py](agent_with_tool.py) therefore has two paths:

| `LLM_PROVIDER` | Tool | How it's declared | Where it runs |
|---|---|---|---|
| `openai` (default) | `WebSearchTool()` | `tools=[WebSearchTool()]` | OpenAI's servers |
| `groq` | Groq's built-in `browser_search` | `ModelSettings(extra_args={"tools": [{"type": "browser_search"}]})` | Groq's servers |

Same concept, same shape (a `tools` list the provider executes), different vendor. On the
Groq path the SDK doesn't have a class for the tool, so the entry goes through
`ModelSettings.extra_args` — the SDK merges `extra_args` into the API call **last**
(`create_kwargs.update(model_settings.extra_args)`), which is exactly why a provider-specific
`tools` list arrives at Groq untouched.

```python
Agent(
    name=..., instructions=...,
    model=OpenAIChatCompletionsModel(model="openai/gpt-oss-120b", openai_client=groq),
    model_settings=ModelSettings(extra_args={"tools": [{"type": "browser_search"}]}),
)
```

Everything the lecture is about — the runner calling the tool for you, and the "go search it
yourself" answer when the tool is gone — is identical on both paths.

---

## 5. Hosted tools in the SDK (check *Tools → Hosted tools* in the docs for the current list)

| Tool | What it does |
|---|---|
| `WebSearchTool` | search the internet |
| `FileSearchTool` | search files you uploaded to OpenAI (vector store) |
| `CodeInterpreterTool` | run code in a sandbox |
| `ComputerTool` | control a computer / browser |
| `ImageGenerationTool` | generate images |
| `LocalShellTool` | run shell commands on **your** machine |

Three kinds of tools overall: **hosted** (this lecture), **function tools** — your own Python
functions (next), **agents as tools** (later). All go in the same `tools=[...]` list.

---

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `429 … no credits remaining` | OpenAI key has no balance; `WebSearchTool` needs OpenAI | add credits, or `LLM_PROVIDER=groq` |
| `Hosted tools are not supported with the ChatCompletions model` | `WebSearchTool` passed to a non-OpenAI model | hosted tools are OpenAI-only; use the provider's own (Groq: `browser_search`) |
| `404 … model 'groq/compound…' does not exist` | Groq's older search models are gone from this account | use `openai/gpt-oss-120b` + `{"type": "browser_search"}` (what the script does) |
| answer says "I can't browse" even with the tool on | the model chose not to search | ask something clearly time-sensitive; instructions here ask it to say when it searched |
| `ModuleNotFoundError: No module named 'agents'` | SDK not installed in the active venv | `pip install openai-agents` |
