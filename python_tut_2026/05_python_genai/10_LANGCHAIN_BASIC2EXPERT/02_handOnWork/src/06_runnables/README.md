# 06 — Runnables

A **Runnable** is anything with `.invoke()`. That single agreement is what lets
prompts, models, parsers and your own functions snap together with `|`.

This module is the machinery under `04_chains` — same pipe, looked at directly.

---

## The files

Read them in order — each widens what can go in a chain.

| # | File | Class | Adds |
|---|---|---|---|
| 1 | `01_runnable_sequence.py` | `RunnableSequence` | the pipe — steps in order |
| 2 | `02_runnable_lambda.py` | `RunnableLambda` | **your own function** as a step |
| 3 | `03_runnable_parallel.py` | `RunnableParallel` | branches → a **dict** |
| 4 | `04_runnable_branch.py` | `RunnableBranch` | **conditional** — pick a chain |
| 5 | `05_runnable_passthrough.py` | `RunnablePassthrough` | carry the **input forward** |

`02` is the only file that makes **no LLM call** — pure Python, offline, free.

---

## The one interface

Everything below is a Runnable, so everything gets the same three methods:

```text
  PromptTemplate     ['invoke', 'batch', 'stream']
  ChatGroq           ['invoke', 'batch', 'stream']
  StrOutputParser    ['invoke', 'batch', 'stream']
  RunnableLambda     ['invoke', 'batch', 'stream']
  the whole chain    ['invoke', 'batch', 'stream']      ← composes to a Runnable too
```

| Method | Does |
|---|---|
| `.invoke(x)` | run once |
| `.batch([x, y])` | run over many inputs |
| `.stream(x)` | yield tokens as they arrive |

**A chain is itself a Runnable.** That is why chains nest inside chains without
any special syntax — and why `|` builds a `RunnableSequence` you can pipe again.

---

## The five shapes

```text
1. SEQUENCE      2. LAMBDA       3. PARALLEL     4. BRANCH        5. PASSTHROUGH
   in              in               in              in                in
   │               │             ┌──┼──┐           ┌┴┐               ├──────┐
   ▼               ▼             ▼  ▼  ▼        cond? cond?          │      ▼
  step           your fn         a  b  c          ▼     ▼          (kept)  chain
   │               │             └──┼──┘        chainA chainB         │      │
   ▼               ▼                ▼              └──┬──┘           └───┬──┘
  step           result          {dict}              ▼                   ▼
   │                                               result            {in + result}
   ▼
  out
```

| Shape | Use when |
|---|---|
| Sequence | each step needs the previous result |
| Lambda | you need plain Python — reshape, filter, log, call an API |
| Parallel | steps are independent; you want all their results |
| Branch | different inputs need different handling |
| Passthrough | a later step needs the **original input**, not just the last output |

---

## Passthrough — the one that needs explaining

It has two shapes, and file `05` shows both.

**Shape 1 — as a placeholder**, so a chain can take a plain string:

```python
chain = {"query": RunnablePassthrough()} | answer_chain
chain.invoke("What is AI?")
```

Piping it bare does **not** work — `RunnablePassthrough() | llm` hands the model
a raw dict and raises `ValueError: Invalid input type <class 'dict'>`.

**Shape 2 — `.assign()`, which keeps the original keys and adds new ones:**

```python
chain = RunnablePassthrough.assign(answer=answer_chain)
result = chain.invoke({"query": "What is AI?"})
# result has BOTH 'query' and 'answer'
```

Without it, `prompt | llm` returns only the answer and the question is gone.
That is the whole point: it is how a question survives beside its answer.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`\|` builds, it does not run** | The result is a `RunnableSequence`. Nothing happens until `.invoke()` |
| **Branch conditions return a `bool`, not a label** | A lambda returning `"technical"` is not a branch — `RunnableBranch` needs `(condition, runnable)` **tuples**, then one bare default |
| **Branch order matters** | `"non-technical"` **contains** `"technical"`, so a naive substring test routes both the same way, silently. Rule out the negative case first |
| **Bare passthrough into a model fails** | A chat model needs a PromptValue, str or messages — never a dict |
| **Parallel is concurrent, not free** | Wall-clock is the slowest branch, but every branch is still a billed call |

---

## Known issues in these files

| File | Issue |
|---|---|
| `01_runnable_sequence.py` | Imports `RunnableSequence` and never references it — the pipe creates one implicitly. Either drop the import, or print `type(chain).__name__` to make it land |
| `02_runnable_lambda.py` | Builds `llm = get_llm()` and never uses it. Removing it makes the file's best feature explicit: it runs offline and free |
