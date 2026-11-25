# Lesson 3: Your First SQL Queries

## Goal
Learn the four basic SQL operations: add, read, change, and delete data.

## What is SQL?
**SQL** (Structured Query Language) is the standard language for talking to relational databases.

SQL is **a language, not a database**. These are databases that understand SQL:

| Name | What it is | Uses SQL? |
|---|---|---|
| **MySQL** | Database software | Yes |
| **PostgreSQL** | Database software | Yes |
| **SQLite** | Small database stored in one file | Yes |
| **SQL Server** | Database software by Microsoft | Yes (with some extra features) |
| **MongoDB** | Document database | No, it uses its own query style |

The core commands are the same across these databases. Small differences exist, such as `LIMIT` (MySQL, PostgreSQL, SQLite) and `TOP` (SQL Server).

## The four operations (CRUD)

| Operation | SQL keyword | Purpose |
|---|---|---|
| **C**reate | `INSERT` | Add rows |
| **R**ead | `SELECT` | Read rows |
| **U**pdate | `UPDATE` | Change rows |
| **D**elete | `DELETE` | Remove rows |

## Setup

```sql
CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT,
  marks INTEGER
);
```

## INSERT

```sql
INSERT INTO students (id, name, city, marks)
VALUES (1, 'Ravi', 'Pune', 85);

INSERT INTO students (id, name, city, marks)
VALUES (2, 'Priya', 'Mumbai', 92),
       (3, 'Akshay', 'Pune', 78);
```

## SELECT

```sql
SELECT * FROM students;                       -- all columns, all rows
SELECT name, marks FROM students;             -- only two columns
SELECT * FROM students WHERE city = 'Pune';   -- filter rows
SELECT * FROM students WHERE marks >= 80;
SELECT * FROM students ORDER BY marks DESC;   -- highest first
```

## UPDATE

```sql
UPDATE students SET marks = 88 WHERE id = 1;
```

**Always use `WHERE` with `UPDATE`.** Without it, every row changes.

## DELETE

```sql
DELETE FROM students WHERE id = 3;
```

**Always use `WHERE` with `DELETE`.** Without it, every row is removed.

## Gotchas
- Text values use **single quotes**: `'Pune'`.
- `=` compares values. Assignment happens only inside `SET`.
- SQL keywords are not case-sensitive (`select` = `SELECT`).
- `NOT NULL` rejects empty values. Try inserting a student with no name to see the error.

## Summary
- SQL is the language. The database software runs it.
- Four operations: `INSERT`, `SELECT`, `UPDATE`, `DELETE`.
- Always double-check `WHERE` in `UPDATE` and `DELETE`.

## Practice
1. Write a query that shows only the names of students with marks of 85 or more.
2. What is wrong with `UPDATE students SET marks = 90;`?
3. Which keyword adds a new student?
