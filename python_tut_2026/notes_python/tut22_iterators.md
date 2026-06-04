# Python Iterators

An **iterator** is an object that produces values **one at a time**, on demand.
Every `for` loop in Python uses an iterator under the hood.

```python
for x in [10, 20, 30]:
    print(x)
```

That `for` loop does **three things** behind the scenes:

1. Calls `iter([10, 20, 30])` — gets an iterator.
2. Calls `next(iterator)` repeatedly to pull each value.
3. Stops when `next()` raises `StopIteration`.

Understanding this turns a lot of Python "magic" into plain mechanics.

---

## The two key words: **iterable** vs **iterator**

People mix these up. They're different.

| Term         | Definition                                           | Examples                                     |
|--------------|------------------------------------------------------|----------------------------------------------|
| **Iterable** | Anything you can loop over with `for`. Has `__iter__`. | `list`, `tuple`, `str`, `dict`, `set`, `range`, files, generators |
| **Iterator** | Produces values one at a time. Has `__next__`.       | What you get from `iter(iterable)`           |

**Rule:** every iterator is an iterable, but not every iterable is an iterator.

```python
nums = [1, 2, 3]
print(hasattr(nums, "__iter__"))       # True  — list is iterable
print(hasattr(nums, "__next__"))       # False — list is NOT an iterator
```

```text
True
False
```

You can ask a list for its iterator:

```python
nums = [1, 2, 3]
it = iter(nums)
print(type(it).__name__)               # list_iterator
print(hasattr(it, "__next__"))         # True
```

```text
list_iterator
True
```

---

## `iter()` and `next()` — the two functions

`iter(x)` gives you an iterator from an iterable.
`next(it)` pulls the next value from that iterator.

```python
nums = [10, 20, 30]
it = iter(nums)

print(next(it))        # 10
print(next(it))        # 20
print(next(it))        # 30
# print(next(it))      # StopIteration — no more values
```

```text
10
20
30
```

When the iterator runs out, `next()` raises `StopIteration`. That's the "no more values" signal.

`next()` can take a default to avoid the exception:

```python
it = iter([1, 2])
print(next(it, "done"))    # 1
print(next(it, "done"))    # 2
print(next(it, "done"))    # 'done'   — no exception
```

---

## What a `for` loop really does

This:

```python
for x in [10, 20, 30]:
    print(x)
```

is equivalent to:

```python
nums = [10, 20, 30]
it = iter(nums)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    print(x)
```

Both print `10`, `20`, `30`. The `for` is just nicer syntax.

This is why **anything with `__iter__`** can be used in a `for` loop — files, generators, dict views, custom classes, all of them.

---

## Iterators are **one-shot**

Once an iterator is exhausted, it's done. It won't restart.

```python
nums = [1, 2, 3]
it = iter(nums)

print(list(it))      # [1, 2, 3]   — consumes the iterator
print(list(it))      # []          — already exhausted
```

```text
[1, 2, 3]
[]
```

If you need to loop over the same data twice, iterate the **iterable** twice — not the iterator.

```python
nums = [1, 2, 3]      # iterable — keep this
for x in nums: print(x)
for x in nums: print(x)   # works — each `for` calls iter() again
```

---

## Common built-in iterators

You've already used many of these without realizing they're iterators.

| Function       | Returns an iterator that…                                |
|----------------|----------------------------------------------------------|
| `iter(x)`      | Wraps an iterable                                        |
| `enumerate(x)` | Yields `(index, value)` pairs                            |
| `zip(a, b)`    | Yields parallel tuples; stops at shortest                |
| `map(fn, x)`   | Yields `fn(item)` for each item                          |
| `filter(fn, x)`| Yields items where `fn(item)` is truthy                  |
| `reversed(x)`  | Yields items in reverse                                  |
| `range(n)`     | (Not technically an iterator; iterable. But very iterator-like.) |

```python
e = enumerate(["a", "b", "c"])
print(type(e).__name__)        # enumerate
print(next(e))                 # (0, 'a')
print(next(e))                 # (1, 'b')

m = map(str.upper, ["a", "b", "c"])
print(list(m))                 # ['A', 'B', 'C']

f = filter(lambda n: n > 0, [-1, 2, -3, 4])
print(list(f))                 # [2, 4]
```

Important: `map`, `filter`, `zip`, `enumerate`, `reversed` are all **lazy**. They produce values on demand. They're **one-shot** like any iterator.

```python
m = map(str.upper, ["a", "b"])
print(list(m))   # ['A', 'B']
print(list(m))   # []   — exhausted
```

---

## Making your own iterator — the iterator protocol

To make a class iterable, implement `__iter__`.
To make it an iterator, also implement `__next__`.

The simplest pattern: have `__iter__` return `self`, and `__next__` produce the next value or raise `StopIteration`.

```python
class Counter:
    def __init__(self, stop):
        self.stop = stop
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n >= self.stop:
            raise StopIteration
        value = self.n
        self.n += 1
        return value

for x in Counter(3):
    print(x)
```

```text
0
1
2
```

It works in a `for`, with `list(...)`, `sum(...)`, anything that consumes an iterator.

```python
print(list(Counter(5)))     # [0, 1, 2, 3, 4]
print(sum(Counter(10)))     # 45
```

---

## Iterator vs generator — generators are easier

Writing the class above takes 13 lines. A **generator** does the same thing in 4:

```python
def counter(stop):
    n = 0
    while n < stop:
        yield n
        n += 1

for x in counter(3):
    print(x)
```

```text
0
1
2
```

Under the hood, the generator function returns a **generator object**, which is itself an iterator (it has `__iter__` and `__next__`).

```python
def counter(stop):
    n = 0
    while n < stop:
        yield n
        n += 1

g = counter(3)
print(hasattr(g, "__iter__"))      # True
print(hasattr(g, "__next__"))      # True
print(next(g))                     # 0
print(next(g))                     # 1
```

```text
True
True
0
1
```

Rule of thumb: **write a generator when you can. Write a custom iterator class only when you need state or methods that a generator can't express.**

---

## Infinite iterators

An iterator doesn't have to end. `itertools` ships a few infinite ones.

```python
import itertools

# Forever 1, 2, 3, 4, ...
for n in itertools.count(start=1):
    if n > 5:
        break
    print(n)
```

```text
1
2
3
4
5
```

```python
import itertools

# Forever cycle through items: A B C A B C A B C ...
g = itertools.cycle(["A", "B", "C"])
for _ in range(7):
    print(next(g))
```

```text
A
B
C
A
B
C
A
```

```python
import itertools

# Repeat one value
print(list(itertools.repeat("hi", 3)))   # ['hi', 'hi', 'hi']
```

Combine with `itertools.islice` to safely take the first N:

```python
import itertools
first_five = list(itertools.islice(itertools.count(), 5))
print(first_five)        # [0, 1, 2, 3, 4]
```

---

## `iter(callable, sentinel)` — the two-argument form

There's a second form of `iter()` that builds an iterator from a callable. It keeps calling the function until the **sentinel** value is returned.

Useful for reading from a source until you hit an end marker.

```python
import random

def roll_die():
    return random.randint(1, 6)

# Roll until you get a 6
random.seed(0)
rolls = list(iter(roll_die, 6))
print(rolls)
```

(Output depends on the seed — each roll is a value, and the loop stops the moment `roll_die()` returns `6`.)

---

## Practical real-world examples

### Reading a huge file line by line

A file object is its own iterator. Don't load the whole file — iterate.

```python
# Pseudocode — file would need to exist
# with open("huge.log") as f:
#     for line in f:
#         if "ERROR" in line:
#             print(line.rstrip())
```

`for line in f` calls `next(f)` until EOF — constant memory, no matter how big the file.

### Chunking an iterable

`itertools.islice` can chunk any iterator into windows.

```python
import itertools

def chunks(iterable, size):
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, size))
        if not batch:
            return
        yield batch

for batch in chunks(range(10), 3):
    print(batch)
```

```text
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]
[9]
```

### Chaining iterables together

```python
import itertools

a = [1, 2, 3]
b = [4, 5, 6]
print(list(itertools.chain(a, b)))     # [1, 2, 3, 4, 5, 6]
```

---

## Common pitfalls

### 1. Iterator vs iterable confusion

A list isn't an iterator. You can't call `next()` on it directly.

```python
nums = [1, 2, 3]
# next(nums)         # TypeError: 'list' object is not an iterator

next(iter(nums))     # 1   — wrap with iter() first
```

### 2. One-shot exhaustion

```python
nums = map(str.upper, ["a", "b"])
print(list(nums))    # ['A', 'B']
print(list(nums))    # []           — surprise!
```

If you need to use the result twice, **materialize** it once into a list:

```python
result = list(map(str.upper, ["a", "b"]))
print(result, result)    # ['A', 'B'] ['A', 'B']
```

### 3. No `len()` on iterators

```python
m = map(str.upper, "abc")
# print(len(m))   # TypeError: object of type 'map' has no len()
```

Convert to a list (or `sum(1 for _ in m)`) if you need a count — but be aware: counting consumes it.

### 4. Iterators can't be sliced or indexed

```python
m = map(str.upper, "abc")
# m[0]   # TypeError: 'map' object is not subscriptable
```

Use `itertools.islice(m, n)` or convert to a list.

### 5. Forgetting to `break` an infinite iterator

```python
import itertools
# for n in itertools.count():       # runs forever — needs a break inside
#     ...
```

---

## Iterator vs iterable — final picture

```text
┌──────────────────────────────────────────────────────────────┐
│  ITERABLE  (has __iter__)                                    │
│  -- you can loop over it with `for`                          │
│  -- examples: list, tuple, str, dict, set, range, file       │
│                                                              │
│  iter(iterable) -> ITERATOR                                  │
│                    (has __iter__ AND __next__)               │
│                    -- you can call next(it) on it            │
│                    -- one-shot; runs out when exhausted      │
│                    -- examples: list_iterator, map, filter,  │
│                       enumerate, zip, generator objects      │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick reference

```text
iter(iterable)             get an iterator
next(it)                   get next value (or StopIteration)
next(it, default)          get next value, no exception

for x in iterable:         use the iterator implicitly
list(iterator)             materialize all values
sum(iterator)              works with any number iterator

# iterator protocol — make your own
class MyIter:
    def __iter__(self): return self
    def __next__(self):
        if done: raise StopIteration
        return value

# generators are simpler — same effect with `yield`
def gen():
    while ...:
        yield value

# built-in lazy iterators (one-shot)
enumerate(x)   zip(a, b)   map(fn, x)   filter(fn, x)   reversed(x)

# itertools highlights
itertools.count(start)         infinite 0, 1, 2, ...
itertools.cycle(iterable)      infinite cycle
itertools.repeat(value, n)     repeat value n times
itertools.islice(it, n)        take first n
itertools.chain(a, b)          glue iterators together
```
