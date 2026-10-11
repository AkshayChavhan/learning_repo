# Cypher Basics — Creating Nodes & Relationships

Cypher is Neo4j's query language. Two verbs cover most of what you need to get
started: `CREATE` to make a node, `MATCH` to find one.

---

## 🟢 Beginner — the two core verbs

| Verb | Does | Syntax |
|---|---|---|
| **CREATE** | makes a new node | `CREATE (u:User {name: "Piyush"})` |
| **MATCH** | finds existing node(s) | `MATCH (u:User {name: "Piyush"}) RETURN u` |

```text
   CREATE (u:User {name: "Piyush"})
            |
            v
        (Piyush:User)        <- a node now exists, no relationships yet
```

`MATCH (n) RETURN n` with no label returns **every** node in the database -
useful for a quick "what's actually in here" check.

---

## 🟡 Intermediate — relationships, and a mistake worth learning from

To connect two nodes, use `MERGE`. Matching only ONE side of the relationship
before merging is a classic bug - worth seeing both ways.

### Wrong - the company is never matched, only merged

```cypher
MATCH (u:User {name: "Piyush"})
MERGE (u)-[:EMPLOYEE]->(c:Company {name: "Google"})
```

Run this for Piyush, then John, then Jane - each time `c` is a fresh,
unmatched variable. `MERGE` looks for the WHOLE pattern (this user -> this
relationship -> a company named Google) and doesn't find it, so it creates a
brand-new Google node every time.

### Right - match both existing nodes first, merge only the relationship

```cypher
MATCH (u:User {name: "Piyush"})
MATCH (c:Company {name: "Google"})
MERGE (u)-[:EMPLOYEE]->(c)
```

Now `c` refers to the one existing Google node, so `MERGE` only creates the
missing piece - the relationship itself.

```text
   WRONG                              RIGHT

   (Piyush)-[EMPLOYEE]->(Google #1)    (Piyush)-+
   (John)  -[EMPLOYEE]->(Google #2)    (John)   -+-[EMPLOYEE]-> (Google)
   (Jane)  -[EMPLOYEE]->(Google #3)    (Jane)   -+
   4 duplicate companies!               1 shared company, 3 relationships
```

**The rule:** `MATCH` every node that should already exist, before merging a
relationship between them. Only let `MERGE`/`CREATE` make something new when
you actually mean to create it.

---

## 🔴 Expert — cleanup, and the bigger point

**Deleting bad data:** `id()` is deprecated - use `elementId()`:

```cypher
MATCH (n) WHERE elementId(n) = "<the id>"
DELETE n
```

**The real takeaway:** in practice, you don't hand-write these queries. You
describe the relationship in plain language, an LLM generates the Cypher,
runs it against the database, and returns the result. The syntax here isn't
about becoming fluent at writing Cypher by hand - it's about understanding
what the LLM is doing on your behalf when it builds a memory graph, so you
can spot exactly this kind of bug (duplicate nodes from an unmatched `MERGE`)
when it happens.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **CREATE** | makes a new node |
| **MATCH** | finds an existing node by label/property |
| **MERGE** | creates the pattern if it doesn't exist - matches it if it does |
| **The duplicate-node bug** | merging with an unmatched variable on one side creates a new node every run |
| **elementId()** | the current way to reference a node's id - `id()` is deprecated |
