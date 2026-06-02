# Python `for` Loop

A **`for` loop** iterates over an **iterable** — list, tuple, string, set, dict, range, etc.
On each turn, the next item is bound to the loop variable.

```python
for fruit in ["apple", "banana", "cherry"]:
    print(fruit)
```

Output:

```text
apple
banana
cherry
```

One-liner over a string:

```python
for ch in "hi":
    print(ch)
```

```text
h
i
```

Four key facts:

- The header ends with a **`:`**
- The body must be **indented** (4 spaces)
- Works on anything iterable — lists, tuples, strings, sets, dicts, files, generators
- Use `break` to exit early, `continue` to skip an iteration

---

## `range()` — looping a fixed number of times

`range()` produces a sequence of integers. Cheap and lazy — it doesn't build a list.

### `range(n)` — 0 up to n-1

```python
for i in range(5):
    print(i)
```

```text
0
1
2
3
4
```

### `range(a, b)` — a up to b-1

```python
for i in range(2, 6):
    print(i)
```

```text
2
3
4
5
```

### `range(a, b, step)` — custom step

```python
for i in range(0, 10, 2):
    print(i)
```

```text
0
2
4
6
8
```

### Negative step — count down

```python
for i in range(5, 0, -1):
    print(i)
```

```text
5
4
3
2
1
```

| Call               | Yields              |
|--------------------|---------------------|
| `range(5)`         | `0 1 2 3 4`         |
| `range(2, 6)`      | `2 3 4 5`           |
| `range(0, 10, 2)`  | `0 2 4 6 8`         |
| `range(5, 0, -1)`  | `5 4 3 2 1`         |

---

## Looping over collections

### List

```python
for n in [10, 20, 30]:
    print(n)
```

### Tuple

```python
for x in (1, 2, 3):
    print(x)
```

### String

```python
for ch in "abc":
    print(ch)
```

### Set — order is **not** guaranteed

```python
for item in {"a", "b", "c"}:
    print(item)
```

### Dict — iterates over **keys** by default

```python
prices = {"apple": 1, "banana": 2, "cherry": 3}

for key in prices:
    print(key)
```

```text
apple
banana
cherry
```

---

## Looping a dict — keys, values, items

A dict gives you keys when iterated directly.
Use `.values()` and `.items()` to get the other views.

```python
prices = {"apple": 1, "banana": 2, "cherry": 3}

# keys (default)
for k in prices:
    print(k)

# values
for v in prices.values():
    print(v)

# both — items() yields (key, value) tuples
for k, v in prices.items():
    print(k, "->", v)
```

```text
apple
banana
cherry
1
2
3
apple -> 1
banana -> 2
cherry -> 3
```

`in` on a dict also checks **keys**:

```python
prices = {"apple": 1, "banana": 2}

print("apple" in prices)   # True
print(1 in prices)         # False — 1 is a value, not a key
```

---

## `enumerate()` — index + value

You rarely need the index by itself. `enumerate()` gives you both.

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(i, fruit)
```

```text
0 apple
1 banana
2 cherry
```

Start counting from a different number with `start=`:

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
```

```text
1 apple
2 banana
3 cherry
```

---

## `zip()` — loop two (or more) sequences in parallel

```python
names = ["Akshay", "Bina", "Chetan"]
ages = [30, 25, 40]

for name, age in zip(names, ages):
    print(name, age)
```

```text
Akshay 30
Bina 25
Chetan 40
```

Works with three or more:

```python
names = ["Akshay", "Bina"]
ages = [30, 25]
cities = ["Pune", "Mumbai"]

for name, age, city in zip(names, ages, cities):
    print(name, age, city)
```

### Unequal lengths — `zip` stops at the shortest

```python
a = [1, 2, 3]
b = ["x", "y"]

for x, y in zip(a, b):
    print(x, y)
```

```text
1 x
2 y
```

The `3` is silently dropped.

### `zip_longest` — fill in missing values

Use it when you don't want the shorter sequence to truncate the loop.

```python
from itertools import zip_longest

a = [1, 2, 3]
b = ["x", "y"]

for x, y in zip_longest(a, b, fillvalue="-"):
    print(x, y)
```

```text
1 x
2 y
3 -
```

---

## `reversed()` and `sorted()` in a `for` loop

Both return new iterables — the original isn't modified.

### `reversed()` — back to front

```python
for n in reversed([1, 2, 3]):
    print(n)
```

```text
3
2
1
```

### `sorted()` — ascending by default

```python
for n in sorted([3, 1, 2]):
    print(n)
```

```text
1
2
3
```

Descending with `reverse=True`:

```python
for n in sorted([3, 1, 2], reverse=True):
    print(n)
```

```text
3
2
1
```

---

## `break` — exit early

`break` leaves the loop immediately.

```python
for n in range(10):
    if n == 4:
        break
    print(n)

print("done")
```

```text
0
1
2
3
done
```

---

## `continue` — skip to next iteration

`continue` jumps to the next item, skipping the rest of the body.

```python
for n in range(6):
    if n % 2 == 0:
        continue
    print(n)
```

```text
1
3
5
```

Even numbers are skipped.

---

## `for ... else` — runs only if the loop completes without `break`

A `for` can have an `else`. It runs when the loop ends **normally** — not when you `break` out.
The classic use is a search loop: "did we find it?"

### Without `break` — `else` runs

```python
for n in [1, 2, 3]:
    print(n)
else:
    print("loop finished normally")
```

```text
1
2
3
loop finished normally
```

### With `break` — `else` is skipped

```python
numbers = [1, 2, 3, 4, 5]
target = 3

for n in numbers:
    if n == target:
        print("found", n)
        break
else:
    print("not found")
```

```text
found 3
```

If the target isn't there, `else` runs:

```python
numbers = [1, 2, 3, 4, 5]
target = 99

for n in numbers:
    if n == target:
        print("found", n)
        break
else:
    print("not found")
```

```text
not found
```

---

## Nested `for` loops

A loop inside a loop. The inner loop runs in full for each outer iteration.

```python
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

for row in grid:
    for value in row:
        print(value, end=" ")
    print()
```

```text
1 2 3 
4 5 6 
7 8 9 
```

Pairs of indices:

```python
for i in range(3):
    for j in range(3):
        print(f"({i},{j})", end=" ")
    print()
```

```text
(0,0) (0,1) (0,2) 
(1,0) (1,1) (1,2) 
(2,0) (2,1) (2,2) 
```

---

## `pass` — empty body placeholder

A `for` body cannot be empty. `pass` is the no-op.

```python
for n in range(5):
    pass        # TODO — fill in later
```

Useful while sketching out structure.

---

## Comprehensions — quick intro

A **comprehension** is a `for` loop that builds a collection in one line.

### List comprehension

```python
nums = [1, 2, 3, 4]
doubled = [x * 2 for x in nums]
print(doubled)
```

```text
[2, 4, 6, 8]
```

### With a filter

```python
nums = [-2, -1, 0, 1, 2]
positive = [x for x in nums if x > 0]
print(positive)
```

```text
[1, 2]
```

### Set comprehension

```python
words = ["hi", "ho", "hi", "ha"]
unique = {w for w in words}
print(unique)
```

### Dict comprehension

```python
nums = [1, 2, 3, 4]
squares = {n: n * n for n in nums}
print(squares)
```

```text
{1: 1, 2: 4, 3: 9, 4: 16}
```

Comprehensions are great for short, single-purpose loops.
For complex bodies, write a regular `for`.

---

## Common pitfalls

### 1. Modifying a list while iterating over it

This is a classic bug. Items get skipped because the indices shift.

```python
nums = [1, 2, 3, 4, 5]

for n in nums:
    if n % 2 == 0:
        nums.remove(n)   # mutating during iteration

print(nums)   # [1, 3, 5]? Not always — items get skipped
```

**Fix A — iterate over a copy** with `nums[:]` or `list(nums)`:

```python
nums = [1, 2, 3, 4, 5]

for n in nums[:]:        # iterate over a copy
    if n % 2 == 0:
        nums.remove(n)

print(nums)   # [1, 3, 5]
```

**Fix B — build a new list** (usually preferred):

```python
nums = [1, 2, 3, 4, 5]
nums = [n for n in nums if n % 2 != 0]
print(nums)   # [1, 3, 5]
```

### 2. Late binding with lambdas in a loop

Lambdas capture the **variable**, not its value at loop time.

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])   # [2, 2, 2] — not [0, 1, 2]
```

Fix with a default argument that captures the current value:

```python
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])   # [0, 1, 2]
```

### 3. Confusing dict iteration — keys, not values

```python
prices = {"apple": 1, "banana": 2}

for x in prices:
    print(x)        # 'apple', 'banana' — keys, not values
```

Use `.values()` or `.items()` if you want the values.

### 4. `range(len(lst))` when `enumerate(lst)` is cleaner

Common but clunky:

```python
fruits = ["apple", "banana", "cherry"]

for i in range(len(fruits)):
    print(i, fruits[i])
```

Cleaner:

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(i, fruit)
```

---

## `for` vs `while`

| Use `for`                               | Use `while`                          |
|-----------------------------------------|--------------------------------------|
| You have a collection or range          | You don't know how many iterations   |
| Number of iterations is known           | Stop when some condition flips       |
| Looping items of a list/dict/string     | Polling, waiting, reading input      |
| One pass over an iterable               | Indefinite repeat until a signal     |

Rule of thumb: if you can write it with `for`, prefer `for`.

---

## Quick reference

```text
for item in iterable:
    body
else:                       # optional — runs if loop didn't break
    body

break                       # exit the loop
continue                    # skip to next item
pass                        # empty body placeholder

# range
range(n)                    # 0 .. n-1
range(a, b)                 # a .. b-1
range(a, b, step)           # custom step (can be negative)

# helpers
enumerate(seq)              # (i, item)
enumerate(seq, start=1)     # (1, item), (2, item), ...
zip(a, b)                   # stops at shortest
zip(a, b, c)                # any number of iterables
zip_longest(a, b, fillvalue=...)   # from itertools — fills shorter
reversed(seq)               # back to front
sorted(seq)                 # ascending — sorted(seq, reverse=True)

# dict iteration
for k in d: ...             # keys (default)
for v in d.values(): ...    # values
for k, v in d.items(): ...  # both

# comprehensions
[x*2 for x in nums]
[x for x in nums if x > 0]
{x for x in nums}
{n: n*n for n in nums}
```
