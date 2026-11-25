# MongoDB Lesson M3: Aggregation Pipelines

## Goal
Build multi-step queries that filter, group, sort, and limit data, and map each step to its SQL clause.

## Key idea
An **aggregation pipeline** is a list of **stages**. Each stage takes the documents from the previous stage, transforms them, and passes the result on.

```
documents → $match → $group → $sort → $limit → results
```

## Sample data

| name | city | marks |
|---|---|---|
| Ravi | Pune | 85 |
| Priya | Mumbai | 92 |
| Akshay | Pune | 78 |
| Neha | Delhi | 66 |
| Sam | Pune | 90 |

```js
db.collection("students").insertMany([
  { name: "Ravi",   city: "Pune",   marks: 85 },
  { name: "Priya",  city: "Mumbai", marks: 92 },
  { name: "Akshay", city: "Pune",   marks: 78 },
  { name: "Neha",   city: "Delhi",  marks: 66 },
  { name: "Sam",    city: "Pune",   marks: 90 }
]);
```

## $match: the WHERE clause

```js
db.collection("students").aggregate([
  { $match: { marks: { $gte: 80 } } }
]);
```

Keeps Ravi, Priya, and Sam. Uses the operators from Lesson M1.

## $group: the GROUP BY clause

```js
db.collection("students").aggregate([
  { $group: { _id: "$city", total: { $sum: 1 } } }
]);
```

| _id | total |
|---|---|
| Pune | 3 |
| Mumbai | 1 |
| Delhi | 1 |

- `_id` is the field to group by. The `$` means "the value of this field."
- `$sum: 1` adds 1 per document, like `COUNT(*)`.

### Accumulators

| Accumulator | SQL equivalent | Example |
|---|---|---|
| `$sum` | `SUM` or `COUNT` | `{ $sum: "$marks" }` |
| `$avg` | `AVG` | `{ $avg: "$marks" }` |
| `$min` | `MIN` | `{ $min: "$marks" }` |
| `$max` | `MAX` | `{ $max: "$marks" }` |
| `$push` | none | Collects values into an array |

```js
db.collection("students").aggregate([
  { $group: { _id: "$city", avgMarks: { $avg: "$marks" } } }
]);
```

## $sort: the ORDER BY clause

```js
db.collection("students").aggregate([
  { $group: { _id: "$city", avgMarks: { $avg: "$marks" } } },
  { $sort: { avgMarks: -1 } }
]);
```

`-1` is descending, `1` is ascending.

## $limit: the LIMIT clause

```js
db.collection("students").aggregate([
  { $sort: { marks: -1 } },
  { $limit: 2 }
]);
```

Returns the top two: Priya (92) and Sam (90).

## $project: choose output fields

```js
db.collection("students").aggregate([
  { $sort: { marks: -1 } },
  { $limit: 2 },
  { $project: { _id: 0, name: 1, marks: 1 } }
]);
```

Works like `SELECT name, marks`. `_id` shows by default, so set it to `0` to hide it.

## Putting it together

**Question:** For students with marks of 80 or more, how many are in each city, largest group first?

**SQL**

```sql
SELECT city, COUNT(*) AS total
FROM students
WHERE marks >= 80
GROUP BY city
ORDER BY total DESC;
```

**MongoDB**

```js
db.collection("students").aggregate([
  { $match: { marks: { $gte: 80 } } },
  { $group: { _id: "$city", total: { $sum: 1 } } },
  { $sort: { total: -1 } }
]);
```

Result: Pune 2, Mumbai 1.

## Clause mapping

| SQL clause | Pipeline stage |
|---|---|
| `WHERE` | `$match` |
| `GROUP BY` with `COUNT`, `SUM`, `AVG` | `$group` |
| `HAVING` | `$match` after `$group` |
| `ORDER BY` | `$sort` |
| `LIMIT` | `$limit` |
| `SELECT` columns | `$project` |

HAVING-style filter, keeping cities with more than one student:

```js
{ $match: { total: { $gt: 1 } } }
```

## $unwind: one document per array item

```js
db.collection("students").aggregate([
  { $unwind: "$hobbies" },
  { $group: { _id: "$hobbies", students: { $sum: 1 } } }
]);
```

Counts how many students have each hobby.

## Gotchas
- **Put `$match` first when you can.** Fewer documents means faster stages.
- **Stage order matters.** `$sort` before `$limit` gives the top results.
- **`$group` drops other fields.** Only `_id` and accumulators remain.
- **Group results have no guaranteed order** without `$sort`.
- **`"$city"` is a value. `city` in `$project` is a field name.**
- **Prisma has limited pipeline support.** Use `groupBy` for simple cases, or the MongoDB driver for complex pipelines.

## Summary
- A pipeline is a list of stages that transform documents step by step.
- `$match`, `$group`, `$sort`, `$limit`, and `$project` map to SQL clauses.
- Filter early and sort before limiting.

## Practice
1. Count the students in each city.
2. Find the highest mark in each city. Hint: `$max`.
3. Show names and marks of Pune students, highest marks first. Hint: `$match`, `$sort`, `$project`.
