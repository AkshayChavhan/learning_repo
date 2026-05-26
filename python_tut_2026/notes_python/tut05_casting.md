# Python Casting (Type Conversion)

**Casting** means converting a value from one type to another.
In Python, you cast by calling the type name as a function.

```python
int("42")     # str → int
str(99)       # int → str
float("3.14") # str → float
```

| From → To       | Function   | Example              | Result    |
|-----------------|------------|----------------------|-----------|
| `str` → `int`   | `int()`    | `int("42")`          | `42`      |
| `str` → `float` | `float()`  | `float("3.14")`      | `3.14`    |
| `int` → `str`   | `str()`    | `str(99)`            | `"99"`    |
| `float` → `int` | `int()`    | `int(3.9)`           | `3`       |
| `int` → `float` | `float()`  | `float(5)`            | `5.0`     |
| anything → `bool` | `bool()` | `bool(0)`             | `False`   |

---

## Why cast?

Python doesn't auto-convert types in many places.
`input()` always returns a string — even if the user types a number.

```python
age = input("Your age: ")   # always a str
print(age + 1)              # TypeError — can't add str and int
```

You must cast first:

```python
age = int(input("Your age: "))
print(age + 1)
```

---

## `int(...)` — to whole number

From a string:

```python
print(int("42"))    # 42
print(int("-7"))    # -7
print(int("  10 ")) # 10  — whitespace is OK
```

From a float — **truncates** toward zero, doesn't round:

```python
print(int(3.9))    #  3
print(int(-3.9))   # -3
print(int(0.999))  #  0
```

From other bases:

```python
print(int("ff", 16))   # 255  — hex string
print(int("1010", 2))  # 10   — binary string
```

**Can fail** — a string with a decimal point won't parse:

```python
# int("3.9")   # ValueError
print(int(float("3.9")))   # 3 — go through float first
```

---

## `float(...)` — to decimal number

```python
print(float("3.14"))   # 3.14
print(float("1e3"))    # 1000.0
print(float(5))        # 5.0
print(float(True))     # 1.0
```

Special strings:

```python
print(float("inf"))    # infinity
print(float("nan"))    # not a number
```

---

## `str(...)` — to text

Works on almost anything.

```python
print(str(42))         # '42'
print(str(3.14))       # '3.14'
print(str(True))       # 'True'
print(str([1, 2, 3]))  # '[1, 2, 3]'
print(str(None))       # 'None'
```

For numbers in a sentence, f-strings are usually cleaner:

```python
age = 30
print("Age: " + str(age))   # works
print(f"Age: {age}")        # cleaner
```

---

## `bool(...)` — to True / False

These values become `False`:

```text
False, None, 0, 0.0, "", [], {}, (), set()
```

Everything else becomes `True`.

```python
print(bool(0))        # False
print(bool(""))       # False
print(bool([]))       # False
print(bool(None))     # False

print(bool(1))        # True
print(bool("hi"))     # True
print(bool([0]))      # True   — list has one item
print(bool("False"))  # True   — non-empty string!
```

Common trap: `"False"` (the string) is **truthy**, because it's a non-empty string.
To parse a string to a real bool, write it yourself:

```python
def to_bool(s):
    return s.strip().lower() in ("true", "1", "yes", "y")

print(to_bool("True"))    # True
print(to_bool("no"))      # False
```

---

## `list(...)`, `tuple(...)`, `set(...)`

Convert between collections.

```python
print(list("abc"))       # ['a', 'b', 'c']
print(list((1, 2, 3)))   # [1, 2, 3]

print(tuple([1, 2, 3]))  # (1, 2, 3)

print(set([1, 1, 2, 3])) # {1, 2, 3}  — duplicates removed
print(set("hello"))      # {'h', 'e', 'l', 'o'}
```

---

## Common casting errors

```python
int("abc")     # ValueError: invalid literal for int()
int("3.9")     # ValueError: int() can't parse a decimal string
float("3,14")  # ValueError: comma is not a decimal point
int(None)      # TypeError: int() argument can't be None
```

Wrap in `try/except` when input might be bad:

```python
raw = input("Enter a number: ")

try:
    n = int(raw)
    print("Got:", n)
except ValueError:
    print("That wasn't a valid number.")
```

---

## Real-world example

```python
# User types ages separated by commas, e.g. "25,30,18"
raw = input("Enter ages, comma-separated: ")
ages = [int(x.strip()) for x in raw.split(",")]

print("Total:", sum(ages))
print("Average:", sum(ages) / len(ages))
```

What happens here:

1. `input()` returns a `str`.
2. `.split(",")` makes a list of strings.
3. `int(x.strip())` casts each one to `int`.
4. `sum` / `len` give the totals.

---

## Quick reference

```text
int(x)     → whole number
float(x)   → decimal number
str(x)     → text
bool(x)    → True / False
list(x)    → list from iterable
tuple(x)   → tuple from iterable
set(x)     → set from iterable (drops duplicates)
```

```text
type(x)            → tells you what type x is
isinstance(x, T)   → True if x is type T (or a subclass)
```
