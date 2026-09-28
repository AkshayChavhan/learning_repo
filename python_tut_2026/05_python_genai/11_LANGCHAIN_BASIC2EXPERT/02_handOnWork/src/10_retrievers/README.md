# 10 — Retrievers

A **retriever** takes a query string and returns Documents. Module 09 could
already do that with `similarity_search()`. The gain here is **composability,
not capability** — a retriever is a Runnable, so it pipes into a chain and can
be swapped for a smarter strategy without touching the code around it.

---

## The files

File 1 is the baseline. Each of the other four fixes a different failure mode of
plain similarity search — at a different point in the pipeline.

| # | File | Fixes | Changes | Extra LLM calls |
|---|---|---|---|---|
| 1 | `01_vector_retriever.py` | — the **baseline** | — | 0 |
| 2 | `02_mmr_retriever.py` | top-k are near-duplicates | the **search** | 0 |
| 3 | `03_multi_query_retriever.py` | one phrasing misses differently-worded chunks | the **query** | 1 |
| 4 | `04_contextual_compression.py` | a relevant chunk is mostly padding | the **results** | **k** |
| 5 | `05_parent_document_retriever.py` | small embeds precisely / large carries context | the **index** | 0 |

```text
        your question
             │
             ▼
  ┌─────────────────────────────────────────┐
  │ 3  MultiQuery — rewrite it 3 ways       │  ← BEFORE retrieval
  └─────────────────────────────────────────┘
             │
             ▼
  ┌─────────────────────────────────────────┐
  │ 1  the vector store       (k nearest)   │
  │ 2  MMR — fetch_k, then pick k diverse   │  ← DURING retrieval
  └─────────────────────────────────────────┘
             │        ▲
             │        └── 5  ParentDocument: match SMALL, return LARGE
             ▼                                 (changes how you INDEX)
  ┌─────────────────────────────────────────┐
  │ 4  Compression — trim each hit          │  ← AFTER retrieval
  └─────────────────────────────────────────┘
             │
             ▼
         documents
```

Cost is **not** monotonic: ParentDocument is the most involved to set up yet
adds no runtime LLM cost. The order above is by *what it changes*, not by price.

---

## The flow of `01_vector_retriever.py`

Every file in this folder repeats this same load → split → embed → store
preamble. Learn it once here.

```text
  data/input/sample.txt                          1 file
         │  TextLoader.load()
         ▼
  [Document]                                     1 Document
         │  RecursiveCharacterTextSplitter(200, 50)
         ▼
  [Document × 16]                                16 chunks
         │  FAISS.from_documents(chunks, embeddings)      💰 16 API calls
         ▼
  ┌──────────────────┬────────────────────┐
  │ index: 16×3072   │ docstore: 16 texts │      the map + the labels
  └──────────────────┴────────────────────┘
         │  .as_retriever(search_kwargs={"k": 2})         free — just a wrapper
         ▼
  retriever
         │  .invoke("What are large language model ?")    💰 1 API call
         ▼
  [Document × 2]
```

| Line | Code | In | Out | API |
|---|---|---|---|---|
| 43–44 | `TextLoader(...).load()` | a file path | `[Document]` × 1 | 0 |
| 46–50 | `splitter.split_documents(...)` | `[Document]` × 1 | **`[Document]` × 16** | 0 |
| 55 | `GoogleGenerativeAIEmbeddings(...)` | a model name | an embedder **client** | 0 |
| 66 | `FAISS.from_documents(chunks, embeddings)` | 16 chunks + client | a vector store | **16** |
| 73 | `vector_store.as_retriever(k=2)` | the store | a retriever | 0 |
| 81 | `retriever.invoke(query)` | a string | **`[Document]` × 2** | **1** |

### What `FAISS.from_documents()` actually builds

Three things, not one — and the third is the one people miss.

```text
  ┌─────────────────────┬──────────────────────────────────────┐
  │  THE INDEX          │  THE DOCSTORE                        │
  │  (numbers only)     │  (the original text)                 │
  ├─────────────────────┼──────────────────────────────────────┤
  │ row 0  [−0.02, …]   │  4589cb4c…  "What is AI?"            │
  │ row 1  [ 0.11, …]   │  fff52895…  "Artificial Intelligence…"│
  └─────────────────────┴──────────────────────────────────────┘
              └──── index_to_docstore_id links them ────┘
```

FAISS alone is pure maths — it answers *"row 1 is closest"*, which is useless on
its own. The docstore is what turns a row number back into text, and it is why
`.invoke()` hands you Documents rather than floats.

Verified: `IndexFlatL2`, 16 vectors, 3072 dimensions, 16 documents kept.

---

## All five compared

The one table to re-read before an interview.

| | `01` Vector | `02` MMR | `03` MultiQuery | `04` Compression | `05` ParentDocument |
|---|---|---|---|---|---|
| **Idea** | k nearest | k nearest, but **diverse** | ask the question **several ways** | **trim** each hit | match **small**, return **large** |
| **Fixes** | — baseline | near-duplicate hits | one phrasing misses a chunk | hits padded with irrelevant text | small embeds well / large reads well |
| **Intervenes** | — | during search | before search | after search | at index time |
| **Extra LLM calls** | 0 | 0 | **1** | **k** (one per doc) | 0 |
| **Needs a chat model** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **Docs returned** | exactly `k` | exactly `k` | **more** than `k` | **`k` or fewer** | ≤ `k` parents |
| **Content returned** | the chunk | the chunk | the chunk | a **shortened** chunk | the **parent**, bigger than indexed |
| **Key parameter** | `k` | `fetch_k`, `lambda_mult` | `include_original` | the compressor | two splitters |
| **Setup effort** | trivial | one kwarg | easy | easy | **highest** |
| **Use when** | the default | results repeat themselves | wording varies a lot | context window is tight | chunks are too small to answer from |

### The line that makes each one

```python
# 01  baseline
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 02  diversity — fetch_k MUST exceed k
retriever = vector_store.as_retriever(
    search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})

# 03  rewrite the question (needs a chat model)
retriever = MultiQueryRetriever.from_llm(
    retriever=base, llm=get_llm(), include_original=True)

# 04  trim the hits (one LLM call per document)
retriever = ContextualCompressionRetriever(
    base_retriever=base, base_compressor=LLMChainExtractor.from_llm(get_llm()))

# 05  index small, return large (two splitters, two stores)
retriever = ParentDocumentRetriever(
    vectorstore=empty_store, docstore=InMemoryStore(),
    child_splitter=child, parent_splitter=parent)
```

Every one of them answers `.invoke(query)` with a list of Documents, so the
chain downstream never knows which is plugged in. **That** is the point of
module 10.

Notes worth carrying:

- `fetch_k` **must** exceed `k`, or MMR has nothing to choose between and
  degrades to plain similarity search. `lambda_mult` (default `0.5`) sets the
  balance — `1.0` is pure relevance, `0.0` is maximum diversity.
- MultiQuery returns **more than `k`**: `k` applies per sub-query, before
  deduplication.
- Compression can return **fewer** documents than the base retriever — a chunk
  with nothing relevant is dropped entirely, not returned empty.
- `04` deliberately uses `k=4` where the others use `k=2`, so there is something
  to trim, and prints a before/after character count.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`k` has no relevance floor** | The store returns `k` documents whenever it holds that many, however poor the match. Judge by score, never by presence in the list |
| **`search_kwargs` is a dict** | `{"k": 2}` with a colon. `{"k"=2}` is a `SyntaxError` |
| **Use `.invoke()`, not `.get_relevant_documents()`** | The latter still works but is deprecated |
| **Third-party imports go BELOW `_bootstrap`** | Above it they run before the re-exec fires, so the wrong interpreter dies on the import instead of being switched |
| **`from_llm`, with an underscore** | `from.llm` is attribute access on a method that does not exist |
| **Compression costs one call PER document** | `k=4` means five requests to answer one question |
| **ParentDocument needs an EMPTY vector store** | FAISS needs one vector to size its index, so `05` seeds a `"dummy"` then deletes it. Call `add_documents()` on the **retriever**, never `from_documents()` on the store |
| **ParentDocument's parents are not persisted** | Its `InMemoryStore` vanishes at exit — saving the vectors is not enough |
| **Every file re-embeds from scratch** | FAISS lives in RAM here, so all 16 embeddings are regenerated on every run |

---

## Where this goes next

A retriever is the *R* in RAG. Module 11 adds tool calling, and `12_projects`
puts retrieval and generation together into an application.
