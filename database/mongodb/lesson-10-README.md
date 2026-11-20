# Lesson 10: Schema Design and Normalization

## Goal
Learn how to plan tables so each fact is stored in one place, and how to add rules to the database.

## Key idea
A **schema** is the plan for your tables: which tables exist, which columns they have, and how they connect. **Normalization** is the process of designing the schema so each fact is stored in one place.

## A bad design

| order_id | customer_name | customer_city | item     | amount |
|----------|---------------|---------------|----------|--------|
| 10       | Ravi          | Pune          | Laptop   | 55000  |
| 11       | Ravi          | Pune          | Mouse    | 800    |
| 12       | Priya         | Mumbai        | Keyboard | 2500   |

| Problem | What happens |
|---|---|
| **Update** | Ravi moves to Delhi. You must change every row, and missing one causes mismatched data. |
| **Insert** | You can't add a customer who has no orders yet. |
| **Delete** | If Priya cancels her only order, her customer details disappear too. |

## A better design

**customers**

| id | name  | city   |
|----|-------|--------|
| 1  | Ravi  | Pune   |
| 2  | Priya | Mumbai |

**orders**

| id | customer_id | item     | amount |
|----|-------------|----------|--------|
| 10 | 1           | Laptop   | 55000  |
| 11 | 1           | Mouse    | 800    |
| 12 | 2           | Keyboard | 2500   |

Now Ravi's city is stored once, you can add customers without orders, and cancelling an order keeps the customer.

## Normal forms

| Form | Rule | Simple test |
|---|---|---|
| **1NF** | Each cell holds one value | No comma-separated lists in a cell |
| **2NF** | Every column depends on the whole key | No column depends on only part of a combined key |
| **3NF** | Columns depend only on the primary key | `customer_city` shouldn't sit in `orders` |

Breaking 1NF:

| id | name | phones |
|----|------|--------|
| 1  | Ravi | 9876543210, 9123456789 |

Fix: store each phone in its own row in a `phones` table.

## Types and constraints

```sql
CREATE TABLE customers (
  id    INTEGER PRIMARY KEY,
  name  TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  city  TEXT
);

CREATE TABLE orders (
  id          INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  item        TEXT NOT NULL,
  amount      INTEGER NOT NULL CHECK (amount > 0)
);
```

| Keyword | Purpose |
|---|---|
| `NOT NULL` | Value is required |
| `UNIQUE` | No duplicates |
| `REFERENCES` | Foreign key; rejects orders for missing customers |
| `CHECK` | Enforces a rule on the data |

## Denormalization
Sometimes you copy data on purpose to make a common read faster. This is **denormalization**. Use it only when you've measured a real speed problem, and keep the copies in sync.

## Gotchas
- **Normalize first, optimize later.**
- **Don't split tables for no reason.**
- **Think about the questions first.** What will the app read and change most often?
- **Foreign keys need matching types.** `orders.customer_id` must match `customers.id`.

## Summary
- Normalization stores each fact in one place and prevents update, insert, and delete problems.
- 1NF, 2NF, and 3NF are the first three normal forms.
- Constraints enforce rules inside the database.
- Denormalize only with a measured reason.

## Practice
1. In the bad design, which problem happens if Priya cancels her only order?
2. Which normal form does a `phones` column with comma-separated values break?
3. Is having both `city` and `city_pincode` in `customers` a problem? Why?
