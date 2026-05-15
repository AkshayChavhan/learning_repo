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
