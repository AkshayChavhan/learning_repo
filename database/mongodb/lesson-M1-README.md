# MongoDB Lesson M1: Query Operators

## Goal
Filter MongoDB documents with comparison, list, OR, and text-pattern operators, and compare each one with SQL.

## Key idea
In SQL you filter with `WHERE`. In MongoDB you pass an object to `find()`. Words starting with `$` are **operators** that do the work of SQL's comparison words.

## Sample data

```js
db.collection("students").insertMany([
  { name: "Ravi",   city: "Pune",   marks: 85 },
  { name: "Priya",  city: "Mumbai", marks: 92 },
  { name: "Akshay", city: "Pune",   marks: 78 },
  { name: "Neha",   city: "Delhi",  marks: 66 }
]);
```

## Equality

```js
db.collection("students").find({ city: "Pune" });   // WHERE city = 'Pune'
```

A plain `field: value` pair means "equals."

## Comparison operators

| MongoDB | Meaning | SQL |
|---|---|---|
| `$eq` | equal | `=` |
| `$ne` | not equal | `<>` |
| `$gt` / `$gte` | greater (or equal) | `>` / `>=` |
| `$lt` / `$lte` | less (or equal) | `<` / `<=` |

```js
db.collection("students").find({ marks: { $gt: 80 } });
db.collection("students").find({ marks: { $gte: 70, $lte: 90 } });
db.collection("students").find({ city: { $ne: "Pune" } });
```

## $in and $nin

```js
db.collection("students").find({ city: { $in: ["Pune", "Mumbai"] } });
```

Same as `IN ('Pune', 'Mumbai')`. `$nin` means "not in."

## AND

```js
db.collection("students").find({ city: "Pune", marks: { $gt: 80 } });
```

Conditions in the same object are combined with AND.

## OR

```js
db.collection("students").find({
  $or: [ { city: "Pune" }, { marks: { $gt: 90 } } ]
});
```

## Text pattern

```js
db.collection("students").find({ name: { $regex: "^A" } });   // like LIKE 'A%'
```

`^` means "starts with." `$regex` is the closest equivalent to `LIKE`.

## Checking a field exists

```js
db.collection("students").find({ email: { $exists: true } });
```

## Side by side

| What you want | SQL | MongoDB |
|---|---|---|
| Pune students | `WHERE city = 'Pune'` | `{ city: "Pune" }` |
| Marks above 80 | `WHERE marks > 80` | `{ marks: { $gt: 80 } }` |
| Pune and above 80 | `WHERE city = 'Pune' AND marks > 80` | `{ city: "Pune", marks: { $gt: 80 } }` |
| Pune or above 90 | `WHERE city = 'Pune' OR marks > 90` | `{ $or: [{ city: "Pune" }, { marks: { $gt: 90 } }] }` |
| City in a list | `WHERE city IN ('Pune','Mumbai')` | `{ city: { $in: ["Pune","Mumbai"] } }` |
| Names starting with A | `WHERE name LIKE 'A%'` | `{ name: { $regex: "^A" } }` |

## Prisma version
Prisma uses friendlier names:

```js
await prisma.student.findMany({ where: { marks: { gt: 80 } } });
await prisma.student.findMany({ where: { city: { in: ["Pune", "Mumbai"] } } });
```

## Gotchas
- **Operators go inside an object:** `{ $gt: 80 }`, not `{ gt: 80 }`.
- **Types matter.** The text `"85"` doesn't match `$gt: 80`.
- **`find()` returns a cursor.** Add `.toArray()` to get an array.
- **Missing fields are not null.** Use `$exists` when you need precision.

## Summary
- Plain `field: value` means equality.
- Comparison operators go inside a nested object.
- Conditions in one object are combined with AND.
- `$or` and `$in` handle OR-style and list-style checks.

## Practice
1. Students with marks between 70 and 85.
2. Students from Delhi or Mumbai.
3. Pune students with marks below 80.
