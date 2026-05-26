# Python Indentation

In Python, indentation is **syntax**, not style.
Spaces at the start of a line decide which block of code that line belongs to.
Other languages use `{ }`.
Python uses whitespace.

---

## Rule 1 — A block starts after `:`

`if`, `for`, `while`, `def`, `class`, `try`, `with` — all end with `:`.
The next line must be indented.

```python
if age >= 18:
    print("adult")
    print("can vote")
print("done")
```

`adult` and `can vote` are inside the `if`.
`done` is outside.

---

## Rule 2 — Use 4 spaces per level

This is the official Python convention (PEP 8).
Don't mix with 2 or 8 spaces in the same file.

```python
def greet(name):
    if name:
        print(f"Hi, {name}")
    else:
        print("Hi, stranger")
```

`def` is at the top.
`if`/`else` are 4 spaces in.
The `print` lines are 8 spaces in.

---

## Rule 3 — Indentation must be consistent in one block

Every line in the same block must use the **same** indent.

```python
if True:
    print("ok")
    print("ok")
      print("broken")    # IndentationError
```

The third `print` has different spacing → Python errors out.

---

## Rule 4 — Never mix tabs and spaces

In Python 3 this is a hard error (`TabError`).
Pick spaces, always spaces.
Configure your editor to insert spaces when you press Tab.

---

## Common errors

`IndentationError: expected an indented block`
You wrote `if x:` but the next line wasn't indented.

`IndentationError: unexpected indent`
A line is indented but nothing above it opened a block.

`IndentationError: unindent does not match any outer indentation level`
You dedented to a level no enclosing block uses.

`TabError: inconsistent use of tabs and spaces`
Some lines use tabs, others spaces.

---

## A full example

```python
def classify(n):
    if n > 0:
        if n % 2 == 0:
            return "positive even"
        else:
            return "positive odd"
    elif n == 0:
        return "zero"
    else:
        return "negative"

print(classify(4))
print(classify(-3))
```

Output:

```text
positive even
negative
```

Each indent level = one block deeper.
Dedenting closes the inner block.

---

## Editor setup that saves hours

In VS Code:

- Set `"editor.insertSpaces": true`
- Set `"editor.tabSize": 4`

Both are the default — just don't change them.
