# 02 — Prompts

The second component. A **prompt template** turns a prompt into a reusable
function: write it once with `{placeholders}`, then `.invoke()` it with
different values. Everything in this folder is either **how to build** that
object or **what to write inside** it.

---

## The files

Read them in this order — the numbering is the reading order.

| File                        | Adds                                                  | Track     |
| --------------------------- | ----------------------------------------------------- | --------- |
| `01_prompt_template.py`     | `PromptTemplate` — one text block with `{vars}`       | mechanics |
| `02_chat_prompt_template.py`| `ChatPromptTemplate` — a **list of role-tagged messages** | mechanics |
| `03_partial_prompt.py`      | `.partial()` — fill some variables early              | mechanics |
| `04_one_shot_prompt.py`     | one worked example                                    | technique |
| `05_few_shot_prompt.py`     | several examples across categories                    | technique |
| `06_chain_of_thought.py`    | reason step by step instead of answering              | technique |
| `07_messages_placeholder.py`| `MessagesPlaceholder` — a slot for conversation history | mechanics |

```text
   MECHANICS (how to build it)          TECHNIQUES (what goes inside)

   01 PromptTemplate ─────────┐
        │  {placeholders}     │
        ▼                     │
   02 ChatPromptTemplate ─────┼────────► 04 one-shot   (1 example)
        │  roles              │                │
        ▼                     │                ▼
   03 .partial()              │          05 few-shot   (N examples)
        │                     │                │
        │                     │                ▼
        │                     │          06 chain-of-thought (no examples)
        ▼                     │                │
   07 MessagesPlaceholder ◄───┴────────────────┘
        └──► the bridge to memory & chains (next module)
```

`07` looks like mechanics but reads best last: it is the only file needing real
`Message` objects and a conversation to exist at all.

---

## The whole module at a glance

```text
              MECHANICS                     TECHNIQUES
                  \                             /
   PromptTemplate ─\        zero / one / few-shot
   ChatPromptTemplate\              chain-of-thought
   .partial()         \                    /
   MessagesPlaceholder \                  /
                        \                /
                         ►   PROMPTS   ◄
                        /                \
        system, human   /                 \  repeated vs growing
        ai, placeholder/                   \ input-heavy vs output-heavy
                      /                     \
                    ROLES                   COST
```

---

## PromptTemplate vs ChatPromptTemplate

|                | `PromptTemplate`          | `ChatPromptTemplate`                |
| -------------- | ------------------------- | ----------------------------------- |
| Produces       | one block of text         | a **list of messages** with roles   |
| Read result by | `prompt.text`             | `prompt.messages` (loop over it)    |
| Use for        | plain completion          | anything conversational — the default today |

> **Never prefix a template with `f`.** The braces belong to LangChain, not to
> Python. An f-string is interpolated at import time and raises `NameError` for
> variables it cannot see.

---

## Roles

Only the tuple form `("role", "template")` is templated. Verified against
`langchain-core 1.6.1`:

| String        | Becomes                       | `.type` after invoke | Use for                   |
| ------------- | ----------------------------- | -------------------- | ------------------------- |
| `"system"`    | `SystemMessagePromptTemplate` | `system`             | persona, rules, format    |
| `"human"`     | `HumanMessagePromptTemplate`  | `human`              | the user's turn           |
| `"user"`      | ↑ **alias of `human`**        | `human`              | same thing, OpenAI habit  |
| `"ai"`        | `AIMessagePromptTemplate`     | `ai`                 | seed the reply, fake turns|
| `"assistant"` | ↑ **alias of `ai`**           | `ai`                 | same thing, OpenAI habit  |
| `"placeholder"`| `MessagesPlaceholder`        | *(expands to a list)*| a history slot            |

**Four real roles, two aliases.** Anything else raises immediately:

```text
ValueError: Unexpected message type: developer.
Use one of 'human', 'user', 'ai', 'assistant', or 'system'.
```

So `"tool"`, `"function"`, `"developer"`, `"bot"` are **not** valid tuple roles.
`tool` still works — as an object:

```python
ChatPromptTemplate.from_messages([
    SystemMessage(content="fixed text"),           # object: NOT templated
    ToolMessage(content="42", tool_call_id="c1"),  # .type == "tool"
    ("human", "{q}"),                              # tuple: {q} IS templated
])
```

| Form                     | `{vars}` filled? | Use for                       |
| ------------------------ | ---------------- | ----------------------------- |
| `("human", "…{topic}…")` | ✅               | almost always                 |
| `HumanMessage(content=…)`| ❌ literal       | fixed text, or history you built |
| `"just a string"`        | ✅               | shorthand — becomes **`human`** |

---

## Variables — all of them, or it fails

Every variable in the template must be filled. The only question is **when**.

```text
   template: {domain} {topic} {word_limit}      you supply: {topic} {word_limit}
                              │
                              ▼
        KeyError: Input to PromptTemplate is missing variables {'domain'}
        raised LOCALLY — the LLM is never called, no tokens spent
```

| Situation                        | Do this                                       |
| -------------------------------- | --------------------------------------------- |
| all values known at call time    | `invoke({domain, topic, word_limit})`         |
| one fixed at **setup**           | `.partial(domain="GenAI")` → `invoke({topic, word_limit})` |
| one **computed** per call        | `.partial(today=lambda: date.today().isoformat())` |
| you want a literal brace         | escape it: `{{domain}}`                       |

### What `.partial()` moves

|                | `.input_variables`               | `.partial_variables`  |
| -------------- | -------------------------------- | --------------------- |
| original       | `['domain','topic','word_limit']`| `{}`                  |
| after `.partial(domain=…)` | `['topic','word_limit']` | `{'domain':'GenAI'}` |

It doesn't render anything — it moves a variable from *"you must supply"* to
*"already supplied"* and returns a **new** template. The original is untouched.
Its main real-world use is `format_instructions` from an output parser.

---

## Techniques

| Technique       | You provide        | Teaches                    | Expensive side |
| --------------- | ------------------ | -------------------------- | -------------- |
| **zero-shot**   | just the task      | nothing — relies on training | neither      |
| **one-shot**    | 1 worked example   | the output **format**      | input          |
| **few-shot**    | N worked examples  | the **decision boundary**  | input          |
| **chain-of-thought** | "think step by step" | *how* to reach the answer | **output** |

```text
FEW-SHOT                              CHAIN-OF-THOUGHT

 INPUT  ████████████ examples          INPUT  ██ question
        ██ question                           ██ "step by step"
          │                                     │
          ▼                                     ▼
 OUTPUT ██ "Feature Request"           OUTPUT ████████████ reasoning
        short, format-locked                  ██ "Approved"
```

Few-shot examples show the **answer only**, never the working — which is why
they fix formatting but not multi-step logic. That is exactly what CoT adds.

### They combine — it's a 2×2

|                     | **No examples**            | **With examples**            |
| ------------------- | -------------------------- | ---------------------------- |
| **Answer directly** | zero-shot (`01`–`03`)      | one-shot (`04`), few-shot (`05`) |
| **Show reasoning**  | **zero-shot CoT (`06`)**   | few-shot CoT *(not in this folder)* |

Few-shot CoT = examples that contain their own reasoning. Strongest and most
expensive: you pay on **both** sides.

---

## Cost — repeated is not the same as growing

LLMs are **stateless**. Every message is re-sent on every call; nothing is
remembered server-side. But that produces two different bills:

```text
FILE 05  (independent tasks)          FILE 07  (one conversation)

 [sys + examples][ticket 1]            [sys][Q1]
 [sys + examples][ticket 2]            [sys][Q1 A1][Q2]
 [sys + examples][ticket 3]            [sys][Q1 A1][Q2 A2][Q3]
  └── same width every call ──┘         └───── widens every turn ─────┘

      REPEATED, flat per call                  GROWING
```

|                | Repeated (`05`)                   | Growing (`07`)                     |
| -------------- | --------------------------------- | ---------------------------------- |
| What changes   | the ticket is **replaced**        | the turn is **appended**            |
| Model's answer | thrown away                       | **fed back in**                     |
| Prompt size    | constant                          | grows every turn                    |
| Fix            | fewer examples, prompt caching    | trim or summarise history           |

**The question that decides which you get:** *does turn N need to know what
happened in turn N−1?* Ticket 4 doesn't care how ticket 3 was classified →
flat. *"Summarise both concepts"* is meaningless without the earlier turns →
grows.

Measured on `05_few_shot_prompt.py` (`tiktoken`, `o200k_base`):

| Part                       | Tokens | Share | Re-sent? |
| -------------------------- | -----: | ----: | -------- |
| system (categories, rules) |     61 |  35%  | ✅ every call |
| the 3 worked examples      |     89 |**51%**| ✅ every call |
| the actual ticket          |     25 |  14%  | new each call |
| **total**                  |**175** |       |          |

**86% of every request is boilerplate.** The model never *learns* the examples —
they work only because they are physically present in the context each time.

---

## MessagesPlaceholder

Reserves a slot that a **list of messages** is dropped into at invoke time.
This is how conversation history reaches a prompt with roles intact, instead of
being flattened into a string.

```python
ChatPromptTemplate.from_messages([
    ("system", "You are a helpful tutor."),
    MessagesPlaceholder(variable_name="chat_history"),   # ← a list goes here
    ("human", "{question}"),
])
```

Two spellings, **same class, different default**:

| Written as                                          | `optional` | Omitting the key at invoke |
| --------------------------------------------------- | ---------- | -------------------------- |
| `MessagesPlaceholder(variable_name="chat_history")` | `False`    | **`KeyError`**             |
| `("placeholder", "{chat_history}")`                 | `True`     | silently inserts nothing   |

Use the explicit form for a real chat loop (history is required); the shorthand
for a first turn where there is no history yet.

---

## Gotchas

| Gotcha                                              | Detail                                                                    |
| --------------------------------------------------- | ------------------------------------------------------------------------- |
| **Never `f"""…{var}…"""`**                          | LangChain owns the braces. An f-string interpolates at import → `NameError` |
| `input_variables=[...]` **is decorative**           | LangChain re-derives it from the template and overwrites what you declared. You **cannot** dodge a `KeyError` by omitting a name. `PromptTemplate.from_template(T)` is equivalent and can't drift |
| **Extra keys are ignored silently**                 | A typo gives `KeyError: word_limit` (missing), never "unknown key `word_limt`" |
| **A bare string is a `human` message**              | `from_messages(["hi {x}"])` → `HumanMessagePromptTemplate`                |
| **Few-shot examples are not messages**              | In `05` all three live inside **one** human string — the prompt has only 2 messages. They look like a dialogue; nothing accumulates |
| **CoT + tight `max_tokens`**                        | Reasoning shares the budget with the answer — a low cap truncates before the decision, or returns an empty `.text` |
| **Adjacent string literals don't add a space**      | `"…support"` `"dark mode…"` → `"supportdark mode"`. Present in `05` and `07` |
