# Graphs — Nodes, Edges & Why AI Memory Needs Them

A **graph** is a data structure made of **nodes** (things that hold data) connected by
**edges** (the connections between them). That's the whole idea — everything else is
detail on top of it.

---

## 🟢 Beginner — nodes + edges

```text
   (A) ──── (B)
```

| Part | What it is |
|---|---|
| **Node** | a dot that carries data — a person, a fact, an entity |
| **Edge** | a connection between two nodes |

A graph needs no special library — it's just a list of which things connect:

```python
nodes = ["A", "B", "C"]
edges = [("A", "B"), ("B", "C")]   # A connects to B, B connects to C

for n1, n2 in edges:
    print(f"{n1} -- {n2}")
```

```text
A -- B
B -- C
```

**Mental model:** people are nodes, friendships are edges.

---

## 🟡 Intermediate — directed vs undirected, and labeled edges

### Two kinds of graph

| | Directed graph | Undirected graph |
|---|---|---|
| Looks like | `A ──► B` | `A ──── B` |
| Meaning | **one-way** relationship | **two-way**, symmetric |
| Example | "A is parent of B" — not the reverse | Facebook friends — always mutual |
| Common use | hierarchies, task dependencies, "follows" | friendships, "is connected to" |

```text
 DIRECTED                      UNDIRECTED

   A ──parent of──► B            A ──friends──── B
   (one-way: B is NOT            (two-way: both sides
    parent of A)                  are friends of each other)
```

### An edge can carry meaning, not just a connection

A real edge is a **triple**, not just a line between two dots:

```text
   (A) ──relation X──► (B)
```

`(node, relation, node)` — e.g. *node A is connected to node B with relation "parent of."*
Knowing **that** two things connect isn't enough on its own — knowing **how** is what
makes a graph useful.

---

## 🔴 Expert — why AI memory systems reach for graphs

| | Vector store (Qdrant, FAISS — covered earlier) | Graph |
|---|---|---|
| Answers | *"what's similar to this?"* | *"what's explicitly related to this, and how?"* |
| Mechanism | distance between embeddings | an actual stored relationship (edge + label) |
| Good at | fuzzy, semantic matches | exact, structured facts |

A memory system built only on embeddings can tell you *"this feels close to that"* —
but it can't tell you *"X is the parent of Y"* with certainty, because that fact was
never a single point in space; it's a **relationship**. That's the generic reason
knowledge graphs show up in AI memory: embeddings handle *similarity*, graphs handle
*explicit, structured relationships* — and real memory systems lean on both.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Node** | a thing that holds data |
| **Edge** | a connection between two nodes |
| **Directed graph** | edges point one way (`A ──► B`, not the reverse) |
| **Undirected graph** | edges go both ways (`A ──── B`, symmetric) |
| **Labeled edge** | `(node, relation, node)` — the connection says *what kind* it is |
