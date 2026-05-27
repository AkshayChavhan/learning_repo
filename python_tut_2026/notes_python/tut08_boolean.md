# Python Booleans

A **boolean** is a value that is either `True` or `False`.
Used everywhere — `if` conditions, loops, flags.

```python
is_active = True
has_paid = False

print(is_active)   # True
print(has_paid)    # False
```

Capital first letter.
`true` / `false` (lowercase) are **not** valid Python.

---

## Boolean from a comparison

Comparison operators return a boolean.

```python
print(5 > 3)      # True
print(5 == 3)     # False
print("a" == "a") # True
print(10 != 5)    # True
```

| Operator | Meaning            |
|----------|--------------------|
| `==`     | Equal              |
| `!=`     | Not equal          |
| `>`      | Greater than       |
| `<`      | Less than          |
| `>=`     | Greater or equal   |
| `<=`     | Less or equal      |

---

## Logical operators — `and`, `or`, `not`

Combine booleans.

```python
a = True
b = False

print(a and b)   # False  — both must be True
print(a or b)    # True   — at least one is True
print(not a)     # False  — flips it
```

Truth table:

| `a`     | `b`     | `a and b` | `a or b` |
|---------|---------|-----------|----------|
| True    | True    | True      | True     |
| True    | False   | False     | True     |
| False   | True    | False     | True     |
| False   | False   | False     | False    |

---

## In an `if` statement

```python
age = 20

if age >= 18:
    print("adult")
else:
    print("minor")
```

You can combine conditions:

```python
age = 25
has_id = True

if age >= 18 and has_id:
    print("can enter")
```

---

## Most values are True

Almost any value evaluates to **True** if it has some sort of content.

- Any string is `True`, except an **empty** string.
- Any number is `True`, except `0`.
- Any list, tuple, set, or dictionary is `True`, except **empty** ones.

```python
print(bool("hello"))     # True
print(bool(123))         # True
print(bool(-1))          # True   — non-zero counts
print(bool(3.14))        # True

print(bool(["apple"]))   # True
print(bool((1, 2)))      # True
print(bool({"k": "v"}))  # True
print(bool({1, 2, 3}))   # True
```

---

## Some values are False

In fact, there are not many values that evaluate to `False`, except empty values, such as `()`, `[]`, `{}`, `""`, the number `0`, and the value `None`.
And of course the value `False` evaluates to `False`.

```python
print(bool(False))   # False
print(bool(None))    # False
print(bool(0))       # False
print(bool(""))      # False
print(bool(()))      # False
print(bool([]))      # False
print(bool({}))      # False
```

---

## Truthy in action

You can put any value directly in an `if` — no need to compare to `True`.

```python
if "hello":          # non-empty string → truthy
    print("yes")

if []:               # empty list → falsy
    print("won't print")

if 0:                # zero → falsy
    print("won't print")
```

**Watch out** — these surprise beginners:

```python
print(bool([0]))       # True  — list has one item (its content is 0, but the list itself is non-empty)
print(bool("False"))   # True  — non-empty string, even though the text says "False"
print(bool("0"))       # True  — non-empty string
print(bool(" "))       # True  — a single space is still a non-empty string
```

---

## Functions that return a boolean

Python has many built-in functions that return `True` or `False`.
The most common is `isinstance()` — check if an object is of a certain type.

```python
x = 200

print(isinstance(x, int))     # True
print(isinstance(x, str))     # False
print(isinstance("hi", str))  # True
```

You can test against several types at once by passing a tuple:

```python
def is_number(x):
    return isinstance(x, (int, float))

print(is_number(5))      # True
print(is_number(3.14))   # True
print(is_number("5"))    # False
```

### Common boolean-returning built-ins

| Function              | Returns `True` when…                            | Example                                                |
|-----------------------|--------------------------------------------------|--------------------------------------------------------|
| `isinstance(x, T)`    | `x` is of type `T` (or a subclass)               | `isinstance(5, int)` → `True`                          |
| `issubclass(A, B)`    | Class `A` is a subclass of `B`                   | `issubclass(bool, int)` → `True`                       |
| `callable(x)`         | `x` can be called like a function                | `callable(print)` → `True`                             |
| `hasattr(obj, "name")`| The object has an attribute called `"name"`      | `hasattr("hi", "upper")` → `True`                      |
| `all(iterable)`       | Every item is truthy (also `True` if empty)      | `all([1, 2, 3])` → `True`                              |
| `any(iterable)`       | At least one item is truthy                      | `any([0, "", 5])` → `True`                             |
| `bool(x)`             | `x` is truthy                                    | `bool([1])` → `True`                                   |
| `"x" in container`    | `"x"` is in the container                        | `"py" in "python"` → `True`                            |

### Using `all()` and `any()`

`all()` — every item must be truthy.

```python
print(all([1, 2, 3]))         # True
print(all([1, 0, 3]))         # False  — 0 is falsy
print(all([]))                # True   — empty is vacuously True
```

`any()` — at least one item must be truthy.

```python
print(any([0, 0, 0]))         # False
print(any([0, 1, 0]))         # True
print(any([]))                # False
```

Common usage with a condition:

```python
nums = [4, 7, 12, 18]

print(all(n > 0 for n in nums))   # True   — all positive
print(any(n > 10 for n in nums))  # True   — at least one over 10
```

---

## Idiomatic checks

Don't write the verbose form on the left.
Write the short idiom on the right.

| Verbose                | Idiomatic        |
|------------------------|------------------|
| `if x == True:`        | `if x:`          |
| `if x == False:`       | `if not x:`      |
| `if x == None:`        | `if x is None:`  |
| `if len(lst) > 0:`     | `if lst:`        |
| `if len(lst) == 0:`    | `if not lst:`    |

```python
name = "Akshay"

if name:                # truthy test
    print("got a name")

users = []

if not users:           # falsy test
    print("no users yet")
```

---

## `bool` is a subtype of `int`

`True` equals `1`, `False` equals `0`.
You can add them like numbers.

```python
print(True + True)     # 2
print(True + 5)        # 6
print(False * 10)      # 0
```

Useful trick — count how many `True`s in a list:

```python
votes = [True, False, True, True, False]
print(sum(votes))      # 3
```

---

## Short-circuit evaluation

`and` and `or` stop as soon as the answer is known.
This lets you write safe checks.

```python
user = None

# Safe — short-circuits on None
if user and user.is_active:
    print("active user")
```

If `user` is `None`, the second part is never evaluated, so no error.

`or` returns the **first truthy value**, not always a bool:

```python
name = ""
display = name or "Guest"
print(display)   # 'Guest'
```

---

## Comparison chaining

Python lets you chain comparisons in a natural way.

```python
age = 25

if 18 <= age < 65:
    print("working age")
```

Equivalent to `18 <= age and age < 65`, but cleaner.

---

## Quick reference

```text
True, False               the two boolean values

==  !=  >  <  >=  <=      comparisons → bool

and  or  not              logical operators
                          short-circuit evaluation

bool(x)                   convert anything to True/False
if x:                     truthy test
if not x:                 falsy test
if x is None:             None check

True + True == 2          bool is a subtype of int
sum([True, False, True])  count True values → 2
```
