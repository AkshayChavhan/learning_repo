"""A tiny coding agent you can read in one sitting.

    python3 coding_agent.py "create hello.py and run it"    # one task
    python3 coding_agent.py                                 # interactive

The whole thing is Think -> Act -> Observe -> repeat.

The model never runs your code. It only *asks* for a tool by name; this
script looks the name up, calls the real Python function, and hands the
result back as a new message. That is the entire trick behind agents.
"""

import json
import os
import subprocess
import sys

from ollama import Client, ResponseError

# ---------------------------------------------------------------- 1. config

MODEL = os.getenv("MODEL", "qwen2.5-coder:7b")   # llama3.2 is too small to code well
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MAX_STEPS = 10

ROOT = os.path.abspath(os.getcwd())              # the agent never leaves this directory

SYSTEM = (
    "You are a coding assistant working in a terminal. "
    "You can read, list and write files and run shell commands with the tools provided. "
    "Work in small steps: look before you change something, change one thing, then verify it. "
    "When the task is done, reply with a short summary and no tool call."
)


# ----------------------------------------------------------------- 2. tools
# A tool is just a Python function. Nothing more.

def _safe_path(path):
    """Resolve a path and refuse anything outside the working directory."""
    full = os.path.abspath(os.path.join(ROOT, path))
    if full != ROOT and not full.startswith(ROOT + os.sep):
        raise ValueError(f"path leaves the working directory: {path}")
    return full


def _confirm(action, detail):
    """Show what is about to happen and wait for y/n."""
    lines = detail.splitlines()
    print(f"\n  {action}")
    for line in lines[:20]:
        print(f"  | {line}")
    if len(lines) > 20:
        print(f"  | ... {len(lines) - 20} more lines")
    return input("  allow? [y/N] ").strip().lower() in ("y", "yes")


def read_file(path):
    """Read a text file and return its contents."""
    try:
        with open(_safe_path(path)) as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}"


def list_files(directory="."):
    """List the files and folders in a directory."""
    try:
        names = sorted(os.listdir(_safe_path(directory)))
        return "\n".join(names) if names else "(empty directory)"
    except Exception as e:
        return f"ERROR: {e}"


def write_file(path, content):
    """Create or overwrite a file. Asks the user first."""
    try:
        full = _safe_path(path)
    except Exception as e:
        return f"ERROR: {e}"

    if not _confirm(f"write {path}", content):
        return "DENIED by the user. Do not try this write again."

    try:
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(full, "w") as f:
            f.write(content)
        return f"wrote {path} ({len(content)} bytes)"
    except Exception as e:
        return f"ERROR: {e}"


def run_command(command):
    """Run a shell command in the working directory. Asks the user first."""
    if not _confirm("run a command", command):
        return "DENIED by the user. Do not try this command again."

    try:
        done = subprocess.run(
            command, shell=True, cwd=ROOT, timeout=60,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
    except subprocess.TimeoutExpired:
        return "ERROR: command took longer than 60 seconds and was killed."
    except Exception as e:
        return f"ERROR: {e}"

    output = done.stdout.decode("utf-8", "replace").strip()
    return f"exit code {done.returncode}\n{output or '(no output)'}"


# --------------------------------------------- 3. describe the tools to the model
# Same functions as above, written out as JSON so the model knows they exist.
# The descriptions ARE prompts - saying when *not* to use a tool matters as
# much as saying when to.

def _tool(name, description, properties, required):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }


TOOLS = [
    _tool(
        "read_file",
        "Read a text file and return its contents. Always read a file before "
        "changing it, so you know what is already there.",
        {"path": {"type": "string", "description": "File path relative to the working directory"}},
        ["path"],
    ),
    _tool(
        "list_files",
        "List the files and folders in a directory. Use this to find your way "
        "around before reading files. Do NOT use it to read a file's contents.",
        {"directory": {"type": "string", "description": "Directory path. Use '.' for the current directory"}},
        ["directory"],
    ),
    _tool(
        "write_file",
        "Create a file or replace it completely. You must pass the whole new "
        "contents, not a patch or a diff. If the file already exists, read it first.",
        {
            "path": {"type": "string", "description": "File path relative to the working directory"},
            "content": {"type": "string", "description": "The complete contents of the file"},
        },
        ["path", "content"],
    ),
    _tool(
        "run_command",
        "Run a shell command, for example to run a script or the tests. Do NOT "
        "use this to read or write files - use read_file and write_file instead.",
        {"command": {"type": "string", "description": "The shell command to run"}},
        ["command"],
    ),
]

AVAILABLE = {
    "read_file": read_file,
    "list_files": list_files,
    "write_file": write_file,
    "run_command": run_command,
}


# ------------------------------------------------------------------ 4. the loop

def _short(args, limit=60):
    text = json.dumps(args)
    return text if len(text) <= limit else text[:limit] + "..."


def run(task, messages=None):
    """Work on one task until it is done. Returns the message history."""
    client = Client(host=HOST)

    if messages is None:
        messages = [{"role": "system", "content": SYSTEM}]
    messages.append({"role": "user", "content": task})

    for step in range(1, MAX_STEPS + 1):
        try:
            reply = client.chat(model=MODEL, messages=messages, tools=TOOLS)  # think
        except ConnectionError:
            print(f"\nCannot reach Ollama at {HOST}. Start it with:  ollama serve\n")
            return messages
        except ResponseError as e:
            print(f"\nOllama said: {e}")
            print(f"If the model is missing:  ollama pull {MODEL}\n")
            return messages

        message = reply.message
        messages.append(message)                                         # memory

        if not message.tool_calls:                     # no tool wanted -> final answer
            print(f"\n{(message.content or '').strip()}\n")
            return messages

        for call in message.tool_calls:                                  # act
            name = call.function.name
            args = dict(call.function.arguments or {})
            print(f"  [{step}] {name}({_short(args)})")

            function = AVAILABLE.get(name)
            if function is None:
                result = f"ERROR: there is no tool called {name!r}. " \
                         f"Available tools: {', '.join(AVAILABLE)}"
            else:
                try:
                    result = function(**args)
                except TypeError as e:
                    result = f"ERROR: wrong arguments for {name}: {e}"

            messages.append({                                            # observe
                "role": "tool",
                "name": name,
                "content": str(result),
            })

    print(f"\nGave up after {MAX_STEPS} steps without finishing.\n")
    return messages


# ------------------------------------------------------------------- 5. the CLI

def main():
    print(f"coding agent  ·  model {MODEL}  ·  {ROOT}")

    if len(sys.argv) > 1:
        run(" ".join(sys.argv[1:]))
        return

    print("Type a task, or 'exit' to quit.")
    messages = None
    while True:
        try:
            task = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if task in ("exit", "quit"):
            return
        if task:
            messages = run(task, messages)


if __name__ == "__main__":
    main()
