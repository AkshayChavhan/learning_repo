# Chat with RAG — setup

Commands to get this folder running, in order.

---

## 1. Start the vector database

```bash
docker compose -f docker-composer.yml up -d
```

> **Pass `-f`.** The file is named `docker-composer.yml` (with an *r*). Docker only
> auto-discovers `compose.yaml`, `compose.yml`, `docker-compose.yaml` and
> `docker-compose.yml` — so a bare `docker compose up` will not find it.

Qdrant then runs on port **6333**:

| URL | What |
|---|---|
| http://localhost:6333/dashboard | Web dashboard |
| http://localhost:6333/collections | Collections, as JSON |

Stop it later with `docker compose -f docker-composer.yml down`.

---

## 2. Create the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

You are in the venv when your prompt starts with `(venv)`. Leave it with `deactivate`.

---

## 3. Install dependencies

```bash
pip install -qU langchain-community pypdf langchain-openai langchain-qdrant
```

| Package | Gives you |
|---|---|
| `langchain-community` + `pypdf` | `PyPDFLoader` — read the PDF |
| `langchain-openai` | `OpenAIEmbeddings` — turn chunks into vectors |
| `langchain-qdrant` | `QdrantVectorStore` — store and search them |

`RecursiveCharacterTextSplitter` needs nothing extra — it ships inside `langchain-core`.

| Flag | Means |
|---|---|
| `-q` | quiet — hide the download spam |
| `-U` | upgrade if already installed |

### Save what you installed

```bash
pip freeze > requirements.txt
```

Rebuild that exact environment later — on another machine, or after deleting `venv/`:

```bash
pip install -r requirements.txt
```

> Run `pip freeze` **inside the activated venv**. Against system python it dumps every
> package on the machine. It also writes every transitive dependency you never asked for —
> **61 lines here, not 4** — each pinned with `==`.

---

## 4. Set your OpenAI key

Embedding calls OpenAI, so this step costs money — a fraction of a cent for these 24 chunks,
but a real bill.

```bash
export OPENAI_API_KEY="sk-..."
```

Without it `index.py` stops after chunking and tells you so.

---

## 5. Run

```bash
python3 index.py
```

```text
loaded 12 pages from sample.pdf
split into 24 chunks (size 1000, overlap 200)
chunk sizes: smallest 78, largest 1000, average 833

stored 24 chunks in Qdrant collection 'rag_sample'
  browse them at http://localhost:6333/dashboard

search: 'What problem does RAG solve?'
  1. page 0 - The problem RAG solves. Ask your local model something about...
```

> **Running it twice stores everything twice.** Qdrant does not deduplicate — 24 chunks
> becomes 48 points. Pass `force_recreate=True` to `from_documents` to wipe first.

---

## The pipeline

```text
   sample.pdf
       |  PyPDFLoader                    read_pdf()
       v
   12 page Documents
       |  RecursiveCharacterTextSplitter split_documents()
       v
   24 chunks  (1000 chars, 200 overlap)
       |  OpenAIEmbeddings               get_embeddings()
       v
   24 vectors (1536 numbers each)
       |  QdrantVectorStore              store_in_qdrant()
       v
   collection 'rag_sample'  ->  similarity_search()
```

---

## What actually got installed

`langchain-community` now requires Python **3.10+**, and this machine has **3.8.10**, so pip
quietly resolved older versions instead of failing:

| Package | Installed here | Current latest |
|---|---|---|
| langchain-community | 0.2.19 | 0.4.2 |
| langchain-core | 0.2.43 | 1.5.4 |
| langchain | 0.2.17 | 1.3.15 |
| langchain-openai | 0.1.25 | 1.5.1 |
| langchain-qdrant | 0.1.4 | 1.1.0 |
| qdrant-client | 1.12.1 | 1.19.0 |
| openai | 1.109.1 | 3.1.0 |
| pypdf | 5.9.0 | 6.15.0 |

Everything here works on these versions. But newer LangChain moved a lot of imports around,
so a current tutorial may not match what's installed. Python 3.11+ would fix that.

---

## Files

| File | What |
|---|---|
| `docker-composer.yml` | Qdrant vector database |
| `sample.pdf` | 12-page test document (Topic 42 — RAG) |
| `index.py` | indexing — `read_pdf`, `split_documents`, `get_embeddings`, `store_in_qdrant` |
| `02_chat.py` | querying — `search`, `build_context`, `build_messages`, `answer` |
| `requirements.txt` | pinned output of `pip freeze` |
| `venv/` | virtual environment (git-ignored) |

---

## 6. Ask it a question

`index.py` is the expensive half — it embeds all 24 chunks. Run it **once**. After that
every question only embeds the question itself.

```bash
python3 02_chat.py "what problem does RAG solve?"
```

```text
question: what problem does RAG solve?

retrieved 4 chunks from pages [0, 1, 0, 7]

--- answer ---
RAG solves the problem of a model not knowing anything about your own
documents [page 0]. ...
```

### How the prompt is built

```text
  system  ->  the rules  +  the retrieved chunks   <- your document, as data
  user    ->  the question, on its own
```

Keeping the document in the **system** message and the question in the **user** message is
deliberate. Retrieved text is data to be read, never instructions to obey. Concatenate them
into one message and a PDF containing *"ignore previous instructions"* becomes a live prompt
injection.

The system prompt also tells the model to answer **only** from the context and to say
*"That is not in the document."* otherwise. Without that rule it quietly blends your document
with its training data, and you cannot tell which sentence came from where.
