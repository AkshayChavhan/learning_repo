# 06 — Scalable RAG with an Async Queue

Project [05](../../05_building_chat_with_rag/rag/) answered a query *inline* — the
HTTP request sat open while embedding and generation ran. This one puts a
**queue** between the API and the work.

```text
POST /chat  ──►  FastAPI  ──►  enqueue job  ──►  Valkey (Redis)
                    │                                  │
              returns job_id                    RQ worker picks it up
              immediately                              │
                                              Qdrant search ──► OpenAI
                                                       │
GET /chat/{job_id} ◄──────────────── result stored ◄───┘
```

**Why it matters:** the API answers in milliseconds instead of seconds, and you
scale throughput by running *more workers*, not a bigger web server.

---

## Layout

| File | Role |
|---|---|
| `main.py` | Entry point — uvicorn on `0.0.0.0:8000` |
| `server.py` | FastAPI routes: `POST /chat` enqueues, `GET /chat/{job_id}` polls |
| `client/rq_client.py` | The RQ `Queue`, connected to Valkey on `localhost:6379` |
| `queues/worker.py` | `process_query()` — Qdrant similarity search → OpenAI answer |
| `docker-compose.yml` | Valkey + Qdrant |

---

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 1. Start the services

```bash
docker compose up -d
docker compose ps
```

| Service | Port | Role |
|---|---|---|
| Valkey (Redis-compatible) | `6379` | the job queue |
| Qdrant | `6333` REST/dashboard, `6334` gRPC | the vector store |

Qdrant keeps its data in a `qdrant-data` volume, so embeddings survive restarts.
Dashboard: <http://localhost:6333/dashboard>

### 2. Environment

| Variable | Where |
|---|---|
| `OPENAI_API_KEY` | `.env` in this folder |

```bash
# from the repo root
export OPENAI_API_KEY='sk-proj-...'
./scripts/setup_env.sh
```

Both `main.py:5` and `queues/worker.py:8` call `load_dotenv()` — the worker
needs it in its own process, since it does the actual OpenAI calls.

### 3. Index some documents first

The worker reads an existing collection — it does **not** create one. Until
something has written to it, `from_existing_collection` fails outright.

> **Project 05's `index.py` will not populate this.** The two projects disagree
> on both settings:
>
> | | project 05 `index.py` | project 06 `worker.py` |
> |---|---|---|
> | collection | `rag_sample` | `rag_collection` |
> | embedding model | `text-embedding-3-small` (1536 dims) | `text-embedding-3-large` (3072 dims) |
>
> Renaming the collection alone is not enough — vectors written with 1536
> dimensions cannot be searched with a 3072-dimension query. To reuse project
> 05's indexer here, change **both** values to match, then re-index from
> scratch.

---

## Run

Three terminals, all with the venv active:

```bash
python main.py          # 1. API      → http://localhost:8000
rq worker               # 2. worker   → picks jobs off the queue
```

```bash
# 3. try it
curl -X POST "http://localhost:8000/chat?query=What+problem+does+RAG+solve%3F"
# {"status":"Chat is running","job_id":"abc-123"}

curl "http://localhost:8000/chat/abc-123"
# {"status":"finished","job_id":"abc-123","result":"..."}
```

`status` moves through `queued → started → finished` (or `failed`). Poll until
it settles.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`job.return_value` is a method in rq 2.x** | Writing it without `()` hands back the bound method; FastAPI serialises it as `{}` and you get `200 OK` with no answer. `server.py:28` calls it correctly |
| **No worker = jobs sit forever** | `POST /chat` always succeeds. If status never leaves `queued`, you forgot `rq worker` |
| **`QdrantVectorStore(...)` takes a client, not a url** | To connect by URL use `from_existing_collection()`, as `worker.py:27` does |
| **Vector DB is built lazily** | `get_vector_db()` defers the connection so importing the module does not require Qdrant — only the worker needs it, the API does not |
| **Collection must already exist** | `from_existing_collection` fails if nothing has written `rag_collection` yet — see step 3, project 05 does not write it |
| **Worker needs its own env** | It is a separate process. `load_dotenv()` in `main.py` does not help it |
