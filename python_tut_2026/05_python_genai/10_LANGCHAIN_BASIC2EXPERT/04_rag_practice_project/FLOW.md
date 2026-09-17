# How One Question Flows Through This App

`README.md` gives the overview. This file **traces a single question end to
end** and shows what the data looks like at every hop — so you can point at any
line in `src/` and say what is in the variable right there.

The example: you uploaded `refund_policy.pdf` and ask **"What is the refund
period?"**

---

## The map

```text
 ┌─────────────────── PHASE 1 · build once ───────────────────┐
 │                                                            │
 │  refund_policy.pdf ─► LOAD ─► SPLIT ─► EMBED ─► STORE      │
 │                      pages    chunks   numbers  FAISS      │
 │                                                  │         │
 └──────────────────────────────────────────────────┼─────────┘
                                                    │ data/vectorstore/
 ┌─────────────────── PHASE 2 · every question ─────┼─────────┐
 │                                                  ▼         │
 │  "What is the refund period?"                              │
 │        │                                                   │
 │        ▼                                                   │
 │     EMBED ─► SEARCH ─► PROMPT ─► GEMINI ─► ANSWER + SOURCES│
 │    numbers   4 chunks  filled     text                     │
 │                        template                            │
 └────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — building the knowledge base

You click **Build Knowledge Base**. `app.py` calls `build_vectorstore()`.

| # | Step | Code | What the variable holds now |
|---|---|---|---|
| 1 | **Save** | `save_uploaded_files()` · `app.py` | `data/documents/refund_policy.pdf` on disk |
| 2 | **Load** | `load_documents()` · `loaders.py` | `[Document, Document, …]` — **one per page**, each with `metadata={"filename": "refund_policy.pdf", "page": 1}` |
| 3 | **Split** | `split_documents()` · `loaders.py` | `[Document × N]` — pieces of ~1000 characters. Each piece **keeps** its page number |
| 4 | **Embed** | `FAISS.from_documents(chunks, embeddings)` · `vectorstore.py` | every chunk becomes `[0.012, -0.034, 0.008, …]` — **3072 numbers** (Gemini) |
| 5 | **Store** | `save_local()` · `vectorstore.py` | `data/vectorstore/index.faiss` (the numbers) + `index.pkl` (the text) |

Two details that matter later:

- **Page numbers are made 1-based** in `loaders.py` (`int(page) + 1`), so the
  citation you see matches what a PDF viewer shows.
- **The text travels with the numbers.** FAISS on its own only knows *"row 7 is
  closest."* The `.pkl` file is what turns row 7 back into readable text.

This phase costs **one embedding API call per chunk**, once. The index sits on
disk until you rebuild or clear it.

---

## Phase 2 — answering a question

You type the question. `app.py` calls `ask_question(question, chat_history)`.

| # | Step | Code | What happens |
|---|---|---|---|
| 1 | **Clean** | `rag_chain.py` | strip whitespace; empty question → `ValueError` |
| 2 | **Load index** | `load_vectorstore()` | read `index.faiss` + `index.pkl` from disk into memory |
| 3 | **Embed the question** | `retriever.invoke()` | `"What is the refund period?"` → 3072 numbers, **same model** as Phase 1 |
| 4 | **Search** | FAISS, `k=4` | the 4 chunks whose numbers sit **closest** to the question's numbers |
| 5 | **Format context** | `format_docs()` | the 4 chunks joined into one text block |
| 6 | **Format history** | `format_chat_history()` | earlier turns as `User: … / Assistant: …`, or `"No previous conversation"` |
| 7 | **Fill the prompt** | `prompt.format()` | `prompts/rag_prompt.txt` with `{context}`, `{chat_history}`, `{question}` filled in |
| 8 | **Ask Gemini** | `llm.invoke(final_prompt)` | one chat call; `.text` is the answer as a plain string |
| 9 | **Collect sources** | `extract_sources()` | `(filename, page)` of each chunk, **de-duplicated**, with a 160-char preview |
| 10 | **Package** | `RAGResponse(...)` · `schemas.py` | `answer` + `sources` + `num_chunks` |
| 11 | **Show** | `app.py` | answer in the chat bubble, sources underneath, everything saved to `st.session_state.messages` |

This phase costs **two API calls**: one to embed the question, one to generate
the answer.

---

## What the model actually sees

Step 7 produces the *only* thing Gemini ever reads. Nothing else — not the PDF,
not the other chunks.

```text
You are a helpful assistant that answers questions using the provided document context.
Rules:
1. Answer using ONLY the information in the Document Context below.
2. Do NOT invent facts that are not supported by the Document Context.
3. If the Document Context does not contain enough information to answer, say:
   "I could not find that information in the provided documents."
4. Use the Conversation History when it helps you understand follow-up questions.
5. Keep your answer clear and concise.

Conversation History: No previous conversation
Document Context:     [chunk 1] …customers may request a full refund within 30 days…
                      [chunk 2] …refunds are processed to the original payment method…
                      [chunk 3] …
                      [chunk 4] …
Question:             What is the refund period?
Answer:
```

Rule 3 is the whole reason this is *retrieval-augmented* and not just *chat*:
if the 4 chunks do not contain the answer, the model is told to say so rather
than guess.

---

## The follow-up question

Now you ask **"Does it apply to international customers?"**

`app.py` passes `st.session_state.messages[:-1]` — every earlier turn, minus the
one you just typed — as `chat_history`. Step 6 turns it into:

```text
Conversation History:
User: What is the refund period?
Assistant: Customers may request a full refund within 30 days.
```

Without that block, *"it"* would mean nothing. Note that history goes into the
**prompt** only — it does **not** change the search. The 4 chunks are still
chosen by the new question alone.

---

## Where the money goes

| When | API calls | Which |
|---|---|---|
| Build, once | N — one per chunk | embedding |
| Each question | 2 | 1 embedding + 1 chat |
| Rebuild | N again | embedding |

Persisting the index is what keeps the left column at *once*.

---

## The one rule that never bends

**The model that embeds the question must be the model that embedded the
chunks.** Numbers from two different models are not comparable — not "less
accurate," but meaningless together. That is why `EMBEDDING_MODEL` is fixed in
`.env` and why switching it means **rebuilding**, never reusing, the index.

---

## Known issue

`src/vectorstore.py:36` defaults `CHUNK_OVERLAP` to **1000** — the same as the
chunk size. Measured: a 4,330-character text splits into **5** chunks with
overlap 150, and **369** with overlap 1000. Every one of those is an embedding
call. Until it is fixed (or `CHUNK_OVERLAP=150` is set in `.env`), builds are
roughly 70× more expensive than intended.
