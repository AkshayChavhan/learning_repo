# Python Arrays

In most languages, "array" is one specific thing.
In Python, "array" can mean **three different things** — and the right one depends on what you're doing.

| What people call "array" | What it really is              | When to use                                  |
|--------------------------|--------------------------------|----------------------------------------------|
| `list`                   | Built-in, holds any type       | Default. Works for everything.               |
| `array.array`            | Stdlib typed array of one C type | Memory-efficient packed numbers              |
| `numpy.ndarray`          | Third-party fast n-d array     | Numerical/scientific work, vector math       |

This chapter covers all three so you know what to reach for.

---

# Part 1 — `list` (the everyday "array")

Most tutorials, courses, and interviewers say "array" but mean **list**.
Lists were already covered in tut10 — this is a quick recap so you can use it as an array.

## Create

```python
nums = [10, 20, 30, 40, 50]
print(nums)
print(len(nums))
```

```text
[10, 20, 30, 40, 50]
5
```

## Index and slice

```python
nums = [10, 20, 30, 40, 50]

print(nums[0])      # 10  — first
print(nums[-1])     # 50  — last
print(nums[1:4])    # [20, 30, 40]
```

## Modify

```python
nums = [10, 20, 30]
nums[1] = 99
print(nums)         # [10, 99, 30]

nums.append(40)
nums.insert(0, 5)
print(nums)         # [5, 10, 99, 30, 40]
```

## Loop

```python
nums = [10, 20, 30]

for n in nums:
    print(n)

for i, n in enumerate(nums):
    print(i, n)
```

## Length and membership

```python
nums = [10, 20, 30]

print(len(nums))        # 3
print(20 in nums)       # True
print(99 in nums)       # False
```

## Why a list is enough most of the time

- Accepts any type (ints, strings, mixed).
- Built-in syntax — no imports.
- Plenty of methods (`append`, `pop`, `sort`, `reverse`, slicing, comprehensions).
- Used in 99% of Python code where another language would use an array.

Reach for a real array (Part 2 or Part 3) only when you have a **specific** reason — memory, performance, or numerical math.

For everything else `list` did, see tut10.

---

# Part 2 — `array.array` (stdlib typed arrays)

The standard library has an `array` module.
It stores items of **one** primitive C type — like a true C array.

When to consider it:

- You're holding **lots** of numbers of the same type (memory matters).
- You need to read/write a packed binary format (file, socket).
- You're interfacing with C extensions or `numpy`.

Otherwise, prefer `list`.

## Create

```python
import array

a = array.array("i", [1, 2, 3, 4, 5])    # 'i' = signed int
print(a)
print(type(a).__name__)
```

```text
array('i', [1, 2, 3, 4, 5])
array
```

The first argument is a **type code** — what each item is.

## Type codes (most common)

| Code | C type           | Python equivalent | Bytes per item |
|------|------------------|-------------------|----------------|
| `b`  | signed char      | int (-128..127)   | 1              |
| `B`  | unsigned char    | int (0..255)      | 1              |
| `h`  | signed short     | int               | 2              |
| `H`  | unsigned short   | int               | 2              |
| `i`  | signed int       | int               | 4              |
| `I`  | unsigned int     | int               | 4              |
| `l`  | signed long      | int               | 4 or 8         |
| `q`  | signed long long | int               | 8              |
| `f`  | float            | float             | 4              |
| `d`  | double           | float             | 8              |
| `u`  | wchar (Unicode)  | str (1 char)      | 2 or 4         |

Check actual size with `.itemsize`:

```python
import array

a = array.array("i", [1, 2, 3])
print(a.typecode)      # 'i'
print(a.itemsize)      # 4   — bytes per item
```

## Use it like a list — same interface

```python
import array

a = array.array("i", [10, 20, 30])

print(a[0])            # 10
print(a[-1])           # 30
print(a[1:3])          # array('i', [20, 30])
print(len(a))          # 3
print(20 in a)         # True

a.append(40)
a[1] = 99
a.pop()
print(a)
```

```text
10
30
array('i', [20, 30])
3
True
array('i', [10, 99, 30])
```

## The one-type rule

Every item must match the type code. Mixed types fail.

```python
import array

a = array.array("i", [1, 2, 3])
# a.append("hi")
# TypeError: an integer is required
# a.append(3.14)
# TypeError: integer argument expected, got float
```

This is the trade-off — strict typing buys you memory and speed, costs you flexibility.

## Memory difference (rough)

```python
import array, sys

big_list = list(range(100_000))
big_arr  = array.array("i", range(100_000))

print("list  bytes:", sys.getsizeof(big_list))
print("array bytes:", sys.getsizeof(big_arr))
```

(Numbers will vary by Python build; `array` typically uses much less memory because each item is a packed 4-byte int, not a full Python `int` object.)

## Convert to/from list

```python
import array

a = array.array("i", [1, 2, 3])
print(list(a))               # [1, 2, 3]

a2 = array.array("i", [10, 20, 30])
a2.extend([40, 50])
print(a2)
```

```text
[1, 2, 3]
array('i', [10, 20, 30, 40, 50])
```

## When NOT to use `array.array`

- You want mixed types — use `list`.
- You only have a few items — `list` overhead doesn't matter.
- You want vector math (`a + b`, `a * 2`, dot products) — use **numpy** instead. `array.array` doesn't do element-wise math.

```python
import array

a = array.array("i", [1, 2, 3])
b = array.array("i", [4, 5, 6])

print(a + b)    # array('i', [1, 2, 3, 4, 5, 6])  — concatenation, NOT element-wise
```

If you wanted `[5, 7, 9]` (element-wise add), you need numpy.

---

# Part 3 — `numpy.ndarray` (the "real" array for numbers)

For numerical work — math, science, machine learning, data analysis — Python's de facto array is **numpy's `ndarray`**.

> Not in the standard library. Install with `pip install numpy`.

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
print(a)
print(type(a).__name__)
print(a.dtype)         # the element type
print(a.shape)         # the shape (length-1 tuple here)
```

```text
[1 2 3 4 5]
ndarray
int64
(5,)
```

(`int64` may differ on Windows / 32-bit systems.)

## Vector math — the killer feature

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a + b)       # element-wise add  -> [5 7 9]
print(a * 2)       # scalar broadcast  -> [2 4 6]
print(a * b)       # element-wise mul  -> [4 10 18]
print(a @ b)       # dot product       -> 32
```

```text
[5 7 9]
[2 4 6]
[ 4 10 18]
32
```

A plain `list` can't do any of this. `array.array` can't either.

## Multi-dimensional — 2D, 3D, n-D

```python
import numpy as np

grid = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

print(grid)
print(grid.shape)        # (3, 3)
print(grid[0])           # first row -> [1 2 3]
print(grid[:, 0])        # first column -> [1 4 7]
print(grid[1, 2])        # row 1, col 2 -> 6
```

```text
[[1 2 3]
 [4 5 6]
 [7 8 9]]
(3, 3)
[1 2 3]
[1 4 7]
6
```

This is impossible with a plain list of lists without writing your own indexing.

## Useful constructors

```python
import numpy as np

print(np.zeros(5))           # [0. 0. 0. 0. 0.]
print(np.ones((2, 3)))       # 2x3 of ones
print(np.arange(0, 10, 2))   # [0 2 4 6 8]   — like range()
print(np.linspace(0, 1, 5))  # 5 evenly spaced points 0..1
```

```text
[0. 0. 0. 0. 0.]
[[1. 1. 1.]
 [1. 1. 1.]]
[0 2 4 6 8]
[0.   0.25 0.5  0.75 1.  ]
```

## Why numpy is so much faster

Numpy operations run as compiled C code under the hood. A loop over a million Python `list` items takes seconds; the equivalent numpy operation takes milliseconds — because the loop is in C, not Python.

This is the only reason every data-science library on top of Python (`pandas`, `scikit-learn`, `pytorch`, `tensorflow`) is built on numpy.

## When NOT to use numpy

- You have **few** items — overhead isn't worth importing a big library.
- You need mixed types — use `list` or `pandas.DataFrame`.
- You're writing a simple script that doesn't do vector math.

Don't reach for numpy by default. Reach for it when you have a lot of numbers and you want to do math on all of them at once.

---

# Choosing — which "array" do I use?

| Question                                                | Use            |
|----------------------------------------------------------|----------------|
| Default — any task, mixed types, short code              | **`list`**     |
| Lots of numbers of one C type, memory matters            | `array.array`  |
| Reading/writing a packed binary file                     | `array.array`  |
| Vector math / matrix math / numerical computing          | **`numpy`**    |
| Multi-dimensional arrays (image, grid, tensor)           | **`numpy`**    |
| Data tables with column names                            | `pandas.DataFrame` |

Rule of thumb: **`list` until you have a specific reason not to.**

---

# Quick comparison cheatsheet

```python
# 1. list  — everyday, mixed types, no import
nums = [1, 2, 3]
nums.append(4)
nums[0] = 99
print(nums)              # [99, 2, 3, 4]


# 2. array.array  — one C type, packed in memory
import array
a = array.array("i", [1, 2, 3])
a.append(4)              # must be an int
print(a)                 # array('i', [1, 2, 3, 4])


# 3. numpy.ndarray  — vector math, multi-dim
import numpy as np
v = np.array([1, 2, 3])
print(v + 10)            # [11 12 13]   — vector + scalar
print(v * v)             # [1 4 9]       — element-wise
```

---

## Quick reference

```text
list:
    [1, 2, 3]                       any type, no import
    a.append(x)  a.pop()  a[i]=x
    in / len / for / slicing
    a + b  -> concatenation
    a * 3  -> repetition

array.array (stdlib):
    import array
    a = array.array("i", [1, 2, 3]) # 'i' = signed int
    type codes: b B h H i I l q f d u
    a.typecode, a.itemsize          # bytes per item
    same list-like methods
    one type only — TypeError on mismatch
    a + b  -> concatenation, NOT element-wise

numpy.ndarray (pip install numpy):
    import numpy as np
    a = np.array([1, 2, 3])
    a.dtype, a.shape
    a + b, a * 2, a @ b             # vector math
    np.zeros, np.ones, np.arange, np.linspace
    2D: grid[row, col],  grid[:, 0]
```
