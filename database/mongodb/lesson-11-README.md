# Lesson 11: Prisma, an ORM

## Goal
Understand what Prisma is, how it fits between your code and the database, and how it maps to the SQL you already learned.

## Key idea
**Prisma** is an **ORM** (Object-Relational Mapper). It sits between your JavaScript code and the database. You describe your data in one file, and Prisma gives you typed functions to read and write it.

```
Your JavaScript code  →  Prisma Client  →  Database (PostgreSQL, MySQL, SQLite, or MongoDB)
```

Prisma writes the SQL (or MongoDB commands) for you, but the real database is still underneath.

## Step 1: describe the data in `schema.prisma`

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model Customer {
  id     Int     @id @default(autoincrement())
  name   String
  city   String?
  orders Order[]
}

model Order {
  id         Int      @id @default(autoincrement())
  item       String
  amount     Int
  customer   Customer @relation(fields: [customerId], references: [id])
  customerId Int
}
```

| Line | Meaning in SQL |
|---|---|
| `model Customer` | A table called `Customer` |
| `id Int @id` | Primary key |
| `name String` | `NOT NULL` text column |
| `city String?` | Nullable text column |
| `orders Order[]` | A relation, not a column |
| `customerId Int` | Foreign key column |
| `@relation(...)` | Foreign key constraint |

## Step 2: create the tables

```bash
npx prisma migrate dev --name init
```

For MongoDB, use `npx prisma db push` instead, because MongoDB has no migrations.

## Step 3: use the Prisma Client

```js
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

await prisma.customer.create({ data: { name: "Ravi", city: "Pune" } });

await prisma.order.create({
  data: { item: "Laptop", amount: 55000, customerId: 1 },
});

// Customer with orders (the JOIN from Lesson 6)
const ravi = await prisma.customer.findUnique({
  where: { id: 1 },
  include: { orders: true },
});

await prisma.customer.update({ where: { id: 1 }, data: { city: "Delhi" } });

await prisma.order.delete({ where: { id: 10 } });
```

## Prisma compared with SQL

| What you want | Raw SQL | Prisma |
|---|---|---|
| Add | `INSERT INTO customers ...` | `prisma.customer.create({ data })` |
| Find one | `SELECT ... WHERE id = 1` | `prisma.customer.findUnique({ where: { id: 1 } })` |
| Find many | `SELECT ... WHERE city = 'Pune'` | `prisma.customer.findMany({ where: { city: "Pune" } })` |
| Join | `JOIN orders ON ...` | `include: { orders: true }` |
| Count | `SELECT COUNT(*) FROM orders` | `prisma.order.count()` |
| Change | `UPDATE ... SET ... WHERE ...` | `prisma.customer.update({ where, data })` |
| Remove | `DELETE FROM ... WHERE ...` | `prisma.order.delete({ where })` |

## Prisma with MongoDB

```prisma
datasource db {
  provider = "mongodb"
  url      = env("DATABASE_URL")
}

model Customer {
  id     String  @id @default(auto()) @map("_id") @db.ObjectId
  name   String
  city   String?
  orders Order[]
}
```

- MongoDB's `_id` is mapped to `id`.
- Use `db push`, not `migrate`.

## Gotchas
- **Prisma doesn't replace SQL knowledge.** Read the generated SQL when a query is slow, and understand indexes.
- **Keep one Prisma Client.** In Next.js, create it once and reuse it, or you may exhaust database connections.
- **`findUnique` needs a unique field.** Use `findFirst` or `findMany` for other filters.
- **Use migrations** instead of editing tables by hand, so the schema and database stay in sync.
- **Relations aren't loaded automatically.** Without `include`, related data is missing.

## Summary
- Prisma is an ORM that lets you use JavaScript instead of writing SQL for everyday tasks.
- `schema.prisma` describes models, fields, and relations.
- Migrations (SQL) or `db push` (MongoDB) create the structure.
- `include` replaces joins.

## Practice
1. Write a Prisma query that finds all customers in Pune, including their orders.
2. In the `Order` model, which line creates the foreign key?
3. What does `city String?` mean compared with `city String`?
