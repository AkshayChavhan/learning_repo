# Python File I/O & Exception Handling

Two topics that almost always show up together — you read a file, the file might not exist, you handle the error. This chapter covers both.

```text
                 ┌────────────────────────────┐
                 │  FILE I/O  +  EXCEPTIONS   │
                 └────────────────────────────┘
                              │
        ┌──────────────────┬──┴────────┬──────────────────┐
        ▼                  ▼           ▼                  ▼
       OPEN             READ/WRITE    CLOSE            ERRORS
   open(path, mode)     read/write    with-block       try/except
   "r" "w" "a" "x"      readlines     auto closes      raise / finally
   text vs binary       writelines    no manual        custom Exception
```

---

# Part 1 — File I/O

Python's built-in `open()` is the gateway to files. Always use it with a `with` block so the file closes automatically.

## The basic shape

```python
with open("hello.txt", "w") as f:
    f.write("Hello, file!\n")

with open("hello.txt", "r") as f:
    content = f.read()

print(content)
```

```text
Hello, file!
```

The `with` block:

- Opens the file.
- Hands you the file object as `f`.
- **Guarantees** the file is closed when the block exits — even if an exception is raised inside.

---

## File modes

The second argument to `open()`.

| Mode  | Meaning                                                 | If file exists | If file missing |
|-------|---------------------------------------------------------|----------------|-----------------|
| `"r"` | Read (default)                                          | OK             | `FileNotFoundError` |
| `"w"` | Write — **truncates** to empty first                    | Overwritten    | Created         |
| `"a"` | Append — writes at the end                              | Appended       | Created         |
| `"x"` | Exclusive create — fails if file exists                 | `FileExistsError` | Created      |
| `"r+"`| Read **and** write (no truncation)                      | OK             | `FileNotFoundError` |
| `"b"` | Binary mode — combine with another, e.g. `"rb"`, `"wb"` | —              | —               |
| `"t"` | Text mode (default) — combine, e.g. `"rt"`              | —              | —               |

Common combos: `"r"`, `"w"`, `"a"`, `"rb"`, `"wb"`, `"r+"`.

```python
# Text read (default)
with open("notes.txt", "r") as f:
    print(f.read())

# Truncate + write
with open("notes.txt", "w") as f:
    f.write("fresh start\n")

# Append
with open("notes.txt", "a") as f:
    f.write("another line\n")

# Binary (don't decode bytes — useful for images, PDFs, etc.)
with open("image.png", "rb") as f:
    raw = f.read()
print(type(raw).__name__, len(raw), "bytes")
```

---

## Reading — three ways

```python
# 1. Whole file as one string
with open("notes.txt") as f:
    text = f.read()

# 2. All lines as a list of strings (keeps trailing \n)
with open("notes.txt") as f:
    lines = f.readlines()

# 3. One line at a time — best for huge files (constant memory)
with open("notes.txt") as f:
    for line in f:
        print(line.rstrip())   # strip trailing newline
```

Rule of thumb: use **#3** unless the file is small. `for line in f:` only loads one line at a time.

---

## Writing — two ways

```python
# Single string
with open("out.txt", "w") as f:
    f.write("line 1\n")
    f.write("line 2\n")        # write() does NOT add newline

# Many lines at once (you supply the newlines)
lines = ["a\n", "b\n", "c\n"]
with open("out.txt", "w") as f:
    f.writelines(lines)        # NOT writelines + "\n" between
```

`write()` returns the number of characters written. `writelines()` does **not** add separators — you must include `\n` yourself.

---

## Encoding ★

Always specify the encoding for text files. The default is platform-dependent.

```python
# Safe — explicit utf-8
with open("notes.txt", "r", encoding="utf-8") as f:
    text = f.read()

with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("café\n")
```

If you don't pass `encoding=`, Python uses the platform default — `utf-8` on Linux/Mac, often `cp1252` on Windows. That mismatch is the #1 cause of `UnicodeDecodeError`.

Binary mode (`"rb"`, `"wb"`) **never** decodes — you get raw `bytes`.

---

## Useful file object attributes

```python
with open("notes.txt") as f:
    print(f.name)        # 'notes.txt'
    print(f.mode)        # 'r'
    print(f.encoding)    # 'UTF-8' (or platform default)
    print(f.closed)      # False
print(f.closed)          # True  — auto-closed
```

---

## Working with paths — `pathlib` ★

`pathlib` is the modern way to handle paths. It works on Windows and Linux/Mac identically.

```python
from pathlib import Path

p = Path("notes.txt")

# One-shot read / write — no need for open() / with
p.write_text("hi from pathlib\n", encoding="utf-8")
text = p.read_text(encoding="utf-8")
print(text)

# Check things
print(p.exists())            # True
print(p.is_file())           # True
print(p.is_dir())            # False
print(p.suffix)              # '.txt'
print(p.stem)                # 'notes'
print(p.parent)              # '.'
print(p.absolute())          # /current/working/dir/notes.txt

# Build paths with / (no string concatenation)
log_dir = Path("logs")
log_file = log_dir / "app.log"
print(log_file)              # logs/app.log

# Delete
# p.unlink()                 # remove file
```

Prefer `pathlib` over `os.path` for new code.

---

# Part 2 — Exception Handling

When Python hits an error it can't recover from, it raises an **exception**. Without a handler, the program crashes with a traceback. With one, you decide what to do.

## The basic shape

```python
try:
    n = int(input("Enter a number: "))
    print("Got:", n)
except ValueError:
    print("Not a number.")
```

If the user types `"abc"`, `int(...)` raises `ValueError`. The `except` block catches it. The program continues.

---

## `try / except / else / finally`

All four clauses, in order:

```python
try:
    # the risky code
    n = int("42")
except ValueError as e:
    # ran ONLY if a ValueError was raised
    print("bad number:", e)
else:
    # ran ONLY if NO exception was raised
    print("parsed:", n)
finally:
    # ALWAYS runs — cleanup, regardless of success or failure
    print("done")
```

```text
parsed: 42
done
```

| Clause     | When it runs                                            |
|------------|---------------------------------------------------------|
| `try`      | Always — the protected code                             |
| `except`   | Only if a matching exception is raised                  |
| `else`     | Only if NO exception was raised                         |
| `finally`  | Always — even if you `return` or re-`raise`              |

`else` is useful when you want code that only runs on success but **outside** the protected block (so you don't accidentally catch errors from that code too).

---

## Catching specific exceptions

Always be **specific** — never catch `Exception` (or worse, bare `except:`) unless you know exactly why.

```python
try:
    with open("nope.txt") as f:
        data = f.read()
except FileNotFoundError:
    print("file is missing")
except PermissionError:
    print("can't read it")
```

Multiple types at once with a tuple:

```python
try:
    risky()
except (ValueError, TypeError) as e:
    print("data problem:", e)
```

---

## Catching the exception object

`except SomeError as e:` binds the exception to `e`. You can inspect it.

```python
try:
    1 / 0
except ZeroDivisionError as e:
    print(type(e).__name__)   # 'ZeroDivisionError'
    print(str(e))             # 'division by zero'
    print(e.args)              # ('division by zero',)
```

---

## Common built-in exceptions

| Exception              | When it fires                                            |
|------------------------|----------------------------------------------------------|
| `ValueError`           | Right type, bad value — `int("abc")`                     |
| `TypeError`            | Wrong type — `"3" + 4`                                   |
| `KeyError`             | Missing dict key — `d["nope"]`                           |
| `IndexError`           | List index out of range — `lst[99]`                      |
| `AttributeError`       | Missing attribute / method — `"hi".does_not_exist()`     |
| `FileNotFoundError`    | Can't find a file                                        |
| `PermissionError`      | OS denied access                                         |
| `ZeroDivisionError`    | `x / 0` for ints / floats                                |
| `StopIteration`        | Iterator exhausted                                       |
| `KeyboardInterrupt`    | User pressed Ctrl-C                                      |
| `ImportError`, `ModuleNotFoundError` | Failed import                              |
| `RuntimeError`         | Generic — usually re-raise rather than handle            |

All of these inherit from `Exception`, which inherits from `BaseException`.

---

## `raise` — throwing your own exception

```python
def get_age(years):
    if years < 0:
        raise ValueError(f"age can't be negative: {years}")
    return years

# get_age(-5)        # ValueError: age can't be negative: -5
```

You can re-raise after partial handling:

```python
try:
    risky()
except ValueError:
    print("logging the bad input")
    raise              # re-raise the same exception — bubbles up
```

Chain with `raise … from`:

```python
try:
    int("abc")
except ValueError as e:
    raise RuntimeError("config parse failed") from e
```

The traceback shows both the original and the new exception — useful for clarity.

---

## Custom exceptions

Define your own by subclassing `Exception`.

```python
class AccountLockedError(Exception):
    """Raised when an account is locked due to failed attempts."""

def login(user, password):
    if user.locked:
        raise AccountLockedError(f"account {user.name} is locked")
```

Custom exceptions help callers catch *your* errors specifically:

```python
try:
    login(user, pwd)
except AccountLockedError:
    show_lockout_message()
```

---

## `else` — code that runs only on success

A common pattern: open + parse + use, but only "use" if "parse" worked.

```python
try:
    with open("config.json") as f:
        text = f.read()
    data = json.loads(text)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print("bad config:", e)
else:
    # ran only if no exception above
    print("loaded", len(data), "keys")
```

Without `else`, the success code would be inside `try`, and any exception there would *also* be caught — usually not what you want.

---

## `finally` — always runs

Use it for cleanup that must happen no matter what. (For files, prefer `with` — but `finally` is needed when there's no context manager.)

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        print("safe_divide finished")
```

`finally` runs even if the `try` block executes `return`, `break`, or re-raises.

---

## File + exception together — a real pattern

```python
from pathlib import Path
import json

def load_config(path):
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"config missing at {p}, using defaults")
        return {}
    except PermissionError:
        print(f"can't read {p}")
        return {}

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"bad JSON in {p}: {e}")
        return {}

print(load_config("missing_or_bad.json"))
```

```text
config missing at missing_or_bad.json, using defaults
{}
```

This is the everyday shape — specific exceptions, specific recoveries, no bare `except`.

---

## EAFP vs LBYL ★

Python idiomatically prefers **EAFP** ("Easier to Ask Forgiveness than Permission") — just try, catch on failure — over **LBYL** ("Look Before You Leap") — checking everything first.

```python
# LBYL — race-y, verbose
if os.path.exists(path):
    with open(path) as f:
        data = f.read()

# EAFP — preferred, no race
try:
    with open(path) as f:
        data = f.read()
except FileNotFoundError:
    data = None
```

The `os.path.exists` check + `open` has a race — the file can vanish between them. EAFP avoids that.

---

## Common pitfalls

### 1. Bare `except`

```python
# DON'T — swallows everything including KeyboardInterrupt and SystemExit
try:
    risky()
except:                        # <-- bare except
    pass
```

It hides bugs. Catch the specific exception you expect.

### 2. Catching `Exception` casually

```python
# DON'T (usually)
try:
    risky()
except Exception:
    pass
```

It hides logic errors (`AttributeError`, `KeyError`) that should bubble up. Use it only at the top of a long-running service where you log + re-raise or restart.

### 3. Not closing the file

Without `with`, you must close it manually — and it won't close if an exception is raised before `close()`.

```python
# Fragile
f = open("data.txt")
data = f.read()
f.close()

# Always
with open("data.txt") as f:
    data = f.read()
```

### 4. `writelines()` doesn't add newlines

```python
with open("out.txt", "w") as f:
    f.writelines(["a", "b", "c"])   # writes 'abc', not 'a\nb\nc'
```

Add the newlines yourself.

### 5. Reading a huge file with `read()` or `readlines()`

Both load the whole file into memory. For large files, iterate:

```python
with open("huge.log") as f:
    for line in f:
        if "ERROR" in line:
            print(line.rstrip())
```

### 6. Forgetting `encoding="utf-8"`

Especially on Windows. Always pass it for text files.

### 7. Catching too broadly hides the real error

```python
# Hides any AttributeError typos in your own code
try:
    user.do_something()
except Exception:
    pass
```

Catch what you expect; let the rest crash loudly during development.

---

## Quick reference

```text
# FILE I/O ---------------------------------------------------
with open(path, mode, encoding="utf-8") as f:
    text = f.read()                # whole file
    lines = f.readlines()          # list[str]
    for line in f: ...             # one at a time — best for big files

with open(path, "w", encoding="utf-8") as f:
    f.write(s)
    f.writelines(list_of_strings)  # you supply '\n'

# modes
"r"  read              "w"  write/truncate     "a"  append
"x"  exclusive create  "rb"/"wb" binary       "r+" read+write

# pathlib (modern)
from pathlib import Path
p = Path("notes.txt")
p.write_text(text)
text = p.read_text()
p.exists()  p.is_file()  p.is_dir()  p.suffix  p.stem  p.parent

# EXCEPTIONS -------------------------------------------------
try:
    risky()
except (ValueError, TypeError) as e:
    handle(e)
else:
    print("succeeded")
finally:
    cleanup()

raise ValueError("bad input")            # throw
raise RuntimeError("wrapper") from e     # chain

class MyError(Exception):                # custom
    pass

# common exceptions
ValueError TypeError KeyError IndexError AttributeError
FileNotFoundError PermissionError ZeroDivisionError
StopIteration KeyboardInterrupt ImportError

# EAFP idiom — try first, handle on failure
try:
    with open(path) as f: ...
except FileNotFoundError:
    ...
```
