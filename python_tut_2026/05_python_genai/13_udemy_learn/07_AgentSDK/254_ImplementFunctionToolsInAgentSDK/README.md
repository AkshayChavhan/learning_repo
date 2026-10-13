# Function Tools — your own Python function as a tool

A **function tool** is any Python function you write, turned into a tool by one decorator:
`@function_tool`. The SDK reads the function's **name**, **type hints** and **docstring** to
tell the LLM what it does and what it takes; the runner calls it when the model asks. This
folder wraps the `get_weather` function from the hand-written weather agent and lets you
watch it being called.

```text
   "What is the weather in Patiala?"
        │
        ▼
   LLM: call get_weather(city="Patiala")  ──►  YOUR Python runs (wttr.in)  ──►  "Clear +24°C"
        │                                                                         │
        ◄─────────────────────────────────────────────────────────────────────────┘
        ▼
   LLM writes the final answer  ──►  result.final_output
```

---

## 1. Setup

```bash
cd python_tut_2026/05_python_genai/13_udemy_learn/07_AgentSDK/254_ImplementFunctionToolsInAgentSDK
source ../../../../../.venv/bin/activate
pip install -r requirements.txt       # openai-agents, python-dotenv, requests
cp .env.example .env                  # keys (gitignored)
```

Function tools run **on your machine**, so unlike hosted tools they work with any provider —
`LLM_PROVIDER=groq` is fine here.

---

## 2. Run

```bash
python agent_with_function_tool.py                        # "What is the weather in Patiala?"
python agent_with_function_tool.py "How is the weather in Mumbai today?"
python agent_with_function_tool.py --show-schema          # what the decorator built
python agent_with_function_tool.py --no-tool              # same question, no tool
```

```text
[groq | tools: ['get_weather']]
> What is the weather in Patiala?

   [tool] get_weather(city='Patiala') <- your Python is running

👋 Hey there! 🌞 Looks like Patiala is enjoying a **clear** sky with a pleasant **+24°C**! Perfect time for a 🍦 …
```

The `[tool] …` line is a `print` inside `get_weather` — proof the answer came from **your**
function hitting `wttr.in`, not from the model's memory or a web search.

---

## 3. The three steps

```python
from agents import Agent, Runner, function_tool          # (1) import the decorator

@function_tool                                           # (2) decorate a typed function WITH a docstring
def get_weather(city: str) -> str:
    """Fetch the current weather for the given city.

    Args:
        city: The city name to fetch the weather for.
    """
    ...

agent = Agent(name=..., instructions=..., tools=[get_weather])   # (3) the function, NO parentheses
```

---

## 4. Where the LLM's knowledge of the tool comes from (`--show-schema`)

```text
tool name   : get_weather
description : Fetch the current weather for the given city.
parameters  : {
  "properties": { "city": { "description": "The city name to fetch the weather for.",
                            "title": "City", "type": "string" } },
  "required": ["city"], "additionalProperties": false, ...
}
```

| From the function | Becomes |
|---|---|
| name `get_weather` | tool name |
| docstring first line | tool description |
| `Args:` section | each parameter's description |
| type hint `city: str` | `"type": "string"` |
| return value | what goes back to the LLM |

**The docstring is not optional.** Delete it and the description is empty — the model has no
idea when to use the tool. `@function_tool(name_override="fetch_weather")` renames the tool
without renaming the function.

---

## 5. The mistake from the lecture

```python
tools=[WebSearchTool(), get_weather()]     # ❌
tools=[WebSearchTool(), get_weather]       # ✅
```

```text
TypeError: 'FunctionTool' object is not callable
```

| | Why |
|---|---|
| `WebSearchTool()` **with** `()` | it's a **class** — you create an instance |
| `get_weather` **without** `()` | after the decorator it isn't a plain function any more, it's a `FunctionTool` object. You pass the object; the runner calls the wrapped function later with the arguments the model chose |

---

## 6. Hosted + function tools in one list

The lecture's list is `tools=[WebSearchTool(), get_weather]` — a hosted tool and a function
tool side by side; the runner handles both. That's the default (OpenAI) path in the script.
On Groq, `WebSearchTool` (OpenAI-only, see folder 253) is dropped and the list is just
`[get_weather]` — which is precisely the lecture's section 5: *remove web search, still 24 °C,
the answer came from your function.*

| Tool kind | Who writes it | Where it runs | Works on Groq? |
|---|---|---|---|
| hosted (`WebSearchTool`) | OpenAI | OpenAI's servers | no (OpenAI-only) |
| **function** (`@function_tool`) | **you** | **your machine** | **yes** |
| agent as tool | you (another agent) | your machine | yes (later) |

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `TypeError: 'FunctionTool' object is not callable` | `get_weather()` with parentheses in `tools=[...]` | pass `get_weather` |
| model answers without calling the tool | docstring missing/vague, or the question isn't about weather | write a clear first line + `Args:`; ask a weather question |
| `Something went wrong` from the tool | wttr.in down or rate-limited | `curl 'https://wttr.in/Patiala?format=%C+%t'` to check; retry |
| `429 … no credits` | OpenAI path with an empty key | `LLM_PROVIDER=groq` |
| `ModuleNotFoundError: requests` | dependency not installed | `pip install -r requirements.txt` |
