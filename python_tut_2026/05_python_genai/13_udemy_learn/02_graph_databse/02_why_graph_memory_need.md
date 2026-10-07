# Why AI Memory Needs a Graph

So far our memory lived in a **vector DB** (Qdrant via mem0). That works for single facts
like *"name is Piyush"* or *"likes pizza"*. What it can't store is the **relationship** between facts.
A **knowledge graph** stores those relationships, so the agent can follow them to answers
nobody ever wrote down.

---

## Topic at a glance

```text
        Problem                          Direct relations
           \                                  /
  isolated facts ──\         X ─EMPLOYS─► John ──/
                    \                          /
  no "how" link ─────\       Alex ─OWNS─► X ──/
                      ►   WHY GRAPH MEMORY?
  coworkers ─────────/       vector = facts ──\
                    /                          \
  reports-to ──────/         graph = links ─────\
           /                                     \
    Indirect relations                      Hybrid setup
```

---

## 🟢 Beginner: what vectors miss

A vector DB stores each memory as a **separate point**. It can find memories that *sound
similar* to a question, but it has no idea how two memories are **connected**.

| Memory | Vector DB | Graph |
|---|---|---|
| "My name is Piyush" | ✅ stores it | ✅ stores it |
| "I like pizza" | ✅ stores it | ✅ stores it |
| "John and Jane work at the same company" | ❌ two unrelated facts | ✅ both linked to one company node |
| "So John and Jane are **coworkers**" | ❌ never stored, never known | ✅ **worked out** by following edges |

> **Key idea:** vectors store **facts**. Graphs store **facts + how they connect**.

---

## 🟡 Intermediate: the company example

Three facts go into memory:

1. Company X **employs** John
2. Company X **employs** Jane
3. Alex **owns** Company X

As a graph:

```text
                ┌──────────┐
                │   Alex   │  (User)
                └────┬─────┘
                     │ OWNS
                     ▼
                ┌───────────┐
                │ Company X │
                └──┬─────┬──┘
           EMPLOYS │     │ EMPLOYS
                   ▼     ▼
             ┌──────┐   ┌──────┐
             │ John │   │ Jane │
             └──────┘   └──────┘
                 ▲          ▲
                 └ ─ ─ ─ ─ ─┘
          COWORKERS (inferred, never stored)
```

### Questions the graph can answer by walking edges

| Who asks | Question | Path walked | Answer |
|---|---|---|---|
| John | "Tell me about Jane" | John ◄EMPLOYS─ X ─EMPLOYS► Jane | Jane is your **coworker** |
| Jane | "Who should I report to?" | Jane ◄EMPLOYS─ X ◄OWNS─ Alex | **Alex** owns your company |
| Jane | "Who can I chat with in a friendly way?" | Jane ◄EMPLOYS─ X ─EMPLOYS► *all* | every employee of X (**John**) |

None of these answers was saved as a fact. They come from **traversal**: starting at a node
and following edges.

### The same idea in plain Python

```python
# each edge is a (subject, RELATION, object) triple
edges = [
    ("CompanyX", "EMPLOYS", "John"),
    ("CompanyX", "EMPLOYS", "Jane"),
    ("Alex",     "OWNS",    "CompanyX"),
]

def employer_of(person):
    return next(s for s, r, o in edges if r == "EMPLOYS" and o == person)

def coworkers_of(person):
    company = employer_of(person)
    return [o for s, r, o in edges if s == company and r == "EMPLOYS" and o != person]

def boss_of(person):
    company = employer_of(person)
    return next(s for s, r, o in edges if r == "OWNS" and o == company)

print("Jane's coworkers:", coworkers_of("Jane"))
print("Jane reports to :", boss_of("Jane"))
```

```text
Jane's coworkers: ['John']
Jane reports to : Alex
```

### Direct vs indirect relationships

| Type | Meaning | Example |
|---|---|---|
| **Direct** | one edge, stored explicitly | Company X ─EMPLOYS► John |
| **Indirect** | several edges, **inferred** at query time | John ↔ Jane are coworkers (2 hops) |
| **Indirect: recommendation** | "you like A → people who like A also like B, C" | likes pizza → also likes pasta, garlic bread |

---

## 🔴 Expert: how it fits into real agent memory

### Vector vs graph, side by side

| | Vector DB (Qdrant, FAISS) | Graph DB (Neo4j, Kuzu) |
|---|---|---|
| Stores | text chunks as embeddings | **entities** (nodes) + **relations** (edges) |
| Search by | meaning / similarity | following connections |
| Best question | *"what do I know about food?"* | *"who is Jane's boss?"* |
| Multi-hop reasoning | ❌ left to luck of top-k + the LLM | ✅ built in (walk N edges) |
| Fuzzy / paraphrased recall | ✅ strong | ❌ weak (needs exact entity) |

**Why "luck"?** Ask a vector DB *"who is Jane's coworker?"* and it returns the top-k chunks most
similar to the question. Most likely that's *"Jane works at Company X"*. The chunk about John
may never come back, because the question doesn't mention him. A graph doesn't depend on
wording: it goes from Jane to Company X to John.

### Use both together (hybrid memory)

```text
 user message
      │
      ▼
 LLM extracts ──► facts ─────────────► Vector DB   ("likes pizza")
      │
      └─────────► entities + relations ► Graph DB  (Jane ─WORKS_AT─► X)

 on a new question:
   vector search  ─┐
                   ├──► merged context ──► LLM answer
   graph traversal ┘
```

The graph doesn't **replace** the vector store. It sits next to it: vectors give fuzzy recall,
the graph gives relationships.

### Humans work the same way

We don't remember facts in isolation. Hearing "Jane" brings up *her company*, which brings up
*her boss*, which brings up *the project you share*. That chain of associations is a graph walk.

---

## Gotchas & best practices

- **Edge direction matters.** `Alex ─OWNS► X` is not `X ─OWNS► Alex`. Walk edges the right way.
- **Inferred ≠ stored.** "Coworkers" is computed at query time. Nothing to update when Jane leaves;
  delete one edge and the inference disappears too.
- **More hops = more context, more noise.** 1–2 hops is usually useful; 5 hops pulls in
  half the company.
- **Duplicate entities break the graph.** `Jane`, `jane`, `Jane D.` become 3 nodes that aren't
  linked. Normalize names (entity resolution).
- **Graph quality = extraction quality.** An LLM turns sentences into triples. A bad extraction
  stores a wrong edge, and that edge sticks around.

> **Interview angle:** *"Why isn't a vector DB enough for agent memory?"*
> Vectors retrieve **similar** text, but they don't know how facts **connect**. A knowledge
> graph stores entities and relations, so the agent can answer multi-hop questions (coworkers,
> reporting chains, recommendations) that were never written down as one fact.
> Production memory (e.g. mem0 with a graph store) uses **both**.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Knowledge graph** | memory stored as `(entity) ─RELATION─► (entity)` triples |
| **Direct relation** | one stored edge (Company X employs John) |
| **Indirect relation** | worked out by following several edges (John ↔ Jane coworkers) |
| **Traversal** | walking edges from a starting node to find connected info |
| **Hybrid memory** | vector DB for fuzzy facts + graph DB for relationships |
