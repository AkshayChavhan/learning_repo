# Hello World Agent — OpenAI Agents SDK

The smallest possible agent with the **OpenAI Agents SDK**: an `Agent` (name + instructions)
run by `Runner.run_sync`. The while-loop, message history and tool dispatch you wrote by hand
in the earlier weather agent are now inside the runner — you declare the agent and read
`result.final_output`.

```text
   Agent(name, instructions)  ──►  Runner.run_sync(agent, input)  ──►  result.final_output
          what it is                   the whole loop, hidden              the answer
```

---

## 1. Setup

```bash
cd python_tut_2026/05_python_genai/13_udemy_learn/07_AgentSDK/252_implementHelloWorldAgent
source ../../../../../.venv/bin/activate      # repo-root venv
pip install -r requirements.txt               # openai-agents + python-dotenv
cp .env.example .env                          # put your keys in (gitignored)
```

| In `.env` | Needed for |
|---|---|
| `OPENAI_API_KEY` | the SDK's default provider (OpenAI) |
| `GROQ_API_KEY`, `GROQ_MODEL`, `LLM_PROVIDER=groq` | running the same agent on Groq instead (free tier) |

The package is `openai-agents`; you **import from `agents`**.

---

## 2. Run

```bash
python hello.py                        # SDK default: OpenAI
LLM_PROVIDER=groq python hello.py      # same Agent/Runner, model served by Groq
```

Output (Groq, `openai/gpt-oss-120b`):

```text
Hey there, Akshay! 🙌😎
Welcome to the land of *chatty* emojis! 🎉✨
If you need a joke, a fact, or just a virtual high‑five, I'm here—armed with 🦸‍♂️💬 and a sprinkle of 🎈.
What shenanigans shall we dive into today? 🚀🤪
```

Different wording every run — it's a model, not a template.

---

## 3. The three real lines ([hello.py](hello.py))

```python
hello_agent = Agent(
    name="Hello World Agent",
    instructions="You greet the user and answer using emojis, in a funny way.",
)
result = Runner.run_sync(hello_agent, "Hello, my name is Akshay")
print(result.final_output)
```

| Line | Meaning |
|---|---|
| `Agent(name=…, instructions=…)` | `name` is a label (shows up in traces); `instructions` is the system prompt |
| `Runner.run_sync(agent, input)` | runs the loop to completion: LLM call → tool calls (none yet) → repeat → stop at the final answer |
| `result.final_output` | the text the agent ended with |

### What the runner replaced

| By hand (weather agent) | With the SDK |
|---|---|
| system prompt string | `instructions=` |
| `while True:` | `Runner.run_sync()` |
| `messages = []` you append to | kept inside the runner |
| parse JSON, `if step == "action": call tool` | `tools=[…]`, dispatched automatically (next lecture) |
| `if step == "output": break` | `result.final_output` |

---

## 4. Running it on a non-OpenAI model

The SDK talks to OpenAI by default. Any **OpenAI-compatible** endpoint can serve an agent
through `OpenAIChatCompletionsModel` — that's what `LLM_PROVIDER=groq` switches on in `hello.py`:

```python
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

set_tracing_disabled(True)   # tracing uploads runs to OpenAI's dashboard and needs an OpenAI key
groq = AsyncOpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
model = OpenAIChatCompletionsModel(model="openai/gpt-oss-120b", openai_client=groq)

Agent(name=..., instructions=..., model=model)
```

| | OpenAI (default) | Groq via `OpenAIChatCompletionsModel` |
|---|---|---|
| `Agent(...)` call | unchanged | one extra `model=` argument |
| API used | Responses API | Chat Completions API |
| tracing | on, visible at platform.openai.com/traces | disabled (no OpenAI key needed) |
| cost | paid | free tier |

Everything else — `Runner`, `final_output`, and later `tools`, `handoffs`, `guardrails` — is
identical.

---

## 5. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'agents'` | SDK not installed in the active venv | `pip install openai-agents` (import name ≠ package name) |
| `429 … You have no credits remaining` | OpenAI key has no balance | add credits, or `LLM_PROVIDER=groq` |
| `404 … The model 'llama-3.3-70b-versatile' does not exist` | Groq retired that model | set `GROQ_MODEL=openai/gpt-oss-120b` (or any current model from `console.groq.com`) |
| `Missing credentials … OPENAI_API_KEY` | `.env` missing or `load_dotenv()` not called before the SDK is used | `cp .env.example .env`; keep `load_dotenv()` at the top |
| `Tracing client error 401` printed after the answer | tracing tried to upload with no valid OpenAI key | `set_tracing_disabled(True)` (already done on the Groq path) |

---

## 6. What's next (same `Agent(...)`, more arguments)

| Feature | Argument |
|---|---|
| tools the agent can call | `tools=[…]` |
| token-by-token output | `Runner.run_streamed` |
| MCP servers as tools | `mcp_servers=[…]` |
| one agent passes to another | `handoffs=[…]` |
| input/output checks | `guardrails` |
| history across runs | `sessions` |
