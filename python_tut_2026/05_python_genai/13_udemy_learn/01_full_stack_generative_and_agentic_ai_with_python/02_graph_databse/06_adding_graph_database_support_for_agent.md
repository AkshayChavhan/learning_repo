# Adding Graph Database Support to Mem0 Agent

**⚠️ CRITICAL: This tutorial is for mem0ai v1.x. mem0ai v2.0.0+ (April 2026) removed all graph_store support from the open-source library. See [Breaking Change](#breaking-change) below.**

This video shows how to connect a Neo4j graph database to mem0's Memory instance so that
as the agent learns facts, it also builds a knowledge graph of **entities** and **relationships**.

---

## 🟢 Beginner: what gets configured

You already have a `MemoryConfig` dict that sets up:
- **LLM** — which AI model extracts facts
- **Embedder** — which model embeds those facts
- **Vector store** — where facts live (Qdrant in your case)

Adding **graph support** adds one more piece:
- **Graph store** — Neo4j, where entities + relationships get stored

```python
# Before: vector DB only
config = {
    "llm": {...},
    "embedder": {...},
    "vector_store": {...},
}

# After: vector DB + graph DB
config = {
    "llm": {...},
    "embedder": {...},
    "vector_store": {...},
    "graph_store": {...},          # NEW
}
```

---

## 🟡 Intermediate: the graph_store configuration block

### Step 1: Get the Neo4j connection URI

If using **Neo4j Aura** (the cloud instance from earlier), the dashboard shows a **Connection URI**:

```text
neo4j+s://abc123def456.databases.neo4j.io
```

Copy it. You'll paste it into the config.

### Step 2: Add the graph_store block to your config

```python
config = {
    "version": "v1.1",
    "llm": {...},
    "embedder": {...},
    "vector_store": {...},
    "graph_store": {                    # NEW BLOCK
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://abc123def456.databases.neo4j.io",
            "username": "neo4j",
            "password": "<your-one-time-password>",
        },
    },
}

mem_client = Memory.from_config(config)
```

### The fields explained

| Field | What it is | Example |
|---|---|---|
| **provider** | which graph DB vendor | `"neo4j"`, `"memgraph"`, `"kuzu"`, `"apache_age"` |
| **url** | Neo4j instance address | `"neo4j+s://abc123...databases.neo4j.io"` |
| **username** | graph DB login | `"neo4j"` (default on Aura) |
| **password** | graph DB password | the one-time password from Aura signup |

### What happens when you call `mem_client.add()`

With `graph_store` configured, the `add()` call now does **two things in parallel**:

1. **Vector DB path** — extract facts, embed them, store in Qdrant
2. **Graph DB path** — extract **entities** from the same text, create nodes, link them

```text
user message
    │
    ├──► LLM extracts facts ──► Vector DB (Qdrant)
    │
    └──► LLM extracts entities ──► Graph DB (Neo4j) builds nodes + edges
```

### What gets returned in search results

With graph enabled, `mem_client.search()` returns **both** paths:

```python
result = mem_client.search("Who is my coworker?", user_id="user_1")

# Real output shape (mem0 1.0.11, verified on 2026-10-08):
{
    "results": [                       # <-- VECTOR results, with a similarity score
        {"id": "...", "memory": "Colleague Jane works at RTLedgers", "score": 0.66, ...},
        ...
    ],
    "relations": [                     # <-- GRAPH results, one dict per edge, no score
        {"source": "jane",   "relationship": "colleague_of", "destination": "user_1"},
        {"source": "user_1", "relationship": "works_at",     "destination": "rtledgers"},
        {"source": "user_1", "relationship": "role",         "destination": "developer"},
    ],
}
# Entity names come back lowercased, and the user is a node called "user_1".
```

The LLM can then use both the vector results *and* the graph relations to answer the question.

---

## 🔴 Expert & Breaking Change

### What Neo4j does with the extracted entities

When you call `mem_client.add()` with graph support enabled:

1. **Entity extraction** — the LLM reads the user message and identifies **named entities**
   (people, companies, concepts).
   ```
   "Jane told me she works at Shopify"  →  entities: [Jane, Shopify]
   ```

2. **Node creation** — each entity becomes a **node** in Neo4j (or gets merged with an
   existing node if it's already there).
   ```cypher
   MERGE (j:Person {name: "Jane"})
   MERGE (s:Company {name: "Shopify"})
   ```

3. **Relationship inference** — the LLM also extracts **relationships** between entities
   and creates edges.
   ```cypher
   MERGE (j:Person {name: "Jane"}) -[:WORKS_AT]-> (s:Company {name: "Shopify"})
   ```

4. **Entity linking** — on later queries, the LLM tries to **match** the question's entities
   to existing nodes. If "Jane" is already a node and the question mentions her, the graph
   walk can now find all her connections without a new vector search.

### 🚨 Breaking Change: mem0ai v2.0.0+ removed this entirely

**Release date:** April 16, 2026  
**What changed:** `graph_store` and `enable_graph` config keys were removed from the open-source SDK.

**Why:** Mem0 Platform (managed service) replaced external graph stores with **native entity linking**
— entities are now extracted and stored in a parallel collection inside your existing vector store.
The open-source followed suit.

**Current state (mem0ai 2.2.1):**
- No `graph_store` config key exists
- Passing `graph_store` to `MemoryConfig()` is silently ignored (no error)
- Graph memory is built-in via entity extraction, not an external database

**If you need the old behavior:**

| Option | Trade-off |
|---|---|
| **Stay on mem0ai 1.0.11** | `pip install mem0ai==1.0.11` in a **separate venv** so the rest of the repo stays on 2.x — **done & verified**, see [06.2_implementation_graph_memery/README.md](06.2_implementation_graph_memery/README.md) |
| **Use Mem0 Platform** | managed service; graph memory is always on; requires API key |
| **Integrate Neo4j directly** | bypass mem0's graph layer; write your own entity extraction + Neo4j calls |

### The upgrade path (mem0 v1.x → v2.x)

If you're migrating from v1.x to v2.x and had `graph_store` in your config:

```python
# v1.x config (this won't work in v2.x)
config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {"url": "...", "username": "...", "password": "..."},
    },
    ...
}

# v2.x config (graph_store removed, entities extracted automatically)
config = {
    "llm": {...},
    "embedder": {...},
    "vector_store": {...},
    # no graph_store key — entity extraction is built-in
}
```

Entities are now extracted during `add()` and stored in a `{collection}_entities` collection
in your vector store. At query time, entities boost ranking on matching memories.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **graph_store config** | (v1.x only) block that connects mem0 to Neo4j / Memgraph / Kuzu for entity storage |
| **Neo4j URI** | address of your Neo4j instance (Aura format: `neo4j+s://...`) |
| **Entity extraction** | the LLM identifies people, companies, concepts from user text |
| **Entity linking** | matching new entities to existing nodes so the graph can walk relationships |
| **Breaking change** | mem0ai v2.0.0+ removed `graph_store` and moved to native entity extraction |

---

## Sources

- [Mem0 v2.0.0 Release (April 2026)](https://newreleases.io/project/github/mem0ai/mem0/release/v2.0.0)
- [Mem0 OSS Migration v2 → v3 Guide](https://docs.mem0.ai/migration/oss-v2-to-v3)
- [Mem0 Graph Memory (Platform, not OSS)](https://docs.mem0.ai/platform/features/graph-memory.md)
