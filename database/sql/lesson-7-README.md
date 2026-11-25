# Lesson 7: Indexes and Query Speed

## Goal
Understand how indexes make queries faster, when to create them, and what they cost.

## Key idea
An **index** is a separate structure that lets the database find rows quickly, the way the alphabetical index at the back of a book helps you find a topic.

Without an index, the database checks every row. This is a **full table scan**. It's fine for 3 rows and slow for 3 million.

## Example

```sql
SELECT * FROM students WHERE name = 'Priya';
```

With no index on `name`, the database reads every row to find Priya.

## Creating an index

```sql
CREATE INDEX idx_students_name ON students (name);
```

Now lookups by `name` use a sorted structure (usually a B-tree) that points to the matching rows.

## Unique index

```sql
CREATE UNIQUE INDEX idx_students_email ON students (email);
```

This prevents two rows from sharing the same email. A `PRIMARY KEY` or `UNIQUE` constraint creates this kind of index automatically.

## Checking whether an index is used (SQLite)

```sql
EXPLAIN QUERY PLAN SELECT * FROM students WHERE name = 'Priya';
```

- `USING INDEX` means the index is used.
- `SCAN` means the whole table is read.

## Trade-off

| Indexes make | Indexes cost |
|---|---|
| Reads (`SELECT`) faster | Writes (`INSERT`, `UPDATE`, `DELETE`) slower |
| Lookups on indexed columns fast | Extra disk space |

Index the columns you search, filter, sort, or join on most often. Don't index every column.

## Gotchas
- **Some patterns can't use an index.** `LIKE '%av%'` can't use an index on `name`, because the pattern starts with `%`. `LIKE 'Ak%'` can.
- **Functions on a column can block the index.** `WHERE LOWER(name) = 'priya'` usually skips a plain index on `name`.
- **Foreign key columns are often worth indexing.** You'll join on them, so `orders.customer_id` is a good candidate.
- **More indexes are not always better.** Each one adds work on every write.

## Summary
- An index lets the database jump to matching rows.
- Index the columns you search, filter, sort, or join on.
- Indexes speed up reads and slow down writes.
- Use `EXPLAIN` to check whether a query uses an index.

## Practice
1. Create an index on `students.city`, then run `EXPLAIN QUERY PLAN` on `SELECT * FROM students WHERE city = 'Pune';`.
2. Why might `WHERE name LIKE '%av%'` not use an index on `name`?
3. Why would you index `orders.customer_id`?
