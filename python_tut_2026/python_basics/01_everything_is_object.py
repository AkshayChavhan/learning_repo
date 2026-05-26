"""
Sub-topic 1 — What 'object' means in Python.

Run from the repo root:
    python "Python Tut 2026/python_basics/01_everything_is_object.py"

Each block below is small. Before you run the file, try to predict
what each `print` will output. Then run it and check.
"""

# ─────────────────────────────────────────────────────────────
# 1. Every value has a type. Even numbers, strings, functions.
# ─────────────────────────────────────────────────────────────
print("─── 1. type() works on everything ───")
print(type(5))             # <class 'int'>
print(type(3.14))          # <class 'float'>
print(type("hello"))       # <class 'str'>
print(type([1, 2, 3]))     # <class 'list'>
print(type(print))         # <class 'builtin_function_or_method'>
print(type(type))          # <class 'type'>  ← even `type` is a type


# ─────────────────────────────────────────────────────────────
# 2. Numbers are objects — they have methods you can call.
#    (Unlike Java primitives.)
# ─────────────────────────────────────────────────────────────
print("\n─── 2. Numbers have methods ───")
print((255).bit_length())  # 8  — needs 8 bits to represent 255
print((-3).__abs__())      # 3  — dunder method behind abs()
print((1.5).is_integer())  # False


# ─────────────────────────────────────────────────────────────
# 3. id() and `is` — identity, not equality.
# ─────────────────────────────────────────────────────────────
print("\n─── 3. id() and `is` ───")
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(a == b)   # True  — same contents
print(a is b)   # False — different objects in memory
print(a is c)   # True  — c is just another name for the same list
print(id(a), id(b), id(c))


# ─────────────────────────────────────────────────────────────
# 4. Mutable vs immutable — what "changing" really means.
# ─────────────────────────────────────────────────────────────
print("\n─── 4. Mutable vs immutable ───")

# Immutable: int. You can't change 5 into 6. You rebind the name.
x = 5
old_id = id(x)
x = x + 1
print(x, "id changed?", id(x) != old_id)   # 6 True

# Mutable: list. You can change the SAME object in place.
nums = [1, 2, 3]
old_id = id(nums)
nums.append(4)
print(nums, "same object?", id(nums) == old_id)  # [1,2,3,4] True


# ─────────────────────────────────────────────────────────────
# 5. Aliasing — two names, one object. Bites you with mutables.
# ─────────────────────────────────────────────────────────────
print("\n─── 5. Aliasing ───")
original = [1, 2, 3]
alias = original           # NOT a copy — same list object
alias.append(999)
print("original:", original)   # [1, 2, 3, 999]  ← surprised?
print("alias:   ", alias)      # [1, 2, 3, 999]

# To actually copy, use list(original) or original.copy() or original[:]
real_copy = original.copy()
real_copy.append("only-in-copy")
print("after copy modification, original:", original)


# ─────────────────────────────────────────────────────────────
# 6. The small-int / interned-string trap.
#    CPython caches small ints (-5..256) and some short strings.
#    `is` may return True or False depending on the value — DO NOT rely on it.
# ─────────────────────────────────────────────────────────────
print("\n─── 6. The `is` trap ───")
a, b = 5, 5
print("small int:", a is b)        # True   (cached)

a, b = 1000, 1000
print("big int:  ", a is b)        # False  (not cached) — usually

# Lesson: use == for equality, use `is` only for `is None`, `is True`, `is False`.


# ─────────────────────────────────────────────────────────────
# 7. Functions and classes are objects too.
#    You can assign them to variables, pass them around, store in lists.
# ─────────────────────────────────────────────────────────────
print("\n─── 7. Functions/classes are objects ───")

def greet(name):
    return f"Hello, {name}!"

f = greet                  # bind another name to the same function object
print(f("Akshay"))         # Hello, Akshay!
print(type(f))             # <class 'function'>

# Stash functions in a list and call them
operations = [str.upper, str.lower, str.title]
for op in operations:
    print(op("hello WORLD"))
