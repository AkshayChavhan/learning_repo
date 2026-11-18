# Lesson 2: How Tables Connect

## Goal
Understand why data is split across tables and how tables link to each other with keys.

## Key idea
Real apps store different kinds of things in separate tables. Each table holds one kind of data, and tables are connected by IDs.

## Example: a shop

**customers**

| id | name  | city   |
|----|-------|--------|
| 1  | Ravi  | Pune   |
| 2  | Priya | Mumbai |

**orders**

| id | customer_id | item     | amount |
|----|-------------|--------|--------|
| 10 | 1           | Laptop   | 55000  |
| 11 | 1           | Mouse    | 800    |
| 12 | 2           | Keyboard | 2500   |

## Foreign key
A **foreign key** is a column that stores a primary key from another table.

- `orders.customer_id` is a foreign key.
- It points to `customers.id`.
- The foreign key lives in the **child** table (`orders`). The parent table (`customers`) doesn't store its children.

## Why not copy the customer's name into each order?
1. **One source of truth:** if Ravi moves to Delhi, you change one row, not every order.
2. **No mismatched data:** you avoid "Ravi" in one order and "Ravee" in another.
3. **Less storage:** a small number takes less space than a long name repeated many times.

## Relationship types

| Type | Meaning | Example |
|---|---|---|
| **One-to-many** | One row relates to many rows | One customer, many orders |
| **One-to-one** | One row relates to exactly one row | One user, one profile |
| **Many-to-many** | Needs a third table in between | Students and courses (through an `enrollments` table) |

## Finding Ravi's orders

```sql
SELECT orders.item, orders.amount
FROM orders
JOIN customers ON orders.customer_id = customers.id
WHERE customers.name = 'Ravi';
```

Read it as: match each order to its customer, then keep only Ravi's orders. (Joins are covered in detail in Lesson 6.)

## Summary
- A foreign key links a row to a row in another table.
- Store the ID, not a copy of the data.
- The main relationship in most apps is one-to-many.

## Practice
1. In `orders`, which column is the foreign key, and what does it point to?
2. Why is storing `customer_id` better than storing the customer's name?
3. What kind of relationship is one customer with many orders?
