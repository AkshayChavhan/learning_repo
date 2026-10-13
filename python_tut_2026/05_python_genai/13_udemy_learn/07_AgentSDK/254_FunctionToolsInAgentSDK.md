# Function Tools — Your Own Python Function as a Tool

A **function tool** is any Python function you write, turned into a tool with one
decorator: `@function_tool`. The SDK reads the function's **name**, **type hints** and
**docstring** to tell the LLM what the tool does and what arguments it takes. Then you drop
it into `tools=[...]` like any other tool.

---

## 1. The three steps

| Step | Code |
|---|---|
| 1. import the decorator | `from agents import function_tool` |
| 2. decorate a normal function, with a **docstring** | `@function_tool` above `def get_weather(city: str) -> str:` |
| 3. pass the function to the agent | `tools=[get_weather]` (no parentheses) |

---

## 2. The code

Reuse the `get_weather` function from the old weather agent:

```python
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool, function_tool

load_dotenv()

@function_tool                                     # ① makes it a tool
def get_weather(city: str) -> str:
    """Fetch the weather for the given city.       # ② docstring = tool description

    Args:
        city: The city name to fetch the weather for.
    """
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

agent = Agent(
    name="Hello World Agent",
    instructions="You greet the user and answer using emojis, in a funny way.",
    tools=[WebSearchTool(), get_weather],          # ③ two tools: hosted + function
)

result = Runner.run_sync(agent, "What is the weather in Patiala?")
print(result.final_output)
```

```bash
python agent_sdk/agent_with_tool.py
```

```text
Patiala is toasty at 27°C ☀️ Perfect weather to rock those shades! 😎
```

---

## 3. Where the LLM gets the tool's description

The decorator builds the tool schema from the function itself:

| From | Becomes |
|---|---|
| function name `get_weather` | tool name |
| docstring first line | tool description: *"Fetch the weather for the given city."* |
| `Args:` section | description of each parameter |
| type hint `city: str` | parameter type |
| return value | what goes back to the LLM |

So the **docstring is not optional**. A vague or missing one means the LLM doesn't know
when to use the tool.

```python
@function_tool(name_override="fetch_weather")      # optional: different tool name
def get_weather(city: str) -> str:
    ...
```

---

## 4. The mistake from the lecture

```python
tools=[WebSearchTool(), get_weather()]     # ❌ error
tools=[WebSearchTool(), get_weather]       # ✅
```

| | Why |
|---|---|
| `WebSearchTool()` **with** parentheses | it's a **class**; you create an instance |
| `get_weather` **without** parentheses | it's a **function**; you pass the reference. The runner calls it later |

With `()` you'd run the function right now, with no `city`, and pass its return value
instead of the tool.

---

## 5. Prove it's your tool, not web search

```python
tools=[get_weather],        # WebSearchTool removed
```

Run again: still 27°C in Patiala. The answer came from **your** function hitting
`wttr.in`, not from a web search.

```text
   "weather in Patiala?"
        │
        ▼
   LLM: "call get_weather(city='Patiala')"  ──►  your Python runs  ──►  "27°C"
        │                                                              │
        ◄──────────────────────────────────────────────────────────────┘
        ▼
   LLM writes the final answer
```

---

## Remember

| Term | One line |
|---|---|
| **function tool** | a Python function made into a tool with `@function_tool` |
| **docstring** | required; it's what the LLM reads to decide when and how to call it |
| **type hints** | define the parameters' types |
| **`tools=[get_weather]`** | pass the function, **no `()`** |
| **`name_override=`** | optional different tool name |
| **mix freely** | hosted + function tools in one list; the runner handles all of them |

> **If someone asks in an interview:** "How do you add a custom tool in the OpenAI Agents
> SDK?" Decorate a typed Python function with `@function_tool` and give it a docstring.
> The SDK generates the JSON schema from the signature and docstring, and the runner calls
> the function automatically when the model requests it.
