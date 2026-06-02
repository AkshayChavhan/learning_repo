# Python `if`, `elif`, `else`

Decisions in Python.
`if` runs a block when a condition is `True`.
`elif` checks another condition if the first failed.
`else` runs when nothing else matched.

```python
age = 20

if age < 13:
    print("child")
elif age < 18:
    print("teen")
else:
    print("adult")
```

Four key facts:

- Every condition ends with a **`:`**
- The body must be **indented** (4 spaces)
- You can have **many `elif`s**, or none
- `else` is optional, but only **one** per `if`

---

## The simplest form

```python
temperature = 35

if temperature > 30:
    print("It's hot")
```

If the condition is `False`, the block is skipped silently. No error.

---

## `if` + `else`

```python
age = 16

if age >= 18:
    print("adult")
else:
    print("minor")
```

Exactly one of the two blocks runs.

---

## `if` + `elif` + `else`

Use `elif` to chain checks.
Python stops at the **first** `True` condition.

```python
score = 75

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"

print(grade)   # 'B'
```

---

## Conditions

A condition is anything that evaluates to `True` or `False`.

### Comparison operators

| Operator | Meaning            | Example       |
|----------|--------------------|---------------|
| `==`     | Equal              | `x == 5`      |
| `!=`     | Not equal          | `x != 5`      |
| `>`      | Greater than       | `x > 5`       |
| `<`      | Less than          | `x < 5`       |
| `>=`     | Greater or equal   | `x >= 5`      |
| `<=`     | Less or equal      | `x <= 5`      |

```python
x = 10

if x > 5:
    print("big")
if x == 10:
    print("exactly ten")
```

---

## Combining conditions — logical operators

| Operator | Meaning                              |
|----------|--------------------------------------|
| `and`    | True if **both** sides are True      |
| `or`     | True if **at least one** is True     |
| `not`    | Flips True ↔ False                   |

```python
age = 25
has_id = True

if age >= 18 and has_id:
    print("can enter")

day = "Sunday"
if day == "Saturday" or day == "Sunday":
    print("weekend")

logged_in = False
if not logged_in:
    print("please log in")
```

---

## Chained comparisons

Python lets you write natural ranges.

```python
age = 25

if 18 <= age < 65:
    print("working age")
```

Equivalent to `18 <= age and age < 65`, but cleaner.

---

## Truthy / falsy in `if`

You don't always need a comparison.
Any value works directly.

These count as **False**:

```text
False, None, 0, 0.0, "", [], {}, (), set()
```

Everything else is **True**.

```python
name = "Akshay"
if name:                # non-empty string → truthy
    print("got a name")

users = []
if not users:           # empty list → falsy
    print("no users yet")
```

Idiomatic checks:

| Verbose                | Idiomatic        |
|------------------------|------------------|
| `if x == True:`        | `if x:`          |
| `if x == False:`       | `if not x:`      |
| `if x == None:`        | `if x is None:`  |
| `if len(lst) > 0:`     | `if lst:`        |
| `if len(lst) == 0:`    | `if not lst:`    |

---

## Nested `if`

You can put an `if` inside another `if`.

```python
age = 25
has_id = True

if age >= 18:
    if has_id:
        print("can enter")
    else:
        print("no ID")
else:
    print("under 18")
```

Often cleaner to combine with `and`:

```python
if age >= 18 and has_id:
    print("can enter")
```

---

## Short `if` — one-line forms

Single-line `if`:

```python
if x > 0: print("positive")
```

Conditional expression (ternary):

```python
age = 20
label = "adult" if age >= 18 else "minor"
print(label)   # 'adult'
```

Use the ternary form when you're picking one of two values.
Avoid it for complex logic — split into a normal `if` then.

---

## `pass` — do nothing

If you need a block but have nothing to put in it yet:

```python
if x > 100:
    pass        # TODO — handle this later
else:
    print("ok")
```

Empty blocks are a `SyntaxError` in Python.
`pass` fills the gap.

---

## `match` / `case` — pattern matching (Python 3.10+)

A cleaner alternative when you have many `elif`s comparing one value.

```python
status = 404

match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case 500:
        print("Server Error")
    case _:
        print("Unknown")
```

`_` is the default case.
Available from Python 3.10 onward.

---

## Common pitfalls

**1. Using `=` instead of `==`** — assignment vs comparison.

```python
# if x = 5:   # SyntaxError — Python won't let you do this
if x == 5:    # correct
    ...
```

**2. Forgetting the `:`**

```python
# if x > 5      # SyntaxError
if x > 5:
    print("big")
```

**3. Wrong indentation** — Python uses indent to define the block.

**4. Comparing to `None` with `==`** — works, but `is None` is the idiom.

```python
if x is None:
    ...
```

---

## Quick reference

```text
if condition:
    ...
elif other_condition:
    ...
else:
    ...

# comparison:   ==  !=  >  <  >=  <=
# logical:      and  or  not
# chain:        a <= x < b
# ternary:      value_if_true if cond else value_if_false
# do nothing:   pass
# match (3.10+):
#   match value:
#       case 1: ...
#       case _: ...
```
