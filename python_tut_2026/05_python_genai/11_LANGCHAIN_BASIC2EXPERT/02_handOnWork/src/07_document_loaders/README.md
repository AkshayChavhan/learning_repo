# 07 — Document Loaders

The entry point to RAG. A loader reads **something** — a file, a folder, a URL —
and returns a list of **`Document`** objects. Every loader returns that same
shape, so nothing downstream cares where the text came from.

---

## The files

| # | File | 1 source → | Loaded here | Metadata keys |
|---|---|---|---|---|
| 1 | `01_text_loader.py` | **1 Document** | 1 | `source` |
| 2 | `02_pdf_loader.py` | **1 per PAGE** | 2 | `source`, `page`, `total_pages`, +5 |
| 3 | `03_csv_loader.py` | **1 per ROW** | 18 | `source`, `row` |
| 4 | `04_web_loader.py` | 1 per URL — **no file** | 1 | `source`, `title`, … |
| 5 | `05_directory_loader.py` | **1 per matched file** | 4 | `source` |

Counts are real, measured against `data/input/`.

```text
  1 TextLoader      sample.txt      →  ▉                  the Document shape
        │                                                  page_content + metadata
        ▼
  2 PyPDFLoader     sample.pdf      →  ▉▉                 finer: 1 per page
        │                                                  + page / total_pages
        ▼
  3 CSVLoader       employees.csv   →  ▉▉▉▉▉▉▉▉▉▉…        finest: 1 per row (18)
        │                                                  + row
        ▼
  4 WebBaseLoader   https://…       →  ▉                  source is the NETWORK
        │                                                  new failure modes
        ▼
  5 DirectoryLoader data/input/**   →  ▉▉▉▉               fan-out over loader 1
                                                           loader_cls=TextLoader
```

Files 1–3 change **granularity**. File 4 changes **where the bytes come from**.
File 5 is not a loader at all — it takes another loader as an argument, so it
has to come last.

---

## The one shape

```python
documents = loader.load()        # ALWAYS a list, even for one document
documents[0].page_content        # the text  (str)
documents[0].metadata            # where it came from  (dict)
```

`.load()` returns a **list** every time. That uniformity is the whole point: a
splitter or vector store accepts the output of any loader without knowing which
one produced it.

```text
   TextLoader  ─┐
   PyPDFLoader ─┤
   CSVLoader   ─┼──►  list[Document]  ──►  splitter  ──►  vector store
   WebLoader   ─┤
   DirLoader   ─┘
```

Only `len()` varies by loader — 1, 2, 18, 4 above from the same call.

---

## Metadata is not decoration

It is the reason a RAG answer can cite its source.

| Key | Set by | Makes possible |
|---|---|---|
| `source` | every loader | *"from `employees.csv`"* |
| `page`, `total_pages` | `PyPDFLoader` | *"page 3 of 12"* |
| `row` | `CSVLoader` | *"row 7"* |
| `title` | `WebBaseLoader` | the page name, not just the URL |

A chunk retrieved three modules from now carries this dict with it unchanged.
Drop the metadata at load time and the citation is gone for good.

---

## Granularity decides what happens next

| Loader output | Typical size | Feed to a splitter? |
|---|---|---|
| a whole `.txt` file | large | **yes** |
| one PDF page | medium | usually |
| one CSV row | tiny | **no** — it is already a unit |
| one web page | large, noisy | yes, after cleaning |

This is the bridge to `08_text_splitters`: a page usually needs splitting, a row
almost never does.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **A 404 does not raise** | `WebBaseLoader` returns a Document with **empty** `page_content` on an error status — a dead link looks exactly like a success. `04` guards with an explicit emptiness check; copy that pattern |
| **`USER_AGENT` is read at IMPORT time** | Set it *before* `from langchain_community.document_loaders import WebBaseLoader`, not before `.load()` |
| **`DirectoryLoader` counts files, not content** | Empty files count as successes. Check character counts, not the document total |
| **The glob is literal** | `"**/*.txt"` skips `.md`, `.csv`, everything else — silently. Four of the six text-ish files in `data/input/` load |
| **A scanned PDF yields nothing** | `PyPDFLoader` needs a real text layer; an image-only PDF gives empty `page_content` and needs OCR |
| **`CSVLoader` renders rows as `column: value` lines** | Not raw CSV — which is why quoted fields matter |
| **These live in `langchain_community`** | Not `langchain_core`, not `langchain` |

---

## Known issues in these files

| File | Issue |
|---|---|
| `01_text_loader.py` | The comment says a Document "has exactly two parts", but the printout beside it uses `model_dump()`, which lists four — `id` and `type` as well. True for the parts that matter; the two lines disagree on their face |
| `05_directory_loader.py` | Loads 4 documents from a folder of 6 text-ish files. Correct behaviour, but the count alone doesn't reveal that `langchain_notes.md` was skipped |
