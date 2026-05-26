# Python Variables

The single most important sentence:

> A variable is a **name bound to an object**.
> Not a box that holds a value.
> A label pointing at a value.

---

## Creating a variable

No declarations.
First assignment creates the name.

```python
age = 25
name = "Akshay"
price = 99.50
is_active = True
```

`=` means **assign**, not "equal".
The name on the **left** is bound to the object on the **right**.

---

## A name has no type — the object does

You can rebind the same name to any type.

```python
x = 5
print(type(x).__name__)   # int

x = "hello"
print(type(x).__name__)   # str

x = [1, 2, 3]
print(type(x).__name__)   # list
```

This is what "dynamically typed" means.

---

## `a = b` does not copy

Both names point to the **same** object.

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)   # [1, 2, 3, 4]
print(b)   # [1, 2, 3, 4]
```

Mutate through one name → see the change through the other.

---

## Rebinding ≠ mutating

`a = [99]` makes `a` point to a **new** list.
`b` still points to the old one.

```python
a = [1, 2, 3]
b = a
a = [99]
print(a)   # [99]
print(b)   # [1, 2, 3]
```

Rule of thumb:

- `a = something` → rebind `a`. Other names unaffected.
- `a.method(...)` or `a[i] = ...` → mutate the object. Every name pointing to it sees the change.

---

## Multiple assignment

Assign several names at once.

```python
x, y = 1, 2
print(x, y)   # 1 2
```

### Swap (no temp variable)

```python
x, y = 1, 2
x, y = y, x
print(x, y)   # 2 1
```

### Unpack a list or tuple

```python
first, second, third = [10, 20, 30]
print(first, second, third)   # 10 20 30
```

### `*rest` catches the leftovers

```python
first, *rest = [10, 20, 30, 40]
print(first)   # 10
print(rest)    # [20, 30, 40]
```

---

## Chained assignment — same object

`p = q = r = []` makes **all three** names point to the **same** list.

```python
p = q = r = []
p.append("oops")
print(q)   # ['oops']
```

If you wanted three separate empty lists, do it explicitly:

```python
p, q, r = [], [], []
```

---

## Augmented assignment

`x += 1` is short for `x = x + 1` — usually.
But there's a subtle difference for **mutable** types like `list`.

### On numbers (immutable) → new object

```python
n = 5
print(id(n))   # some address
n += 1
print(id(n))   # DIFFERENT — n now points to a new int
```

### On lists (mutable) → same object, mutated

```python
lst = [1, 2]
print(id(lst))   # some address
lst += [3]
print(id(lst))   # SAME — list was modified in place
```

---

## Type hints are documentation

You can annotate a variable with `: type` after the name.
Python does **not** enforce this at runtime.

```python
age: int = 30
age = "thirty"   # legal! Python won't complain.
```

Tools like `mypy` and `pyright` check hints.
Python itself ignores them.

---

## Naming rules

- Letters, digits, underscores only
- Can't start with a digit
- Case-sensitive (`Name` ≠ `name`)
- Can't be a reserved keyword (`for`, `class`, `if`, `lambda`, etc.)

See the full list of keywords:

```python
import keyword
print(keyword.kwlist)
```

---

## Naming conventions (PEP 8)

```python
user_name = "akshay"      # snake_case for variables and functions
MAX_RETRIES = 3           # UPPER_SNAKE_CASE for constants
class UserAccount: ...    # PascalCase for classes
_internal = "hands off"   # leading underscore = "internal"
```

---

## Don't shadow built-ins

Names like `list`, `dict`, `str`, `id`, `type`, `sum`, `max` are built-in.
Don't reuse them.

```python
list = [1, 2, 3]
# Now `list(...)` the type is hidden in this scope.
# new = list("abc")   # TypeError: 'list' object is not callable
```

---

## Quick check

Predict the output, then run it:

```python
a = [1, 2, 3]
b = a
a += [4]
print(a, b)        # both [1, 2, 3, 4] — += mutates the list

c = [1, 2, 3]
d = c
c = c + [4]
print(c, d)        # c is [1, 2, 3, 4], d is [1, 2, 3]
```

`+=` mutates the list in place.
`c = c + [...]` builds a new list and rebinds `c`.
