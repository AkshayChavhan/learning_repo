# Python Recursion & Generators

This chapter covers two function patterns — **recursion** (functions that call themselves) and **generators** (functions that produce values one at a time).

---

# Part 1 — Recursion

A **recursive function** is a function that calls itself.

```python
def countdown(n):
    if n == 0:
        print("done")
        return
    print(n)
    countdown(n - 1)

countdown(3)
```

```text
3
2
1
done
```

---

## The two parts of every recursive function

Every recursive function needs two pieces:

- A **base case** — the stopping condition. Without it, the calls never end.
- A **recursive case** — the function calls itself with a **smaller** input, moving toward the base case.

In `countdown` above:

- Base case: `n == 0` (print "done" and return).
- Recursive case: `countdown(n - 1)` (smaller `n`).

Miss either one and you get either an infinite loop or no progress.

---

## Classic example — factorial

`n! = n * (n-1) * (n-2) * ... * 1`. Iterative first:

```python
def factorial_iter(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(factorial_iter(5))
```

```text
120
```

Now recursively. Notice the base case (`n <= 1`) and the recursive case (`n * factorial(n - 1)`).

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))
```

```text
120
```

Same answer. The recursive version mirrors the math definition closely.

---

## Classic example — fibonacci

The Fibonacci sequence: `0, 1, 1, 2, 3, 5, 8, 13, ...` — each term is the sum of the previous two.

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(10))
```

```text
55
```

Beautiful — but **slow** for large `n`. Naive recursive `fib` recomputes the same values over and over, and the call count grows **exponentially**.

```python
calls = 0

def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(20), "with", calls, "calls")
```

```text
6765 with 21891 calls
```

21,891 calls for `fib(20)`. For `fib(40)` it explodes into hundreds of millions.

The fix is **memoization** — cache results so each `n` is computed once. `@functools.lru_cache(maxsize=None)` (from tut18) does this in one line.

```python
import functools

@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))
```

```text
12586269025
```

Now `fib(50)` finishes instantly. Same recursion, cached results.

---

## Recursing on a list

Sum the elements of a list — without using `sum()` or a loop.

```python
def sum_list(items):
    if not items:                    # base case: empty list
        return 0
    return items[0] + sum_list(items[1:])

print(sum_list([1, 2, 3, 4, 5]))
```

```text
15
```

Each call peels off the first element and recurses on the rest. The base case is the empty list — its sum is `0`.

---

## Recursing on a nested structure

Recursion really shines on **nested** data. Here's a flattener — turn a list of lists (of lists ...) into a flat list.

```python
def flatten(items):
    result = []
    for x in items:
        if isinstance(x, list):
            result.extend(flatten(x))     # recurse on sublists
        else:
            result.append(x)              # base case: plain value
    return result

print(flatten([1, [2, [3, 4]], 5]))
```

```text
[1, 2, 3, 4, 5]
```

A loop alone can't easily handle arbitrary nesting depth — recursion can.

---

## The recursion depth limit

Python caps how deep recursion can go. Check it:

```python
import sys
print(sys.getrecursionlimit())
```

```text
1000
```

The default is around 1000 calls. Go deeper and you get a `RecursionError: maximum recursion depth exceeded`.

You **can** raise it with `sys.setrecursionlimit(10000)` — but don't, casually. Too high and Python can crash the interpreter (real stack overflow). If you're hitting the limit, it's usually a sign to **rewrite as iteration**.

---

## Recursion vs iteration

| Situation                              | Better choice |
|----------------------------------------|---------------|
| Linear count / sum / running total     | iteration     |
| Walking a tree / nested dict / JSON    | recursion     |
| Graph / filesystem traversal           | recursion     |
| Anything with a clean mathematical form (factorial, fib) | either — recursion reads nicer |
| Very deep input (millions of items)    | iteration (depth limit)  |

Rule of thumb: if the structure is **nested or branching**, reach for recursion. If it's **flat and linear**, a `for` loop is usually clearer.

---

## Recursion pitfalls

### 1. Missing base case

No base case = infinite recursion = `RecursionError`.

```python
def bad(n):
    return bad(n - 1)        # no stopping condition

# bad(5) -> RecursionError: maximum recursion depth exceeded
```

Always write the base case **first**.

### 2. Base case never reached

A base case that the recursive step never reaches is just as bad.

```python
def bad(n):
    if n == 0:
        return 0
    return bad(n + 1)        # n grows — never hits 0

# bad(1) -> RecursionError: base case n==0 is never reached
```

Make sure each recursive call moves **toward** the base case.

### 3. Recomputing the same thing

Naive `fib` recomputes `fib(5)` thousands of times. Fix with `@functools.lru_cache(maxsize=None)`.

### 4. Going too deep

Python's ~1000-call limit is real. For huge inputs, rewrite as a loop.

---

# Part 2 — Generators

A **generator** is a function that uses `yield` instead of `return`.
It **pauses** and **resumes** — emitting one value at a time, on demand.

```python
def counter():
    yield 1
    yield 2
    yield 3

for x in counter():
    print(x)
```

```text
1
2
3
```

Key point: calling `counter()` doesn't run the body. It returns a **generator object**. The body only runs as you iterate.

```python
def counter():
    yield 1
    yield 2
    yield 3

g = counter()
print(g)                  # a generator object, not [1, 2, 3]
```

```text
<generator object counter at 0x...>
```

---

## `yield` vs `return`

They are **not** the same.

| Keyword  | Effect                                         |
|----------|------------------------------------------------|
| `return` | Ends the function. One value comes out, done.  |
| `yield`  | **Pauses** the function. Resumes on next call. |

A function can have **many** `yield`s — each emits one value, and execution picks up right after the `yield` on the next iteration.

```python
def steps():
    print("start")
    yield "a"
    print("between")
    yield "b"
    print("end")

for x in steps():
    print("got", x)
```

```text
start
got a
between
got b
end
```

See the interleaving — the generator runs **just enough** to produce the next value, then pauses.

---

## `next()` and `StopIteration`

You can drive a generator manually with `next()`.

```python
def counter():
    yield 1
    yield 2
    yield 3

g = counter()
print(next(g))           # 1
print(next(g))           # 2
print(next(g))           # 3
# print(next(g))         # raises StopIteration
```

```text
1
2
3
```

When the function ends (or hits a `return`), the next `next()` raises **`StopIteration`** — that's the signal "no more values."

A `for` loop catches `StopIteration` for you. You'll usually use `for`, not `next()` directly.

---

## Generators are lazy

A generator doesn't compute everything up front. It produces values **on demand** — perfect for big or infinite sequences.

```python
def big_squares(n):
    for i in range(n):
        yield i * i

g = big_squares(1_000_000)
print(next(g))           # 0
print(next(g))           # 1
print(next(g))           # 4
```

```text
0
1
4
```

Nothing big was built. The million squares only exist if you actually pull them.

---

## A useful example — read a large file line by line

Loading a 10 GB file into a list crashes. A generator reads one line at a time, in **constant memory**.

```python
def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.rstrip("\n")

# for line in read_lines("huge.log"):
#     if "ERROR" in line:
#         print(line)
```

You never hold more than one line in memory. This pattern (generator + `for`) is the bread-and-butter of streaming data in Python.

(In fact, Python's open file objects are **already** iterable line-by-line — but writing your own generator lets you add filtering, parsing, or transformations.)

---

## An infinite generator

Generators can run **forever** — they only produce on demand.

```python
def naturals():
    n = 1
    while True:
        yield n
        n += 1

g = naturals()
print(next(g), next(g), next(g))
```

```text
1 2 3
```

If you wrote `for x in naturals(): print(x)`, you'd get an **infinite loop** — values forever.

Combine with `itertools.islice` to take just the first N:

```python
import itertools

def naturals():
    n = 1
    while True:
        yield n
        n += 1

first_five = list(itertools.islice(naturals(), 5))
print(first_five)
```

```text
[1, 2, 3, 4, 5]
```

`islice` pulls only the values it needs, then stops asking.

---

## Generator expressions

A **generator expression** looks like a list comprehension — but with `()` instead of `[]`.

```python
squares = (x * x for x in range(5))
print(squares)
for s in squares:
    print(s)
```

```text
<generator object <genexpr> at 0x...>
0
1
4
9
16
```

Compare with the list version:

| Form                          | Builds              | When to use                              |
|-------------------------------|---------------------|------------------------------------------|
| `[x*x for x in range(5)]`     | Full list in memory | You need the list (indexing, reuse, len) |
| `(x*x for x in range(5))`     | A generator object  | One-pass iteration over big/infinite data |

When a generator expression is the **only argument** to a function, you can drop the outer parens:

```python
total = sum(x * x for x in range(10))
print(total)
```

```text
285
```

Reads cleanly — and never builds the intermediate list.

---

## `yield from` — delegate to another generator

`yield from` re-emits every value of another iterable from inside your generator.

```python
def inner():
    yield from range(3)

for x in inner():
    print(x)
```

```text
0
1
2
```

Useful for **chaining** generators:

```python
def chained():
    yield from [1, 2, 3]
    yield from "ab"
    yield from range(2)

print(list(chained()))
```

```text
[1, 2, 3, 'a', 'b', 0, 1]
```

Without `yield from`, you'd write `for x in inner(): yield x`. Same result, more code.

---

## `send()`, `throw()`, `close()`

Generators can also **receive** values back via `g.send(value)`, take exceptions via `g.throw(...)`, and be shut down with `g.close()`. These power **coroutines** and live in advanced topics — you'll rarely reach for them in everyday code.

---

## Generators vs lists

| Feature              | List                       | Generator                   |
|----------------------|----------------------------|-----------------------------|
| Memory               | All values stored          | One value at a time         |
| Speed to build       | Slow for big sizes         | Instant (lazy)              |
| Random access (`x[i]`) | Yes                      | No                          |
| `len()`              | Yes                        | No                          |
| Re-iterate           | Yes (many times)           | **No** — one pass only      |
| Infinite sequences   | No                         | Yes                         |

Use a **list** when you need the data sitting in memory (multiple passes, indexing, length).
Use a **generator** when you process items once, in order, and want to save memory.

---

## Generator pitfalls

### 1. A generator is one-shot

Once exhausted, it yields nothing more.

```python
def counter():
    yield 1
    yield 2
    yield 3

g = counter()
print(list(g))           # [1, 2, 3]
print(list(g))           # [] -- already exhausted
```

```text
[1, 2, 3]
[]
```

To iterate again, **call the generator function again** to get a fresh generator object.

### 2. Calling the function gives a generator, not the values

```python
def counter():
    yield 1
    yield 2

print(counter())         # <generator object ...>  -- not (1, 2)
print(list(counter()))   # [1, 2]
```

```text
<generator object counter at 0x...>
[1, 2]
```

Forgetting this is the #1 surprise for newcomers. Iterate (or `list(...)`) to actually pull values.

### 3. No `len()`, no indexing

A generator doesn't know how many values it will produce.

```python
def counter():
    yield 1
    yield 2
    yield 3

g = counter()
# len(g)        # TypeError: object of type 'generator' has no len()
# g[0]          # TypeError: 'generator' object is not subscriptable
```

If you need `len` or `[i]`, materialize with `list(g)` first — but then you've lost the memory savings.

---

## Quick reference

```text
# RECURSION -------------------------------------------------

# shape -- every recursive function has these two parts
def f(n):
    if base_case(n):
        return base_value
    return ... f(smaller(n)) ...

# example: factorial
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)

# slow recursion -> cache it
import functools

@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

# recursion depth
import sys
sys.getrecursionlimit()          # default ~1000
# sys.setrecursionlimit(N)       # use with care

# pitfalls
# - missing base case          -> infinite recursion
# - base case never reached    -> infinite recursion
# - exponential recomputation  -> use @lru_cache
# - very deep input            -> rewrite as a loop


# GENERATORS ------------------------------------------------

# shape -- yield instead of return, possibly multiple times
def gen(...):
    ...
    yield value
    ...
    yield value

# calling does NOT run the body -- returns a generator object
g = gen()                # <generator object ...>
for x in g:              # body runs lazily as you iterate
    ...

# manual driving
next(g)                  # next value, or raises StopIteration

# delegation
def outer():
    yield from other_iterable

# generator expression -- parens, lazy
squares = (x * x for x in range(10))
total = sum(x * x for x in range(10))     # parens optional as sole arg

# infinite generator + islice
import itertools
def naturals():
    n = 1
    while True:
        yield n
        n += 1
first5 = list(itertools.islice(naturals(), 5))

# pitfalls
# - one-shot: after exhaustion, yields nothing
# - calling gen() returns a generator object, not values
# - no len(), no indexing, no re-iteration
```
