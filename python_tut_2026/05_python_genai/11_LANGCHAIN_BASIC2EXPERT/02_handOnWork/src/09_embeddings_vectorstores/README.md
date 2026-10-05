# 09 — Embeddings & Vector Stores

An **embedding** turns text into a list of numbers positioned so that texts with
similar *meaning* sit close together. A **vector store** holds those numbers and
finds the nearest ones to a query.

This is what makes search work on **meaning** rather than keywords.

---

## The mental model: pins on a map

Imagine giving every sentence a **pin on a map**. Sentences about similar things
get pinned close together. Sentences about different things get pinned far apart.

```text
              coffee stuff
                   ☕


                                    🔵 "A vector store saves embeddings…"
        🔵 "Python is a           ❓ your question
           programming language"    ↑
                                  closest pin wins

              🔵 "Machine learning…"
```

To answer a question you **pin the question too**, then look at which document
pin is nearest. No word matching at all — just *"what is closest on the map."*

| The analogy | The code |
|---|---|
| the map | the vector store |
| a pin's position | the embedding — 3072 numbers |
| pinning a sentence | `embed_documents(...)` |
| pinning your question | `embed_query(...)` |
| "which pins are nearest?" | `similarity_search(query, k=2)` |

---

## The files

Read them in order. Each column below only ever gains — nothing is introduced
and then taken away.

| # | File | Loader | Splitter | Store | Persists | Body lines |
|---|---|---|---|---|---|---|
| 1 | `01_embeddings.py` | – | – | – | – | 8 |
| 2 | `02_similarity_search.py` | – | – | FAISS | – | 23 |
| 3 | `03_faiss_vectorstore.py` | ✅ | ✅ | FAISS | – | 27 |
| 4 | `04_chroma_vectorstore.py` | ✅ | ✅ | Chroma | ✅ | 31 |

```text
1  text ──► vector                    what an embedding IS
2         vector ──► nearest          what SEARCH is (4 hand-written docs)
3  file ──► chunks ──► vectors ──►    the real pipeline, in memory
4                              ──►    …and persisted to disk
```

---

## 1 — What an embedding actually is

```python
vector = embeddings.embed_query("refund policy")
```

```text
  returns   : list of 3072 floats
  first 3   : [-0.0261, 0.0095, 0.011]
```

Just numbers. The magic is only in *where* they sit:

```text
  "refund policy"  vs  "how do I get my money back"   →  0.671
  "refund policy"  vs  "the server is down"           →  0.574
```

**Zero shared keywords** with the first pair, yet it scores higher. That gap is
the entire basis of semantic search.

| Method | Use for |
|---|---|
| `embed_query(str)` | one string — the user's question |
| `embed_documents([str])` | many strings — your chunks |

---

## 2 — What search actually is

Four steps, and the first two build the map while the last two search it:

```text
 1. Here are 4 sentences          →  DOCUMENTS = [...]
         │
 2. Put a pin on the map for each →  FAISS.from_documents(...)
         │
 3. Here's my question,              query = "How do I store and
    pin that too                              look up text by meaning?"
         │
 4. Which 2 pins are nearest?     →  similarity_search(query, k=2)
```

`02` uses **four hand-written Documents** instead of a loaded file, on purpose:
you can see which one *should* win before you run it.

```python
results = vector_store.similarity_search(query, k=2)                 # documents
scored  = vector_store.similarity_search_with_score(query, k=2)      # + distance
```

`_with_score` is the one worth meeting here — it tells you **how close** a match
is, which is the only way to drop weak hits.

> **Score direction is store-specific.** FAISS returns **L2 distance**, where
> **lower is closer**. Chroma and others may return a similarity where **higher**
> is better. Check which you have before filtering on a threshold, or you will
> keep exactly the wrong results.

There is **no relevance floor**. Ask for `k=2` and you get 2 documents whenever
the store holds that many, however poor the match. Relevance is judged by the
score, never by presence in the result list.

---

## 3 → 4 — FAISS vs Chroma

Same `from_documents()` interface, same `similarity_search()`. The difference is
**durability**.

| | FAISS (`03`) | Chroma (`04`) |
|---|---|---|
| Lives in | RAM | a directory on disk |
| Survives the process | ❌ gone at exit | ✅ 1.6 MB written |
| Extra code needed | none | `persist_directory`, wiping the old index |
| Good for | speed, throwaway indexes | durability, metadata filtering |

### Are the pins saved anywhere?

In `02` and `03`, **no** — the map is drawn in RAM and thrown away at exit.

```text
   4 sentences ──► API calls ──► pins in RAM ──► search ──► print
                                      │
                                 script exits
                                      │
                                      ▼
                                  🗑️  gone
```

| File | Store | Where the pins live | Survives exit? |
|---|---|---|---|
| `02` | FAISS | RAM | ❌ |
| `03` | FAISS | RAM | ❌ |
| `04` | **Chroma** | `data/chroma_db/` | ✅ |

`04` writes a real database — 1.6 MB currently on disk:

```text
data/chroma_db/
├── chroma.sqlite3                      432 KB  ← the text, metadata, ids
└── 42b10898-…/
    ├── data_level0.bin                         ← the actual vectors
    ├── header.bin
    ├── length.bin
    └── link_lists.bin                          ← the nearest-neighbour graph
```

One keyword is the whole difference:

```python
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(chroma_db_path),   # ← drop this and Chroma is RAM-only too
)
```

**FAISS is not incapable of persisting** — `02` and `03` simply do not ask. It has
`save_local()` / `load_local()`. In-memory is a choice here, not a limitation.

### Why it matters beyond convenience

Embedding is the **expensive** step — one API call per chunk. Four hand-written
sentences cost nothing, but a 500-page PDF split into 2,000 chunks is 2,000
calls. Persist the index and you pay that **once**; skip it and you pay on
**every run**.

`04` deliberately wipes its directory with `shutil.rmtree` before rebuilding —
see the gotcha below for why that is not optional.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **An index is only valid for the model that built it** | Gemini is 3072 dimensions, OpenAI's `text-embedding-3-small` is 1536. Reusing a directory after switching models gives **meaningless scores, not an error** — always rebuild |
| **`text-embedding-004` is 404 on this account** | Only `gemini-embedding-001` / `-2` / `-2-preview` are served. Check with `curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GOOGLE_API_KEY"` |
| **OpenAI returns 429 `credit_balance_exhausted`** | Every file here runs on Gemini; the OpenAI lines are commented alternatives |
| **Score direction differs per store** | FAISS: lower is closer. Others: higher may be better |
| **`k` has no quality threshold** | The store returns `k` results regardless of how bad they are |
| **`faiss-cpu` needs an exact pin** | `==1.10.0`. Newer versions ship no arm64 wheel for Python 3.11 and building from source needs swig/cmake |
| **Generated indexes are gitignored** | `data/chroma_db/` is rebuilt on every run — never versioned |

---

## Where this goes next

A vector store gives you `similarity_search()`. Module 10 wraps it in
`as_retriever()`, which turns it into a Runnable that pipes into a chain — and
adds smarter strategies (MMR, multi-query, compression) on top of the same
index.
