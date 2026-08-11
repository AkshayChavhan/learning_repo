# Python Collections — Master Comparison Table

A single page covering all four built-in collections.
Read this first; dive into a specific file only when you need the deep version.

The four collections:

| Type     | Syntax           | One-line idea                              |
|----------|------------------|--------------------------------------------|
| **list** | `[1, 2, 3]`      | Ordered, changeable, allows duplicates     |
| **tuple**| `(1, 2, 3)`      | Ordered, **frozen**, allows duplicates     |
| **set**  | `{1, 2, 3}`      | Unordered, changeable, **unique** items    |
| **dict** | `{"k": "v"}`     | Key → value pairs                          |

---

## Core feature comparison

| Feature              | list                    | tuple                   | set                  | dict                          |
|----------------------|-------------------------|-------------------------|----------------------|-------------------------------|
| Syntax               | `[1, 2, 3]`             | `(1, 2, 3)`             | `{1, 2, 3}`          | `{"k": "v"}`                  |
| Empty form           | `[]`                    | `()`                    | `set()` (NOT `{}`)   | `{}`                          |
| Ordered              | Yes                     | Yes                     | No                   | Yes (3.7+, insertion order)   |
| Mutable              | Yes                     | **No**                  | Yes                  | Yes                           |
| Allows duplicates    | Yes                     | Yes                     | **No**               | Keys: no. Values: yes         |
| Indexed (`x[0]`)     | Yes                     | Yes                     | No                   | By key, not index             |
| Sliceable (`x[1:3]`) | Yes                     | Yes                     | No                   | No                            |
| Can be dict key      | No                      | Yes (if items hashable) | No (use frozenset)   | No                            |
| Items must be hashable| No                     | No                      | **Yes**              | Keys yes, values no           |
| `len(x)`             | Works                   | Works                   | Works                | Works (number of keys)        |
| `in x` check         | Slow (scans items)      | Slow (scans items)      | **Fast** (hash)      | **Fast** (checks keys)        |
| Memory               | Medium                  | Smaller                 | Larger               | Larger                        |

---

## Add an item

| Collection | How to add                                                  | Notes                                  |
|------------|-------------------------------------------------------------|----------------------------------------|
| **list**   | `lst.append(x)` — at end                                    | Modifies in place                      |
| **list**   | `lst.insert(i, x)` — at index `i`                            | Shifts items right                     |
| **list**   | `lst.extend([a, b])` — many items                           | Each item added separately             |
| **tuple**  | **Can't add.** Build a new one: `t + (x,)`                  | Tuples are immutable                   |
| **set**    | `s.add(x)` — one item                                       | Duplicate is silently ignored          |
| **set**    | `s.update([a, b])` — many items                             | Adds each, drops duplicates            |
| **dict**   | `d[k] = v` — set a key/value                                | Same syntax adds or updates            |
| **dict**   | `d.update({k1: v1, k2: v2})` — many pairs                   | Existing keys are overwritten          |

---

## Remove an item

| Collection | How to remove                                               | Notes                                  |
|------------|-------------------------------------------------------------|----------------------------------------|
| **list**   | `lst.remove(x)` — by value                                  | First occurrence only; `ValueError` if missing |
| **list**   | `lst.pop()` / `lst.pop(i)` — by index                       | Returns the removed item               |
| **list**   | `del lst[i]` — by index                                     | No return value                        |
| **list**   | `lst.clear()` — remove all                                  | Empty list left behind                 |
| **tuple**  | **Can't remove.** Convert → list → modify → tuple           | Tuples are immutable                   |
| **set**    | `s.remove(x)` — by value                                    | `KeyError` if missing                  |
| **set**    | `s.discard(x)` — by value                                   | Silent if missing                      |
| **set**    | `s.pop()` — random item                                     | Returns the removed item               |
| **set**    | `s.clear()`                                                 |                                        |
| **dict**   | `del d[k]`                                                  | `KeyError` if key missing              |
| **dict**   | `d.pop(k)` / `d.pop(k, default)`                            | Returns the value                      |
| **dict**   | `d.popitem()`                                               | Removes and returns last (k, v) pair   |
| **dict**   | `d.clear()`                                                 |                                        |

---

## Access an item

| Collection | How to access            | Example                          | If missing                |
|------------|--------------------------|----------------------------------|---------------------------|
| **list**   | `lst[i]`                 | `lst[0]`, `lst[-1]`              | `IndexError`              |
| **list**   | Slice: `lst[a:b]`        | `lst[1:4]`                       | Empty list, no error      |
| **tuple**  | `t[i]`                   | `t[0]`                           | `IndexError`              |
| **tuple**  | Slice: `t[a:b]`          | `t[1:4]`                         | Empty tuple, no error     |
| **set**    | **No indexing.** Loop instead | `for x in s:`               | —                         |
| **dict**   | `d[k]`                   | `d["name"]`                      | `KeyError`                |
| **dict**   | `d.get(k, default)`      | `d.get("name", "N/A")`           | Returns default           |

---

## Change an item

| Collection | How to change                          | Notes                                  |
|------------|----------------------------------------|----------------------------------------|
| **list**   | `lst[i] = x` — by index                | Easy                                   |
| **list**   | `lst[a:b] = [x, y]` — replace slice    | Can change list length                 |
| **tuple**  | **Can't change.** Rebuild              |                                        |
| **set**    | Can't change an item directly. Remove old + add new |                            |
| **dict**   | `d[k] = v` — by key                    | Same syntax as adding                  |

---

## Loop patterns

| Collection | Plain loop                  | With index / key                       |
|------------|-----------------------------|----------------------------------------|
| **list**   | `for x in lst:`             | `for i, x in enumerate(lst):`          |
| **tuple**  | `for x in t:`               | `for i, x in enumerate(t):`            |
| **set**    | `for x in s:` (order varies) | No index — sets are unordered          |
| **dict**   | `for k in d:` (keys)        | `for k, v in d.items():`               |
| **dict**   | `for v in d.values():`      | `for k in d.keys():`                   |

---

## Common methods at a glance

| Method        | list   | tuple  | set    | dict   |
|---------------|--------|--------|--------|--------|
| `len(x)`      | ✅     | ✅     | ✅     | ✅     |
| `x in c`      | ✅     | ✅     | ✅     | ✅ (keys) |
| `.append(x)`  | ✅     | ❌     | ❌     | ❌     |
| `.insert(i,x)`| ✅     | ❌     | ❌     | ❌     |
| `.extend(it)` | ✅     | ❌     | ❌     | ❌     |
| `.add(x)`     | ❌     | ❌     | ✅     | ❌     |
| `.update(it)` | ❌     | ❌     | ✅     | ✅     |
| `.remove(x)`  | ✅     | ❌     | ✅     | ❌     |
| `.discard(x)` | ❌     | ❌     | ✅     | ❌     |
| `.pop(...)`   | ✅     | ❌     | ✅ (random) | ✅ (by key) |
| `.popitem()`  | ❌     | ❌     | ❌     | ✅     |
| `.clear()`    | ✅     | ❌     | ✅     | ✅     |
| `.count(x)`   | ✅     | ✅     | ❌     | ❌     |
| `.index(x)`   | ✅     | ✅     | ❌     | ❌     |
| `.sort()`     | ✅     | ❌     | ❌     | ❌     |
| `.reverse()`  | ✅     | ❌     | ❌     | ❌     |
| `.copy()`     | ✅     | ❌ (no need) | ✅ | ✅     |
| `.keys()`     | ❌     | ❌     | ❌     | ✅     |
| `.values()`   | ❌     | ❌     | ❌     | ✅     |
| `.items()`    | ❌     | ❌     | ❌     | ✅     |
| `.get(k, d)`  | ❌     | ❌     | ❌     | ✅     |
| Set math (`\|`, `&`, `-`, `^`) | ❌ | ❌ | ✅ | ❌ |

---

## Joining and combining

| Collection | Combine                              | Repeat                  |
|------------|--------------------------------------|-------------------------|
| **list**   | `a + b` (new list)                   | `[0] * 5`               |
| **list**   | `a.extend(b)` (in place)             |                         |
| **list**   | `[*a, *b]` (unpack)                  |                         |
| **tuple**  | `a + b` (new tuple)                  | `(0,) * 5`              |
| **tuple**  | `(*a, *b)`                           |                         |
| **set**    | `a \| b` (union)                     | No repeat — items unique |
| **set**    | `a.update(b)`                        |                         |
| **dict**   | `{**a, **b}` (merge)                 | No repeat               |
| **dict**   | `a \| b` (3.9+)                      |                         |
| **dict**   | `a.update(b)`                        |                         |

---

## Copying

| Collection | Shallow copy                         | Deep copy (nested data)             |
|------------|--------------------------------------|-------------------------------------|
| **list**   | `lst.copy()`, `list(lst)`, `lst[:]`  | `copy.deepcopy(lst)`                |
| **tuple**  | Not needed (immutable) — `t` is fine | `copy.deepcopy(t)` if contains lists |
| **set**    | `s.copy()`, `set(s)`                  | `copy.deepcopy(s)`                  |
| **dict**   | `d.copy()`, `dict(d)`, `{**d}`        | `copy.deepcopy(d)`                  |

**Reminder:** `b = a` is **not** a copy for any mutable type — both names point to the same object.

---

## When to pick which

| Use a…   | When you need…                                                      |
|----------|---------------------------------------------------------------------|
| **list** | Order matters and the data will change (add, remove, sort)          |
| **tuple**| Fixed groupings (coordinates, records) or a hashable container       |
| **set**  | Uniqueness, fast `in` checks, or set math (union/intersection/etc.) |
| **dict** | Look up values by a key (most common general-purpose container)     |

---

## Mini reference cheatsheet

```text
list   →  [1, 2, 3]        ordered, changeable, duplicates ok
tuple  →  (1, 2, 3)        ordered, frozen, duplicates ok
set    →  {1, 2, 3}        unordered, unique, hashable items
dict   →  {"k": "v"}       key → value lookup
```

```text
Add:       list.append/insert/extend   |  set.add/update   |  dict[k]=v
Remove:    list.remove/pop/del         |  set.remove/discard/pop  |  dict.pop/del
Access:    list[i] / dict[k]
Loop:      for x in collection         |  for k, v in dict.items()
Length:    len(x)
Membership:x in collection
```
