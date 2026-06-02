# Python Dictionaries

A **dictionary** stores items as **key → value** pairs.
You look up a value by its key (not by index).

```python
user = {
    "name": "Akshay",
    "age": 30,
    "city": "Mumbai",
}

print(user["name"])    # 'Akshay'
print(user["age"])     # 30
```

Four key facts:

- **Key → value pairs** — every entry has both.
- **Ordered** — keeps the insertion order (Python 3.7+).
- **Mutable** — add, change, and remove entries any time.
- **Keys must be unique and hashable** — values can be anything.

---

## Why dictionaries

The most common general-purpose container in Python.

Use a dict when:

- You want to look up values by a name (not a position).
- You're storing related data about one thing (a user, a record, a config).
- You need fast lookups (`in` is very fast on dicts).
- You're loading JSON — JSON objects map to Python dicts.

---

## Creating a dictionary

```python
empty = {}                                       # empty dict
user = {"name": "Akshay", "age": 30}             # literal

# Using dict()
user = dict(name="Akshay", age=30)
print(user)   # {'name': 'Akshay', 'age': 30}

# From a list of pairs
pairs = [("a", 1), ("b", 2)]
print(dict(pairs))   # {'a': 1, 'b': 2}

# From two parallel lists
keys = ["a", "b", "c"]
values = [1, 2, 3]
print(dict(zip(keys, values)))   # {'a': 1, 'b': 2, 'c': 3}
```

> `{}` is an **empty dict**, not an empty set.
> Empty set is `set()`.

---

## Access a value

By key:

```python
user = {"name": "Akshay", "age": 30}

print(user["name"])    # 'Akshay'
# print(user["email"]) # KeyError — key doesn't exist
```

Safe access with `.get()` — returns `None` (or a default) if missing:

```python
print(user.get("name"))            # 'Akshay'
print(user.get("email"))           # None
print(user.get("email", "N/A"))    # 'N/A'
```

Use `.get()` whenever a key might be missing.

---

## Add or change a value

Same syntax — both add and update.

```python
user = {"name": "Akshay"}

user["age"] = 30           # adds a new key
print(user)                # {'name': 'Akshay', 'age': 30}

user["age"] = 31           # updates existing key
print(user)                # {'name': 'Akshay', 'age': 31}
```

Update many at once with `.update()`:

```python
user.update({"age": 32, "city": "Mumbai"})
print(user)
```

---

## Remove a value

| Method        | What it does                                          |
|---------------|-------------------------------------------------------|
| `del d[k]`    | Delete by key — `KeyError` if missing                 |
| `d.pop(k)`    | Remove and **return** the value — `KeyError` if missing |
| `d.pop(k, x)` | Same, but return `x` if missing (no error)             |
| `d.popitem()` | Remove and return the **last** (key, value) pair       |
| `d.clear()`   | Remove all entries                                    |

```python
user = {"name": "Akshay", "age": 30, "city": "Mumbai"}

removed = user.pop("age")
print(removed)    # 30
print(user)       # {'name': 'Akshay', 'city': 'Mumbai'}

del user["city"]
print(user)       # {'name': 'Akshay'}

user.clear()
print(user)       # {}
```

---

## Check if a key exists

`in` checks keys — not values.

```python
user = {"name": "Akshay", "age": 30}

print("name" in user)      # True
print("Akshay" in user)    # False — that's a value, not a key
print("email" not in user) # True
```

---

## Loop through a dictionary

```python
user = {"name": "Akshay", "age": 30, "city": "Mumbai"}

# Keys (the default)
for key in user:
    print(key)

# Same thing, explicit
for key in user.keys():
    print(key)

# Values only
for value in user.values():
    print(value)

# Key + value together (most useful)
for key, value in user.items():
    print(key, "→", value)
```

---

## The three views — `.keys()`, `.values()`, `.items()`

These return live "views" of the dictionary — they update if the dict changes.

```python
user = {"name": "Akshay", "age": 30}

keys = user.keys()
print(keys)          # dict_keys(['name', 'age'])

user["city"] = "Mumbai"
print(keys)          # dict_keys(['name', 'age', 'city']) — auto-updated!

# Convert to a list if you need a snapshot
print(list(user.keys()))
print(list(user.values()))
print(list(user.items()))
```

---

## All dict methods

| Method                  | What it does                                       |
|-------------------------|----------------------------------------------------|
| `d[k]`                  | Get value by key (errors if missing)               |
| `d[k] = v`              | Set / add a value                                  |
| `d.get(k)`              | Get value, returns `None` if missing               |
| `d.get(k, default)`     | Get value, returns default if missing              |
| `d.setdefault(k, v)`    | Get value, or set to `v` if missing (returns it)   |
| `d.pop(k)` / `d.pop(k, default)` | Remove and return                         |
| `d.popitem()`           | Remove and return last (k, v) pair                 |
| `d.update(other)`       | Merge another dict (or kwargs) into this one       |
| `d.clear()`             | Remove all entries                                 |
| `d.copy()`              | Shallow copy                                       |
| `d.keys()`              | View of keys                                       |
| `d.values()`            | View of values                                     |
| `d.items()`             | View of (key, value) pairs                         |
| `dict.fromkeys(iter, v)`| New dict with each key set to value `v`            |
| `len(d)`                | Number of entries                                  |
| `k in d`                | True if key is present                             |

### `setdefault()` — useful when grouping

Adds a key with a default value only if it's not already there.

```python
d = {}
d.setdefault("fruits", []).append("apple")
d.setdefault("fruits", []).append("banana")
d.setdefault("veg", []).append("carrot")

print(d)   # {'fruits': ['apple', 'banana'], 'veg': ['carrot']}
```

### `dict.fromkeys()` — quick init

```python
print(dict.fromkeys(["a", "b", "c"], 0))   # {'a': 0, 'b': 0, 'c': 0}
```

---

## Merge two dictionaries

| Method                    | Notes                                             |
|---------------------------|---------------------------------------------------|
| `{**a, **b}`              | Make a new merged dict. `b`'s keys win on conflict |
| `a.update(b)`             | Merge `b` into `a` in place                       |
| `a \| b` (Python 3.9+)    | Like `{**a, **b}` — new dict                      |
| `a \|= b` (Python 3.9+)   | In-place merge                                    |

```python
a = {"x": 1, "y": 2}
b = {"y": 99, "z": 3}

print({**a, **b})   # {'x': 1, 'y': 99, 'z': 3}

a.update(b)
print(a)            # {'x': 1, 'y': 99, 'z': 3}
```

---

## Nested dictionaries

Values can be other dicts.

```python
users = {
    "akshay": {"age": 30, "city": "Mumbai"},
    "riya":   {"age": 25, "city": "Delhi"},
}

print(users["akshay"]["city"])   # 'Mumbai'
print(users["riya"]["age"])      # 25
```

Loop through nested:

```python
for name, info in users.items():
    print(name, info["city"])
```

---

## Dict comprehensions

Build a dict from another iterable, all in one line.

```python
# Square of each number
squares = {n: n * n for n in range(5)}
print(squares)   # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Swap keys and values
user = {"name": "Akshay", "age": 30}
flipped = {v: k for k, v in user.items()}
print(flipped)   # {'Akshay': 'name', 30: 'age'}

# Only keep some entries
nums = {"a": 1, "b": 2, "c": 3, "d": 4}
evens = {k: v for k, v in nums.items() if v % 2 == 0}
print(evens)     # {'b': 2, 'd': 4}
```

---

## Copying a dictionary

`b = a` is **not** a copy — both names point to the same dict.

```python
a = {"x": 1}
b = a
b["y"] = 2
print(a)    # {'x': 1, 'y': 2}  — same dict!
```

Real (shallow) copy:

```python
b = a.copy()       # method 1
c = dict(a)        # method 2
d = {**a}          # method 3
```

For nested dicts, use `copy.deepcopy()`:

```python
import copy
nested = {"user": {"name": "Akshay"}}
deep = copy.deepcopy(nested)
```

---

## Valid keys

Keys must be **hashable** — that means immutable in practice.

| Can be a key? | Type                |
|---------------|---------------------|
| ✅            | `str`, `int`, `float`, `bool`, `tuple`, `frozenset`, `None` |
| ❌            | `list`, `dict`, `set` |

```python
d = {}
d[(1, 2)] = "ok — tuple is hashable"

# d[[1, 2]] = "fails"   # TypeError: unhashable type: 'list'
```

Values can be **anything** — lists, dicts, even functions.

---

## Quick reference

```text
{"k": "v"}            create
{}                    empty dict (NOT empty set!)
dict(k=v, k2=v2)      from kwargs
dict(zip(keys, vals)) from parallel lists

d[k]                  get (KeyError if missing)
d.get(k, default)     get safely
d[k] = v              add or update
d.update(other)       merge another dict
d.pop(k)              remove + return
del d[k]              delete
d.clear()             empty

k in d                key exists?
len(d)                number of entries

d.keys()              view of keys
d.values()            view of values
d.items()             view of (k, v) pairs

for k in d:           loop over keys
for k, v in d.items(): loop over pairs

{**a, **b}            merge into new dict
a | b                 merge (3.9+)
{k: v for k in seq}   comprehension

d.copy()              shallow copy
copy.deepcopy(d)      deep copy
```
