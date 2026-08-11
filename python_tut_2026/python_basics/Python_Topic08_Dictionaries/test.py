# =============================================================
# PYTHON DICTIONARIES — every method, operator and pattern
# =============================================================
# A dict maps KEY -> VALUE. Ordered (3.7+), mutable, keys are UNIQUE.
# Keys must be HASHABLE (str, int, tuple...) — values can be anything.
# Lookup by key is O(1) — that's the whole point.
# =============================================================

import sys
from collections import Counter, defaultdict

person = {"name": "Akshay", "age": 29, "city": "Pune", "skills": ["py", "js"]}
print("person        ->", person)
print("type / len    ->", type(person), len(person))


# -------------------------------------------------------------
# 1) CREATING DICTS
# -------------------------------------------------------------
print("\n--- 1) CREATING ---")
print("literal       ->", {"a": 1, "b": 2})
print("empty         ->", {}, dict())
print("dict(kwargs)  ->", dict(a=1, b=2))              # keys must be valid names
print("dict(pairs)   ->", dict([("a", 1), ("b", 2)]))
print("dict(zip)     ->", dict(zip("abc", [1, 2, 3])))
print("fromkeys      ->", dict.fromkeys(["a", "b"], 0))    # same default value
print("fromkeys None ->", dict.fromkeys("abc"))            # values default to None
print("comprehension ->", {x: x * x for x in range(4)})
print("nested        ->", {"user": {"name": "A", "tags": [1, 2]}})

# Keys must be hashable; duplicate keys -> LAST one wins
print("dup keys      ->", {"a": 1, "a": 2})            # {'a': 2}
try:
    {[1, 2]: "x"}
except TypeError as e:
    print("list key      -> TypeError:", e)
print("tuple key OK  ->", {(0, 1): "point"})


# -------------------------------------------------------------
# 2) READING VALUES
# -------------------------------------------------------------
print("\n--- 2) READING ---")
print("person['name']->", person["name"])
try:
    person["salary"]
except KeyError as e:
    print("missing key   -> KeyError:", e)             # [] is STRICT

print("get('name')   ->", person.get("name"))
print("get missing   ->", person.get("salary"))        # None — SAFE, no error
print("get + default ->", person.get("salary", 0))     # 0
print("nested read   ->", person["skills"][0])
print("chained get   ->", person.get("meta", {}).get("x", "n/a"))   # safe nesting


# -------------------------------------------------------------
# 3) ADDING & UPDATING
# -------------------------------------------------------------
print("\n--- 3) WRITING ---")
d = {"a": 1}
d["b"] = 2                    # same syntax adds OR overwrites
print("add key       ->", d)
d["a"] = 99
print("overwrite     ->", d)
d.update({"c": 3, "a": 1})    # merge another dict in
print("update(dict)  ->", d)
d.update(e=5)                 # kwargs form
print("update(kwargs)->", d)
d.update([("f", 6)])          # pairs form
print("update(pairs) ->", d)

# setdefault: read it, but insert a default if the key is missing
d2 = {"a": 1}
print("setdefault hit->", d2.setdefault("a", 999))     # 1 — existing value kept
print("setdefault new->", d2.setdefault("b", 2))       # 2 — and it gets INSERTED
print("after         ->", d2)


# -------------------------------------------------------------
# 4) REMOVING
# -------------------------------------------------------------
print("\n--- 4) REMOVING ---")
d = {"a": 1, "b": 2, "c": 3, "d": 4}
print("pop('a')      ->", d.pop("a"), "| left:", d)    # returns the VALUE
print("pop + default ->", d.pop("zz", "none"))         # safe when missing
try:
    d.pop("zz")
except KeyError as e:
    print("pop missing   -> KeyError:", e)

print("popitem()     ->", d.popitem(), "| left:", d)   # removes the LAST pair
del d["b"]
print("del d['b']    ->", d)
d.clear()
print("clear()       ->", d)


# =============================================================
# 5) THE VIEW METHODS — keys / values / items
# =============================================================
print("\n--- 5) VIEWS ---")
print("keys()        ->", person.keys())
print("values()      ->", person.values())
print("items()       ->", list(person.items())[:2], "...")
print("as lists      ->", list(person.keys()), "|", list(person.values())[:2])

# Views are LIVE windows — they update when the dict changes
ks = person.keys()
person["email"] = "a@b.com"
print("live view     ->", "email" in ks)               # True — no re-fetch needed
del person["email"]

# keys() behaves like a SET
other = {"name": 0, "salary": 0}
print("keys & keys   ->", person.keys() & other.keys())   # common keys
print("keys - keys   ->", person.keys() - other.keys())   # only in person


# -------------------------------------------------------------
# 6) LOOPING
# -------------------------------------------------------------
print("\n--- 6) LOOPING ---")
small = {"a": 1, "b": 2}
for k in small:                        # iterating a dict gives its KEYS
    print("  key         ->", k)
for v in small.values():
    print("  value       ->", v)
for k, v in small.items():             # the standard way
    print("  item        ->", k, "=", v)
for i, (k, v) in enumerate(small.items()):
    print("  enumerated  ->", i, k, v)

print("in checks KEYS->", "name" in person, "| 'Akshay' in person:", "Akshay" in person)
print("value check   ->", "Akshay" in person.values())


# -------------------------------------------------------------
# 7) MERGING
# -------------------------------------------------------------
print("\n--- 7) MERGING ---")
a, b = {"x": 1, "y": 2}, {"y": 99, "z": 3}
merged = {**a, **b}                    # right side WINS on conflicts
print("{**a, **b}    ->", merged)
copy_a = a.copy()
copy_a.update(b)
print("update()      ->", copy_a)
if sys.version_info >= (3, 9):
    print("a | b (3.9+)  ->", a | b)
else:
    print("a | b         -> needs 3.9+ | 3.8 way: {**a, **b} =", {**a, **b})
print("originals safe->", a, b)


# -------------------------------------------------------------
# 8) COPYING — shallow vs deep
# -------------------------------------------------------------
print("\n--- 8) COPY ---")
orig = {"n": 1, "inner": [1, 2]}
alias = orig                           # same object
shallow = orig.copy()                  # or dict(orig)
alias["n"] = 99
print("alias effect  ->", orig)                    # orig changed too
shallow["inner"].append(3)
print("shallow trap  ->", orig["inner"])           # inner list is SHARED
from copy import deepcopy
deep = deepcopy(orig)
deep["inner"].append(777)
print("deepcopy safe ->", orig["inner"], "vs", deep["inner"])


# -------------------------------------------------------------
# 9) COMPREHENSIONS
# -------------------------------------------------------------
print("\n--- 9) COMPREHENSION ---")
print("squares       ->", {x: x * x for x in range(5)})
print("from two lists->", {k: v for k, v in zip("abc", [1, 2, 3])})
print("with filter   ->", {k: v for k, v in {"a": 1, "b": 5}.items() if v > 2})
print("invert        ->", {v: k for k, v in {"a": 1, "b": 2}.items()})
print("transform val ->", {k: v * 10 for k, v in {"a": 1, "b": 2}.items()})
print("upper keys    ->", {k.upper(): v for k, v in {"a": 1}.items()})


# -------------------------------------------------------------
# 10) SORTING A DICT
# -------------------------------------------------------------
print("\n--- 10) SORTING ---")
scores = {"riya": 82, "amit": 91, "zoya": 45, "kiran": 77}
print("by key        ->", dict(sorted(scores.items())))
print("by value      ->", dict(sorted(scores.items(), key=lambda kv: kv[1])))
print("by value desc ->", dict(sorted(scores.items(), key=lambda kv: -kv[1])))
print("top scorer    ->", max(scores, key=scores.get))
print("lowest        ->", min(scores, key=scores.get))
print("top 2         ->", sorted(scores, key=scores.get, reverse=True)[:2])
print("sum / avg     ->", sum(scores.values()), round(sum(scores.values()) / len(scores), 1))


# -------------------------------------------------------------
# 11) NESTED DICTS
# -------------------------------------------------------------
print("\n--- 11) NESTED ---")
db = {
    "u1": {"name": "Amit", "tags": ["admin"]},
    "u2": {"name": "Riya", "tags": ["dev", "lead"]},
}
print("read deep     ->", db["u2"]["tags"][1])
print("safe deep     ->", db.get("u9", {}).get("name", "unknown"))
for uid, info in db.items():
    print("  %s -> %-5s tags=%s" % (uid, info["name"], info["tags"]))
print("all names     ->", [u["name"] for u in db.values()])
print("filter        ->", {k: v for k, v in db.items() if "dev" in v["tags"]})


# -------------------------------------------------------------
# 12) COUNTING PATTERNS
# -------------------------------------------------------------
print("\n--- 12) COUNTING ---")
text = "the cat the dog the bird"
manual = {}
for word in text.split():
    manual[word] = manual.get(word, 0) + 1             # classic get() pattern
print("manual count  ->", manual)

auto = defaultdict(int)                                # never raises KeyError
for word in text.split():
    auto[word] += 1
print("defaultdict   ->", dict(auto))

print("Counter       ->", dict(Counter(text.split())))
print("most_common(2)->", Counter(text.split()).most_common(2))

groups = defaultdict(list)                             # grouping pattern
for word in text.split():
    groups[len(word)].append(word)
print("group by len  ->", dict(groups))


# -------------------------------------------------------------
# 13) DICT AS A SWITCH / DISPATCH TABLE
# -------------------------------------------------------------
print("\n--- 13) DISPATCH ---")
ops = {
    "add": lambda p, q: p + q,
    "sub": lambda p, q: p - q,
    "mul": lambda p, q: p * q,
}
print("ops['mul']    ->", ops["mul"](3, 4))
print("safe dispatch ->", ops.get("div", lambda *_: "unsupported")(3, 4))
print("beats a long if/elif chain and is O(1)")


# -------------------------------------------------------------
# 14) GOTCHAS
# -------------------------------------------------------------
print("\n--- 14) GOTCHAS ---")
print("1 vs True key ->", {1: "one", True: "bool", 1.0: "float"})   # all ONE key
print("insertion ord ->", list({"z": 1, "a": 2, "m": 3}))           # z a m — 3.7+
print("mutating loop -> iterate over list(d) if you delete keys")
dd = {"a": 1, "b": 2, "c": 3}
for k in list(dd):                       # a COPY of the keys
    if dd[k] > 1:
        del dd[k]
print("safe delete   ->", dd)


# -------------------------------------------------------------
# 15) CHEAT SHEET
# -------------------------------------------------------------
#   d[k]            strict read (KeyError)  |  d.get(k, default)   safe read
#   d[k] = v        add / overwrite         |  d.setdefault(k, v)  read-or-insert
#   d.update(other) merge in place          |  {**a, **b}          merge to new
#   d.pop(k)        remove + return value   |  d.popitem()         remove last pair
#   del d[k]        remove                  |  d.clear()           empty it
#   d.keys/values/items()  live views       |  d.copy()            shallow copy
#   dict.fromkeys(keys, val)  bulk build    |  Counter/defaultdict  counting
print("\n--- 15) FINAL ---")
print("person        ->", person)
print("methods       ->", [m for m in dir(dict) if not m.startswith("_")])
