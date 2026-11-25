# Lesson 4: Filtering with AND, OR, and LIKE

## Goal
Write queries that match more than one condition and search text by pattern.

## Key idea
`WHERE` picks rows that match a condition. Combine conditions to make the filter more precise.

## AND: both must be true

```sql
SELECT * FROM students WHERE city = 'Pune' AND marks >= 80;
```

Returns students who live in Pune **and** scored 80 or more.

## OR: at least one must be true

```sql
SELECT * FROM students WHERE city = 'Pune' OR city = 'Mumbai';
```

Returns students from Pune **or** Mumbai.

## Brackets: make the grouping clear

```sql
SELECT * FROM students
WHERE (city = 'Pune' OR city = 'Mumbai') AND marks >= 80;
```

## IN: a shorter form of many ORs

```sql
SELECT * FROM students WHERE city IN ('Pune', 'Mumbai');
```

Same result as the OR example above.

## LIKE: match text patterns

| Symbol | Meaning |
|---|---|
| `%` | Any number of characters (including none) |
| `_` | Exactly one character |

```sql
SELECT * FROM students WHERE name LIKE 'A%';     -- starts with A
SELECT * FROM students WHERE name LIKE '%a';     -- ends with a
SELECT * FROM students WHERE name LIKE '%av%';   -- contains "av"
SELECT * FROM students WHERE name LIKE '_avi';   -- 4 letters, ends in "avi"
```

## NOT: reverse a condition

```sql
SELECT * FROM students WHERE NOT city = 'Pune';
SELECT * FROM students WHERE city <> 'Pune';   -- same meaning
```

## Gotchas
- **`AND` is checked before `OR`.** Without brackets, `city = 'Pune' OR city = 'Mumbai' AND marks >= 80` means Pune students of any mark, plus Mumbai students with 80 or more. Use brackets.
- **`LIKE` case sensitivity depends on the database.** `'A%'` may not match `'akshay'` everywhere.
- **`NULL` doesn't work with `=`.** Use `WHERE city IS NULL`. `WHERE city = NULL` returns nothing.

## Summary
- `AND` requires all conditions. `OR` requires at least one.
- Use brackets when mixing `AND` and `OR`.
- `IN` is shorter than several `OR`s.
- `LIKE` with `%` and `_` searches text patterns.
- Use `IS NULL` to find empty values.

## Practice
1. Students with marks between 70 and 90 (try `AND`, then `BETWEEN`).
2. What does `WHERE name LIKE 'R%'` match?
3. Why does `WHERE city = NULL` return nothing?
