# Comments & `print()`

Two things you'll use in every Python file.
Comments explain code to humans.
`print()` shows values on the screen.

---

## Comments

A comment is a line Python ignores.
Start it with `#`.

```python
# This is a comment.
age = 25       # comments can also sit at the end of a line
```

Use comments to explain **why**, not **what**.

Good — explains why:

```python
retries = 3   # API sometimes flakes; retry a few times
```

Bad — just repeats the code:

```python
x = x + 1     # add 1 to x
```

For a longer note, stack `#` lines:

```python
# This script downloads daily sales data,
# cleans it, and saves a CSV for the dashboard.
```

---

## `print()` — talk to the screen

`print()` is a function, so it always needs `( )`.

### Printing text

Text goes inside quotes.
Single `'…'` or double `"…"`, both work.

```python
print("Hello, world!")
print('Single or double, both fine')
```

Output:

```text
Hello, world!
Single or double, both fine
```

### Printing numbers

No quotes for numbers.
Quotes would turn them into text.

```python
print(42)
print(3.14)
print(-7)
```

Output:

```text
42
3.14
-7
```

### Printing calculations

Pass an expression.
Python solves it, then prints the result.

```python
print(2 + 3)
print(10 * 4)
print(100 / 7)
print(2 ** 8)
```

Output:

```text
5
40
14.285714285714286
256
```

### Mixing text and numbers — commas

Pass several items separated by commas.
`print()` joins them with spaces.

```python
name = "Akshay"
age = 30
print("Name:", name, "Age:", age)
print("2 + 3 =", 2 + 3)
```

Output:

```text
Name: Akshay Age: 30
2 + 3 = 5
```

### Mixing text and numbers — f-strings (cleaner)

Put `f` before the quote.
Drop variables or expressions inside `{ }`.

```python
name = "Akshay"
age = 30
print(f"{name} is {age} years old")
print(f"2 + 3 = {2 + 3}")
```

Output:

```text
Akshay is 30 years old
2 + 3 = 5
```

---

That's it.
Comments document your intent.
`print()` shows results.
