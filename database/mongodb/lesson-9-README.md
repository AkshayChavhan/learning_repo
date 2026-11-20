# Lesson 9: Document Databases and MongoDB

## Goal
Understand how MongoDB stores data as documents and how its basic operations compare with SQL.

## Key idea
SQL stores data in **tables** with fixed columns. A **document database** stores data as **documents**, which look like JavaScript objects. **MongoDB** is the most popular one.

```js
{ name: "Ravi", city: "Pune", marks: 85 }
```

## Three words to learn

| SQL | MongoDB | Meaning |
|---|---|---|
| Table | **Collection** | A group of related items |
| Row | **Document** | One item |
| Column | **Field** | One piece of information |

## Same student, two styles

| id | name | city | marks |
|----|------|------|-------|
| 1  | Ravi | Pune | 85    |

```js
{ _id: 1, name: "Ravi", city: "Pune", marks: 85 }
```

`_id` is MongoDB's version of a primary key. MongoDB creates one automatically if you don't provide it.

## Basic operations

```js
// Create
db.collection("students").insertOne({ name: "Ravi", city: "Pune", marks: 85 });

// Read
db.collection("students").find({ city: "Pune" });

// Update
db.collection("students").updateOne({ name: "Ravi" }, { $set: { marks: 88 } });

// Delete
db.collection("students").deleteOne({ name: "Ravi" });
```

| What you want | SQL | MongoDB |
|---|---|---|
| Add | `INSERT INTO students ...` | `insertOne({...})` |
| Find | `SELECT * FROM students WHERE city = 'Pune'` | `find({ city: "Pune" })` |
| Change | `UPDATE students SET marks = 88 WHERE name = 'Ravi'` | `updateOne({ name: "Ravi" }, { $set: { marks: 88 } })` |
| Remove | `DELETE FROM students WHERE name = 'Ravi'` | `deleteOne({ name: "Ravi" })` |

MongoDB uses JavaScript-style code, not SQL.

## Flexible shape
Documents in one collection can have different fields:

```js
{ name: "Ravi", city: "Pune", marks: 85 }
{ name: "Priya", email: "priya@example.com", hobbies: ["dance"] }
```

## Nested data
Related data can sit inside one document:

```js
{
  name: "Ravi",
  city: "Pune",
  orders: [
    { item: "Laptop", amount: 55000 },
    { item: "Mouse", amount: 800 }
  ]
}
```

Reading Ravi and his orders takes one read, with no join.

## When to choose which

| Your data | Usually better |
|---|---|
| Clear relationships between separate things | SQL |
| Strict rules and many joins | SQL |
| Items with different shapes, like product catalogs | MongoDB |
| Data read together as one unit, like a blog post with comments | MongoDB |

## Gotchas
- **"Flexible" doesn't mean "no rules."** `marks` could be stored as text in one document and a number in another.
- **Duplicate data is common.** You may copy a customer's name into many documents.
- **Documents have a 16 MB limit.** Don't put an unlimited list inside one document.

## Summary
- MongoDB stores **documents** in **collections**.
- Documents in one collection can have different fields.
- MongoDB uses JavaScript-style queries, not SQL.

## Practice
1. Write a query that finds all students with marks above 80. Hint: `$gt`.
2. Why can two documents in one collection have different fields?
3. Give one example where you'd choose MongoDB and one where you'd choose SQL.
