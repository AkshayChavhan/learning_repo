# Agent as a Tool — One Agent Calls Another

An agent can be given **another agent** as a tool. The user talks to one agent (the
**orchestrator**); when a question needs a specialist, the orchestrator calls the
specialist agent like it would call a function, gets the answer back, and replies. One
method does it: `specialist.as_tool(...)`.

---

## 1. The idea

```text
   user ──► physics agent ──"solve this equation"──► maths agent
                 ▲                                      │ uses its own tools: add, subtract…
                 └──────────── answer ──────────────────┘
   physics agent replies to the user
```

| Example | Orchestrator | Specialist used as tool |
|---|---|---|
| science tutor | physics agent | maths agent |
| company chat | sales agent | technical agent |
| translation (this lecture) | translation orchestrator | Spanish agent, French agent |

The specialist agent runs its **own** loop, with its **own** instructions and tools, and
returns only its final answer to the caller.

---

## 2. The code

```python
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

# two specialists: plain agents, nothing special about them
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish.",
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French.",
)

# the orchestrator: the one the user talks to
orchestrator_agent = Agent(
    name="Orchestrator agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate. "
        "If asked for multiple translations, call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(                                   # ← agent → tool
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
)

result = Runner.run_sync(orchestrator_agent, "Say 'Hello, how are you?' in Spanish.")
print(result.final_output)
```

```bash
python agent_sdk/agent_tool.py
```

```text
Hola, ¿cómo estás?
```

| Line | Meaning |
|---|---|
| `spanish_agent.as_tool(...)` | wrap an agent so it looks like a function tool |
| `tool_name` | the name the LLM sees (like a function name) |
| `tool_description` | when to use it (like a docstring) |
| `tools=[...]` | same list as hosted and function tools; mix all three |

---

## 3. See the tool call happen

The result holds more than the final text:

```python
for item in result.raw_responses:
    print(item)
```

```text
... type='function_call'  name='translate_to_spanish'  arguments='{"input": "Hello, how are you?"}'
... type='function_call_output'  output='Hola, ¿cómo estás?'
```

Ask for French instead and you see `translate_to_french` called. The orchestrator
**chose** the right agent from the tool descriptions.

```text
   "Say hello in Spanish"
        │
        ▼
   orchestrator: call translate_to_spanish ──► spanish_agent runs its own loop ──► "Hola…"
        │                                                                          │
        ◄──────────────────────────────────────────────────────────────────────────┘
        ▼
   orchestrator replies
```

---

## 4. `run` vs `run_sync`

The docs example uses `await Runner.run(...)` inside an `async def main()`. For a script,
drop `await` and use `Runner.run_sync(...)`, as above. Same result.

| | Use |
|---|---|
| `Runner.run_sync(agent, input)` | plain scripts |
| `await Runner.run(agent, input)` | inside async code (web servers, streaming) |

---

## Remember

| Term | One line |
|---|---|
| **agent as a tool** | one agent in another's `tools` list |
| **`agent.as_tool(tool_name=, tool_description=)`** | the one call that does it |
| **orchestrator** | the agent the user talks to; it delegates |
| **specialist** | an ordinary agent; runs its own loop, returns its final answer |
| **`result.raw_responses`** | shows the function calls made, including agent-tool calls |
| **three tool kinds together** | hosted, function and agent tools all go in `tools=[]` |

> **If someone asks in an interview:** "How do you compose agents in the OpenAI Agents
> SDK?" Either hand off the conversation to another agent, or use `agent.as_tool()` to let
> an orchestrator call a specialist agent as a tool, get its output, and keep control of
> the conversation. Agent-as-tool keeps the orchestrator in charge; handoff transfers it.
