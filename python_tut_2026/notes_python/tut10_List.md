# Python Lists

A **list** is an ordered, changeable collection.
Holds any type — numbers, strings, even other lists.

```python
fruits = ["apple", "banana", "mango"]
print(fruits)
```

Four key facts:

- **Ordered** — items keep the order you added them.
- **Changeable** — add, remove, or replace items at any time.
- **Allows duplicates** — same value can appear many times.
- **Mixed types OK** — `[1, "hi", True, 3.14]` is valid.

---

## Creating a list

```python
empty = []
nums = [1, 2, 3, 4]
mixed = [1, "hi", True, 3.14]
nested = [[1, 2], [3, 4]]

# From other types
chars = list("abc")        # ['a', 'b', 'c']
from_range = list(range(5)) # [0, 1, 2, 3, 4]
```

---

## Indexing — get an item

Indexes start at `0`.
Negative indexes count from the end.

```python
fruits = ["apple", "banana", "mango", "orange"]

print(fruits[0])    # 'apple'    — first
print(fruits[2])    # 'mango'
print(fruits[-1])   # 'orange'   — last
print(fruits[-2])   # 'mango'    — second to last
```

Index out of range → `IndexError`.

```python
# print(fruits[10])   # IndexError
```

---

## Slicing — get a sub-list

`list[start:stop:step]`.
`stop` is **exclusive**.

```python
nums = [10, 20, 30, 40, 50]

print(nums[1:4])    # [20, 30, 40]
print(nums[:3])     # [10, 20, 30]   — start to index 3
print(nums[2:])     # [30, 40, 50]   — from index 2 to end
print(nums[::2])    # [10, 30, 50]   — every 2nd
print(nums[::-1])   # [50, 40, 30, 20, 10]   — reverse
```

---

## Change items

Replace by index:

```python
fruits = ["apple", "banana", "mango"]
fruits[1] = "grape"
print(fruits)   # ['apple', 'grape', 'mango']
```

Replace a slice (can change the list's length):

```python
nums = [1, 2, 3, 4, 5]
nums[1:4] = [20, 30]
print(nums)   # [1, 20, 30, 5]
```

---

## Add items

| Method            | What it does                              |
|-------------------|-------------------------------------------|
| `append(x)`       | Add `x` to the end                        |
| `insert(i, x)`    | Insert `x` at index `i`                   |
| `extend(iter)`    | Add all items from another iterable       |

```python
fruits = ["apple", "banana"]

fruits.append("mango")
print(fruits)   # ['apple', 'banana', 'mango']

fruits.insert(0, "grape")
print(fruits)   # ['grape', 'apple', 'banana', 'mango']

fruits.extend(["orange", "kiwi"])
print(fruits)   # ['grape', 'apple', 'banana', 'mango', 'orange', 'kiwi']
```

`append` vs `extend` — common confusion:

```python
a = [1, 2]
a.append([3, 4])    # adds the list as ONE item
print(a)            # [1, 2, [3, 4]]

b = [1, 2]
b.extend([3, 4])    # adds each item one by one
print(b)            # [1, 2, 3, 4]
```

---

## Remove items

| Method        | What it does                                       |
|---------------|----------------------------------------------------|
| `remove(x)`   | Remove **first occurrence** of value `x`           |
| `pop(i)`      | Remove and **return** item at index `i` (default: last) |
| `pop()`       | Remove and return the last item                    |
| `clear()`     | Remove all items                                   |
| `del list[i]` | Delete item at index `i` (no return value)         |

```python
fruits = ["apple", "banana", "mango", "banana"]

fruits.remove("banana")   # removes only the first one
print(fruits)             # ['apple', 'mango', 'banana']

last = fruits.pop()
print(last)               # 'banana'
print(fruits)             # ['apple', 'mango']

del fruits[0]
print(fruits)             # ['mango']

fruits.clear()
print(fruits)             # []
```

---

## Loop through a list

```python
fruits = ["apple", "banana", "mango"]

for fruit in fruits:
    print(fruit)
```

With index using `enumerate`:

```python
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

Loop two lists in parallel with `zip`:

```python
names = ["Akshay", "Riya"]
ages = [30, 25]

for name, age in zip(names, ages):
    print(name, age)
```

---

## Check membership and count

```python
nums = [1, 2, 3, 2, 4, 2]

print(2 in nums)        # True
print(99 in nums)       # False
print(99 not in nums)   # True

print(nums.count(2))    # 3
print(nums.index(3))    # 2   — index of first 3
print(len(nums))        # 6
```

---

## Sort and reverse

`sort()` modifies the list in place.
`sorted()` returns a new list.

```python
nums = [4, 1, 7, 2]

nums.sort()
print(nums)     # [1, 2, 4, 7]

nums.sort(reverse=True)
print(nums)     # [7, 4, 2, 1]

# sorted() doesn't change the original
original = [4, 1, 7, 2]
new = sorted(original)
print(new)       # [1, 2, 4, 7]
print(original)  # [4, 1, 7, 2]
```

Sort by a key:

```python
names = ["Akshay", "Bo", "Charlie"]
names.sort(key=len)
print(names)    # ['Bo', 'Akshay', 'Charlie']  — by length
```

Reverse the list:

```python
nums = [1, 2, 3]
nums.reverse()
print(nums)     # [3, 2, 1]
```

---

## Copying a list

`b = a` is **not** a copy — both names point to the same list.

```python
a = [1, 2, 3]
b = a
b.append(99)
print(a)    # [1, 2, 3, 99]   — same list!
```

Real copies:

```python
a = [1, 2, 3]

b = a.copy()         # method 1
c = list(a)          # method 2
d = a[:]             # method 3

b.append(99)
print(a)   # [1, 2, 3]   — unchanged
print(b)   # [1, 2, 3, 99]
```

For nested lists, use `copy.deepcopy()`:

```python
import copy
nested = [[1, 2], [3, 4]]
deep = copy.deepcopy(nested)
```

---

## Join two lists

There are several ways to join two lists.
Each has a different effect — pick based on what you need.

### 1. Using `+` — new list

`+` creates a **new** list. The originals are unchanged.

```python
a = [1, 2, 3]
b = [4, 5, 6]

c = a + b
print(c)    # [1, 2, 3, 4, 5, 6]
print(a)    # [1, 2, 3]  — unchanged
```

### 2. Using `extend()` — modifies the first list

`extend()` adds all items from `b` into `a` **in place**.
The first list grows. The second is unchanged.

```python
a = [1, 2, 3]
b = [4, 5, 6]

a.extend(b)
print(a)    # [1, 2, 3, 4, 5, 6]
print(b)    # [4, 5, 6]  — unchanged
```

### 3. Using `append()` in a loop

Adds items one by one.
Same effect as `extend()`, but more verbose.

```python
a = [1, 2, 3]
b = [4, 5, 6]

for item in b:
    a.append(item)

print(a)    # [1, 2, 3, 4, 5, 6]
```

### 4. Unpacking with `*` (Python 3.5+)

Useful when you want to combine more than two, or insert items between them.

```python
a = [1, 2, 3]
b = [4, 5, 6]

c = [*a, *b]
print(c)    # [1, 2, 3, 4, 5, 6]

# Mix items into the new list
d = [0, *a, 99, *b]
print(d)    # [0, 1, 2, 3, 99, 4, 5, 6]
```

### Which to use?

| Goal                                       | Use         |
|--------------------------------------------|-------------|
| Make a brand-new list, keep originals      | `a + b`     |
| Add `b` into `a` (modify `a`)              | `a.extend(b)` |
| Combine more than two, or insert items     | `[*a, *b]`  |

---

## Repeating a list

`*` repeats a list.

```python
print([0] * 5)            # [0, 0, 0, 0, 0]
print(["a", "b"] * 3)     # ['a', 'b', 'a', 'b', 'a', 'b']
```

Useful for an empty list of a fixed size:

```python
slots = [None] * 4
print(slots)              # [None, None, None, None]
```

**Warning** — don't use `*` to make a list of mutable objects.
All copies point to the **same** object:

```python
grid = [[]] * 3       # three references to the SAME inner list
grid[0].append(1)
print(grid)           # [[1], [1], [1]]  — surprise!

# Use a comprehension instead:
grid = [[] for _ in range(3)]
grid[0].append(1)
print(grid)           # [[1], [], []]
```

---

## List comprehensions

A short way to build a list from another iterable.

```python
# Squares of 0..4
squares = [x * x for x in range(5)]
print(squares)   # [0, 1, 4, 9, 16]

# Only even numbers
evens = [x for x in range(10) if x % 2 == 0]
print(evens)     # [0, 2, 4, 6, 8]

# Transform strings
words = ["hello", "world"]
upper = [w.upper() for w in words]
print(upper)     # ['HELLO', 'WORLD']
```

---

## All list methods

| Method        | What it does                                        |
|---------------|-----------------------------------------------------|
| `append(x)`   | Add `x` to the end                                  |
| `extend(it)`  | Add all items from an iterable                      |
| `insert(i,x)` | Insert `x` at index `i`                             |
| `remove(x)`   | Remove first occurrence of `x`                      |
| `pop(i)`      | Remove and return item at index `i` (default: last) |
| `clear()`     | Remove all items                                    |
| `index(x)`    | Index of first `x` — raises `ValueError` if missing |
| `count(x)`    | Number of times `x` appears                         |
| `sort()`      | Sort in place                                       |
| `reverse()`   | Reverse in place                                    |
| `copy()`      | Return a shallow copy                               |

---

## Quick reference

```text
[1, 2, 3]         create
lst[0]            first item
lst[-1]           last item
lst[a:b]          slice from a to b (exclusive)
lst[a:b:s]        with step s

lst.append(x)     add to end
lst.insert(i, x)  insert at index i
lst.extend(it)    add each item from iterable
lst.remove(x)     remove first x
lst.pop()         remove + return last
lst.pop(i)        remove + return at index i
del lst[i]        delete at index i
lst.clear()       empty the list

x in lst          True if x is present
len(lst)          number of items
lst.count(x)      how many x
lst.index(x)      where is x

lst.sort()        sort in place
sorted(lst)       new sorted list
lst.reverse()     reverse in place

lst.copy()        shallow copy
list(lst)         shallow copy
lst[:]            shallow copy
copy.deepcopy(lst) deep copy

[x*2 for x in lst]            comprehension
[x for x in lst if cond]       comprehension with filter
```
