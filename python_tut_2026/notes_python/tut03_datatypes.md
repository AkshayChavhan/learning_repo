# Python Data Types

The built-in types you'll use almost every day.
Each value in Python is an object of some type.

| Type    | Example          | What it is                       |
|---------|------------------|----------------------------------|
| `int`   | `42`, `-7`       | Whole number, no size limit      |
| `float` | `3.14`, `1.5e-3` | Decimal number (64-bit double)   |
| `bool`  | `True`, `False`  | True / false flag                |
| `str`   | `"hello"`        | Text                             |
| `None`  | `None`           | "No value" / "nothing"           |
| `list`  | `[1, 2, 3]`      | Ordered, changeable collection   |
| `tuple` | `(1, 2, 3)`      | Ordered, frozen collection       |
| `dict`  | `{"k": "v"}`     | Key → value lookup               |
| `set`   | `{1, 2, 3}`      | Unique items, no order           |

---

## `int` — whole numbers

Python integers grow as big as you need.
No 32-bit or 64-bit limit.

```python
a = 42
b = -7
big = 2 ** 200

print(big)
```

Write large numbers with underscores for readability:

```python
salary = 1_500_000
print(salary)   # 1500000
```

Other bases:

```python
print(0xff)    # 255  — hex
print(0o377)   # 255  — octal
print(0b1111)  # 15   — binary
```

---

## `float` — decimal numbers

Same precision as `double` in Java or C.

```python
pi = 3.14
tiny = 1.5e-3   # 0.0015
print(pi, tiny)
```

Float math is not always exact:

```python
print(0.1 + 0.2)          # 0.30000000000000004
print(0.1 + 0.2 == 0.3)   # False
```

Compare floats safely with `math.isclose`:

```python
import math
print(math.isclose(0.1 + 0.2, 0.3))   # True
```

---

## `bool` — True or False

Used in conditions and flags.
Only two values: `True` and `False` (capital first letter).

```python
is_active = True
has_paid = False

print(is_active and has_paid)   # False
print(is_active or has_paid)    # True
print(not is_active)            # False
```

Behind the scenes, `bool` is a subtype of `int`:

```python
print(True + True)   # 2
print(False + 5)     # 5
```

---

## `str` — text

Wrap text in single or double quotes.
Both work the same way.

```python
name = "Akshay"
city = 'Mumbai'

print(name, city)
```

f-strings let you drop variables inside:

```python
age = 30
print(f"{name} is {age} years old")
```

Common string operations:

```python
print(len("hello"))          # 5
print("hello".upper())       # HELLO
print("hello".replace("l", "L"))  # heLLo
print("a,b,c".split(","))    # ['a', 'b', 'c']
```

Strings are **immutable** — methods return a new string.
The original is unchanged.

```python
s = "hello"
s.upper()
print(s)   # hello — still lowercase
```

---

## `None` — the "nothing" value

There is exactly one `None`.
Use it when a variable has no value yet.

```python
result = None

def get_user():
    pass   # returns None

print(get_user() is None)   # True
```

Always check `None` with `is`, not `==`.

---

## `list` — ordered, changeable

A list holds items in order.
You can add, remove, or change items.

```python
fruits = ["apple", "banana", "mango"]

fruits.append("orange")
print(fruits)            # ['apple', 'banana', 'mango', 'orange']

fruits[0] = "grape"
print(fruits)            # ['grape', 'banana', 'mango', 'orange']

print(fruits[1])         # banana
print(len(fruits))       # 4
```

---

## `tuple` — ordered, frozen

Like a list, but **you can't change it** after creation.
Useful for fixed groupings (coordinates, records, returning multiple values).

```python
point = (3, 5)
print(point[0])   # 3

# point[0] = 99   # TypeError — tuples are immutable

x, y = point      # unpack
print(x, y)       # 3 5
```

A 1-item tuple needs a trailing comma:

```python
not_a_tuple = (5)      # just an int in parentheses
real_tuple = (5,)      # tuple with one item
```

---

## `dict` — key → value lookup

Stores pairs.
Look up a value by its key.

```python
user = {
    "name": "Akshay",
    "age": 30,
    "city": "Mumbai",
}

print(user["name"])    # Akshay
print(user["age"])     # 30

user["email"] = "a@x.com"   # add a new key
print(user)
```

Safe lookup with a default:

```python
print(user.get("phone", "N/A"))   # N/A
```

Loop through keys and values:

```python
for key, value in user.items():
    print(key, "→", value)
```

---

## `set` — unique items, no order

A set holds **unique** values.
Order is not guaranteed.

```python
tags = {"python", "code", "python"}
print(tags)            # {'python', 'code'} — duplicate removed
print(len(tags))       # 2

tags.add("learn")
tags.add("python")     # ignored, already there
print(tags)
```

Set math:

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)   # union        → {1, 2, 3, 4, 5}
print(a & b)   # intersection → {3}
print(a - b)   # difference   → {1, 2}
```

---

## Mutable vs immutable — important

**Immutable** (can't be changed after creation):
`int`, `float`, `bool`, `str`, `tuple`, `None`

**Mutable** (can be changed in place):
`list`, `dict`, `set`

```python
# Mutable example
nums = [1, 2, 3]
nums.append(4)
print(nums)   # [1, 2, 3, 4] — same list, now longer

# Immutable example
s = "hello"
s = s + " world"
print(s)      # 'hello world' — but this is a NEW string, not the old one
```

---

## Check the type

`type()` tells you what something is.

```python
print(type(42))           # <class 'int'>
print(type(3.14))         # <class 'float'>
print(type("hi"))         # <class 'str'>
print(type([1, 2]))       # <class 'list'>
print(type({"k": "v"}))   # <class 'dict'>
```

For checks in `if` conditions, use `isinstance`:

```python
x = 5
if isinstance(x, int):
    print("x is an int")
```

---

## Quick converters

The type name is also the constructor.

```python
print(int("42"))        # 42
print(float("3.14"))    # 3.14
print(str(99))          # '99'
print(list("abc"))      # ['a', 'b', 'c']
print(tuple([1, 2]))    # (1, 2)
print(set([1, 1, 2]))   # {1, 2}
print(bool(0))          # False
print(bool("x"))        # True
```

---

## Cheat sheet

```text
int     →  whole number
float   →  decimal number
bool    →  True / False
str     →  text
None    →  nothing
list    →  [ordered, changeable]
tuple   →  (ordered, frozen)
dict    →  {key: value}
set     →  {unique, unordered}
```
