# 08 — Text Splitters

A splitter cuts loaded documents into **chunks** small enough to embed and
retrieve. One `Document` in, many out.

Chunk size is a trade-off, not a setting to get "right":

```text
   too small                     too large
      │                              │
  precise vector,              rich context,
  no context                   vague vector
      │                              │
      └────────── overlap ───────────┘
             keeps a sentence that
          straddles a boundary intact
```

---

## The files

Read them in order. Files 1–3 are a **controlled experiment** — same file, same
loader, same call. Only the splitter changes.

| # | File | Splits on | Result on `sample.txt` |
|---|---|---|---|
| 1 | `01_character_splitter.py` | **one** fixed separator `"\n"` | 12 chunks, 59–195 chars |
| 2 | `02_recursive_splitter.py` | a **list** of separators, with fallback | 16 chunks, 11–185 chars |
| 3 | `03_token_splitter.py` | **tokens**, not characters | 11 chunks, 161–265 chars |
| 4 | `04_markdown_splitter.py` | **document structure** | 12 chunks + header metadata |

Same input, same `chunk_size=200` for 1–2 — the counts differ because the
splitting strategy does.

---

## 1 → 2: why recursive exists

`CharacterTextSplitter` splits on **one** separator and accepts whatever falls
out. If that separator is not in the text, it cannot split at all.

Measured on a 599-character line containing no `\n`, with `chunk_size=200`:

```text
  CharacterTextSplitter    1 chunk  of 599 chars   ← chunk_size ignored, NO warning
  RecursiveCharacter...    4 chunks of 199,199,199,149
```

That is the whole argument for recursive. It walks a separator list —
paragraph → line → word → character — and only falls to the next when a piece
is still too big. It **always** honours `chunk_size`.

Use `CharacterTextSplitter` only when the input has reliable structure to split
on. Use recursive as the default.

---

## 2 → 3: characters vs tokens

`TokenTextSplitter` changes the **unit**, not the strategy.

| | Bounded by | Character length |
|---|---|---|
| Character / Recursive | characters | fixed |
| Token | tokens | **varies — 161 to 265 here** |

That variation is the point, not a defect. Context windows, pricing and
`max_tokens` are all measured in tokens, so a token-bounded chunk is the one
that actually fits a budget. A 200-character chunk might be 40 tokens or 90.

---

## 3 → 4: size vs structure

`MarkdownHeaderTextSplitter` is the only one that **keeps** structure instead of
discarding it, and it breaks the pattern of the first three on every axis:

| | Files 1–3 | `04_markdown_splitter.py` |
|---|---|---|
| API | `split_documents(documents)` | `split_text(string)` |
| Input | `sample.txt` via `TextLoader` | `langchain_notes.md` via `open()` |
| Cuts on | length | header levels `#` `##` `###` |
| Output | plain chunks | chunks **+ header metadata** |

```python
{'h1': 'LangChain Notes', 'h2': 'Core Components', 'h3': 'Models'}
```

That header trail rides along into the vector store, so a chunk retrieved later
still knows which section it came from — context an answer needs to stay
grounded. It is the bridge into module 09.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`CharacterTextSplitter` can ignore `chunk_size`** | Oversized pieces are emitted as-is. It logs `Created a chunk of size N, which is longer than the specified M` — **except when the separator is absent entirely**, where the first piece escapes the check and it is completely silent |
| **Overlap is duplication** | `chunk_overlap=50` means 50 characters appear in two chunks. More chunks, more tokens embedded, more storage |
| **Overlap must be smaller than chunk size** | Otherwise chunks repeat more than they advance |
| **Markdown uses a different method** | `split_text()` on a **string**, not `split_documents()` on Documents — passing Documents raises |
| **`strip_headers=True` is the default** | The `### Models` line is removed from `page_content` and lives only in metadata |
| **Chunks are recomputed, never stored** | Change the splitter and the vector index must be rebuilt, not reused |

---

## The one case that is silent

`01_character_splitter.py`'s Concept Summary says an oversized chunk is emitted
"with a warning". That is **correct for the normal case** — verified:

| Input | Chunks | Warning |
|---|---|---|
| separator absent (1 piece) | 1 × 299 | **none** |
| separator present, 2 oversized pieces | 2 × 299 | ⚠️ once |
| separator present, 3 oversized pieces | 3 × 299 | ⚠️ twice |

The warning (`base.py:168`) sits inside the merge loop and is guarded by
`total > chunk_size`. On the **first** piece `total` is still `0`, so a lone
oversized piece slips through unreported. It is a `logging` record, not
`warnings.warn` — so it also vanishes if logging is reconfigured.
