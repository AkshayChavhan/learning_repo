# 11 — Tool Calling

A **tool** is a Python function the model is allowed to ask for. Files `01`–`03`
are three ways to *make* one; `04` is the different thing — *handing* them to a
model so it can decide when to use them. Nothing here runs a tool on the
model's behalf yet; that loop is the step after this module.

---

## The files

| # | File | Builds | Input shape | The model involved? |
|---|---|---|---|---|
| 1 | `01_basic_tool.py` | `Tool(name=, func=, description=)` by hand | **one string** | no |
| 2 | `02_tool_decorator.py` | `@tool` on a plain function | dict, from **type hints** | no |
| 3 | `03_structured_tool.py` | `StructuredTool.from_function(args_schema=…)` | dict, from a **Pydantic model** | no |
| 4 | `04_tool_binding.py` | nothing — `llm.bind_tools([...])` | — | **yes** |

```text
  01  Tool()                 "here is a function, call it by this name"
        │                      one string in, you type every field
        ▼
  02  @tool                  the same, read off the function itself
        │                      name ← def, description ← docstring, schema ← hints
        ▼
  03  StructuredTool         the same, with a Pydantic schema you control
        │                      per-field descriptions, validation, enums
        ▼
  04  bind_tools()           give 1–3 to a model → it answers with a TOOL CALL
                               .tool_calls = [{name, args, id}]  ·  nothing executed
```

Files 1–3 answer *"how do I describe a function to a model?"* with increasing
precision. File 4 answers *"what happens when the model is shown it?"*

---

## Three ways to make a tool — side by side

| | `01` `Tool()` | `02` `@tool` | `03` `StructuredTool.from_function` |
|---|---|---|---|
| **How you build it** | three keyword args, by hand | one decorator | factory + a `BaseModel` |
| **Class produced** | `Tool` (legacy) | `StructuredTool` | `StructuredTool` |
| **Input** | **one `str`** | dict | dict |
| **`name` from** | you type it | the function name | you type it |
| **`description` from** | you type it | the docstring | you type it |
| **Argument schema from** | none — `{"tool_input": string}` | type hints | Pydantic fields |
| **Per-field descriptions reach the model** | — | ❌ `Args:` block is plain text | ✅ `Field(description=…)` |
| **Validates input** | no | types only | types + your constraints |
| **Constrained choices (`enum`)** | — | — | ✅ via `Literal[...]` |
| **Lines to write** | most | fewest | middle |

Verified on the installed library: `02` and `03` both produce `StructuredTool`.
The decorator is not a lesser tool — it is the *same class* with the schema
inferred rather than declared.

### When to use which

| Reach for | When |
|---|---|
| **`Tool()`** | wrapping something that already takes a single string — a search query, a lookup key. Rare today |
| **`@tool`** | **the default.** Any function you own with clear type hints and a good docstring |
| **`StructuredTool` + Pydantic** | several arguments the model must fill *accurately*; a field with a fixed set of values; descriptions that must reach the model; or a schema you also want to reuse for validation elsewhere |
| **`bind_tools()`** | whenever the *model* should decide whether, and with what, to call something |

The dividing line between `02` and `03` is one question: **does the model need
per-argument guidance?** `a: int` needs none. `operation: str` with four legal
values needs an enum.

---

## `04` is not a way to make a tool

`bind_tools([multiply, add])` changes nothing about the tools. It sends their
schemas to the model alongside your message, so the model now has a second way
to reply:

| Model's reply | `.text` | `.tool_calls` |
|---|---|---|
| ordinary prose | the answer | `[]` |
| **a tool call** | **empty** | `[{"name": "multiply", "args": {"a": 25, "b": 4}, "id": "fc_…"}]` |

An empty `.text` on a tool call is **expected**, not a failure — `04` prints a
fallback so that is visible.

### What the model actually sees

This is the exact payload `bind_tools` sends for `multiply` in `04`:

```json
{
  "type": "function",
  "function": {
    "name": "multiply",
    "description": "Multiply two numbers.",
    "parameters": {
      "properties": { "a": {"type": "integer"}, "b": {"type": "integer"} },
      "required": ["a", "b"],
      "type": "object"
    }
  }
}
```

Three things to notice. The **name** and **description** are the docstring and
`def` from `02`'s technique. The parameters carry **no descriptions** — bare
type hints give none, which is fine for `a: int` and exactly the gap `03`
closes for anything less obvious. And this JSON is *all* the model gets: it
never sees your Python.

---

## The step this module stops before

```text
  you  ──"25 × 4?"──►  model  ──►  AIMessage(tool_calls=[multiply(25, 4)])
                                          │
                              04 STOPS HERE — the model DECIDED
                                          │
                        (next)  you run multiply(25, 4)  →  100
                                          │
                        ToolMessage(content="100", tool_call_id="fc_…")
                                          │
                                  model  ──►  "25 × 4 is 100."
```

`04` proves the model chose the right tool with the right arguments. It never
runs `multiply`, and the model never sees `100`. Executing the call, returning
the result as a `ToolMessage` with the **same `id`**, and invoking the model
again is the **agent loop** — the whole of the next topic.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`Tool()` takes ONE string** | `func` receives a single `str`. Several typed arguments → `@tool` or `StructuredTool` |
| **`.text` is empty on a tool call** | The answer is in `.tool_calls`. Print a fallback, don't treat it as an error |
| **The `Args:` docstring block is text, not schema** | Per-argument descriptions reach the model only with `@tool(parse_docstring=True)` or a Pydantic `Field(description=…)` |
| **`raise`, never `return`, an error inside a tool** | A returned exception is handed to the model as a normal result |
| **A free `str` for a fixed set of choices** | `Literal["add", "subtract", …]` becomes an `enum` the model cannot misspell |
| **`.schema()` is Pydantic v1** | Warns on v2. Use `.model_json_schema()` |
| **Project imports go below the `sys.path` block** | Above it, `llm_client` is not importable and the script dies |
| **Loop variable vs the thing indexed** | `for tool_call in result.tool_calls:` then `tool_call["name"]` — one letter off was a `TypeError` in `04`'s first draft |
| **Tool calling is a provider feature** | A model without it ignores `bind_tools` and answers in prose |

---

## Known issues in these files

| File | Issue |
|---|---|
| `03_structured_tool.py:34` | `return ValueError(...)` — divide-by-zero hands the model an exception object as a result. Should be `raise` |
| `03_structured_tool.py:22` | `operation: str` with the legal values only in prose — and the prose says `"multplipy"`. A `Literal` fixes both |
| `02_tool_decorator.py:35` | `.args_schema.schema()` prints a Pydantic deprecation warning on every run. `.model_json_schema()` is the current call |
| `04_tool_binding.py` | `multiply` / `add` arguments carry no descriptions — harmless for `int`s, but it is the pattern `03` exists to fix |
