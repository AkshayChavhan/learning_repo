# Coding Agent CLI

A coding agent in one file — about 200 lines, no framework.

It reads files, writes files and runs commands **because you let it**, one `y/n` at a time.

---

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then install Ollama itself and pull a model:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5-coder:7b        # ~4.7 GB
```

## Run

```bash
python3 coding_agent.py "create hello.py that prints hello, then run it"
python3 coding_agent.py             # interactive; 'exit' to quit
```

Config is two environment variables:

| Variable | Default | Notes |
|---|---|---|
| `MODEL` | `qwen2.5-coder:7b` | `llama3.2` works but codes badly. `gemma:2b` **cannot** tool-call at all |
| `OLLAMA_HOST` | `http://localhost:11434` | Point it anywhere that speaks the Ollama API |

**No `.env` and no API key.** Both variables have working defaults and the model runs
locally through Ollama — nothing leaves the machine. Override them inline when you want
something different:

```bash
MODEL=llama3.2 python3 coding_agent.py "..."
```

See [ENVIRONMENT.md](../../../ENVIRONMENT.md) for the projects that *do* need keys.

---

## The idea

```text
   1. THINK    what should I do?      <- the model
        |
   2. ACT      use a tool             <- your code
        |
   3. OBSERVE  what happened?         <- back into the messages list
        |
   repeat, up to MAX_STEPS, then
   4. ANSWER
```

**The model never runs anything.** It replies with text that happens to be
structured — `{"tool": "read_file", "arguments": {"path": "x.py"}}`. This script
parses that, calls the real function, and appends the result as a `tool` message.
Step 2 is your code, not the model's. That is why sandboxing and permission
prompts are possible at all.

## The tools

| Tool | Does | Asks first |
|---|---|---|
| `read_file` | Return a file's contents | no |
| `list_files` | List a directory | no |
| `write_file` | Create or overwrite a file | **yes** |
| `run_command` | Run a shell command | **yes** |

## Safety

- Writes and commands print what they're about to do and wait for `y/n`.
- Paths that escape the working directory are refused.
- Commands are killed after 60 seconds.
- Broken tool calls return a readable sentence to the model instead of crashing,
  so it can correct itself. `MAX_STEPS = 10` stops runaway loops.

The agent works in **whatever directory you launch it from** — so `cd` somewhere
scratch before turning it loose.

## Where it's thin

One `write_file` rewrites a whole file, so large files cost a lot of tokens — a
real editing tool does exact string replacement. There's no streaming, no
persistent memory between runs, and no test harness. Those are the next steps.

---

Topic 41 · Phase 6 — see `01_What_Are_AI_Agents.pdf`.
