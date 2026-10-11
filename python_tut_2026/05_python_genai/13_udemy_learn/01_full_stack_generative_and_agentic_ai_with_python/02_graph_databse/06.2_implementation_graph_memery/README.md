# Graph Memory Agent — mem0 + Qdrant + Neo4j (working setup)

> Verified working: 2026-10-08 · mem0ai **1.0.11** · chat LLM **Groq** `openai/gpt-oss-120b` ·
> embeddings **Gemini** 768-d · vectors **Qdrant** (Docker) · graph **Neo4j Aura**

One chat loop, two memories. Every message is split by an LLM into **facts** (→ Qdrant) and
**entities + relationships** (→ Neo4j). On the next question both are searched and handed
to the chat model.

```text
 "> My colleague Jane also works at RTLedgers, and Alex owns RTLedgers."
        │
        ▼  mem_client.add()
   ┌─────────────────────┐        ┌───────────────────────────────┐
   │ LLM → facts         │        │ LLM → entities + relations     │
   │ "Jane works at RTL" │        │ (jane)-[works_at]->(rtledgers) │
   │ "Alex owns RTL"     │        │ (alex)-[owns]->(rtledgers)     │
   └────────┬────────────┘        └──────────────┬────────────────┘
            ▼                                    ▼
        Qdrant  mem0_gemini               Neo4j Aura  user_id=user_1
            └──────── mem_client.search() ───────┘
                       results + relations ──► chat LLM ──► answer
```

---

## Why this folder has its OWN venv

| | mem0ai **2.x** (repo-root `.venv`) | mem0ai **1.0.11** (this folder's `.venv`) |
|---|---|---|
| `graph_store` config | **silently ignored** — no error, no Neo4j writes | works |
| `search()` returns | `{"results": [...]}` | `{"results": [...], "relations": [...]}` |
| Why | v2.0.0 (Apr 2026) deleted the graph layer (~4 000 lines) | last release with it |

Details: [../06_adding_graph_database_support_for_agent.md](../06_adding_graph_database_support_for_agent.md)

---

## Setup (once)

```bash
cd python_tut_2026/05_python_genai/13_udemy_learn/02_graph_databse/06.2_implementation_graph_memery
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

`.env` keys this script reads:

| Key | Used for |
|---|---|
| `NEO_CONNECTION_URI`, `NEO_USERNAME`, `NEO_PASSWORD` | Neo4j Aura (password is shown **once** at instance creation) |
| `NEO_DATABASE` *(optional)* | skip the auto-detect — Aura names the DB after the instance id, **not** `neo4j` |
| `GOOGLE_API_KEY` | Gemini embeddings (always) + Gemini chat (`MEM0_PROVIDER=gemini`) |
| `GROQ_API_KEY`, `GROQ_MODEL` | Groq chat (`MEM0_PROVIDER=groq`) |
| `OPENAI_API_KEY`, `OPENAI_MODEL` | OpenAI chat + embeddings (`MEM0_PROVIDER=openai`) |

---

## Run

```bash
docker-compose up -d                          # Qdrant on localhost:6333
curl -s http://localhost:6333/healthz         # "healthz check passed"
MEM0_PROVIDER=groq .venv/bin/python mem.py    # ← the combination that works today
```

| `MEM0_PROVIDER` | chat LLM | embedder | status (2026-10-08) |
|---|---|---|---|
| `gemini` *(default)* | Gemini 3.6/3.8-flash | Gemini 768-d | chat **flaps with 503 "high demand"** — embeddings fine |
| **`groq`** | `openai/gpt-oss-120b` | Gemini 768-d | ✅ reliable, tool-calling works |
| `openai` | gpt-4.1-mini | OpenAI 1536-d | ❌ key has **no credits** (429) |

---

## Test script

Type these at the `>` prompt, in order. Stop with `Ctrl+C`.

| # | Type | Expect |
|---|---|---|
| 1 | `My name is Akshay and I work at RTLedgers as a developer. My colleague Jane also works at RTLedgers, and Alex owns RTLedgers.` | `Found Relations: []` (nothing yet) → `Memory added successfully` → `get_all` shows ~4 facts |
| 2 | `Who is my coworker, and who should I report to?` | `Found Relations:` **non-empty** dicts → AI: **Jane** / **Alex** |
| 3 | `I like pizza and I use Python and Next.js` | more facts; graph gains `(user_1)-[likes]->(pizza)`-style edges |
| 4 | `What should I eat tonight?` | AI suggests **pizza** from memory |

Real output of turn 2 (trimmed):

```text
Found Relations: [{'source': 'jane',   'relationship': 'colleague_of', 'destination': 'user_1'},
                  {'source': 'user_1', 'relationship': 'works_at',     'destination': 'rtledgers'},
                  {'source': 'user_1', 'relationship': 'role',         'destination': 'developer'}]
AI :->  Your coworker: Jane … Who you should report to: Alex – owner of RTLedgers
```

Things to notice:
- **Entity names are lowercased** (`rtledgers`, `jane`) and **you are a node** called `user_1`.
- The AI's own answers are stored too (`add()` gets both messages), so turn 2 wrote
  `(user_1)-[coworker]->(jane)` and `(user_1)-[reports_to]->(alex)` — **inferred relations became edges**.
- Vector results carry a `score`; graph results don't — they're exact matches, not similarity.

---

## Verify in Neo4j (Aura query console)

```cypher
MATCH (n) WHERE n.user_id = 'user_1' RETURN n                     // only mem0's nodes
MATCH (a)-[r]->(b) WHERE a.user_id = 'user_1'
RETURN a.name, type(r), b.name                                     // the triples
```

Nodes you created by hand earlier have **no** `user_id`; everything mem0 writes has one, so the
filter separates them. After the test above the graph looked like:

```text
(user_1)-[named]->(akshay)        (akshay)-[works_at]->(rtledgers)   (alex)-[owns]->(rtledgers)
(user_1)-[works_at]->(rtledgers)  (jane)-[works_at]->(rtledgers)     (alex)-[owner_of]->(rtledgers)
(user_1)-[role]->(developer)      (jane)-[colleague_of]->(user_1)
(user_1)-[coworker]->(jane)       (user_1)-[reports_to]->(alex)
```

### Reset between tests

```cypher
MATCH (n) WHERE n.user_id = 'user_1' DETACH DELETE n               // mem0's graph only
```
```bash
curl -s -X DELETE http://localhost:6333/collections/mem0_gemini    # vector memories
rm -f ~/.mem0/history_mem0_v1.db                                   # mem0's change log
```

---

## Troubleshooting — every error hit while getting this to work

| Error | Real cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'dotenv'` | ran with system Python / wrong venv | `.venv/bin/python mem.py` (this folder's venv) |
| `[Errno 61] Connection refused` on 6333 | Qdrant not running (often Docker Desktop itself quit) | `open -a Docker` → `docker-compose up -d` |
| `port is already allocated` (6333) | stale Qdrant container from `01_mem_agent` owns the port | `docker ps -a` → `docker rm -f <that-container>` |
| `Vector dimension error: expected dim: 1536, got 768` | mem0 creates the Qdrant collection with **1536** unless told; Gemini embeds to **768** | `"embedding_model_dims": EMBED_DIMS` in `vector_store` config |
| `404 … gemini-2.0-flash is no longer available` | Google retired the model | `GEMINI_CHAT_MODEL` in `.env` |
| `503 UNAVAILABLE … high demand` (Gemini) | Google-side overload, survives the SDK's own retries | switch chat LLM: `MEM0_PROVIDER=groq` |
| `429 … credit_balance_exhausted` (OpenAI) | no credits on the key | top up, or use Groq |
| `DatabaseNotFound … database 'neo4j' does not exist` | langchain's `Neo4jGraph` defaults to db **`neo4j`**; Aura names it after the **instance id** (`a26c4b8b`) | `"database": NEO_DATABASE` (auto-detected via `CALL db.info()`) |
| Neo4j stays empty, no error at all | you're on mem0ai **2.x** — `graph_store` is ignored | use this folder's venv (1.0.11) |
