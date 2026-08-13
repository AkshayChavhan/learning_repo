# Python Tuples

A **tuple** is an ordered collection — like a list, but **frozen**.
Once created, you can't change it.

```python
point = (3, 5)
print(point)
```

Four key facts:

- **Ordered** — items keep their position.
- **Immutable** — can't add, remove, or change items after creation.
- **Allows duplicates** — same value can appear many times.
- **Mixed types OK** — `(1, "hi", True)` is valid.

---

## Why tuples exist

Lists are great when data changes.
Tuples are great when data **shouldn't** change.

Use a tuple for:

- Fixed groupings: `(x, y)` coordinates, `(r, g, b)` color.
- Returning multiple values from a function.
- Dictionary keys (lists can't be keys, tuples can).
- Anything you want to protect from accidental mutation.

---

## Creating a tuple

```python
empty = ()
nums = (1, 2, 3)
mixed = (1, "hi", True, 3.14)

# Parentheses are optional — commas make the tuple
also_a_tuple = 1, 2, 3
print(also_a_tuple)   # (1, 2, 3)
```

### The one-item tuple trap

A single value in parentheses is **not** a tuple.
You need a trailing comma.

```python
not_a_tuple = (5)
print(type(not_a_tuple).__name__)   # int

real_tuple = (5,)
print(type(real_tuple).__name__)    # tuple
```

### From other iterables

```python
print(tuple([1, 2, 3]))   # (1, 2, 3)
print(tuple("abc"))       # ('a', 'b', 'c')
print(tuple(range(4)))    # (0, 1, 2, 3)
```

---

## Indexing and slicing

Same as lists.

```python
nums = (10, 20, 30, 40, 50)

print(nums[0])     # 10
print(nums[-1])    # 50
print(nums[1:4])   # (20, 30, 40)
print(nums[::-1])  # (50, 40, 30, 20, 10)
```

---

## Tuples are immutable

You can't change an item after creation.

```python
nums = (1, 2, 3)
# nums[0] = 99   # TypeError: 'tuple' object does not support item assignment
# nums.append(4) # AttributeError: 'tuple' has no attribute 'append'
```

To "change" a tuple, build a new one:

```python
nums = (1, 2, 3)
nums = nums + (4,)
print(nums)   # (1, 2, 3, 4)
```

Or convert to a list, modify, convert back:

```python
nums = (1, 2, 3)
temp = list(nums)
temp.append(4)
nums = tuple(temp)
print(nums)   # (1, 2, 3, 4)
```

---

## Unpacking

Assign each item to its own variable.

```python
point = (3, 5)
x, y = point
print(x, y)   # 3 5
```

Number of names must match the number of items:

```python
# x, y = (1, 2, 3)   # ValueError: too many values to unpack
```

Use `*` to catch the rest:

```python
first, *rest = (1, 2, 3, 4, 5)
print(first)   # 1
print(rest)    # [2, 3, 4, 5]

*head, last = (1, 2, 3, 4, 5)
print(head)    # [1, 2, 3, 4]
print(last)    # 5
```

---

## Returning multiple values

Functions can return a tuple — and Python unpacks it for you.

```python
def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([4, 1, 7, 2])
print(low, high)   # 1 7
```

The function returns a `(1, 7)` tuple; the call site unpacks it.

---

## Loop through a tuple

```python
colors = ("red", "green", "blue")

for c in colors:
    print(c)

for i, c in enumerate(colors):
    print(i, c)
```

---

## Membership and count

```python
nums = (1, 2, 3, 2, 4, 2)

print(2 in nums)         # True
print(99 not in nums)    # True
print(nums.count(2))     # 3
print(nums.index(3))     # 2
print(len(nums))         # 6
```

Tuples have **only 2 methods**: `count()` and `index()`.
That's it. Because they're immutable, there's nothing to add or remove.

---

## Joining and repeating

```python
print((1, 2) + (3, 4))    # (1, 2, 3, 4)
print((0,) * 5)           # (0, 0, 0, 0, 0)
```

---

## Tuple vs list

| Feature           | `list`                | `tuple`               |
|-------------------|-----------------------|-----------------------|
| Syntax            | `[1, 2, 3]`           | `(1, 2, 3)`           |
| Ordered           | Yes                   | Yes                   |
| Mutable           | Yes — can change      | No — frozen           |
| Methods           | Many (~11)            | Only 2 (`count`, `index`) |
| Can be dict key   | No                    | Yes (if items are hashable) |
| Memory            | More                  | Less                  |
| Use when…         | Data changes          | Data is fixed         |

---

## Tuples as dictionary keys

Lists can't be used as keys.
Tuples can — as long as their items are hashable.

```python
locations = {
    (0, 0): "origin",
    (1, 0): "east",
    (0, 1): "north",
}

print(locations[(1, 0)])   # 'east'
```

---

## Named tuples (bonus)

`collections.namedtuple` gives you a tuple with named fields — readable and still immutable.

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 5)

print(p.x, p.y)    # 3 5
print(p[0])        # 3   — still works like a regular tuple
```

Modern alternative: `dataclass(frozen=True)` — covered later in the OOP chapter.

---

## Quick reference

```text
(1, 2, 3)         create
1, 2, 3           also creates a tuple (parens optional)
(5,)              one-item tuple (comma is required!)
tuple([1, 2])     create from iterable

t[0]              first item
t[-1]             last item
t[a:b]            slice

x, y = t          unpacking
first, *rest = t  unpack with *
a + b             join
a * n             repeat

x in t            membership
len(t)            length
t.count(x)        how many x
t.index(x)        index of first x
```
