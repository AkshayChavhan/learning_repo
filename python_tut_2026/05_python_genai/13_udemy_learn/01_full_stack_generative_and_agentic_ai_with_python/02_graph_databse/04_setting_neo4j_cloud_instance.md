# Setting Up Neo4j — Aura Cloud Instance

Neo4j can run locally via Docker, but it's heavy. For learning, the free
**Neo4j Aura** cloud instance is the path of least resistance — hosted,
free tier, up in minutes.

---

## 🟢 Beginner — why cloud, not local Docker

| Option | Trade-off |
|---|---|
| **Docker (local)** | possible, but Neo4j is heavy to run locally |
| **Neo4j Aura (cloud)** | hosted, free tier, no local resource cost |

---

## 🟡 Intermediate — the setup steps

```text
1. Go to Neo4j Aura login -> sign in (Google works, free)
2. Dashboard -> Create Instance -> select FREE ($0)
3. Aura generates a one-time password - cannot be viewed again later
4. Save immediately: username ("neo4j") + that password -> into .env
5. Download the credentials file + continue
6. Wait for the instance to provision ("up and running")
7. Open the built-in query console
```

| What you get at the end | |
|---|---|
| A running, empty graph database | zero nodes, zero relationships - a blank slate |
| A console to query it | where Cypher queries get written next |

---

## 🔴 Expert — the gotcha that actually matters

**The password is shown exactly once.** Aura generates it, shows it one
time, and never again - there's no "forgot password" recovery for that
credential. Copy it immediately into `.env`, alongside the username,
before doing anything else:

```text
NEO4J_URI=<your instance URI>
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<the one-time password, saved NOW>
```

Everything else in the signup flow is just clicking through a wizard -
this is the one step that's easy to miss and hard to undo.

**Not covered yet:** writing actual Cypher queries - that's next, and you
don't need to be a pro at it to get started.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Neo4j Aura** | Neo4j's hosted cloud service - free tier available |
| **One-time password** | shown once at instance creation, never retrievable again |
| **Cypher** | the query language used to talk to the database - covered next |
