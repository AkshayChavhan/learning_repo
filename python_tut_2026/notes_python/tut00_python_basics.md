# tut00 — Python Basics

Just enough Python to make Objects (tut01) feel natural.
Each sub-topic = short notes + a runnable `.py` file in `../python_basics/`.

---

## 0.1 — Running Python & the REPL

There are three ways to run Python.

**1. A script file.**
Write code in `something.py`, then run it from a terminal.

```bash
python3 something.py
```

**2. The REPL** (interactive prompt).
Type `python3` with no arguments.
Each line is evaluated immediately.

```text
$ python3
>>> 2 + 2
4
>>> name = "Akshay"
>>> f"Hello, {name}!"
'Hello, Akshay!'
>>> exit()
```

**3. A one-liner.**

```bash
python3 -c "print(2 + 2)"
```

---

### `print()` is a function

Parentheses are required.

```python
print("hi")
```

---

### Indentation defines blocks

No braces.
4 spaces per level.

```python
if x > 5:
    print("big")
    print("still inside")
print("outside")
```

---

### Bare expressions are silent in a script

The REPL shows the value of any expression you type.
A `.py` file does not — you must call `print()`.

```python
2 + 2          # script: nothing shown
print(2 + 2)   # script: 4
```

---

### Comments and docstrings

```python
# single-line comment
x = 5  # trailing comment

def greet(name):
    """A docstring — stored in greet.__doc__."""
    return f"Hi, {name}!"
```

---

### Common first-week errors

`SyntaxError` → missing parentheses on `print`, missing `:`, or a typo.
`IndentationError` → mixed or inconsistent indent.
`TabError` → tabs mixed with spaces.

---

**Runnable examples:** [`../python_basics/00a_running_python.py`](../python_basics/00a_running_python.py)

```bash
python3 "python_tut_2026/python_basics/00a_running_python.py"
```

---

## 0.2 — Variables, names, and assignment

The single most important sentence:

> A variable is a **name bound to an object**.
> Not a box that holds a value.
> A label pointing at a value.

When you write `x = 5`:

1. Python creates the integer object `5`.
2. The name `x` is bound to it.

When you write `x = "hi"` after:

1. Python creates the string object `"hi"`.
2. `x` is re-bound to the new object.
3. The old `5` is unaffected.

---

### No declarations, no fixed type

First assignment creates the name.
The name has no type — the object does.

```python
x = 5
print(type(x).__name__)   # int

x = "hello"
print(type(x).__name__)   # str
```

---

### `a = b` does not copy

Both names point to the **same** object.

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)   # [1, 2, 3, 4]
```

Mutate through one name → see the change through the other.

---

### Rebinding is not mutation

`a = [99]` makes `a` point to a new list.
`b` still points to the old one.

```python
a = [1, 2, 3]
b = a
a = [99]
print(a)   # [99]
print(b)   # [1, 2, 3]
```

---

### Unpacking

Assign several names in one shot.

```python
x, y = 1, 2
x, y = y, x          # swap, no temp variable
first, *rest = [10, 20, 30, 40]
```

---

### Chained assignment

All names point to the **same** object.

```python
p = q = r = []
p.append("oops")
print(q)   # ['oops']
```

If you wanted three separate empty lists, do it explicitly:

```python
p, q, r = [], [], []
```

---

### Type hints are documentation, not enforcement

```python
age: int = 30
age = "thirty"   # legal! Python does not check at runtime.
```

Tools like `mypy` and `pyright` check hints.
Python itself ignores them.

---

### Don't shadow built-ins

Names like `list`, `dict`, `str`, `id`, `type`, `sum`, `max` are built-in.
Don't reuse them.

```python
list = [1, 2, 3]     # now list() the type is hidden in this scope
```

---

### Naming conventions (PEP 8)

- `snake_case` → variables, functions, modules
- `PascalCase` → classes
- `UPPER_SNAKE_CASE` → constants
- `_leading_underscore` → "internal, don't touch"
- `__dunder__` → reserved for Python's protocols

---

**Runnable examples:** [`../python_basics/00b_variables.py`](../python_basics/00b_variables.py)

```bash
python3 "python_tut_2026/python_basics/00b_variables.py"
```

---

## 0.3 — Basic types & literals

The built-in types you'll use 95% of the time.

| Type    | Example literal           | What it is                         |
|---------|---------------------------|------------------------------------|
| `int`   | `42`, `-7`, `1_000_000`   | Arbitrary-precision integer        |
| `float` | `3.14`, `1.5e-3`          | 64-bit IEEE-754 double             |
| `bool`  | `True`, `False`           | A subtype of `int`                 |
| `str`   | `"hi"`, `'hi'`            | Immutable text                     |
| `None`  | `None`                    | The single "no value" object       |

---

### `int` — unlimited size

Python integers grow as needed.
No 32- or 64-bit cap.

```python
print(2 ** 200)
```

Different bases:

```python
print(0xff)       # 255 — hex
print(0o377)      # 255 — octal
print(0b1111)     # 15  — binary
print(1_000_000)  # underscores for readability
```

---

### `float` — has precision gotchas

Same as Java `double` or C `double`.

```python
print(0.1 + 0.2)               # 0.30000000000000004
print(0.1 + 0.2 == 0.3)        # False
```

Use `math.isclose` to compare floats safely.

```python
import math
print(math.isclose(0.1 + 0.2, 0.3))   # True
```

---

### Division operators

```python
print(7 / 2)    # 3.5   — true division, always float
print(7 // 2)   # 3     — floor division
print(7 % 2)    # 1     — modulo
print(2 ** 10)  # 1024  — power
```

`//` rounds toward negative infinity:

```python
print(-7 // 2)   # -4, not -3
```

---

### `bool` is a subtype of `int`

`True == 1`, `False == 0`.

```python
print(True + True)            # 2
print(sum([True, False, True]))  # 2
```

---

### Truthiness

Every object can be tested with `if x:`.

Falsy values:

```text
False, None, 0, 0.0, "", [], {}, (), set()
```

Everything else is truthy.

Surprises:

```python
print(bool("False"))   # True — non-empty string
print(bool([0]))       # True — list has one item
```

---

### `None` — the one sentinel

There is exactly one `None`.
Check with `is`, never `==`.

```python
def f():
    pass

print(f() is None)   # True
```

---

### Type conversions

The type name is the constructor.

```python
print(int("42"))        # 42
print(int("ff", 16))    # 255
print(int(3.9))         # 3   — TRUNCATES, doesn't round
print(float("3.14"))    # 3.14
print(str(42))          # '42'
print(list("abc"))      # ['a', 'b', 'c']
```

Common error — `int()` won't parse a decimal string:

```python
int("3.9")   # ValueError
```

Workaround:

```python
int(float("3.9"))   # 3
```

---

### `type()` vs `isinstance()`

`isinstance` accepts subclasses (so `bool` counts as `int`).
Use `isinstance` by default.

```python
print(type(True) is int)        # False — type is bool
print(isinstance(True, int))    # True  — bool is a subclass
```

Check against several types in one call:

```python
isinstance(x, (int, float))
```

---

### Three "huh?" facts worth remembering

1. `0.1 + 0.2 != 0.3` — floating point.
2. `True + True == 2` — bool *is* int.
3. `round(2.5) == 2` and `round(3.5) == 4` — Python rounds half-to-even.

---

**Runnable examples:** [`../python_basics/00c_basic_types.py`](../python_basics/00c_basic_types.py)

```bash
python3 "python_tut_2026/python_basics/00c_basic_types.py"
```
