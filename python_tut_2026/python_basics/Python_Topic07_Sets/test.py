# =============================================================
# PYTHON SETS — every method, operator and pattern
# =============================================================
# Sets are UNORDERED, UNIQUE and MUTABLE.
# No indexing, no slicing, no duplicates.
# Items must be HASHABLE (immutable): int, str, tuple — NOT list/dict/set.
# Superpower: O(1) membership tests + real math set operations.
# =============================================================

A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7}
print("A / B         ->", A, B)
print("type / len    ->", type(A), len(A))


# -------------------------------------------------------------
# 1) CREATING SETS
# -------------------------------------------------------------
print("\n--- 1) CREATING ---")
print("literal       ->", {1, 2, 3})
print("dupes dropped ->", {1, 1, 2, 2, 3})         # {1, 2, 3}
print("set('hello')  ->", set("hello"))            # unique letters
print("set([1,1,2])  ->", set([1, 1, 2]))
print("set(range(4)) ->", set(range(4)))
print("comprehension ->", {x * x for x in range(5)})
print("mixed types   ->", {1, "two", 3.0, True, (4, 5)})

# THE #1 TRAP: {} is an EMPTY DICT, not an empty set
print("type({})      ->", type({}))                # <class 'dict'>
print("type(set())   ->", type(set()))             # <class 'set'>
print("empty set     ->", set())                   # prints as set()

# Items must be hashable
try:
    {[1, 2]}
except TypeError as e:
    print("list inside   -> TypeError:", e)
print("tuple inside  ->", {(1, 2)})                # fine — tuples are hashable

# Sneaky: True == 1 and 1.0 == 1, so they collapse into ONE item
print("{1, True, 1.0}->", {1, True, 1.0})          # {1} — first one inserted wins


# -------------------------------------------------------------
# 2) NO ORDER, NO INDEX
# -------------------------------------------------------------
print("\n--- 2) UNORDERED ---")
try:
    A[0]
except TypeError as e:
    print("A[0]          -> TypeError:", e)
print("order varies  ->", {"banana", "apple", "cherry"})   # NOT insertion order
print("sort it       ->", sorted(A))               # -> a LIST, ordered
print("== ignores order ->", {1, 2, 3} == {3, 2, 1})       # True


# =============================================================
# 3) ADDING ITEMS
# =============================================================
print("\n--- 3) ADD ---")
S = {1, 2}
S.add(3)
print("add(3)        ->", S)
S.add(3)
print("add dup       ->", S)                       # silently ignored, no error
S.update([4, 5])
print("update(list)  ->", S)                       # adds EACH item
S.update("ab")
print("update('ab')  ->", S)                       # a string is iterable -> chars!
S.update([9], {10}, (11,))
print("update(many)  ->", S)                       # takes multiple iterables


# =============================================================
# 4) REMOVING ITEMS
# =============================================================
print("\n--- 4) REMOVE ---")
S = {1, 2, 3, 4, 5}
S.remove(1)
print("remove(1)     ->", S)
try:
    S.remove(99)
except KeyError as e:
    print("remove missing-> KeyError:", e)         # remove() is STRICT

S.discard(2)
print("discard(2)    ->", S)
S.discard(99)
print("discard miss  ->", S)                       # discard() is SAFE — no error

popped = S.pop()
print("pop()         ->", popped, "| left:", S)    # removes an ARBITRARY item
S.clear()
print("clear()       ->", S)                       # set()


# =============================================================
# 5) SET MATH — the reason sets exist
# =============================================================
print("\n--- 5) SET MATH ---")
print("A =", A, " B =", B)
print("union        | ->", A | B, "|", A.union(B))               # everything
print("intersection & ->", A & B, "|", A.intersection(B))        # in BOTH
print("difference   - ->", A - B, "|", A.difference(B))          # in A only
print("difference B-A ->", B - A)                                # NOT symmetric!
print("symmetric   ^ ->", A ^ B, "|", A.symmetric_difference(B))  # in one, not both

# Method form accepts ANY iterable; the operator form needs real sets
print("union w/ list ->", A.union([8, 9]))
try:
    A | [8, 9]
except TypeError as e:
    print("A | list      -> TypeError:", e)

# Multiple arguments at once
print("3-way union   ->", A.union(B, {100}))
print("3-way inter   ->", {1, 2, 3}.intersection({2, 3, 4}, {3, 2}))


# =============================================================
# 6) IN-PLACE SET MATH  (the *_update family)
# =============================================================
print("\n--- 6) IN-PLACE MATH ---")
U = {1, 2, 3}
U.update({3, 4})                     # same as  U |= {3, 4}
print("update        ->", U)
U = {1, 2, 3}
U.intersection_update({2, 3, 9})     # same as  U &= {...}
print("intersection_ ->", U)
U = {1, 2, 3}
U.difference_update({1})             # same as  U -= {...}
print("difference_   ->", U)
U = {1, 2, 3}
U.symmetric_difference_update({3, 4})  # same as  U ^= {...}
print("symmetric_    ->", U)

V = {1, 2}
V |= {3}
V &= {1, 3}
print("operator form ->", V)


# =============================================================
# 7) COMPARING SETS
# =============================================================
print("\n--- 7) COMPARISONS ---")
small, big = {1, 2}, {1, 2, 3}
print("issubset   <= ->", small.issubset(big), "|", small <= big)
print("issuperset >= ->", big.issuperset(small), "|", big >= small)
print("proper subset <->", small < big)            # subset AND not equal
print("equal is subset->", big <= big, "| proper:", big < big)   # True False
print("isdisjoint    ->", {1, 2}.isdisjoint({3, 4}))   # True — nothing in common
print("isdisjoint(A,B)->", A.isdisjoint(B))            # False — they share 4, 5


# =============================================================
# 8) COPYING
# =============================================================
print("\n--- 8) COPY ---")
orig = {1, 2, 3}
alias = orig                # same object
copy1 = orig.copy()         # new set
copy2 = set(orig)           # new set too
alias.add(99)
copy1.add(777)
print("orig          ->", sorted(orig))            # 99 leaked in via the alias
print("copy1         ->", sorted(copy1))           # independent
print("same object?  ->", orig is alias, orig is copy1)


# =============================================================
# 9) frozenset — the IMMUTABLE set
# =============================================================
print("\n--- 9) frozenset ---")
fs = frozenset([1, 2, 3])
print("frozenset     ->", fs)
print("all math works->", fs | {4}, fs & {1, 9})
try:
    fs.add(4)
except AttributeError as e:
    print("fs.add(4)     -> AttributeError:", e)
# Because it's immutable, it IS hashable -> can live inside a set / be a dict key
print("set of sets   ->", {frozenset([1, 2]), frozenset([3])})
print("as dict key   ->", {frozenset(["a", "b"]): "pair"})


# =============================================================
# 10) REAL-WORLD PATTERNS
# =============================================================
print("\n--- 10) PATTERNS ---")
dupes = [3, 1, 3, 2, 1, 5]
print("dedupe        ->", list(set(dupes)))                  # order LOST
print("dedupe ordered->", list(dict.fromkeys(dupes)))        # order KEPT
print("has dupes?    ->", len(dupes) != len(set(dupes)))

old_users = {"amit", "riya", "kiran"}
new_users = {"riya", "kiran", "zoya"}
print("joined        ->", new_users - old_users)             # {'zoya'}
print("left          ->", old_users - new_users)             # {'amit'}
print("stayed        ->", old_users & new_users)
print("all ever      ->", old_users | new_users)
print("changed either->", old_users ^ new_users)

print("common chars  ->", set("python") & set("typhoon"))
print("unique words  ->", len(set("the cat the dog the bird".split())))

# Membership speed: set is O(1), list is O(n)
big_set = set(range(100000))
big_list = list(range(100000))
print("99999 in set  ->", 99999 in big_set, "(hash lookup, instant)")
print("99999 in list ->", 99999 in big_list, "(scans 100k items)")


# =============================================================
# 11) COMPREHENSIONS
# =============================================================
print("\n--- 11) COMPREHENSION ---")
print("basic         ->", {x * 2 for x in range(5)})
print("with filter   ->", {x for x in range(10) if x % 3 == 0})
print("from string   ->", {c for c in "hello world" if c.isalpha()})
print("auto-dedupes  ->", {len(w) for w in ["a", "bb", "cc", "d"]})   # {1, 2}


# =============================================================
# 12) LOOPING & CONVERSION
# =============================================================
print("\n--- 12) LOOP & CONVERT ---")
for item in sorted(A):                 # sort it for predictable output
    print("  item ->", item, end="")
print()
print("set -> list   ->", list(A))
print("set -> tuple  ->", tuple(A))
print("set -> sorted ->", sorted(A, reverse=True))
print("len / min / max->", len(A), min(A), max(A))
print("sum / any / all->", sum(A), any(A), all(A))
print("enumerate     ->", list(enumerate(sorted(A)))[:2])


# =============================================================
# 13) CHEAT SHEET
# =============================================================
#   add(x)          add one           |  remove(x)   strict delete (KeyError)
#   update(it,...)  add many          |  discard(x)  safe delete (no error)
#   |  union        &  intersection   |  pop()       remove random item
#   -  difference   ^  symmetric diff |  clear()     empty it
#   <= issubset     >= issuperset     |  isdisjoint  nothing in common
#   *_update()      = do it in place  |  frozenset   immutable + hashable
print("\n--- 13) FINAL ---")
print("A unchanged   ->", sorted(A))
print("B unchanged   ->", sorted(B))
