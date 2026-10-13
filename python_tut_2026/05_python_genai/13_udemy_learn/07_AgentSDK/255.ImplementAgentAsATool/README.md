# Agent as a Tool — one agent calls another

An agent can be given **another agent** as a tool. The user talks to the **orchestrator**;
when a request needs a specialist, the orchestrator calls that agent like a function, gets its
final answer back, and replies. One method does it: `specialist.as_tool(...)`.

```text
   user ──► Orchestrator agent ──translate_to_spanish("Hello, how are you?")──► Spanish agent
                    ▲                                                              │ own loop, own instructions
                    └──────────────────── "Hola, ¿cómo estás?" ────────────────────┘
   orchestrator replies to the user
```

---

## 1. Setup

```bash
cd python_tut_2026/05_python_genai/13_udemy_learn/07_AgentSDK/255.ImplementAgentAsATool
source ../../../../../.venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Agent-as-tool runs **in-process** (the specialist is just another `Runner` loop), so it works on
any provider — `LLM_PROVIDER=groq` included. On Groq, note that **every** agent needs the
`model=` argument, specialists too, because each runs its own loop.

---

## 2. Run

```bash
python agent_tool.py                                           # Spanish
python agent_tool.py "Say 'Good morning' in French."
python agent_tool.py "Say 'See you tomorrow' in Spanish and French."
python agent_tool.py --trace                                   # also show the tool calls
```

```text
> Say 'Hello, how are you?' in Spanish.

Hola, ¿cómo estás?

--- trace ---
  call   translate_to_spanish({"input":"Hello, how are you?"})
  output 'Hola, ¿cómo estás?'
  reply  by Orchestrator agent
```

Ask for both languages and the orchestrator calls **both** specialists in one run:

```text
> Say 'See you tomorrow' in Spanish and French.

Spanish: Nos vemos mañana
French:  À demain

--- trace ---
  call   translate_to_spanish({"input":"See you tomorrow"})
  output 'Nos vemos mañana'
  call   translate_to_french({"input":"See you tomorrow"})
  output 'À demain'
  reply  by Orchestrator agent
```

The orchestrator **chose** which tool(s) to call from the `tool_description`s — nothing in the
code routes by language.

---

## 3. The code ([agent_tool.py](agent_tool.py))

```python
spanish_agent = Agent(name="Spanish agent", instructions="You translate the user's message to Spanish.")
french_agent  = Agent(name="French agent",  instructions="You translate the user's message to French.")

orchestrator_agent = Agent(
    name="Orchestrator agent",
    instructions="You are a translation agent. You use the tools given to you to translate. "
                 "If asked for multiple translations, call the relevant tools.",
    tools=[
        spanish_agent.as_tool(tool_name="translate_to_spanish",
                              tool_description="Translate the user's message to Spanish"),
        french_agent.as_tool(tool_name="translate_to_french",
                             tool_description="Translate the user's message to French"),
    ],
)
result = Runner.run_sync(orchestrator_agent, "Say 'Hello, how are you?' in Spanish.")
```

| Piece | Meaning |
|---|---|
| `spanish_agent` / `french_agent` | ordinary agents, nothing special about them |
| `agent.as_tool(tool_name=, tool_description=)` | wraps an agent so it looks like a function tool |
| `tool_name` | the name the LLM sees (like a function name) |
| `tool_description` | when to use it (like a docstring) — this is what the orchestrator decides by |
| `tools=[...]` | the same list as hosted and function tools; all three kinds can mix |
| the tool's single argument `input` | the SDK adds it: the text handed to the specialist |

---

## 4. Seeing the call happen (`--trace`)

`result.final_output` is only the text. `result.new_items` holds every step of the run:

| `item.type` | What it is |
|---|---|
| `tool_call_item` | the orchestrator decided to call a tool: `raw_item.name`, `raw_item.arguments` |
| `tool_call_output_item` | what the specialist returned: `item.output` |
| `message_output_item` | a final text message, with `item.agent.name` |

(The note's `result.raw_responses` shows the same calls at the raw-API level; `new_items` is
the SDK's tidier view.)

---

## 5. Agent-as-tool vs handoff

| | Agent as tool (this lecture) | Handoff (later) |
|---|---|---|
| who stays in charge | the **orchestrator** — it gets the answer and replies | control **transfers** to the other agent |
| shape | `tools=[other.as_tool(...)]` | `handoffs=[other]` |
| use when | you need a sub-result and want to keep the conversation | the other agent should take over the conversation |

## 6. `run` vs `run_sync`

| | Use |
|---|---|
| `Runner.run_sync(agent, input)` | plain scripts (this folder) |
| `await Runner.run(agent, input)` | inside async code (web servers, streaming) |

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| specialist fails with `429 no credits` while orchestrator works | on Groq, only the orchestrator got `model=` | pass `model=MODEL` to **every** `Agent(...)` |
| orchestrator answers itself instead of calling a tool | vague `tool_description`, or instructions don't say to use tools | describe each tool clearly; tell the orchestrator to use them |
| only one language returned when two were asked | orchestrator instructions lack "if asked for multiple translations, call the relevant tools" | keep that sentence |
| `ModuleNotFoundError: No module named 'agents'` | SDK not in the active venv | `pip install openai-agents` |
