# =============================================================
# PYTHON TUPLES — every method, operator and pattern
# =============================================================
# Tuples are ORDERED, allow DUPLICATES, and are IMMUTABLE (frozen).
# Because they can't change, they are HASHABLE -> usable as dict keys
# and set members. Only 2 methods exist: count() and index().
# =============================================================

from collections import namedtuple

point = (10, 20, 30, 20)
print("point         ->", point)
print("type / len    ->", type(point), len(point))


# -------------------------------------------------------------
# 1) CREATING TUPLES
# -------------------------------------------------------------
print("\n--- 1) CREATING ---")
print("literal       ->", (1, 2, 3))
print("no parens     ->", 1, 2, 3)                 # tuple packing still works
packed = 1, 2, 3
print("packed        ->", packed, type(packed))
print("empty         ->", (), tuple())
print("tuple('abc')  ->", tuple("abc"))            # ('a', 'b', 'c')
print("tuple([1,2])  ->", tuple([1, 2]))
print("tuple(range(4))->", tuple(range(4)))
print("nested        ->", ((1, 2), (3, 4)))
print("mixed types   ->", (1, "two", 3.0, True, None, [9]))

# THE #1 TRAP: a single-item tuple NEEDS a trailing comma
print("(5)  is       ->", type((5)))               # <class 'int'>   -> just parens!
print("(5,) is       ->", type((5,)))              # <class 'tuple'> -> comma makes it
print("len((5,))     ->", len((5,)))               # 1


# -------------------------------------------------------------
# 2) INDEXING & SLICING  (identical to lists)
# -------------------------------------------------------------
print("\n--- 2) INDEX & SLICE ---")
print("point[0]      ->", point[0])                # 10
print("point[-1]     ->", point[-1])               # 20
print("point[1:3]    ->", point[1:3])              # (20, 30)
print("point[::-1]   ->", point[::-1])             # reversed COPY
print("point[::2]    ->", point[::2])              # every 2nd
print("nested index  ->", ((1, 2), (3, 4))[1][0])  # 3
# point[99] -> IndexError, but a slice out of range is safe:
print("point[10:20]  ->", point[10:20])            # ()


# -------------------------------------------------------------
# 3) IMMUTABILITY — what you CANNOT do
# -------------------------------------------------------------
print("\n--- 3) IMMUTABLE ---")
try:
    point[0] = 99
except TypeError as e:
    print("assign        -> TypeError:", e)

for op, fn in [("append", "append"), ("remove", "remove"), ("sort", "sort")]:
    print("has .%-7s ->" % op, hasattr(point, fn))   # all False

# Workaround: convert -> change -> convert back (this builds a NEW tuple)
tmp = list(point)
tmp[0] = 99
print("via list      ->", tuple(tmp))

# Or rebuild with slicing / concatenation
print("rebuild slice ->", (99,) + point[1:])

# BUT: immutable means the tuple's SLOTS are frozen, not the objects inside
mixed = (1, [2, 3])
mixed[1].append(4)
print("inner list    ->", mixed)         # (1, [2, 3, 4]) — inner list IS mutable
print("=> a tuple with a list inside is NOT hashable:")
try:
    hash(mixed)
except TypeError as e:
    print("   hash()     -> TypeError:", e)


# =============================================================
# 4) THE ONLY 2 TUPLE METHODS
# =============================================================
print("\n--- 4) THE 2 METHODS ---")
print("count(20)     ->", point.count(20))         # 2
print("count(99)     ->", point.count(99))         # 0 — safe, never errors
print("index(20)     ->", point.index(20))         # 1 — FIRST match
print("index(20, 2)  ->", point.index(20, 2))      # 3 — start searching at 2
# point.index(99) -> ValueError. Guard it:
print("guard         ->", point.index(30) if 30 in point else -1)


# -------------------------------------------------------------
# 5) OPERATORS
# -------------------------------------------------------------
print("\n--- 5) OPERATORS ---")
print("concat  +     ->", (1, 2) + (3, 4))         # NEW tuple
print("repeat  *     ->", (1, 2) * 3)
print("in            ->", 30 in point, 99 in point)
print("not in        ->", 99 not in point)
print("==            ->", (1, 2) == (1, 2))        # True — compares values
t1, t2 = tuple([1, 2]), tuple([1, 2])
print("is            ->", t1 is t2)                # False — two separate objects
print("< compares    ->", (1, 2, 9) < (1, 3))      # True — element by element
print("sort tuples   ->", sorted([(2, "b"), (1, "c"), (1, "a")]))

acc = (1, 2)
before = id(acc)
acc += (3,)                    # NOT in-place — builds a brand new tuple
print("+= rebinds    ->", acc, "| same object:", id(acc) == before)


# -------------------------------------------------------------
# 6) UNPACKING — the real superpower of tuples
# -------------------------------------------------------------
print("\n--- 6) UNPACKING ---")
x, y, z, w = point
print("basic unpack  ->", x, y, z, w)

first, *rest = point
print("first, *rest  ->", first, rest)             # 10 [20, 30, 20]  <- rest is a LIST
head, *mid, tail = point
print("head,*mid,tail->", head, mid, tail)

a, b = 1, 2
a, b = b, a
print("swap          ->", a, b)                    # 2 1 — a tuple under the hood

print("ignore with _ ->", [v for v in (1, 2, 3)])
_, keep, *_rest = (1, 2, 3, 4)
print("_ convention  ->", keep)                    # 2

# Nested unpacking
(p1, p2), (p3, p4) = ((1, 2), (3, 4))
print("nested unpack ->", p1, p2, p3, p4)

# Unpacking in a loop
for idx, letter in [(0, "a"), (1, "b")]:
    print("  loop unpack ->", idx, letter)

# Wrong count -> ValueError
try:
    q, r = (1, 2, 3)
except ValueError as e:
    print("bad unpack    -> ValueError:", e)


# -------------------------------------------------------------
# 7) TUPLES AND FUNCTIONS
# -------------------------------------------------------------
print("\n--- 7) FUNCTIONS ---")


def min_max(values):
    """Returning multiple values IS returning a tuple."""
    return min(values), max(values)


lo, hi = min_max([4, 9, 1])
print("multi return  ->", lo, hi, "| raw:", min_max([4, 9, 1]))


def show(*args, **kwargs):
    """*args collects extra positionals into a TUPLE."""
    return type(args).__name__, args, type(kwargs).__name__


print("*args is tuple->", show(1, 2, 3))

# * unpacks a tuple INTO arguments
def add(p, q, r):
    return p + q + r


nums3 = (1, 2, 3)
print("call with *   ->", add(*nums3))             # 6
print("merge with *  ->", (*nums3, *(4, 5)))       # (1, 2, 3, 4, 5)


# -------------------------------------------------------------
# 8) TUPLE AS DICT KEY / SET MEMBER  (hashability)
# -------------------------------------------------------------
print("\n--- 8) HASHABLE ---")
print("hash((1,2))   ->", hash((1, 2)) == hash((1, 2)))   # stable
grid = {(0, 0): "origin", (1, 2): "target"}
print("dict key      ->", grid[(1, 2)])
print("set of tuples ->", {(1, 2), (1, 2), (3, 4)})       # dedupes
# {[1, 2]: "x"}  ->  TypeError: unhashable type: 'list'
print("list as key   -> TypeError (lists are unhashable)")


# -------------------------------------------------------------
# 9) namedtuple — tuples with named fields
# -------------------------------------------------------------
print("\n--- 9) namedtuple ---")
Person = namedtuple("Person", ["name", "age", "city"])
akshay = Person("Akshay", 29, "Pune")
print("namedtuple    ->", akshay)
print("by name       ->", akshay.name, akshay.age)
print("by index      ->", akshay[0])               # still a real tuple
print("unpack        ->", [v for v in akshay])
print("_asdict()     ->", dict(akshay._asdict()))
print("_replace()    ->", akshay._replace(age=30))  # returns a NEW one
print("_fields       ->", akshay._fields)
print("is a tuple?   ->", isinstance(akshay, tuple))


# -------------------------------------------------------------
# 10) COMPREHENSIONS & CONVERSION
# -------------------------------------------------------------
print("\n--- 10) COMPREHENSION ---")
print("no tuple comp ->", type(x * 2 for x in range(3)))   # generator, NOT a tuple
print("wrap in tuple ->", tuple(x * 2 for x in range(3)))  # (0, 2, 4)
print("list -> tuple ->", tuple([1, 2, 3]))
print("tuple -> list ->", list((1, 2, 3)))
print("zip gives tuples ->", list(zip([1, 2], "ab")))
print("enumerate too ->", list(enumerate("ab")))
print("sorted(t)     ->", sorted(point))           # returns a LIST


# -------------------------------------------------------------
# 11) TUPLE vs LIST — when to use which
# -------------------------------------------------------------
#   tuple  -> fixed record, heterogeneous data, dict key, safe constant,
#             function returns, unpacking. Smaller & slightly faster.
#   list   -> collection that grows/shrinks, homogeneous items, needs sorting.
print("\n--- 11) TUPLE vs LIST ---")
import sys as _sys
print("memory tuple  ->", _sys.getsizeof((1, 2, 3, 4, 5)), "bytes")
print("memory list   ->", _sys.getsizeof([1, 2, 3, 4, 5]), "bytes")
print("tuple methods ->", len([m for m in dir(tuple) if not m.startswith("_")]))
print("list methods  ->", len([m for m in dir(list) if not m.startswith("_")]))


# -------------------------------------------------------------
# 12) IMMUTABILITY PROOF
# -------------------------------------------------------------
print("\n--- 12) PROOF ---")
orig = (1, 2, 3)
same = orig                      # both names point to the SAME frozen object
new = orig + (4,)                # a NEW object
print("orig / same   ->", orig, same, "| same obj:", orig is same)
print("after +       ->", "orig:", orig, "new:", new)   # orig can never change
print("point final   ->", point)
