# 04 — Chains

A **chain** connects components so the output of one becomes the input of the
next. In modern LangChain you build one with the pipe operator.

---

## The files

Read them in order — each adds one idea to the one before.

| # | File | Mechanism | Adds |
|---|---|---|---|
| 1 | `01_sequential_chain.py` | `prompt \| llm \| parser` | the pipe — steps in order |
| 2 | `02_parallel_chain.py` | `RunnableParallel(a=…, b=…)` | branches side by side |
| 3 | `03_custom_chain.py` | `RunnableLambda(func)` | plain Python as a step |
| 4 | `04_router_chain.py` | `RunnableLambda(route)` | pick which chain runs |

Files 1–2 are pure LCEL. Files 3–4 both use `RunnableLambda` — 3 in the obvious
way, 4 in the subtle way.

---

## The pipe

`|` is **not** "or". LangChain overloads it to mean *feed the left result into
the right* — the same idea as a Unix pipe.

```python
title_chain = title_prompt | llm | StrOutputParser()
```

```text
   {"topic": "Fat loss"}
            │
            ▼
      title_prompt         fills the template
            │  StringPromptValue
            ▼
           llm             generates text
            │  AIMessage
            ▼
   StrOutputParser()       unwraps to a plain string
            │
            ▼
     "10 Fat Loss Hacks…"
```

The label on each arrow is **what type flows across it** — that is the real
content of the line.

Two things that trip people up:

- **`|` builds an object, it does not run anything.** The result is a
  `RunnableSequence` sitting in a variable. Nothing is sent until `.invoke()`.
- **`StrOutputParser()` is not optional.** `llm` returns an `AIMessage`, not
  text. Without it the next prompt interpolates
  `content='…' response_metadata={…}` into your template.

---

## The four shapes

```text
1. SEQUENTIAL          2. PARALLEL              3. CUSTOM         4. ROUTER
   in                     in                      in                 in
   │                    ┌──┼──┐                   │                  │
   ▼                    ▼  ▼  ▼                   ▼               ┌──┴──┐
  step 1               a   b   c              your function       ?     ?
   │                    └──┼──┘                (loops, ifs,       ▼     ▼
   ▼                       ▼                    many steps)      chain A/B
  step 2                 {dict}                     │                │
   │                                                ▼                ▼
   ▼                                              result           result
  out
```

| Shape | Use when | Result |
|---|---|---|
| Sequential | each step **needs** the previous result | the last step's output |
| Parallel | steps are **independent** | a `dict`, one key per branch |
| Custom | you need loops, conditionals, several dependent calls | whatever you return |
| Router | different input types need different handling | the chosen chain's output |

**Sequential vs parallel is about dependency, not preference.** Parallel takes
about as long as its slowest branch; sequential takes the sum. Never serialise
work that does not feed each other.

---

## RunnableLambda — two different uses

Both files wrap a Python function, but for opposite reasons.

| File | The function returns | What LangChain does |
|---|---|---|
| `03_custom_chain.py` | a **value** (a dict) | uses it as the result |
| `04_router_chain.py` | a **Runnable** (a chain) | invokes it with the original input |

That second one is the subtle bit: `route()` picks a chain and hands it back,
and LCEL then runs it for you. That is why `04` comes after `03`.

```python
# 03 - wrap a function, it runs
custom_chain = RunnableLambda(blog_generation_workflow)

# 04 - return a chain, LCEL invokes it
chain = RunnableLambda(route)
```

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`\|` runs nothing** | It only builds a `RunnableSequence`. Work happens at `.invoke()` |
| **Missing `StrOutputParser()`** | The next prompt receives an `AIMessage` repr instead of text |
| **Prompt variable names must match** | The key in `.invoke({...})` must equal the `{placeholder}` in the template, or `KeyError` |
| **Keyword routing is brittle** | `04`'s `route()` matches substrings — `"non-technical"` contains `"technical"`. Rule out the negative case first, or classify with an LLM |
| **Parallel is not free** | Branches run concurrently but each is still a billed call |

---

## Known issues in these files

| File | Issue |
|---|---|
| `02_parallel_chain.py` | All three prompts are the identical string `"Write a short summary about {topic}"`, so it prints three answers to the same question. Shows the mechanism, not the benefit — give each its own text |
| `03_custom_chain.py` | Prints `print_title("Router Chain")` — copy-pasted from `04` |
