# Lesson 5: Sorting, Limiting, and Counting

## Goal
Control the order of results, limit how many rows you get, and count or summarize data.

## ORDER BY: sort results

```sql
SELECT name, marks FROM students ORDER BY marks;          -- lowest to highest (default)
SELECT name, marks FROM students ORDER BY marks DESC;     -- highest to lowest
SELECT name, marks FROM students ORDER BY city, name;     -- city first, then name
```

- `ASC` = ascending (default).
- `DESC` = descending.
- A second column breaks ties in the first.

## LIMIT: return only some rows

```sql
SELECT name, marks FROM students ORDER BY marks DESC LIMIT 3;   -- top 3 scorers
```

`LIMIT` runs after sorting. Without `ORDER BY`, the three rows are unpredictable.

SQL Server uses `TOP` instead of `LIMIT`.

## COUNT: count rows

```sql
SELECT COUNT(*) FROM students;
SELECT COUNT(*) FROM students WHERE city = 'Pune';
```

## Aggregate functions

An **aggregate** takes many rows and returns one value.

| Function | Returns | Example |
|---|---|---|
| `COUNT(*)` | Number of rows | How many students? |
| `SUM(column)` | Total | Total marks |
| `AVG(column)` | Average | Average mark |
| `MIN(column)` | Smallest value | Lowest mark |
| `MAX(column)` | Largest value | Highest mark |

```sql
SELECT AVG(marks) FROM students;
SELECT MAX(marks), MIN(marks) FROM students;
```

## GROUP BY: aggregate per group

```sql
SELECT city, COUNT(*) AS total_students
FROM students
GROUP BY city;
```

Read it as: group the students by city, then count each group.

## HAVING: filter groups

```sql
SELECT city, COUNT(*) FROM students
GROUP BY city
HAVING COUNT(*) > 1;
```

- `WHERE` filters **rows** before grouping.
- `HAVING` filters **groups** after grouping.

## Gotchas
- **`LIMIT` without `ORDER BY` is unpredictable.**
- **A plain column and an aggregate need `GROUP BY`.** `SELECT name, COUNT(*) FROM students;` fails.
- **`COUNT(*)` counts all rows.** `COUNT(column)` skips NULL values in that column.

## Summary
- `ORDER BY` sorts. `DESC` reverses the order.
- `LIMIT` returns the first N rows after sorting.
- Aggregates (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) summarize many rows.
- `GROUP BY` summarizes per group. `HAVING` filters groups.

## Practice
1. Show the two lowest marks with their names.
2. What is the difference between `WHERE` and `HAVING`?
3. Why does `SELECT name, COUNT(*) FROM students;` cause an error?
