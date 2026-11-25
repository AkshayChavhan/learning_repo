# Lesson 8: Transactions and ACID

## Goal
Learn how to group SQL statements so they all succeed or all fail, and understand the ACID guarantees.

## Key idea
A **transaction** is a group of statements that succeed or fail together. Either every statement runs, or none of them do.

Example: a transfer of ₹1,000 from Ravi to Priya takes two steps. If the computer crashes after the first step and before the second, the money disappears. A transaction prevents this.

## Example

```sql
CREATE TABLE accounts (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  balance INTEGER NOT NULL
);

INSERT INTO accounts VALUES (1, 'Ravi', 5000), (2, 'Priya', 2000);

BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;
```

| Keyword | Meaning |
|---|---|
| `BEGIN` | Start the transaction |
| `COMMIT` | Save all changes permanently |
| `ROLLBACK` | Cancel all changes since `BEGIN` |

Cancelling a transaction:

```sql
BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
ROLLBACK;
```

Ravi's balance returns to 5000.

## ACID

| Letter | Name | Meaning | Bank example |
|---|---|---|---|
| **A** | Atomicity | All steps happen, or none do | Both updates succeed, or neither does |
| **C** | Consistency | Rules stay true after the transaction | Balance never goes negative |
| **I** | Isolation | Concurrent transactions don't interfere | Two transfers at once don't corrupt balances |
| **D** | Durability | Committed data survives a crash | Transfer stays after a power cut |

## Consistency with constraints

```sql
CREATE TABLE accounts (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  balance INTEGER NOT NULL CHECK (balance >= 0)
);
```

Any statement that would make a balance negative now fails.

## Isolation levels

When transactions run at the same time, the isolation level controls how much they see of each other.

| Level | What can go wrong |
|---|---|
| **Read uncommitted** | You can see changes that might be rolled back (rare in practice) |
| **Read committed** | A value can change between two reads in the same transaction |
| **Repeatable read** | Your reads stay stable, but new rows can appear |
| **Serializable** | Behaves as if transactions ran one after another. Safest, but slowest. |

Most databases default to read committed or repeatable read.

## Gotchas
- **Forgetting `COMMIT`** leaves changes uncommitted. They may be lost if the connection closes.
- **Keep transactions short.** Long transactions lock rows and slow other users.
- **Many tools auto-commit.** Each statement may be its own transaction unless you turn that off.
- **Syntax varies slightly.** MySQL, PostgreSQL, and SQLite all support `BEGIN`, `COMMIT`, and `ROLLBACK`, with small differences.

## Summary
- A transaction groups statements so they all succeed or all fail.
- `BEGIN` starts it, `COMMIT` saves it, `ROLLBACK` cancels it.
- ACID stands for Atomicity, Consistency, Isolation, and Durability.
- Constraints such as `CHECK` help keep data consistent.

## Practice
1. Write a transaction that moves ₹500 from Priya to Ravi.
2. What does `ROLLBACK` do after two `UPDATE` statements?
3. Which ACID property stops two bank transfers from corrupting each other?
