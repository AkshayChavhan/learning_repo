# MongoDB Lesson M2: Updating Documents

## Goal
Change fields, numbers, arrays, and nested data in MongoDB documents.

## Key idea
Use `updateOne` or `updateMany` with **update operators** that start with `$`. Without an operator, MongoDB replaces the whole document.

## Sample data

```js
db.collection("students").insertMany([
  { name: "Ravi",  city: "Pune",   marks: 85, hobbies: ["cricket"] },
  { name: "Priya", city: "Mumbai", marks: 92, hobbies: ["dance", "music"] },
  { name: "Neha",  city: "Delhi",  marks: 66, hobbies: [] }
]);
```

## $set: change or add a field

```js
db.collection("students").updateOne({ name: "Ravi" }, { $set: { marks: 88 } });
db.collection("students").updateOne({ name: "Ravi" }, { $set: { email: "ravi@example.com" } });
```

Like `UPDATE students SET marks = 88 WHERE name = 'Ravi'`. Other fields stay the same.

## updateMany

```js
db.collection("students").updateMany({ city: "Pune" }, { $set: { region: "West" } });
```

`updateOne` changes the first match. `updateMany` changes all matches. An empty filter `{}` changes every document.

## $inc: change a number

```js
db.collection("students").updateOne({ name: "Neha" }, { $inc: { marks: 5 } });
```

Safer than reading, adding in JavaScript, and saving back, because two updates at once can overwrite each other.

## $unset: remove a field

```js
db.collection("students").updateOne({ name: "Ravi" }, { $unset: { email: "" } });
```

## Arrays

```js
// Add, even if duplicate
db.collection("students").updateOne({ name: "Ravi" }, { $push: { hobbies: "chess" } });

// Remove every matching item
db.collection("students").updateOne({ name: "Priya" }, { $pull: { hobbies: "music" } });

// Add only if not already there
db.collection("students").updateOne({ name: "Neha" }, { $addToSet: { hobbies: "painting" } });
```

| Operator | Effect |
|---|---|
| `$push` | Adds an item, even a duplicate |
| `$addToSet` | Adds only if missing |
| `$pull` | Removes matching items |

## Nested fields: dot notation

```js
{ name: "Ravi", address: { city: "Pune", pincode: "411001" } }

db.collection("students").updateOne(
  { name: "Ravi" },
  { $set: { "address.pincode": "411038" } }
);
```

Quotes are needed around the dotted name. `city` stays unchanged.

## replaceOne

```js
db.collection("students").replaceOne(
  { name: "Ravi" },
  { name: "Ravi", city: "Pune", marks: 90 }
);
```

Removes every field not in the new document. Use only when you want that.

## Upsert

```js
db.collection("students").updateOne(
  { name: "Sam" },
  { $set: { city: "Chennai", marks: 70 } },
  { upsert: true }
);
```

Inserts a new document if no match exists, otherwise updates the existing one.

## SQL comparison

| What you want | SQL | MongoDB |
|---|---|---|
| Change a field | `UPDATE students SET marks = 88 WHERE name = 'Ravi'` | `updateOne({ name: "Ravi" }, { $set: { marks: 88 } })` |
| Add to a number | `SET marks = marks + 5` | `{ $inc: { marks: 5 } }` |
| Add to a list | Usually a separate table | `{ $push: { hobbies: "chess" } }` |

## Prisma version

```js
await prisma.student.update({ where: { id: "1" }, data: { marks: 88 } });
await prisma.student.update({ where: { id: "1" }, data: { marks: { increment: 5 } } });
await prisma.student.update({ where: { id: "1" }, data: { hobbies: { push: "chess" } } });
```

## Gotchas
- **Always use an operator.** A plain object replaces the document.
- **`updateMany({}, ...)` changes everything.** Check the filter.
- **`$push` allows duplicates.** Use `$addToSet` for unique items.
- **Dot notation needs quotes:** `"address.city"`.

## Summary
- `$set` changes or adds, `$unset` removes.
- `$inc` changes numbers safely.
- `$push`, `$addToSet`, and `$pull` work on arrays.
- Dot notation reaches nested fields.

## Practice
1. Set Neha's city to `"Bengaluru"`.
2. Add the hobby `"football"` to Ravi, only if it isn't already there.
3. Increase all Pune students' marks by 2. Which function, and why?
