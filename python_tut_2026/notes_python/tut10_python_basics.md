# tut00 — Python Basics (prerequisites for Objects)

> Just enough Python to make [`tut01_object.md`](tut01_object.md) land. If you already know another language, this chapter is mostly *"how does Python spell this thing?"* — short and brisk.

---

## 0.1 — Running Python & the REPL

**Concept.** There are three ways you'll run Python during this course:

1. **A script file** — write code in `something.py`, run it with `python something.py`. This is the default for everything we save in `python_basics/`.
2. **The REPL** (Read–Eval–Print–Loop) — run `python` with no arguments and you get an interactive prompt (`>>>`). Type an expression, it prints the value. Great for poking at things.
3. **A one-liner** — `python -c "print(2+2)"` runs a single statement from the command line. Useful in shell scripts.

**Three details that trip people up:**

- **No semicolons, no braces.** Python uses **indentation** to mark blocks. The indentation level must be consistent within a block (4 spaces is the convention).
- **`print()` is a function, not a statement.** Parentheses are required: `print("hi")`. (Python 2 differed; ignore Python 2.)
- **The REPL auto-displays expressions.** In a `.py` file, just writing `2 + 2` produces no output — you must `print(2 + 2)`. In the REPL, typing `2 + 2` shows `4` because the REPL prints the value of every expression.

**Comments.**

```python
# Single-line comment with #
x = 5  # comments can also trail code

"""
A triple-quoted string used at the top of a function/class/module
acts as a docstring — accessible via help() and __doc__.
A bare triple-quoted string elsewhere is a no-op expression that
people sometimes (mis)use as a multi-line comment.
"""
```

**Coming from Java/C++/JS:**

- No `main()` function is required to run a file — top-level code runs top to bottom. (There *is* a `if __name__ == "__main__":` idiom — sub-topic 0.8.)
- No compile step. `python file.py` runs straight from source. (Internally it compiles to bytecode and caches in `__pycache__/`, but that's invisible.)
- No braces means **whitespace is syntax**. Mixing tabs and spaces is a *syntax error* in Python 3.

**Pitfalls.**

1. **`IndentationError`** — the most common first-week error. Always use the same indent (4 spaces) inside a block. Configure your editor to insert spaces for Tab.
2. **Running the wrong Python.** Many systems have both `python` (old Python 2) and `python3`. On modern Linux/Mac, `python3` is safe; on Windows, `python` usually works. We'll just say `python` in this course — substitute whichever is on your PATH.
3. **Forgetting parentheses on `print`** — gives `SyntaxError`.

**Runnable examples:** [`../python_basics/00a_running_python.py`](../python_basics/00a_running_python.py)

**Run it:**
```bash
python "Python Tut 2026/python_basics/00a_running_python.py"
```

**Try the REPL too:**
```bash
python
>>> 2 + 2
4
>>> name = "Akshay"
>>> f"Hello, {name}!"
'Hello, Akshay!'
>>> exit()   # or Ctrl-D
```

---

## 0.2 — Variables, names, and assignment

**Concept.** The single most important sentence about Python variables:

> **A variable is a name bound to an object.** It is not a box that holds a value; it is a *label* pointing at a value.

When you write `x = 5`:

1. Python creates (or reuses) the integer object `5`.
2. The name `x` is bound to that object in the current namespace.

When you later write `x = "hi"`:

1. Python creates the string object `"hi"`.
2. The name `x` is re-bound to the new object. The old `5` is unaffected and (if no other name references it) eventually garbage-collected.

This is why Python is **dynamically typed**: the *name* `x` has no type — the *object* it points to does. A name can point to any object, and you can rebind it to a different type any time.

**Three rules of names.**

1. **No declarations.** First assignment creates the name. `int x;` doesn't exist in Python.
2. **No type on the name.** `x = 5; x = "hi"` is legal. Type hints (`x: int = 5`) are optional documentation, not enforced at runtime.
3. **Multiple names can point to the same object.** `a = b` makes `a` *another label* for the object `b` points to — no copy is made.

**Tools to introspect names and bindings:**

| What you want to know | How |
|---|---|
| What type is bound to `x`? | `type(x)` |
| Are `a` and `b` the same object? | `a is b` |
| What's the object's identity? | `id(x)` |
| What names exist in the current scope? | `dir()` (no args) |
| What's bound to a specific name (as a dict)? | `globals()`, `locals()` |

**Assignment forms.**

```python
x = 5                    # simple assignment
x, y = 1, 2              # tuple unpacking (very Pythonic)
x, y = y, x              # swap — no temp variable needed
a = b = c = 0            # chained: all three names → same object
first, *rest = [1, 2, 3] # extended unpacking: first=1, rest=[2,3]
x: int = 5               # annotated assignment (type hint, optional)
```

**Augmented assignment** (`+=`, `-=`, etc.) has a subtlety:

- For **immutable** objects (`int`, `str`, `tuple`), `x += 1` is equivalent to `x = x + 1` — a *new* object is created, `x` is rebound.
- For **mutable** objects (`list`), `lst += [4]` calls `lst.__iadd__([4])` which mutates the list in place. Same object, just changed.

**Coming from Java/C++/JS:**

- **Java/C++:** Drop the mental model of "variables are typed boxes." Python is closer to Java's *reference* variables — only references exist, no primitives. Assignment never copies.
- **JS:** Closest analogue. Python's `x = …` is like JS `let x = …` (no declaration keyword). But Python has no `const`. Convention is `UPPER_SNAKE_CASE` for constants, enforced by discipline, not the language.
- **C:** A Python name is *not* a pointer you can manipulate. You can't dereference it, take its address, or do pointer arithmetic. You can only rebind it.

**Naming rules and conventions.**

- **Rules:** letters, digits, underscores; can't start with a digit; case-sensitive (`Name` ≠ `name`); can't be a reserved keyword (`for`, `class`, `lambda`, etc.). See `import keyword; print(keyword.kwlist)`.
- **PEP 8 conventions** (style guide everyone follows):
  - `snake_case` for variables, functions, modules: `user_count`, `read_file`.
  - `PascalCase` for classes: `UserAccount`.
  - `UPPER_SNAKE_CASE` for constants: `MAX_RETRIES`.
  - `_leading_underscore` = "internal, don't touch" (convention, not enforced).
  - `__double_leading_underscore` = name mangling (covered in tut01.7).
  - `__dunder__` = reserved for Python's protocol methods. Don't invent your own.

**Pitfalls.**

1. **Shadowing built-ins.** Don't name a variable `list`, `dict`, `str`, `id`, `type`, `sum`, `max`. You'll silently lose access to the built-in for the rest of that scope.
2. **`UnboundLocalError`.** Inside a function, if you *assign* to a name anywhere in the function, Python treats it as local *for the whole function* — even on lines before the assignment. Touching it before the assignment raises `UnboundLocalError`. (Real fix is `global` or `nonlocal`; covered in tut00.7.)
3. **Assuming `a = b` copies.** For mutable objects, both names now point to the same object. Modify through one, see the change through the other.
4. **Confusing `=` (assignment) with `==` (equality).** `if x = 5:` is a SyntaxError in Python — unlike C, you can't accidentally use `=` in a condition. (Walrus `:=` is the explicit "assign-in-expression" form, added in 3.8.)

**Runnable examples:** [`../python_basics/00b_variables.py`](../python_basics/00b_variables.py)

**Run it:**
```bash
python3 "python_tut_2026/python_basics/00b_variables.py"
```

---

## 0.3 — Basic types & literals

**Concept.** Python's built-in basic types — what you'll use 95% of the time before you write your own classes. Each type has a **literal syntax** (how you write a value of that type directly in source code).

| Type | Literal example | What it is |
|---|---|---|
| `int` | `42`, `-7`, `0`, `1_000_000` | Arbitrary-precision integer |
| `float` | `3.14`, `1.5e-3`, `inf`, `nan` | 64-bit IEEE-754 double |
| `bool` | `True`, `False` | A subtype of `int` (`True == 1`, `False == 0`) |
| `str` | `"hi"`, `'hi'`, `"""multi"""` | Immutable Unicode text |
| `bytes` | `b"raw"`, `b'\\x00\\xff'` | Immutable raw bytes |
| `NoneType` | `None` | The single "no value" sentinel |
| `complex` | `3+4j` | Complex number (rare) |

> All literals you type evaluate to objects. `42` is the same kind of thing as `[1,2,3]` — an object Python creates and you can pass around.

### `int` — unlimited size

Python ints aren't 32- or 64-bit. They grow as needed.

```python
2 ** 200    # 1606938044258990275541962092341162602522202993782792835301376
```

**Different number bases:**

```python
255          # decimal
0xff         # hex   → 255
0o377        # octal → 255
0b11111111   # binary → 255
1_000_000    # underscores allowed for readability
```

### `float` — IEEE-754 doubles

Same as Java `double` or C `double`. **Has the usual floating-point precision issues** — `0.1 + 0.2` is **not** exactly `0.3`. Use `decimal.Decimal` for money, `math.isclose` for approximate equality.

```python
3.14
1.5e-3       # scientific notation → 0.0015
float("inf") # positive infinity
float("nan") # not a number — interestingly, nan != nan
```

### `bool` — a flavor of `int`

This is unusual: `bool` is a *subclass* of `int`. So `True + True == 2`, `isinstance(True, int) == True`. Useful trick: summing booleans counts how many are `True`.

```python
sum([True, False, True, True])   # 3
```

**Truthiness** — every object can be tested with `if x:`. Falsy values:

- `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `()`, `set()`
- Everything else is truthy (including `"False"`, `[0]`, `{0: None}`).

```python
if name:                 # idiomatic — true if name is non-empty
    print("got a name")
```

Don't write `if x == True:` — write `if x:`. Don't write `if x == None:` — write `if x is None:`.

### `str` — immutable Unicode

(Full deep-dive in tut00.4.) Three quote styles, all interchangeable except triple-quoted spans lines.

```python
'single'
"double"
"""triple — spans
multiple lines"""
f"f-string: 2+2 = {2+2}"
r"raw string: \n is two chars"
```

### `None` — the one and only

There is **exactly one** `None` object. Test with `is`, never `==`. Used for:

- Default function returns when there's no explicit `return`.
- Sentinel meaning "no value yet" / "not set".

```python
def f():
    pass

f() is None    # True
```

### Conversion (constructors)

Each type's name is also its constructor:

```python
int("42")        # 42 — parse string to int
int("ff", 16)    # 255 — with base
int(3.9)         # 3   — TRUNCATES toward zero (not rounding)
float("3.14")    # 3.14
str(42)          # '42'
bool(0)          # False
bool("False")    # True (!) — non-empty string is truthy
list("abc")      # ['a', 'b', 'c']
```

### `type()` vs `isinstance()`

```python
type(x) is int               # exact match — usually NOT what you want
isinstance(x, int)           # x is int OR a subclass of int (e.g., bool!)
isinstance(x, (int, float))  # one of several types
```

Use `isinstance` by default. Use `type(x) is …` only when you specifically want to reject subclasses.

**Coming from Java/C++/JS:**

- **Java:** No `int` vs `Integer` distinction. Every Python value is an object.
- **C/C++:** No fixed-width ints by default. Use `numpy` types or the `array`/`struct` modules when you need width.
- **JS:** Python distinguishes `int` and `float` (JS has one `number`). And **integer division** is a separate operator: `/` is true division (returns float), `//` is floor division (returns int when both operands are int).

```python
7 / 2     # 3.5    (true division — always float)
7 // 2    # 3      (floor division)
7 % 2     # 1      (modulo)
2 ** 10   # 1024   (power — not ^)
```

### Pitfalls

1. **`/` is always float**, even for two ints. `1 / 1` is `1.0`, not `1`. Use `//` for int division.
2. **`bool` is `int`** — `isinstance(True, int)` is `True`. Sometimes surprising in JSON / API code.
3. **Floating-point equality.** `0.1 + 0.2 == 0.3` is `False`. Use `math.isclose(a, b)`.
4. **`int("3.9")` is a `ValueError`** — `int()` won't parse a string with a decimal point. Use `int(float("3.9"))`.
5. **`bool("False")` is `True`** — because `"False"` is a non-empty string. To parse a string to a bool, write your own helper or use `argparse`/`distutils.util.strtobool`.

**Runnable examples:** [`../python_basics/00c_basic_types.py`](../python_basics/00c_basic_types.py)

**Run it:**
```bash
python3 "python_tut_2026/python_basics/00c_basic_types.py"
```
