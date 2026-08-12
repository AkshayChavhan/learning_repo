# Python Sets

A **set** is an unordered collection of **unique** items.
Duplicates are silently dropped.

```python
nums = {1, 2, 3, 2, 1}
print(nums)   # {1, 2, 3}
```

Four key facts:

- **Unordered** — no index, no slicing. Items have no fixed position.
- **No duplicates** — every value appears at most once.
- **Mutable** — you can add and remove items.
- **Items must be hashable** — strings, numbers, tuples are fine; lists and dicts are not.

---

## Why sets exist

Use a set when you care about **membership and uniqueness**, not order.

Common reasons:

- Remove duplicates from a list.
- Fast `in` checks (much faster than lists for large data).
- Set math — union, intersection, difference.
- Track "seen" items in a loop.

---

## Creating a set

```python
empty = set()           # NOT {} — that's an empty dict!
nums = {1, 2, 3}
mixed = {1, "hi", 3.14, True}

# From other iterables
from_list = set([1, 2, 2, 3])     # {1, 2, 3}
from_str = set("hello")           # {'h', 'e', 'l', 'o'}
```

### The empty-set trap

```python
a = {}            # this is an empty DICT
b = set()         # this is an empty set

print(type(a).__name__)   # dict
print(type(b).__name__)   # set
```

---

## Sets are unordered

You can't index a set.
The print order is not guaranteed.

```python
s = {3, 1, 2}
# print(s[0])    # TypeError: 'set' object is not subscriptable
print(s)         # might print {1, 2, 3} or any order
```

---

## Add and remove items

| Method        | What it does                                         |
|---------------|------------------------------------------------------|
| `add(x)`      | Add a single item                                    |
| `update(it)`  | Add all items from an iterable                       |
| `remove(x)`   | Remove `x` — raises `KeyError` if missing            |
| `discard(x)`  | Remove `x` — does nothing if missing                 |
| `pop()`       | Remove and return an arbitrary item                  |
| `clear()`     | Remove all items                                     |

```python
s = {1, 2, 3}

s.add(4)
print(s)               # {1, 2, 3, 4}

s.update([5, 6, 2])    # 2 already there → ignored
print(s)               # {1, 2, 3, 4, 5, 6}

s.remove(3)
print(s)               # {1, 2, 4, 5, 6}

s.discard(99)          # missing → no error
s.remove(99)           # missing → KeyError

popped = s.pop()       # removes some item
print(popped)
print(s)
```

---

## Membership and length

```python
fruits = {"apple", "banana", "mango"}

print("apple" in fruits)     # True
print("grape" not in fruits) # True
print(len(fruits))           # 3
```

`in` is very fast on sets — much faster than on lists.

```python
import time

big_list = list(range(1_000_000))
big_set = set(big_list)

start = time.time()
print(999_999 in big_list)   # slow — checks every item
print("list time:", time.time() - start)

start = time.time()
print(999_999 in big_set)    # fast — one hash lookup
print("set time:", time.time() - start)
```

---

## Set math

The real superpower of sets.

| Operator | Method                  | Meaning                              |
|----------|-------------------------|--------------------------------------|
| `\|`     | `union()`               | Items in either set                  |
| `&`      | `intersection()`        | Items in **both** sets               |
| `-`      | `difference()`          | Items in left but not right          |
| `^`      | `symmetric_difference()`| Items in one set but not both        |

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # {1, 2, 3, 4, 5, 6}  — union
print(a & b)   # {3, 4}              — intersection
print(a - b)   # {1, 2}              — difference (only in a)
print(b - a)   # {5, 6}              — difference (only in b)
print(a ^ b)   # {1, 2, 5, 6}        — symmetric difference
```

Same as methods:

```python
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))
print(a.symmetric_difference(b))
```

---

## Subset and superset

```python
a = {1, 2}
b = {1, 2, 3, 4}

print(a.issubset(b))      # True
print(b.issuperset(a))    # True
print(a.isdisjoint({9}))  # True — no items in common
```

Shortcuts:

```python
print(a <= b)   # subset
print(b >= a)   # superset
```

---

## Remove duplicates from a list

The most common real-world use of sets.

```python
nums = [1, 2, 2, 3, 1, 4]
unique = list(set(nums))
print(unique)        # [1, 2, 3, 4]  — order not guaranteed
```

If order matters, use a dict (Python 3.7+ keeps insertion order):

```python
nums = [1, 2, 2, 3, 1, 4]
unique = list(dict.fromkeys(nums))
print(unique)        # [1, 2, 3, 4]  — original order kept
```

---

## Loop through a set

Same as any iterable.
Order is **not** guaranteed.

```python
for item in {"a", "b", "c"}:
    print(item)
```

---

## `frozenset` — the immutable cousin

A `frozenset` is a set that can't be changed.
Use it when you need a set as a dict key or another set's item.

```python
fs = frozenset([1, 2, 3])
print(fs)              # frozenset({1, 2, 3})

# fs.add(4)            # AttributeError — no add()

# A set of sets — needs frozensets
groups = {frozenset([1, 2]), frozenset([3, 4])}
print(groups)
```

---

## Set vs list vs tuple

| Feature           | `list`   | `tuple`  | `set`             |
|-------------------|----------|----------|-------------------|
| Ordered           | Yes      | Yes      | No                |
| Mutable           | Yes      | No       | Yes               |
| Allows duplicates | Yes      | Yes      | No                |
| Indexable (`x[0]`)| Yes      | Yes      | No                |
| `in` check speed  | Slow     | Slow     | Fast              |
| Items hashable    | Any      | Any      | Required          |

---

## Quick reference

```text
{1, 2, 3}             create
set()                 empty set (not {})
set([1, 2, 2])        from iterable → {1, 2}

s.add(x)              add one item
s.update(iter)        add many items
s.remove(x)           remove (errors if missing)
s.discard(x)          remove (silent if missing)
s.pop()               remove + return some item
s.clear()             empty the set

x in s                membership (fast)
len(s)                size

a | b                 union
a & b                 intersection
a - b                 difference
a ^ b                 symmetric difference

a <= b                a is subset of b
a >= b                a is superset of b
a.isdisjoint(b)       no common items

frozenset(iter)       immutable set
list(set(lst))        remove duplicates
```
