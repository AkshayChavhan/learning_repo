# =============================================================
# PYTHON GENERATORS & RECURSION
# =============================================================
# GENERATOR = a function with `yield`. It PAUSES and resumes,
#             producing values one at a time (lazy, tiny memory).
# RECURSION = a function that calls itself, shrinking the problem
#             until it hits a BASE CASE.
# =============================================================

import sys
import functools
from itertools import islice, count, cycle


# =============================================================
# PART A — GENERATORS
# =============================================================

# -------------------------------------------------------------
# 1) yield vs return
# -------------------------------------------------------------
print("--- 1) yield BASICS ---")


def normal():
    return [1, 2, 3]              # builds the WHOLE list, then hands it over


def generated():
    yield 1                       # pauses here, hands out 1
    yield 2                       # resumes here on the next request
    yield 3


print("normal()      ->", normal())
print("generated()   ->", generated())              # a generator OBJECT, no values yet
print("as a list     ->", list(generated()))
print("type          ->", type(generated()))

gen = generated()
print("next()        ->", next(gen))                # runs until the 1st yield
print("next()        ->", next(gen))                # resumes, runs to the 2nd
print("next()        ->", next(gen))
try:
    next(gen)
except StopIteration:
    print("next()        -> StopIteration = it's exhausted")


# -------------------------------------------------------------
# 2) EXECUTION IS LAZY — watch the pauses
# -------------------------------------------------------------
print("\n--- 2) LAZY EXECUTION ---")


def chatty():
    print("    [start]")
    yield "a"
    print("    [resumed after a]")
    yield "b"
    print("    [finishing]")


c = chatty()
print("  created — nothing ran yet")
print("  got:", next(c))
print("  got:", next(c))
try:
    next(c)
except StopIteration:
    print("  done")


# -------------------------------------------------------------
# 3) GENERATORS IN LOOPS & THE ONE-SHOT TRAP
# -------------------------------------------------------------
print("\n--- 3) LOOPS & EXHAUSTION ---")


def countdown(n):
    while n > 0:
        yield n
        n -= 1


for v in countdown(4):
    print("  ", v, end="")
print()

g = countdown(3)
print("first pass    ->", list(g))
print("second pass   ->", list(g))     # [] — generators are ONE-SHOT
print("fix: call the function again ->", list(countdown(3)))


# -------------------------------------------------------------
# 4) GENERATOR EXPRESSIONS  ( ) instead of [ ]
# -------------------------------------------------------------
print("\n--- 4) GENERATOR EXPRESSIONS ---")
list_comp = [n * n for n in range(5)]           # builds all 5 now
gen_expr = (n * n for n in range(5))            # builds nothing yet
print("list comp     ->", list_comp)
print("gen expr      ->", gen_expr)
print("consumed      ->", list(gen_expr))
print("sum directly  ->", sum(n * n for n in range(5)))   # no brackets needed

big_list = [n for n in range(100000)]
big_gen = (n for n in range(100000))
print("list  bytes   ->", sys.getsizeof(big_list))
print("gen   bytes   ->", sys.getsizeof(big_gen), "<- constant, no matter the size")


# -------------------------------------------------------------
# 5) INFINITE GENERATORS
# -------------------------------------------------------------
print("\n--- 5) INFINITE ---")


def naturals():
    n = 0
    while True:                    # infinite — safe because it's LAZY
        yield n
        n += 1


print("first 5       ->", list(islice(naturals(), 5)))
print("itertools.count->", list(islice(count(10, 5), 4)))
print("itertools.cycle->", list(islice(cycle("ab"), 5)))


def fib_stream():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("fib stream    ->", list(islice(fib_stream(), 10)))
print("first > 100   ->", next(n for n in fib_stream() if n > 100))


# -------------------------------------------------------------
# 6) yield from — delegate to another iterable
# -------------------------------------------------------------
print("\n--- 6) yield from ---")


def inner_gen():
    yield 1
    yield 2


def outer_manual():
    for v in inner_gen():
        yield v
    yield 3


def outer_delegate():
    yield from inner_gen()         # same thing, one line
    yield 3


print("manual        ->", list(outer_manual()))
print("yield from    ->", list(outer_delegate()))


def flatten(nested):
    """Recursion + yield from = a clean deep flattener."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


print("flatten       ->", list(flatten([1, [2, [3, [4, 5]], 6], 7])))


# -------------------------------------------------------------
# 7) send / close  (two-way generators)
# -------------------------------------------------------------
print("\n--- 7) send / close ---")


def accumulator():
    total = 0
    while True:
        received = yield total       # yield OUT, and receive a value back IN
        if received is None:
            received = 0
        total += received


acc = accumulator()
print("prime it      ->", next(acc))       # run to the first yield
print("send(10)      ->", acc.send(10))
print("send(5)       ->", acc.send(5))
acc.close()
try:
    next(acc)
except StopIteration:
    print("close()       -> generator shut down")


# -------------------------------------------------------------
# 8) REAL USES OF GENERATORS
# -------------------------------------------------------------
print("\n--- 8) REAL USES ---")


def read_lines(text):
    """Stream a huge file line by line without loading it all."""
    for line in text.splitlines():
        yield line.strip()


print("pipeline in   ->", list(read_lines(" a \n b \n c ")))

# Chained pipeline — each stage is lazy, nothing is materialised in between
nums = range(1, 21)
evens = (n for n in nums if n % 2 == 0)
squares = (n * n for n in evens)
big = (n for n in squares if n > 50)
print("pipeline out  ->", list(big))


def batched(iterable, size):
    """Yield fixed-size chunks — a very common utility."""
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            return
        yield chunk


print("batched       ->", list(batched(range(7), 3)))


# =============================================================
# PART B — RECURSION
# =============================================================

# -------------------------------------------------------------
# 9) THE SHAPE OF A RECURSIVE FUNCTION
# -------------------------------------------------------------
print("\n--- 9) RECURSION BASICS ---")
#   1. BASE CASE     -> when to stop (without it: RecursionError)
#   2. RECURSIVE STEP-> call yourself on a SMALLER problem


def factorial(n):
    if n <= 1:                     # base case
        return 1
    return n * factorial(n - 1)    # recursive step


print("factorial(5)  ->", factorial(5))
print("trace         -> 5*4*3*2*1 = 120")


def countdown_rec(n):
    if n == 0:
        return ["liftoff"]
    return [n] + countdown_rec(n - 1)


print("countdown     ->", countdown_rec(4))


def sum_list(items):
    if not items:                  # empty list = base case
        return 0
    return items[0] + sum_list(items[1:])


print("sum_list      ->", sum_list([1, 2, 3, 4]))


def reverse_str(s):
    if len(s) <= 1:
        return s
    return reverse_str(s[1:]) + s[0]


print("reverse       ->", reverse_str("python"))


def palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return palindrome(s[1:-1])


print("palindrome    ->", palindrome("racecar"), palindrome("hello"))


# -------------------------------------------------------------
# 10) TREE / NESTED RECURSION
# -------------------------------------------------------------
print("\n--- 10) NESTED DATA ---")


def deep_sum(data):
    """Recursion shines on nested structures of unknown depth."""
    total = 0
    for item in data:
        total += deep_sum(item) if isinstance(item, list) else item
    return total


print("deep_sum      ->", deep_sum([1, [2, [3, [4]]], 5]))


def depth(data):
    if not isinstance(data, list):
        return 0
    return 1 + max((depth(x) for x in data), default=0)


print("depth         ->", depth([1, [2, [3, [4]]]]))

tree = {"value": 1, "children": [
    {"value": 2, "children": []},
    {"value": 3, "children": [{"value": 4, "children": []}]},
]}


def tree_sum(node):
    return node["value"] + sum(tree_sum(child) for child in node["children"])


print("tree_sum      ->", tree_sum(tree))


def walk(node, level=0):
    print("  " + "  " * level + "- " + str(node["value"]))
    for child in node["children"]:
        walk(child, level + 1)


walk(tree)


# -------------------------------------------------------------
# 11) THE COST OF NAIVE RECURSION
# -------------------------------------------------------------
print("\n--- 11) COST & MEMOIZATION ---")

calls = {"n": 0}


def fib_slow(n):
    calls["n"] += 1
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)


print("fib_slow(20)  ->", fib_slow(20), "in", calls["n"], "calls  <- exponential")


@functools.lru_cache(maxsize=None)
def fib_fast(n):
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)


print("fib_fast(100) ->", fib_fast(100), "instantly (memoized)")
print("cache stats   ->", fib_fast.cache_info())


def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


print("fib_iter(100) ->", fib_iter(100), "<- no recursion at all, O(n)")


# -------------------------------------------------------------
# 12) RECURSION LIMITS
# -------------------------------------------------------------
print("\n--- 12) LIMITS ---")
print("limit         ->", sys.getrecursionlimit())      # usually 1000


def runaway(n):
    return runaway(n + 1)                                # no base case


try:
    runaway(0)
except RecursionError as e:
    print("no base case  -> RecursionError:", str(e)[:45])

print("no tail-call optimisation in Python -> deep recursion always costs stack")
print("=> for depth > ~1000, rewrite it as a loop or use an explicit stack")


def flatten_iterative(nested):
    """The loop version of a recursive walk — uses an explicit stack."""
    out, stack = [], list(nested)[::-1]
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item[::-1])
        else:
            out.append(item)
    return out


print("iterative     ->", flatten_iterative([1, [2, [3, [4, 5]]], 6]))


# -------------------------------------------------------------
# 13) GENERATORS vs RECURSION vs LOOPS — when to use what
# -------------------------------------------------------------
#   generator -> huge/infinite streams, pipelines, saving memory, lazy reads
#   recursion -> naturally nested data: trees, JSON, folders, divide & conquer
#   loop      -> everything else; always the cheapest and the safest
print("\n--- 13) CHEAT SHEET ---")
#   yield          pause & emit a value        | next(g)      pull one value
#   (x for x in y) generator expression        | list(g)      drain it
#   yield from     delegate to another gen     | g.send(v)    push a value in
#   islice(g, n)   take n from an infinite gen | StopIteration = exhausted
#   base case      the line that stops recursion
#   @lru_cache     memoize repeated recursive calls
print("\n--- 13) DONE ---")
print("gen memory    ->", sys.getsizeof(n for n in range(10 ** 9)), "bytes for a BILLION items")
print("factorial(10) ->", factorial(10))
