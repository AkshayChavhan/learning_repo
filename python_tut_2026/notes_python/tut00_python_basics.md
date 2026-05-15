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
