# Lesson 6: Joining Tables

## Goal
Combine data from two or more tables using `JOIN`.

## Key idea
In Lesson 2 you saw that related data lives in separate tables. A **JOIN** combines rows from two tables where a matching column has the same value.

## Setup

```sql
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  item TEXT,
  amount INTEGER
);

INSERT INTO customers VALUES (1, 'Ravi', 'Pune'), (2, 'Priya', 'Mumbai'), (3, 'Akshay', 'Pune');
INSERT INTO orders VALUES (10, 1, 'Laptop', 55000), (11, 1, 'Mouse', 800), (12, 2, 'Keyboard', 2500);
```

Akshay (id 3) has no orders.

## INNER JOIN: only matching rows

```sql
SELECT customers.name, orders.item, orders.amount
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;
```

Returns Ravi's two orders and Priya's one order. Akshay is left out.

`JOIN` alone means the same as `INNER JOIN`.

## LEFT JOIN: keep all rows from the left table

```sql
SELECT customers.name, orders.item
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id;
```

Akshay now appears, with `item` empty (NULL).

## Table aliases

```sql
SELECT c.name, o.item, o.amount
FROM customers AS c
JOIN orders AS o ON c.id = o.customer_id;
```

`AS` is optional.

## Joining with a filter

```sql
SELECT c.name, o.item
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE c.city = 'Pune';
```

## Gotchas
- **Always write `ON`.** Without it, every customer pairs with every order, which gives wrong results.
- **Use `table.column` when names clash.** Both tables have `id`. Write `c.id` or `o.id`, or you get an "ambiguous column" error.
- **Choose `LEFT JOIN`** when you want the left table's rows even without a match.
- **A `WHERE` condition on the right table of a LEFT JOIN can remove unmatched rows.** Put that condition in `ON` to keep them.

## Summary
- `JOIN` (or `INNER JOIN`) returns only matching rows.
- `LEFT JOIN` returns all left-table rows, with NULLs where there's no match.
- Use aliases (`c`, `o`) to keep queries short.
- `ON` says which columns must match.

## Practice
1. Write a `LEFT JOIN` that lists all customers and their items, including customers with no orders.
2. Why does `SELECT id FROM customers JOIN orders ON ...` cause an error?
3. Predict how many rows the `INNER JOIN` returns, then run it to check.
