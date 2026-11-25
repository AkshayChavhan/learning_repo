# Lesson 1: What is a Database?

## Goal
Understand what data is, why apps need databases, and the basic parts of a table.

## Key idea
**Data** is information stored as facts. Every app stores data: users, orders, students, marks.

A **database** is software that stores, finds, and protects data, even when many people use it at once.

## Why not Excel or a notebook?
A spreadsheet works for a small list, but it fails when:
- Many people write at the same time and overwrite each other.
- The data grows to thousands or millions of rows.
- You need fast answers to questions like "all students who scored above 80."
- The computer crashes in the middle of a save and the file gets damaged.

## Tables, rows, and columns

| id | name   | city   | marks |
|----|--------|--------|-------|
| 1  | Ravi   | Pune   | 85    |
| 2  | Priya  | Mumbai | 92    |
| 3  | Akshay | Pune   | 78    |

| Term | Meaning | Example above |
|---|---|---|
| **Table** | A group of related data | The whole list |
| **Row** (record) | One complete entry | Ravi's row |
| **Column** (field) | One type of information, present in every row | `city` |
| **Primary key** | A unique value that identifies one row | `id` |

The primary key must be **unique** (no repeats) and **never empty**.

## First SQL example

```sql
CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  name TEXT,
  city TEXT,
  marks INTEGER
);

INSERT INTO students VALUES (1, 'Ravi', 'Pune', 85);
INSERT INTO students VALUES (2, 'Priya', 'Mumbai', 92);
INSERT INTO students VALUES (3, 'Akshay', 'Pune', 78);

SELECT * FROM students;
SELECT name FROM students WHERE marks > 80;
```

Try it in DB Fiddle (SQLite). Predict the output before you run each line.

## Common confusions
- **Database vs. database software:** the database is the data. The software (MySQL, PostgreSQL, SQLite, MongoDB) manages it.
- **Row vs. column:** a row is one record. A column is one field that every row has.

## Summary
- A database stores data safely, finds it quickly, and protects it from bad entries.
- Data is organized in tables made of rows and columns.
- Each row gets a primary key so it can be identified.

## Practice
1. In the `students` table, what is a row and what is a column?
2. Why might a spreadsheet stop being enough for an app?
3. Why is the primary key useful?
