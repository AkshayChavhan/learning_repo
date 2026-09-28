# 03 — Output Parsers

The third component. A model always returns **text**. A parser turns that text
into something Python can use — a list, a dict, a typed object. This folder is
the climb from *"a string that looks like JSON"* to *"a guaranteed shape."*

---

## The files

Read them in order — each one fixes a weakness of the last.

| File                        | Returns                | Validation | Extra API call |
| --------------------------- | ---------------------- | ---------- | -------------- |
| `01_csv_output_parser.py`   | `list[str]`            | none       | no             |
| `02_json_output_parser.py`  | `dict`                 | none       | no             |
| `03_pydantic_parser.py`     | **typed object**       | ✅ full    | no             |
| `04_output_fixing_parser.py`| typed object, repaired | ✅ + retry | **on failure** |
| `05_structured_output.py`   | dict / typed object    | ✅ by API  | no             |

```text
  01 CSV        "Python, SQL, Go"        →  ['Python','SQL','Go']
       │                                     no keys, no meaning
       ▼
  02 JSON       '{"ram":"16GB"}'         →  {'ram': '16GB'}
       │                                     keys, but no schema
       ▼
  03 Pydantic   '{"experience":5}'       →  Employee(experience=5)
       │                                     schema + validation + dot access
       ▼
  04 Fixing     '{"experience":"5 yrs"}' →  Employee(experience=5)
       │                                     a second LLM call repairs it
       ▼
  05 Structured  (no parsing at all)     →  shape guaranteed by the API
```

---

## The whole module at a glance

```text
            PROMPT SIDE                      REPLY SIDE
                 \                               /
   get_format_instructions()        parser.invoke(reply)
   goes INTO the prompt    \                    /  turns text into an object
                            \                  /
                             ►  OUTPUT PARSER ◄
                            /                  \
        list → dict →      /                    \   OutputParserException
        object → schema   /                      \  OutputFixingParser
                         /                        \
                   PROGRESSION                  FAILURE
```

---

## The two halves everyone confuses

A parser does **two unrelated jobs at two different times**:

```text
   parser.get_format_instructions()          parser.invoke(response)
              │                                        │
              ▼                                        ▼
      goes INTO the prompt                    runs ON the reply
      "please emit this shape"                "turn that text into an object"
              │                                        │
        BEFORE the call                         AFTER the call
```

**Instructions alone change nothing.** `llm.invoke()` still returns an
`AIMessage` whose `.text` is a JSON *string* — no `.name`, no `.department`.
Something has to parse it.

### `.invoke()` is not "call the LLM"

Every component is a `Runnable`; `.invoke()` means *run this thing once*.
Whatever is **before the dot** is what runs:

| Call | Input | Output | Network? |
| ---- | ----- | ------ | -------- |
| `prompt.invoke(dict)` | `dict` | `PromptValue` | **no** — string formatting |
| `llm.invoke(pv)` | `PromptValue` | `AIMessage` | **yes** ← the only one |
| `parser.invoke(msg)` | `AIMessage` | `Employee` | **no** — local parsing |

```text
  dict ──prompt──► PromptValue ──llm──► AIMessage ──parser──► Employee
                                   ▲
                          only this leaves your machine
```

Same three types line up end to end, which is why the whole thing later
collapses to `chain = prompt | llm | parser`.

---

## What `format_instructions` actually costs

Measured with `tiktoken` (`o200k_base`) on the parsers in this folder:

| Parser | `get_format_instructions()` | Tokens | Says |
| ------ | --------------------------- | -----: | ---- |
| `CommaSeparatedListOutputParser` | one sentence | **28** | *"a list of comma separated values, eg: `foo, bar, baz`"* |
| `JsonOutputParser` | one line | **5** | *"Return a JSON object."* |
| `PydanticOutputParser` | full JSON Schema | **240** | the schema, field descriptions and an example |

> **`JsonOutputParser` sends no schema at all** — literally five tokens. That is
> why the keys you get back are whatever the model felt like emitting. The
> `Field(description=...)` text in `03` is what fills those 240 tokens, and it
> is the only reason the model knows to call it `experience` and not `years`.

Pass `JsonOutputParser(pydantic_object=Employee)` and it gains the schema too.

---

## The parsers compared

| | `01` CSV | `02` JSON | `03` Pydantic | `05` structured output |
| --- | --- | --- | --- | --- |
| Returns | `list[str]` | `dict` | `Employee` | `dict` or model |
| Field access | `x[0]` | `x["ram"]` | `x.name` ✅ | `x["rating"]` |
| Keys guaranteed | — | ❌ model's choice | ✅ | ✅ |
| Types validated | ❌ | ❌ | ✅ | ✅ |
| Shape enforced by | the prompt (hope) | the prompt (hope) | the prompt + local check | **the API** |
| Prompt cost | 28 tok | 5 tok | 240 tok | 0 — schema goes out-of-band |
| Use when | a simple list | shape is unknown / dynamic | fields are known | provider supports it — **prefer this** |

---

## When parsing fails

Feed `03`'s parser the malformed output from `04` and it raises — the two
errors are exactly the realistic ones:

```text
OutputParserException: Failed to parse Employee from completion {...}

  experience   Input should be a valid integer   input_value='5 years'
  skills       Input should be a valid list      input_value='Python, SQL'
```

Nearly right, still useless. `OutputFixingParser` wraps the real parser and,
**on failure only**, sends the broken text back to an LLM to repair:

```python
fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
parsed = fixing_parser.invoke(malformed_output)   # Employee(experience=5, ...)
```

| | Happy path | Failure path |
| --- | --- | --- |
| API calls | 0 extra | **1 extra** |
| Latency | unchanged | roughly doubled |

It lives in **`langchain_classic`** (`pip install langchain-classic`), not
`langchain_core`. Treat it as a safety net, not a strategy — if you need it
often, reach for `with_structured_output` instead.

---

## `with_structured_output()` — the modern answer

```python
llm = get_llm().with_structured_output(movie_review_schema)
response = llm.invoke("Review the movie 'Interstellar'.")
response["rating"]        # 8.6
```

No `format_instructions`, no parser, no `.invoke()` on the reply. The schema
travels to the provider **out of band** (as a tool/JSON-schema constraint), so
the shape is enforced by the API rather than requested in the prose and hoped
for.

| You pass | You get back |
| -------- | ------------ |
| a JSON Schema `dict` (file `05`) | a `dict` |
| a Pydantic class | an instance of that class |

| | Parser approach (`01`–`04`) | `with_structured_output` (`05`) |
| --- | --- | --- |
| Where the schema goes | inside the prompt text | out-of-band to the API |
| Shape guaranteed | no — the model may ignore it | **yes** |
| Prompt tokens | up to 240 | none |
| Failure mode | `OutputParserException` | rarely fails |
| Works everywhere | ✅ any model | ❌ provider must support it |

> **It guarantees SHAPE, never TRUTH.** A perfectly valid `MovieReview` can
> still hold an invented rating. Validation is not verification.

---

## Gotchas

| Gotcha | Detail |
| ------ | ------ |
| **Instructions ≠ parsing** | `get_format_instructions()` only *asks*. Without `parser.invoke()` you still hold a string |
| `JsonOutputParser` **sends no schema** | 5 tokens, no field names — you get whatever keys the model picked. Add `pydantic_object=` to fix |
| **The CSV parser is `csv.reader`, not `.split(",")`** | A **quoted** comma survives: `'a, "b, c", d'` → `['a', 'b, c', 'd']`. An **unquoted** one splits — and the model has no reason to quote. That is the real fragility |
| **The CSV parser doesn't strip numbering** | `"1. Python, 2. SQL"` → `['1. Python', '2. SQL']` |
| `OutputFixingParser` **costs a second call** | Only on failure, but it doubles latency when it fires |
| `OutputFixingParser` **is in `langchain_classic`** | Not `langchain_core`. Needs `pip install langchain-classic` |
| **Valid ≠ correct** | Both Pydantic and `with_structured_output` check the *shape*. The values can still be hallucinated |
| **`with_structured_output` isn't universal** | Provider must support tool calling / JSON mode. The parsers are the portable fallback |
