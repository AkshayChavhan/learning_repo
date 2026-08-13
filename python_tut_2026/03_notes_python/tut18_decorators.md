# Python Decorators

A **decorator** is a function that takes another function and returns a new function — usually one that wraps the original to add behavior **before** or **after** it runs.

```python
@timer
def slow():
    ...
```

The `@timer` line means: replace `slow` with `timer(slow)`.

Three key facts:

- A decorator is just a **function that takes a function**.
- It returns a **new function** (the "wrapper").
- The `@` syntax is **shorthand** — nothing magical underneath.

The shape:

```text
@decorator
def target():
    ...

# is exactly the same as:

def target():
    ...
target = decorator(target)
```

---

## Prerequisite recap — functions are first-class

You already saw this in tut17.
A function is a value. Pass it, return it, store it in a variable.

```python
def shout(text):
    return text.upper()

f = shout                 # store the function
print(f("hi"))            # 'HI'

def call_it(fn, value):   # pass a function
    return fn(value)

print(call_it(shout, "hi"))   # 'HI'
```

```text
HI
HI
```

This is the only trick a decorator relies on.

---

## The manual way

Write a wrapper, then **replace** the original name with the wrapper.

```python
def shout(fn):
    def wrapper():
        return fn().upper()
    return wrapper

def hello():
    return "hello"

hello = shout(hello)      # replace hello with the wrapper

print(hello())            # 'HELLO'
```

```text
HELLO
```

What happened:

- `shout(hello)` returned `wrapper`.
- The name `hello` now points to `wrapper`.
- Calling `hello()` runs `wrapper()`, which calls the original and uppercases the result.

The original function isn't gone — `wrapper` still holds a reference to it via `fn`.

---

## The `@` syntax

`@shout` above `def hello` does **exactly** the same thing.

```python
def shout(fn):
    def wrapper():
        return fn().upper()
    return wrapper

@shout
def hello():
    return "hello"

print(hello())            # 'HELLO'
```

```text
HELLO
```

Side-by-side:

```text
@shout                       def hello():
def hello():                     return "hello"
    return "hello"           hello = shout(hello)
```

Both rebind `hello` to `shout(hello)`. The `@` form is just nicer to read.

---

## Decorating a function that takes arguments

The wrapper must accept whatever the original accepts.
The safe pattern: `*args, **kwargs`, then pass them through.

```python
def shout(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return result.upper()
    return wrapper

@shout
def greet(name, greeting="Hello"):
    return greeting + ", " + name

print(greet("Akshay"))
print(greet("Akshay", greeting="Hi"))
```

```text
HELLO, AKSHAY
HI, AKSHAY
```

Why `*args, **kwargs`? You don't know — and don't want to know — every signature your decorator might wrap. Pass everything through.

---

## A real-world example — timer

Measure how long a function takes.

```python
import time

def timer(fn):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(fn.__name__, "took", round(elapsed * 1000, 2), "ms")
        return result
    return wrapper

@timer
def slow_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

print(slow_sum(1_000_000))
```

```text
slow_sum took 38.21 ms
499999500000
```

The exact ms varies — the point is you added timing without touching `slow_sum`.

---

## Another useful one — logger

Print arguments and return value.

```python
def log(fn):
    def wrapper(*args, **kwargs):
        print("call", fn.__name__, "args=", args, "kwargs=", kwargs)
        result = fn(*args, **kwargs)
        print("  -> returned", result)
        return result
    return wrapper

@log
def add(a, b):
    return a + b

add(2, 3)
add(10, b=5)
```

```text
call add args= (2, 3) kwargs= {}
  -> returned 5
call add args= (10,) kwargs= {'b': 5}
  -> returned 15
```

Great for quick debugging — drop `@log` on any function, see what it gets and what it gives back.

---

## The metadata problem

After decoration, `__name__` and `__doc__` point to the **wrapper**, not the original.

```python
def shout(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name):
    """Return a friendly greeting."""
    return "Hello, " + name

print(greet.__name__)     # wrapper  (we wanted 'greet')
print(greet.__doc__)      # None     (we wanted the docstring)
```

```text
wrapper
None
```

`help(greet)` would also show `wrapper`. Useless for introspection.

---

## `functools.wraps` — preserve metadata

`@functools.wraps(fn)` copies the original's `__name__`, `__doc__`, and friends onto the wrapper.

```python
import functools

def shout(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name):
    """Return a friendly greeting."""
    return "Hello, " + name

print(greet.__name__)     # 'greet'
print(greet.__doc__)      # 'Return a friendly greeting.'
```

```text
greet
Return a friendly greeting.
```

Rule of thumb: **always** put `@functools.wraps(fn)` on your wrapper. It costs one line and avoids surprises.

---

## Decorators with arguments

Sometimes you want to configure the decorator itself — for example, "repeat this function 3 times".

That needs **three levels** of nesting:

- Outer: takes the **decorator's arguments**.
- Middle: takes the **function**.
- Inner: takes the **call's arguments**.

```python
import functools

def repeat(n):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def hello(name):
    print("hello,", name)
    return name

hello("Akshay")
```

```text
hello, Akshay
hello, Akshay
hello, Akshay
```

Read `@repeat(3)` as: call `repeat(3)`, get back a real decorator, then apply it to `hello`.

The three layers, in plain English:

| Level   | Takes                | Returns        |
|---------|----------------------|----------------|
| outer   | decorator's config   | the decorator  |
| middle  | the function         | the wrapper    |
| inner   | the call's `*args`   | the call's result |

---

## Stacking decorators

You can apply more than one. They stack **bottom-up**.

```python
import functools

def bold(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return "<b>" + fn(*args, **kwargs) + "</b>"
    return wrapper

def italic(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return "<i>" + fn(*args, **kwargs) + "</i>"
    return wrapper

@bold
@italic
def greet(name):
    return "hello, " + name

print(greet("Akshay"))
```

```text
<b><i>hello, Akshay</i></b>
```

How to read it:

- `@italic` is applied **first** (closest to `def`).
- Then `@bold` is applied to the result.
- So the final function is `bold(italic(greet))`.

Swap the order and the output changes:

```python
import functools

def bold(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return "<b>" + fn(*args, **kwargs) + "</b>"
    return wrapper

def italic(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return "<i>" + fn(*args, **kwargs) + "</i>"
    return wrapper

@italic
@bold
def greet(name):
    return "hello, " + name

print(greet("Akshay"))    # <i><b>hello, Akshay</b></i>
```

```text
<i><b>hello, Akshay</b></i>
```

---

## Class-method decorators you'll meet

You've already seen `@` on methods. Three built-ins worth naming now:

| Decorator        | What it does                                              |
|------------------|-----------------------------------------------------------|
| `@property`      | Turns a method into a read-only attribute                 |
| `@staticmethod`  | Method that doesn't take `self` or `cls`                  |
| `@classmethod`   | Method whose first argument is the class, not an instance |

These belong to the OOP chapter — just know they're the same `@` syntax, applied to methods inside a class. No magic.

---

## Useful built-ins from `functools`

### `@functools.lru_cache` — caching

Caches results so the same arguments don't recompute.

```python
import functools

@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30))
print(fib.cache_info())
```

```text
832040
CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
```

Without the cache, `fib(30)` makes millions of calls. With it, each `n` is computed once.

### `@functools.cache` — the 3.9+ shortcut

Same idea as `lru_cache(maxsize=None)`, just shorter. **Python 3.9 or newer.**

```python
# Python 3.9+ only:
# import functools
#
# @functools.cache
# def fib(n):
#     if n < 2:
#         return n
#     return fib(n - 1) + fib(n - 2)
#
# print(fib(50))   # 12586269025
```

On Python 3.8, stick with `@functools.lru_cache(maxsize=None)` — it does the same thing.

Use `lru_cache(maxsize=128)` (or any limit) when you want a **bounded** cache that drops old entries. Use `cache` / `lru_cache(maxsize=None)` when you want unlimited memoization.

---

## Common pitfalls

### 1. Forgetting `*args, **kwargs` in the wrapper

A wrapper with no parameters works for **no-argument** functions only.

```python
def shout(fn):
    def wrapper():               # accepts nothing
        return fn().upper()
    return wrapper

@shout
def greet(name):
    return "hello, " + name

# greet("Akshay")
# TypeError: wrapper() takes 0 positional arguments but 1 was given
```

Fix — accept everything and pass it through:

```python
def shout(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name):
    return "hello, " + name

print(greet("Akshay"))           # 'HELLO, AKSHAY'
```

### 2. Forgetting `@functools.wraps`

Without it, introspection breaks — `__name__`, `__doc__`, and `help()` all point to `wrapper`.

```python
import functools

def log(fn):
    @functools.wraps(fn)         # add this — always
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

@log
def add(a, b):
    """Add two numbers."""
    return a + b

print(add.__name__)              # 'add'
print(add.__doc__)               # 'Add two numbers.'
```

### 3. Decorators run at **definition** time, not call time

The body of the decorator executes when Python first sees the `@`.

```python
def loud(fn):
    print("decorating", fn.__name__)     # runs at import / def time
    def wrapper(*args, **kwargs):
        print("calling", fn.__name__)    # runs when the function is called
        return fn(*args, **kwargs)
    return wrapper

@loud
def greet(name):
    return "hi, " + name

print("---")
greet("Akshay")
```

```text
decorating greet
---
calling greet
```

`decorating greet` printed **before** anything called `greet`. Side effects in a decorator's body fire on definition.

### 4. Order matters when stacking

`@a` over `@b` is not the same as `@b` over `@a`. The closest decorator to `def` is applied first.

```python
def add_one(fn):
    def wrapper(x):
        return fn(x) + 1
    return wrapper

def double(fn):
    def wrapper(x):
        return fn(x) * 2
    return wrapper

@add_one
@double
def f(x):
    return x

@double
@add_one
def g(x):
    return x

print(f(5))      # double first: 10, then +1 -> 11
print(g(5))      # +1 first: 6, then double -> 12
```

```text
11
12
```

---

## When NOT to use a decorator

Decorators are a hammer. Not everything is a nail.

- Don't write a decorator for a **one-off** bit of logic — just inline it.
- Don't decorate to "make code look fancy" — clarity wins.
- Don't hide important behavior in a decorator (auth, transactions, retries can all be fine — but **name them clearly** so a reader knows what `@retry` actually does).
- If you only need the behavior in one place, a plain function call is shorter and easier to read.

Decorators shine when:

- The **same** cross-cutting behavior (timing, logging, caching, auth, retry) is needed on **many** functions.
- The behavior is generic and doesn't care about the function's internals.

---

## Quick reference

```text
# minimal decorator
def deco(fn):
    def wrapper(*args, **kwargs):
        # before
        result = fn(*args, **kwargs)
        # after
        return result
    return wrapper

@deco
def f(...): ...

# equivalent without @:
def f(...): ...
f = deco(f)

# preserve metadata — do this every time
import functools

def deco(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

# decorator with arguments — three levels
def repeat(n):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def f(...): ...

# stacking — applied bottom-up
@a
@b
@c
def f(...): ...
# means: f = a(b(c(f)))

# useful built-ins
@functools.lru_cache(maxsize=None)   # bounded cache
@functools.lru_cache(maxsize=None)                     # unbounded cache (3.9+)
@property                            # method -> read-only attribute
@staticmethod                        # no self / no cls
@classmethod                         # first arg is the class

# pitfalls
wrapper(*args, **kwargs)             # accept everything
@functools.wraps(fn)                 # preserve metadata
# decorator body runs at def time, not call time
# order in a stack matters
```
