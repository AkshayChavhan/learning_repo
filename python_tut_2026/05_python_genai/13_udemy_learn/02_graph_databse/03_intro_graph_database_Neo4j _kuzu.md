# Graph Databases — Neo4j vs KuzuDB

A graph (nodes + edges) is a concept. A **graph database** is where you actually
store one — persist it, and query relationships directly instead of reconstructing
them from joins.

---

## 🟢 Beginner — storing a graph for real

```text
   (Person) ──ACTED_IN──► (Movie)
```

That's a graph database entry: a `Person` node, a `Movie` node, connected by an
`ACTED_IN` relationship — a node-relation-node triple, made persistent.

| | What it is |
|---|---|
| **Graph database** | built to store nodes + edges and query relationships directly |
| **Neo4j** | the most popular one — very big, very scalable, and self-hostable |

---

## 🟡 Intermediate — Neo4j vs KuzuDB

| | Neo4j | KuzuDB |
|---|---|---|
| Maturity | established, industry standard | one of the earliest graph databases — relatively new |
| Support / ecosystem | wide, mature | very limited — still catching up |
| Self-hostable | yes | yes |
| Query language | **Cypher** — Neo4j's own language for pattern-matching relationships, e.g. `(Person)-[ACTED_IN]->(Movie)` | — |
| Where it stands | industry standard — "everyone uses it, it really shines out" | the newer alternative, not yet battle-tested at the same scale |

**Bottom line:** both exist, but Neo4j is the pick for this course.

---

## 🔴 Expert — why "industry standard" beats "newer"

This is a maturity argument, not a technical-superiority one:

- **Community + tooling** — more drivers, integrations, and production war-stories accumulated over years
- **Battle-tested at scale** — the "very big, very scalable" reputation comes from real production use, not benchmarks alone
- **KuzuDB isn't technically worse** — it's just newer, so its support/tooling hasn't caught up yet. That gap closes with time; right now it's the real reason to default to Neo4j

**Ties back:** Neo4j is the engine that actually stores the `(node, relation, node)`
triples from the earlier topic — e.g. `Person ACTED_IN Movie` — and lets you query
them directly.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Graph database** | a database built to store and query nodes + edges directly |
| **Neo4j** | the industry-standard graph database — mature, scalable, self-hostable |
| **Cypher** | Neo4j's query language for matching patterns over nodes and relationships |
| **KuzuDB** | a newer graph database — capable, but limited support so far |
