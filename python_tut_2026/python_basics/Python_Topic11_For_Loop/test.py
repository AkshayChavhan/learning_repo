# =============================================================
# PYTHON for LOOP — walk through any iterable
# =============================================================
#   for <var> in <iterable>:
#       body
#
# Python's for is a FOR-EACH: it hands you the items, never an index
# counter you manage yourself. Anything iterable works: list, tuple,
# string, set, dict, range, file, generator.
# =============================================================

from itertools import islice

nums = [10, 20, 30, 40]
word = "python"
person = {"name": "Akshay", "age": 29, "city": "Pune"}


# -------------------------------------------------------------
# 1) LOOPING OVER EVERYTHING
# -------------------------------------------------------------
print("--- 1) ITERABLES ---")
for n in nums:
    print("  list   ->", n, end="")
print()
for ch in word:
    print("  str    ->", ch, end="")
print()
for item in (1, 2, 3):
    print("  tuple  ->", item, end="")
print()
for item in {1, 2, 3}:
    print("  set    ->", item, end="")           # order not guaranteed
print()
for key in person:                               # a dict yields its KEYS
    print("  dict   ->", key, end="")
print()
for i in range(4):
    print("  range  ->", i, end="")
print()
for line in "a\nb".splitlines():
    print("  lines  ->", line, end="")
print()


# -------------------------------------------------------------
# 2) range() — the counting iterable
# -------------------------------------------------------------
print("\n--- 2) range ---")
print("range(5)      ->", list(range(5)))            # 0..4 (stop EXCLUDED)
print("range(2,6)    ->", list(range(2, 6)))         # 2..5
print("range(0,10,2) ->", list(range(0, 10, 2)))     # step
print("range(5,0,-1) ->", list(range(5, 0, -1)))     # countdown
print("range(0)      ->", list(range(0)))            # [] — loop runs 0 times
print("len(nums)     ->", list(range(len(nums))))    # index positions
print("lazy          ->", range(1000000))            # stores 3 numbers, not 1M


# -------------------------------------------------------------
# 3) enumerate() — index AND value
# -------------------------------------------------------------
print("\n--- 3) enumerate ---")
# The clumsy C-style way:
for i in range(len(nums)):
    print("  by index ->", i, nums[i], end="")
print()
# The pythonic way:
for i, v in enumerate(nums):
    print("  enumerate->", i, v, end="")
print()
for i, v in enumerate(nums, start=1):            # start counting at 1
    print("  start=1  ->", i, v, end="")
print()
print("as list       ->", list(enumerate("ab")))


# -------------------------------------------------------------
# 4) zip() — walk several iterables together
# -------------------------------------------------------------
print("\n--- 4) zip ---")
names = ["amit", "riya", "zoya"]
ages = [30, 25, 41]
for nm, ag in zip(names, ages):
    print("  zip      ->", nm, ag, end=" |")
print()
print("stops at shortest ->", list(zip([1, 2, 3], "ab")))
for nm, ag, city in zip(names, ages, ["Pune", "Delhi", "Goa"]):
    print("  3-way    ->", nm, ag, city, end=" |")
print()
print("zip + enumerate ->", [(i, n, a) for i, (n, a) in enumerate(zip(names, ages))])
print("unzip with *  ->", list(zip(*[(1, "a"), (2, "b")])))
print("build dict    ->", dict(zip(names, ages)))


# -------------------------------------------------------------
# 5) LOOPING OVER DICTS
# -------------------------------------------------------------
print("\n--- 5) DICT LOOPS ---")
for k in person:
    print("  keys     ->", k, end=" |")
print()
for v in person.values():
    print("  values   ->", v, end=" |")
print()
for k, v in person.items():                      # the standard way
    print("  items    -> %s=%s" % (k, v), end=" |")
print()
for i, (k, v) in enumerate(person.items()):
    print("  numbered -> %d.%s" % (i, k), end=" |")
print()
print("sorted by key ->", [k for k in sorted(person)])


# -------------------------------------------------------------
# 6) reversed / sorted / and other loop helpers
# -------------------------------------------------------------
print("\n--- 6) HELPERS ---")
print("reversed      ->", [n for n in reversed(nums)])
print("slice reverse ->", nums[::-1])
print("sorted        ->", [n for n in sorted([3, 1, 2])])
print("sorted desc   ->", sorted([3, 1, 2], reverse=True))
print("sorted by key ->", sorted(names, key=len))
print("sorted dict   ->", sorted(person.items(), key=lambda kv: str(kv[1])))
print("islice        ->", list(islice(range(100), 3)))     # first 3 only


# -------------------------------------------------------------
# 7) break / continue / else
# -------------------------------------------------------------
print("\n--- 7) break / continue / else ---")
for n in nums:
    if n == 30:
        print("  break at ->", n)
        break
    print("  saw      ->", n, end="")
print()

for n in nums:
    if n == 20:
        continue                                  # skip just this one
    print("  kept     ->", n, end="")
print()

# for ... else — the else runs ONLY when the loop finished with NO break
target = 99
for n in nums:
    if n == target:
        print("found", n)
        break
else:
    print("for/else      -> %d not found (else ran)" % target)

for n in nums:
    if n == 20:
        break
else:
    print("never printed")
print("with break    -> else skipped")


# -------------------------------------------------------------
# 8) NESTED LOOPS
# -------------------------------------------------------------
print("\n--- 8) NESTED ---")
for r in range(1, 4):
    row = ""
    for c in range(1, 4):
        row += "%3d" % (r * c)
    print("  table    ->", row)

grid = [[1, 2], [3, 4]]
for row in grid:
    for cell in row:
        print("  cell     ->", cell, end="")
print()
print("flatten       ->", [c for row in grid for c in row])   # same order

# break only exits the INNER loop — use a flag or a function to exit both
found_at = None
for i, row in enumerate(grid):
    for j, cell in enumerate(row):
        if cell == 3:
            found_at = (i, j)
            break
    if found_at:
        break
print("2D search     ->", found_at)


# -------------------------------------------------------------
# 9) COMPREHENSIONS — a for loop as an expression
# -------------------------------------------------------------
print("\n--- 9) COMPREHENSIONS ---")
squares = []
for n in range(5):
    squares.append(n * n)
print("loop version  ->", squares)
print("comprehension ->", [n * n for n in range(5)])          # same, one line
print("with filter   ->", [n for n in range(10) if n % 3 == 0])
print("with ternary  ->", ["hi" if n else "lo" for n in range(3)])
print("nested        ->", [(i, j) for i in range(2) for j in "ab"])
print("dict comp     ->", {n: n * n for n in range(4)})
print("set comp      ->", {n % 3 for n in range(10)})
print("generator     ->", sum(n * n for n in range(5)))       # lazy, no list built


# -------------------------------------------------------------
# 10) TRAPS
# -------------------------------------------------------------
print("\n--- 10) TRAPS ---")

# 1. Never mutate the list you're iterating
data = [1, 2, 3, 4, 5, 6]
for v in data[:]:                                 # iterate a COPY
    if v % 2 == 0:
        data.remove(v)
print("safe removal  ->", data)
print("better        ->", [v for v in [1, 2, 3, 4, 5, 6] if v % 2])

# 2. The loop variable LEAKS after the loop ends
for leaked in range(3):
    pass
print("leaked var    ->", leaked)                 # 2 — still alive

# 3. An exhausted iterator gives nothing the second time
it = iter([1, 2])
print("first pass    ->", [x for x in it])
print("second pass   ->", [x for x in it])        # [] — already consumed

# 4. zip() silently stops at the shortest input
print("uneven zip    ->", list(zip([1, 2, 3], [9])))

# 5. Modifying dict size during iteration -> RuntimeError
dd = {"a": 1, "b": 2}
for k in list(dd):                                # loop over a COPY of the keys
    if k == "a":
        del dd[k]
print("safe dict del ->", dd)

# 6. Building a string in a loop is O(n^2) — join is O(n)
print("slow concat   -> s += x in a loop")
print("fast join     ->", "".join(str(n) for n in nums))


# -------------------------------------------------------------
# 11) HOW for ACTUALLY WORKS (under the hood)
# -------------------------------------------------------------
print("\n--- 11) UNDER THE HOOD ---")
#   for x in obj:  is really:
#       it = iter(obj)
#       while True:
#           try: x = next(it)
#           except StopIteration: break
manual = iter([1, 2])
print("iter()        ->", manual)
print("next()        ->", next(manual))
print("next()        ->", next(manual))
try:
    next(manual)
except StopIteration:
    print("next()        -> StopIteration = loop would end here")


# -------------------------------------------------------------
# 12) COMMON PATTERNS
# -------------------------------------------------------------
print("\n--- 12) PATTERNS ---")
print("sum           ->", sum(nums))
print("max by key    ->", max(names, key=len))
print("count matches ->", sum(1 for n in nums if n > 15))
print("any / all     ->", any(n > 35 for n in nums), all(n > 5 for n in nums))
print("build dict    ->", {n: n * n for n in range(3)})
print("group by      ->", {p: [n for n in names if n.startswith(p)] for p in "arz"})
print("first match   ->", next((n for n in nums if n > 15), None))
print("chunk by 2    ->", [nums[i:i + 2] for i in range(0, len(nums), 2)])
print("repeat n times->", [x for _ in range(2) for x in "ab"])


# -------------------------------------------------------------
# 13) CHEAT SHEET
# -------------------------------------------------------------
#   for x in seq:            for-each over any iterable
#   range(a, b, step)        counting loop
#   enumerate(seq, start)    index + value
#   zip(a, b)                walk several sequences together
#   d.items()                key + value from a dict
#   reversed / sorted        change the walk order
#   break / continue         exit / skip
#   else:                    runs only if NO break happened
#   [expr for x in seq if c] the same loop as a one-line expression
print("\n--- 13) DONE ---")
print("nums          ->", nums)
