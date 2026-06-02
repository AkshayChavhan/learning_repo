# Python Functions

A **function** is a named, reusable block of code.
You define it once and call it whenever you need it.

```python
def greet():
    print("Hello!")

greet()
greet()
```

Output:

```text
Hello!
Hello!
```

Three key facts:

- Defined with **`def`**, named, optional **parameters** in `()`.
- The header ends with a **`:`**, the body is **indented** (4 spaces).
- An optional **`return`** sends a value back. No `return` means `None`.

The shape:

```text
def name(parameters):
    body
    return value      # optional
```

---

## Parameters and arguments

The names in the `def` header are **parameters**.
The values you pass at the call site are **arguments**.

```python
def add(a, b):           # a, b are parameters
    return a + b

print(add(2, 3))         # 2, 3 are arguments
```

```text
5
```

### Positional arguments

Matched to parameters **by position** — first argument to first parameter, and so on.

```python
def describe(name, age):
    print(name, "is", age)

describe("Akshay", 30)
```

```text
Akshay is 30
```

Swap the order and the meaning changes:

```python
def describe(name, age):
    print(name, "is", age)

describe(30, "Akshay")   # wrong — but Python doesn't know
```

```text
30 is Akshay
```

---

## Default parameter values

A parameter can have a default. The caller may omit it.

```python
def greet(name="World"):
    print("Hello,", name)

greet()
greet("Akshay")
```

```text
Hello, World
Hello, Akshay
```

Defaults make parameters **optional** — pass a value to override.

---

## Keyword arguments at the call site

You can pass arguments by **name**, not by position.

```python
def greet(name="World"):
    print("Hello,", name)

greet(name="Akshay")
```

```text
Hello, Akshay
```

Why they help readability:

```python
def book_flight(passenger, source, destination, seat):
    print(passenger, source, "->", destination, "seat", seat)

# positional — what does each value mean?
book_flight("Akshay", "PNQ", "BLR", "12A")

# keyword — meaning is obvious at the call site
book_flight(passenger="Akshay", source="PNQ", destination="BLR", seat="12A")
```

---

## Mixing positional and keyword arguments

You can mix them, but **positionals must come first**.

```python
def book_flight(passenger, source, destination, seat="Any"):
    print(passenger, source, "->", destination, "seat", seat)

book_flight("Akshay", "PNQ", destination="BLR", seat="12A")
```

```text
Akshay PNQ -> BLR seat 12A
```

Putting a positional **after** a keyword is a syntax error:

```python
# book_flight(passenger="Akshay", "PNQ", "BLR")
# SyntaxError: positional argument follows keyword argument
```

---

## `return` — sending a value back

A function returns the value after `return`.

```python
def square(n):
    return n * n

result = square(5)
print(result)
```

```text
25
```

### Multiple return values — actually a tuple

`return a, b` builds a tuple. The caller can unpack it.

```python
def min_max(nums):
    return min(nums), max(nums)

pair = min_max([4, 1, 9, 2])
print(pair)                  # (1, 9) — a tuple

lo, hi = min_max([4, 1, 9, 2])   # unpack
print(lo, hi)
```

```text
(1, 9)
1 9
```

### No `return` (or a bare `return`) gives `None`

```python
def shout(text):
    print(text.upper())      # prints, but doesn't return

result = shout("hi")
print(result)                # None
```

```text
HI
None
```

A bare `return` also yields `None` — useful to exit early:

```python
def safe_divide(a, b):
    if b == 0:
        return                # bare return — exits, returns None
    return a / b

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # None
```

---

## `*args` — variable positional arguments

Use `*args` when the number of positional arguments isn't fixed.
Inside the function, `args` is a **tuple**.

```python
def total(*args):
    print(args, type(args).__name__)
    return sum(args)

print(total(1, 2, 3))
print(total(1, 2, 3, 4, 5))
```

```text
(1, 2, 3) tuple
6
(1, 2, 3, 4, 5) tuple
15
```

The name `args` is convention. `*nums` would work too.

---

## `**kwargs` — variable keyword arguments

`**kwargs` collects extra keyword arguments into a **dict**.

```python
def show(**kwargs):
    print(kwargs, type(kwargs).__name__)

show(name="Akshay", age=30)
```

```text
{'name': 'Akshay', 'age': 30} dict
```

Iterate like any dict:

```python
def show(**kwargs):
    for k, v in kwargs.items():
        print(k, "=", v)

show(name="Akshay", age=30, city="Pune")
```

```text
name = Akshay
age = 30
city = Pune
```

---

## Combining everything

Order in the signature is fixed:

```text
def f(positional, default=value, *args, **kwargs):
```

```python
def f(a, b, *args, **kwargs):
    print("a =", a)
    print("b =", b)
    print("args =", args)
    print("kwargs =", kwargs)

f(1, 2, 3, 4, x=10, y=20)
```

```text
a = 1
b = 2
args = (3, 4)
kwargs = {'x': 10, 'y': 20}
```

---

## Unpacking when calling

The `*` and `**` operators also work at the **call site** — to spread an iterable or a dict into arguments.

```python
def add3(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add3(*nums))           # same as add3(1, 2, 3)

opts = {"a": 1, "b": 2, "c": 3}
print(add3(**opts))          # same as add3(a=1, b=2, c=3)
```

```text
6
6
```

---

## Positional-only `/` and keyword-only `*` markers

You can restrict **how** an argument must be passed.

```python
def f(a, /, b, *, c):
    print(a, b, c)
```

- `a` is **before `/`** — positional only. Cannot pass `a=1`.
- `b` is **between `/` and `*`** — positional or keyword.
- `c` is **after `*`** — keyword only. Cannot pass it positionally.

```python
def f(a, /, b, *, c):
    print(a, b, c)

f(1, 2, c=3)            # OK
f(1, b=2, c=3)          # OK
# f(a=1, b=2, c=3)      # TypeError — a is positional-only
# f(1, 2, 3)            # TypeError — c is keyword-only
```

| Marker | Effect                                |
|--------|---------------------------------------|
| `/`    | Everything **before** it is positional-only |
| `*`    | Everything **after** it is keyword-only     |

---

## Type hints

Hints document the **expected** types. They're not enforced at runtime.

```python
def greet(name: str) -> str:
    return "Hello, " + name

print(greet("Akshay"))
```

```text
Hello, Akshay
```

Python doesn't stop you from passing the wrong type — it just trusts the call.
Tools like `mypy` or your editor check hints separately.

```python
def add(a: int, b: int) -> int:
    return a + b

print(add(2, 3))         # 5
print(add("a", "b"))     # 'ab' — Python doesn't complain
```

---

## Docstrings

A **docstring** is a triple-quoted string right under the `def`.
It explains what the function does.

```python
def area(width, height):
    """Return the area of a rectangle."""
    return width * height

print(area.__doc__)
```

```text
Return the area of a rectangle.
```

`help(area)` shows the docstring along with the signature.
First line should be a one-line summary.

---

## Scope — local vs global

Names defined **inside** a function are **local**. They vanish when the function returns.

```python
def f():
    x = 10            # local
    print(x)

f()
# print(x)            # NameError — x doesn't exist out here
```

A function can **read** a global, but assigning creates a new local:

```python
count = 0

def bump():
    count = count + 1     # UnboundLocalError — assignment makes it local

# bump()
```

Use `global` to actually modify the module-level name:

```python
count = 0

def bump():
    global count
    count = count + 1

bump()
bump()
print(count)              # 2
```

`nonlocal` is similar but for **enclosing function** scopes — used with closures.
Covered in detail when we get to closures.

```python
def outer():
    x = 1
    def inner():
        nonlocal x
        x = 99
    inner()
    print(x)              # 99

outer()
```

---

## Functions are first-class objects

A function is just a value. You can:

- Assign it to a variable.
- Pass it as an argument.
- Return it from another function.

### Assign to a variable

```python
def square(n):
    return n * n

f = square                # no parentheses — referencing, not calling
print(f(5))               # 25
```

### Pass as an argument

```python
def apply(func, value):
    return func(value)

def square(n):
    return n * n

print(apply(square, 4))   # 16
```

### Return from a function

```python
def make_multiplier(factor):
    def multiply(n):
        return n * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))          # 10
print(triple(5))          # 15
```

---

## `lambda` — small anonymous functions

`lambda` makes a one-expression function inline.

```python
square = lambda x: x * x
print(square(5))          # 25
```

Most useful as an argument to functions like `sorted`, `map`, `filter`:

```python
words = ["banana", "fig", "apple"]
print(sorted(words, key=lambda w: len(w)))
```

```text
['fig', 'apple', 'banana']
```

When to use `lambda`:

- Tiny, **one-expression** helper used once.
- Passing a quick callable to `sorted`, `map`, `filter`, `min`, `max`.

When not to:

- Anything with multiple statements — write a real `def`.
- Anything that needs a name in tracebacks — `def` shows the name, `lambda` shows `<lambda>`.

---

## Common pitfalls

### 1. Mutable default argument

A default value is evaluated **once**, when the function is defined.
A mutable default (list, dict, set) is **shared** across calls.

```python
def add_item(item, items=[]):     # BUG — list is created once
    items.append(item)
    return items

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['a', 'b']   <- not ['b']!
print(add_item("c"))    # ['a', 'b', 'c']
```

Fix: use `None` as the sentinel and create the list inside.

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['b']
print(add_item("c"))    # ['c']
```

### 2. Forgetting to `return`

A function with no `return` gives back `None`.

```python
def double(n):
    n * 2                # computed and thrown away

result = double(5)
print(result)            # None
```

Fix:

```python
def double(n):
    return n * 2

print(double(5))         # 10
```

### 3. Shadowing a parameter with a local

A local variable with the same name as a parameter overwrites it.

```python
def greet(name):
    name = "World"       # shadows the parameter
    print("Hello,", name)

greet("Akshay")          # Hello, World
```

Usually a typo or accidental reuse. Pick a different local name.

### 4. Confusing `print()` with `return`

`print` shows a value. `return` **sends it back** to the caller.

```python
def add_print(a, b):
    print(a + b)         # only prints

def add_return(a, b):
    return a + b         # gives the value back

x = add_print(2, 3)      # prints 5, but x is None
y = add_return(2, 3)     # y is 5

print(x)                 # None
print(y)                 # 5
print(y * 10)            # 50 — you can use a returned value
```

In a REPL these can look the same. In real code, only `return` lets the caller use the result.

---

## Quick reference

```text
# define
def name(p1, p2=default, *args, **kwargs):
    """docstring"""
    return value

# call
name(1, 2)                       # positional
name(p1=1, p2=2)                 # keyword
name(1, p2=2)                    # mix — positionals first

# return
return value                     # send back
return a, b                      # tuple of two
return                           # bare — returns None
# (no return)                    # also returns None

# variable args
*args                            # extra positionals -> tuple
**kwargs                         # extra keywords   -> dict

# call-site unpacking
f(*iterable)                     # spread into positionals
f(**mapping)                     # spread into keywords

# restrict how params are passed
def f(a, /, b, *, c): ...        # a positional-only, c keyword-only

# type hints (not enforced)
def f(x: int) -> str: ...

# scope
global name                      # rebind a module-level name
nonlocal name                    # rebind an enclosing function's name

# first-class
f = some_function                # assign
some_function(other)             # pass as argument
def make(): return inner         # return a function

# lambda
lambda x: x * 2                  # one-expression anonymous function

# pitfalls to remember
def f(items=None):               # not items=[]
    if items is None:
        items = []
```
