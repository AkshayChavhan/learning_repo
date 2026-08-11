"""
tut00.2 — Variables, names, and assignment.

Run from the repo root:
    python3 "Python Tut 2026/python_basics/00b_variables.py"

Core idea: a variable is a NAME BOUND TO AN OBJECT.
Not a box that holds a value — a label pointing at a value.
"""

# ─────────────────────────────────────────────────────────────
# 1. First assignment creates a name. No declaration needed.
# ─────────────────────────────────────────────────────────────
print("─── 1. No declarations ───")
x = 5
print("x =", x, "type:", type(x).__name__)

x = "now a string"   # same name, totally different object
print("x =", x, "type:", type(x).__name__)

# The "type" lives on the OBJECT, not on the name.


# ─────────────────────────────────────────────────────────────
# 2. Names point to objects. id() shows the identity.
# ─────────────────────────────────────────────────────────────
print("\n─── 2. Names → objects ───")
a = [10, 20, 30]
b = a                # NOT a copy — same object, two names
print("a is b?", a is b)     # True
print("id(a):", id(a), " id(b):", id(b))

b.append(40)         # mutate through b…
print("a after b.append:", a)   # …a sees the change too


# ─────────────────────────────────────────────────────────────
# 3. Rebinding doesn't affect other names pointing to the old object.
# ─────────────────────────────────────────────────────────────
print("\n─── 3. Rebinding ≠ mutating ───")
a = [1, 2, 3]
b = a
print("before: a =", a, " b =", b)

a = [99, 99]        # a now points at a NEW list
print("after:  a =", a, " b =", b)   # b still points to [1,2,3]


# ─────────────────────────────────────────────────────────────
# 4. Tuple unpacking — multiple assignment in one shot.
# ─────────────────────────────────────────────────────────────
print("\n─── 4. Unpacking ───")
x, y = 1, 2
print("x, y =", x, y)

x, y = y, x          # swap, no temp variable
print("after swap: x, y =", x, y)

first, *rest = [10, 20, 30, 40]
print("first =", first, " rest =", rest)

*head, last = [10, 20, 30, 40]
print("head =", head, " last =", last)


# ─────────────────────────────────────────────────────────────
# 5. Chained assignment — all names point to the SAME object.
# ─────────────────────────────────────────────────────────────
print("\n─── 5. Chained assignment ───")
p = q = r = []
print("p is q is r?", p is q is r)   # True
p.append("oops")
print("q now:", q)   # ['oops'] — surprise if you wanted three separate lists


# ─────────────────────────────────────────────────────────────
# 6. Augmented assignment: += on mutable vs immutable.
# ─────────────────────────────────────────────────────────────
print("\n─── 6. += has two flavors ───")

# Immutable: int. += creates a NEW int and rebinds.
n = 5
old_id = id(n)
n += 1
print("int:  same object?", id(n) == old_id)   # False — rebound

# Mutable: list. += mutates in place (calls __iadd__).
lst = [1, 2]
old_id = id(lst)
lst += [3]
print("list: same object?", id(lst) == old_id) # True — mutated


# ─────────────────────────────────────────────────────────────
# 7. Type hints are documentation, not enforcement.
# ─────────────────────────────────────────────────────────────
print("\n─── 7. Type hints ───")
age: int = 30
print("age =", age, "type:", type(age).__name__)

age = "thirty"       # legal! Python does NOT enforce hints at runtime.
print("age =", age, "type:", type(age).__name__)
# Tools like mypy/pyright would flag this. Python itself shrugs.


# ─────────────────────────────────────────────────────────────
# 8. Shadowing a built-in — common mistake.
# ─────────────────────────────────────────────────────────────
print("\n─── 8. Don't shadow built-ins ───")
list = [1, 2, 3]     # we just lost access to the `list` type in this scope
print("our 'list':", list)

# This would now fail because `list` no longer refers to the type:
# new_list = list("abc")    # TypeError: 'list' object is not callable

del list             # restore access by deleting our binding
print("after `del list`, list('abc') =", list("abc"))


# ─────────────────────────────────────────────────────────────
# 9. Peek at the namespace — what names exist?
# ─────────────────────────────────────────────────────────────
print("\n─── 9. dir() shows current names ───")
some_local_names = [n for n in dir() if not n.startswith("_")]
print("non-dunder names in this script:", some_local_names[:10], "...")


# ─────────────────────────────────────────────────────────────
# 10. The walrus operator := (Python 3.8+) — assign inside an expression.
# ─────────────────────────────────────────────────────────────
print("\n─── 10. Walrus operator ───")
data = "hello world"
if (n := len(data)) > 5:
    # `n` is assigned AND used in the condition
    print(f"'{data}' has {n} chars — longer than 5")
