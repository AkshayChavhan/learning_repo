# =============================================================
# PYTHON LISTS — every method, operator and pattern
# =============================================================
# Lists are MUTABLE, ORDERED, allow DUPLICATES, hold ANY type.
# Mutating methods (append/sort/reverse...) change the list IN PLACE
# and return None — they do NOT give you a new list.
# =============================================================

from copy import deepcopy

nums = [40, 10, 30, 20, 10]
print("nums          ->", nums)
print("type / len    ->", type(nums), len(nums))


# -------------------------------------------------------------
# 1) CREATING LISTS
# -------------------------------------------------------------
print("\n--- 1) CREATING ---")
print("literal       ->", [1, 2, 3])
print("empty         ->", [], list())
print("list('abc')   ->", list("abc"))            # ['a', 'b', 'c']
print("list(range(5))->", list(range(5)))         # [0, 1, 2, 3, 4]
print("mixed types   ->", [1, "two", 3.0, True, None, [9]])
print("repeat *      ->", [0] * 5)                # [0, 0, 0, 0, 0]
print("comprehension ->", [x * x for x in range(5)])
print("nested (2D)   ->", [[1, 2], [3, 4]])


# -------------------------------------------------------------
# 2) INDEXING & SLICING   list[start : stop : step]
# -------------------------------------------------------------
print("\n--- 2) INDEX & SLICE ---")
print("nums[0]       ->", nums[0])                # 40  first
print("nums[-1]      ->", nums[-1])               # 10  last
print("nums[1:4]     ->", nums[1:4])              # [10, 30, 20]  stop EXCLUDED
print("nums[:3]      ->", nums[:3])               # from start
print("nums[2:]      ->", nums[2:])               # to end
print("nums[::2]     ->", nums[::2])              # every 2nd
print("nums[::-1]    ->", nums[::-1])             # reversed COPY
print("slice is copy ->", nums[:] is nums)        # False — new list object
# nums[99]  -> IndexError, but a SLICE out of range is safe:
print("nums[10:20]   ->", nums[10:20])            # [] — no error


# -------------------------------------------------------------
# 3) MODIFYING — index, slice & del
# -------------------------------------------------------------
print("\n--- 3) MODIFYING ---")
mod = [1, 2, 3, 4, 5]
mod[0] = 99
print("mod[0] = 99   ->", mod)                    # [99, 2, 3, 4, 5]
mod[1:3] = ["a", "b", "c"]                        # slice assign can CHANGE length
print("slice assign  ->", mod)                    # [99, 'a', 'b', 'c', 4, 5]
mod[0:2] = []                                     # deleting via slice
print("slice delete  ->", mod)                    # ['b', 'c', 4, 5]
del mod[0]
print("del mod[0]    ->", mod)                    # ['c', 4, 5]
del mod[0:2]
print("del slice     ->", mod)                    # [5]


# =============================================================
# 4) ALL 11 LIST METHODS
# =============================================================
print("\n--- 4) THE 11 METHODS ---")

# 4.1 append(x) — add ONE item at the end
L = [1, 2, 3]
L.append(4)
print("append(4)     ->", L)                      # [1, 2, 3, 4]
L.append([5, 6])
print("append(list)  ->", L)                      # [1,2,3,4,[5,6]] <- NESTED

# 4.2 extend(iterable) — add EACH item of an iterable
L = [1, 2, 3]
L.extend([4, 5])
print("extend([4,5]) ->", L)                      # [1, 2, 3, 4, 5]
L.extend("ab")
print("extend('ab')  ->", L)                      # [1,2,3,4,5,'a','b'] <- FLAT

# 4.3 insert(i, x) — insert BEFORE index i
L = [1, 2, 3]
L.insert(1, 99)
print("insert(1,99)  ->", L)                      # [1, 99, 2, 3]
L.insert(0, "start")
print("insert(0,..)  ->", L)                      # ['start', 1, 99, 2, 3]
L.insert(100, "end")
print("insert(big i) ->", L)                      # clamps to the end, no error

# 4.4 remove(x) — delete the FIRST match BY VALUE
L = [10, 20, 30, 20]
L.remove(20)
print("remove(20)    ->", L)                      # [10, 30, 20] — only first one
# L.remove(99)  ->  ValueError: list.remove(x): x not in list

# 4.5 pop(i) — remove & RETURN by index (default: last)
L = [1, 2, 3, 4]
print("pop()         ->", L.pop(), "| list:", L)  # 4  [1, 2, 3]
print("pop(0)        ->", L.pop(0), "| list:", L)  # 1  [2, 3]
# pop() is O(1) at the end, O(n) from the front

# 4.6 clear() — empty it in place
L = [1, 2, 3]
L.clear()
print("clear()       ->", L)                      # []

# 4.7 index(x) — first position of a value
L = [10, 20, 30, 20]
print("index(20)     ->", L.index(20))            # 1
print("index(20, 2)  ->", L.index(20, 2))         # 3 — start searching at 2
# L.index(99)  ->  ValueError. Guard with:  if 99 in L

# 4.8 count(x) — how many times a value appears
print("count(20)     ->", L.count(20))            # 2
print("count(99)     ->", L.count(99))            # 0 — safe, never errors

# 4.9 sort() — sorts IN PLACE, returns None
L = [40, 10, 30, 20]
L.sort()
print("sort()        ->", L)                      # [10, 20, 30, 40]
L.sort(reverse=True)
print("sort(reverse) ->", L)                      # [40, 30, 20, 10]
words = ["banana", "Fig", "apple", "cherry"]
words.sort(key=len)
print("sort(key=len) ->", words)                  # shortest first
words.sort(key=str.lower)
print("sort(key=lower)->", words)                 # case-insensitive A-Z
print("sort() returns->", [3, 1].sort())          # None <- classic bug source

# 4.10 reverse() — flips IN PLACE, returns None
L = [1, 2, 3]
L.reverse()
print("reverse()     ->", L)                      # [3, 2, 1]

# 4.11 copy() — SHALLOW copy (new list, same inner objects)
L = [1, 2, 3]
C = L.copy()
C.append(4)
print("copy()        ->", "orig:", L, "copy:", C)  # orig unchanged


# -------------------------------------------------------------
# 5) OPERATORS ON LISTS
# -------------------------------------------------------------
print("\n--- 5) OPERATORS ---")
print("concat  +     ->", [1, 2] + [3, 4])        # [1, 2, 3, 4] — NEW list
print("repeat  *     ->", [1, 2] * 3)             # [1, 2, 1, 2, 1, 2]
print("in            ->", 30 in nums, 99 in nums)  # True False
print("not in        ->", 99 not in nums)         # True
print("==            ->", [1, 2] == [1, 2])       # True — compares VALUES
print("is            ->", [1, 2] is [1, 2])       # False — different objects
print("< compares    ->", [1, 2, 9] < [1, 3])     # True — element by element

acc = [1, 2]
acc += [3]                 # in-place extend (mutates)
print("+= mutates    ->", acc)                    # [1, 2, 3]


# -------------------------------------------------------------
# 6) BUILT-IN FUNCTIONS THAT TAKE LISTS
# -------------------------------------------------------------
print("\n--- 6) BUILT-INS ---")
print("len / sum     ->", len(nums), sum(nums))
print("min / max     ->", min(nums), max(nums))
print("max(key=)     ->", max(words, key=len))        # longest word
print("sorted()      ->", sorted(nums), "| orig:", nums)   # NEW list, orig intact
print("sorted(rev)   ->", sorted(nums, reverse=True))
print("reversed()    ->", list(reversed(nums)))       # iterator -> list
print("any / all     ->", any([0, 0, 1]), all([1, 2, 0]))  # True False
print("enumerate     ->", list(enumerate(["a", "b"])))     # [(0,'a'), (1,'b')]
print("enumerate(1)  ->", list(enumerate(["a", "b"], 1)))  # start counting at 1
print("zip           ->", list(zip([1, 2, 3], "abc")))     # [(1,'a'), (2,'b'), (3,'c')]
print("map           ->", list(map(str.upper, ["a", "b"])))
print("filter        ->", list(filter(lambda n: n > 15, nums)))
print("list(set())   ->", list(set([1, 1, 2, 2, 3])))      # dedupe (order lost)


# -------------------------------------------------------------
# 7) LIST COMPREHENSIONS  (the pythonic loop)
# -------------------------------------------------------------
print("\n--- 7) COMPREHENSIONS ---")
print("basic         ->", [x * 2 for x in range(5)])
print("with filter   ->", [x for x in nums if x > 15])
print("with ternary  ->", ["even" if x % 2 == 0 else "odd" for x in range(4)])
print("over string   ->", [ch.upper() for ch in "abc"])
print("nested loops  ->", [(i, j) for i in [1, 2] for j in "ab"])
print("flatten 2D    ->", [x for row in [[1, 2], [3, 4]] for x in row])
print("nested comp   ->", [[r * c for c in range(1, 4)] for r in range(1, 3)])
print("with enumerate->", [f"{i}:{v}" for i, v in enumerate("abc")])


# -------------------------------------------------------------
# 8) UNPACKING
# -------------------------------------------------------------
print("\n--- 8) UNPACKING ---")
first, second, *rest = [1, 2, 3, 4, 5]
print("first/second/rest ->", first, second, rest)     # 1 2 [3, 4, 5]
head, *middle, tail = [1, 2, 3, 4, 5]
print("head/middle/tail  ->", head, middle, tail)      # 1 [2, 3, 4] 5
print("merge with *      ->", [*[1, 2], *[3, 4]])      # [1, 2, 3, 4]
p, q = [1, 2]
p, q = q, p
print("swap              ->", p, q)                    # 2 1


# -------------------------------------------------------------
# 9) COPYING — the aliasing trap
# -------------------------------------------------------------
print("\n--- 9) COPY vs ALIAS ---")
orig = [1, 2, 3]
alias = orig                 # NOT a copy — same object, two names
alias.append(4)
print("alias effect  ->", "orig:", orig, "| same obj:", orig is alias)

shallow = orig.copy()        # 3 equivalent ways: .copy() / orig[:] / list(orig)
shallow.append(99)
print("shallow copy  ->", "orig:", orig, "copy:", shallow)

# Shallow copy still SHARES the inner lists
nested = [[1, 2], [3, 4]]
sh = nested.copy()
sh[0].append(99)
print("shallow nested->", "orig:", nested)             # inner list CHANGED too!

deep = deepcopy(nested)
deep[0].append(777)
print("deepcopy      ->", "orig:", nested, "deep:", deep)   # orig safe


# -------------------------------------------------------------
# 10) 2D LISTS
# -------------------------------------------------------------
print("\n--- 10) 2D LISTS ---")
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("grid[1][2]    ->", grid[1][2])                  # 6  (row 1, col 2)
print("row / column  ->", grid[0], [row[1] for row in grid])
print("transpose     ->", [list(t) for t in zip(*grid)])
print("flatten       ->", [x for row in grid for x in row])

# THE TRAP: * copies the REFERENCE, not the row
bad = [[0] * 3] * 3
bad[0][0] = 99
print("bad  [[0]*3]*3->", bad)              # ALL rows changed!
good = [[0] * 3 for _ in range(3)]
good[0][0] = 99
print("good comprehen->", good)             # only row 0 changed


# -------------------------------------------------------------
# 11) LOOPING PATTERNS
# -------------------------------------------------------------
print("\n--- 11) LOOPING ---")
print("plain         ->", [v for v in ["a", "b"]])
for i, v in enumerate(["a", "b"]):
    print("  enumerate   ->", i, v)
for x, y in zip([1, 2], ["a", "b"]):
    print("  zip         ->", x, y)

# TRAP: never mutate a list while iterating over it
data = [1, 2, 3, 4, 5, 6]
for v in data[:]:            # iterate over a COPY
    if v % 2 == 0:
        data.remove(v)
print("safe removal  ->", data)                        # [1, 3, 5]
print("better way    ->", [v for v in [1, 2, 3, 4, 5, 6] if v % 2])


# -------------------------------------------------------------
# 12) LIST AS STACK & QUEUE
# -------------------------------------------------------------
print("\n--- 12) STACK & QUEUE ---")
stack = [1, 2, 3]
stack.append(4)                       # push  — O(1)
print("stack pop     ->", stack.pop(), "| left:", stack)   # LIFO

queue = [1, 2, 3]
print("queue pop(0)  ->", queue.pop(0), "| left:", queue)  # FIFO but O(n)
# For real queues use:  from collections import deque -> popleft() is O(1)


# -------------------------------------------------------------
# 13) PERFORMANCE CHEAT SHEET
# -------------------------------------------------------------
#   append / pop()        O(1)     fast — end of list
#   insert(0,x) / pop(0)  O(n)     slow — shifts everything
#   x in list             O(n)     use a set for fast lookups
#   sort()                O(n log n)  Timsort, STABLE
#   len()                 O(1)
print("\n--- 13) PERF ---")
print("stable sort   ->", sorted([("b", 2), ("a", 2), ("c", 1)], key=lambda t: t[1]))
print("set lookup    ->", 30 in set(nums))     # O(1) vs O(n) for big data


# -------------------------------------------------------------
# 14) MUTABLE DEFAULT ARGUMENT — famous interview trap
# -------------------------------------------------------------
print("\n--- 14) MUTABLE DEFAULT ---")


def bad_add(item, store=[]):          # default list is created ONCE, reused!
    store.append(item)
    return store


def good_add(item, store=None):       # correct pattern
    if store is None:
        store = []
    store.append(item)
    return store


print("bad_add(1)    ->", bad_add(1))     # [1]
print("bad_add(2)    ->", bad_add(2))     # [1, 2]     <- leaked from last call!
print("bad_add(3)    ->", bad_add(3))     # [1, 2, 3]  <- keeps growing forever
print("good_add(1)   ->", good_add(1))    # [1]
print("good_add(2)   ->", good_add(2))    # [2]  fresh list every call
print("good_add(3)   ->", good_add(3))    # [3]


# -------------------------------------------------------------
# 15) MUTABILITY PROOF (vs strings & numbers)
# -------------------------------------------------------------
print("\n--- 15) MUTABLE ---")
proof = [1, 2, 3]
print("id before     ->", id(proof) == id(proof))
before = id(proof)
proof.append(4)
print("same object?  ->", id(proof) == before)   # True — mutated in place
proof = proof + [5]
print("after + rebind->", id(proof) == before)   # False — NEW list created
print("final nums    ->", nums)                  # untouched all the way through
