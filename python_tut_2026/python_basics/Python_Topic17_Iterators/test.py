# =============================================================
# PYTHON ITERATORS — the protocol behind every for loop
# =============================================================
#   ITERABLE  -> has __iter__()  -> you can loop over it   (list, str, dict...)
#   ITERATOR  -> has __iter__() AND __next__()  -> produces values ONE at a time
#
#   iter(obj) turns an iterable INTO an iterator
#   next(it)  pulls the next value, raises StopIteration when empty
# =============================================================

import sys
from itertools import (count, cycle, repeat, islice, chain, zip_longest,
                       product, permutations, combinations, groupby,
                       accumulate, tee, starmap, compress, dropwhile, takewhile)


# -------------------------------------------------------------
# 1) ITERABLE vs ITERATOR
# -------------------------------------------------------------
print("--- 1) ITERABLE vs ITERATOR ---")
nums = [1, 2, 3]
it = iter(nums)
print("list          ->", nums, type(nums).__name__)
print("iter(list)    ->", it, type(it).__name__)
print("list has __iter__ ->", hasattr(nums, "__iter__"))
print("list has __next__ ->", hasattr(nums, "__next__"))     # False!
print("it has both       ->", hasattr(it, "__iter__"), hasattr(it, "__next__"))
print("iter(it) is it    ->", iter(it) is it)   # an iterator returns ITSELF

print("next()        ->", next(it))
print("next()        ->", next(it))
print("next()        ->", next(it))
try:
    next(it)
except StopIteration:
    print("next()        -> StopIteration (exhausted)")
print("next w/ default->", next(it, "EMPTY"))    # no exception when you pass one


# -------------------------------------------------------------
# 2) HOW A for LOOP REALLY WORKS
# -------------------------------------------------------------
print("\n--- 2) UNDER THE HOOD ---")
print("for x in obj:  ==  it = iter(obj); while True: next(it) ... except StopIteration: break")
manual = iter(["a", "b"])
while True:
    try:
        value = next(manual)
    except StopIteration:
        break
    print("  manual loop ->", value, end="")
print()


# -------------------------------------------------------------
# 3) WHAT IS ITERABLE
# -------------------------------------------------------------
print("\n--- 3) ITERABLES EVERYWHERE ---")
for obj in ([1, 2], (1, 2), {1, 2}, {"a": 1}, "ab", range(2), enumerate("a")):
    print("  %-18s iterable=%s" % (type(obj).__name__, hasattr(obj, "__iter__")))
print("int is NOT    ->", hasattr(42, "__iter__"))
try:
    iter(42)
except TypeError as e:
    print("iter(42)      -> TypeError:", e)


# -------------------------------------------------------------
# 4) THE EXHAUSTION TRAP
# -------------------------------------------------------------
print("\n--- 4) ONE-SHOT ---")
it = iter([1, 2, 3])
print("first pass    ->", list(it))
print("second pass   ->", list(it))              # [] — already consumed
print("a LIST reruns ->", [list(nums), list(nums)])   # lists are re-iterable

# zip / map / filter are ITERATORS in Python 3 — same trap
z = zip([1, 2], "ab")
print("zip once      ->", list(z))
print("zip twice     ->", list(z))               # []
m = map(str.upper, "ab")
print("map once      ->", list(m), "| twice ->", list(m))

# Partial consumption leaves the rest behind
half = iter([1, 2, 3, 4])
next(half)
print("after 1 next  ->", list(half))            # [2, 3, 4]


# -------------------------------------------------------------
# 5) BUILDING A CUSTOM ITERATOR (class form)
# -------------------------------------------------------------
print("\n--- 5) CUSTOM ITERATOR ---")


class Countdown:
    """Implement __iter__ + __next__ and it works in any for loop."""

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self                       # I am my own iterator

    def __next__(self):
        if self.current <= 0:
            raise StopIteration           # THIS is what ends the loop
        self.current -= 1
        return self.current + 1


for v in Countdown(4):
    print("  ", v, end="")
print()
print("as a list     ->", list(Countdown(3)))
c = Countdown(2)
print("manual next   ->", next(c), next(c))


class Repeater:
    """Re-iterable: __iter__ hands out a FRESH iterator each time."""

    def __init__(self, items):
        self.items = items

    def __iter__(self):
        return iter(self.items)           # new iterator per loop


r = Repeater([1, 2])
print("re-iterable   ->", list(r), list(r))      # both work


class Squares:
    """The old __getitem__ protocol also makes an object iterable."""

    def __getitem__(self, i):
        if i > 3:
            raise IndexError
        return i * i


print("__getitem__   ->", list(Squares()))


# -------------------------------------------------------------
# 6) GENERATORS — iterators without the boilerplate
# -------------------------------------------------------------
print("\n--- 6) GENERATOR SHORTCUT ---")


def countdown_gen(start):
    while start > 0:
        yield start
        start -= 1


print("generator     ->", list(countdown_gen(4)))
g = countdown_gen(2)
print("is an iterator->", hasattr(g, "__next__"), iter(g) is g)
print("=> 3 lines replace the whole Countdown class above")
print("gen expression->", list(x * x for x in range(4)))


# -------------------------------------------------------------
# 7) MEMORY — the real payoff
# -------------------------------------------------------------
print("\n--- 7) MEMORY ---")
big_list = [x for x in range(100000)]
big_iter = (x for x in range(100000))
print("list  bytes   ->", sys.getsizeof(big_list))
print("iter  bytes   ->", sys.getsizeof(big_iter), "<- constant for ANY size")
print("sum via iter  ->", sum(x for x in range(100000)), "(nothing stored)")


# -------------------------------------------------------------
# 8) BUILT-INS THAT RETURN ITERATORS
# -------------------------------------------------------------
print("\n--- 8) BUILT-IN ITERATORS ---")
print("enumerate     ->", enumerate("ab"), "->", list(enumerate("ab")))
print("zip           ->", list(zip([1, 2], "ab")))
print("map           ->", list(map(lambda n: n * 2, [1, 2])))
print("filter        ->", list(filter(lambda n: n > 1, [1, 2, 3])))
print("reversed      ->", list(reversed([1, 2, 3])))
# 2-argument iter(callable, sentinel): call the function until it returns sentinel
feed = iter([1, 1, 1, 99, 5])
print("iter(fn, stop)->", list(iter(lambda: next(feed), 99)))   # [1, 1, 1]


# -------------------------------------------------------------
# 9) itertools — INFINITE ITERATORS
# -------------------------------------------------------------
print("\n--- 9) itertools: INFINITE ---")
print("count(10, 2)  ->", list(islice(count(10, 2), 5)))
print("cycle('abc')  ->", list(islice(cycle("abc"), 7)))
print("repeat(9, 3)  ->", list(repeat(9, 3)))
print("islice is what makes infinite iterators safe")


# -------------------------------------------------------------
# 10) itertools — COMBINING & FILTERING
# -------------------------------------------------------------
print("\n--- 10) itertools: COMBINE ---")
print("chain         ->", list(chain([1, 2], "ab", (3,))))
print("chain.from_it ->", list(chain.from_iterable([[1, 2], [3]])))
print("zip_longest   ->", list(zip_longest([1, 2, 3], "ab", fillvalue="-")))
print("compress      ->", list(compress("abcd", [1, 0, 1, 0])))
print("takewhile     ->", list(takewhile(lambda n: n < 3, [1, 2, 3, 1])))
print("dropwhile     ->", list(dropwhile(lambda n: n < 3, [1, 2, 3, 1])))
print("starmap       ->", list(starmap(pow, [(2, 3), (3, 2)])))
print("accumulate    ->", list(accumulate([1, 2, 3, 4])))          # running sum
print("accumulate max->", list(accumulate([3, 1, 5, 2], max)))
print("islice(2, 5)  ->", list(islice(range(10), 2, 5)))
print("islice step   ->", list(islice(range(10), 0, 10, 3)))

t1, t2 = tee(iter([1, 2, 3]), 2)                 # clone a one-shot iterator
print("tee           ->", list(t1), list(t2))


# -------------------------------------------------------------
# 11) itertools — COMBINATORICS & GROUPING
# -------------------------------------------------------------
print("\n--- 11) itertools: MATH ---")
print("product       ->", list(product("ab", [1, 2])))
print("product rep=2 ->", list(product("ab", repeat=2)))
print("permutations  ->", list(permutations("abc", 2)))
print("combinations  ->", list(combinations("abc", 2)))

# groupby needs the data SORTED by the same key first
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
for letter, group in groupby(sorted(words), key=lambda w: w[0]):
    print("  groupby ->", letter, list(group))
print("unsorted trap ->", [(k, list(g)) for k, g in groupby("aabba")])


# -------------------------------------------------------------
# 12) PIPELINES — chaining lazy stages
# -------------------------------------------------------------
print("\n--- 12) PIPELINES ---")
source = range(1, 21)
stage1 = (n for n in source if n % 2 == 0)       # filter
stage2 = (n * n for n in stage1)                 # transform
stage3 = takewhile(lambda n: n < 200, stage2)    # cut off
print("pipeline      ->", list(stage3))
print("=> nothing is computed until the final list() pulls the values")

lines = ["  alpha ", "", " beta", "   ", "gamma "]
cleaned = (ln.strip() for ln in lines)
non_empty = (ln for ln in cleaned if ln)
print("text pipeline ->", list(non_empty))


# -------------------------------------------------------------
# 13) PRACTICAL PATTERNS
# -------------------------------------------------------------
print("\n--- 13) PATTERNS ---")
print("first match   ->", next((n for n in [1, 5, 9] if n > 4), None))
print("no match      ->", next((n for n in [1, 2] if n > 4), "none"))
print("take n        ->", list(islice(count(), 4)))
print("skip n        ->", list(islice(range(10), 7, None)))
print("last item     ->", next(reversed([1, 2, 3])))
print("any / all lazy->", any(n > 2 for n in [1, 2, 3]), all(n > 0 for n in [1, 2]))
print("count matches ->", sum(1 for n in range(20) if n % 3 == 0))
print("pairwise      ->", list(zip([1, 2, 3], [1, 2, 3][1:])))   # 3.10 has pairwise()
chunk_src = iter(range(7))
print("chunks of 3   ->", list(iter(lambda: list(islice(chunk_src, 3)), [])))
print("dedupe keep   ->", list(dict.fromkeys([1, 2, 1, 3])))
print("flatten       ->", list(chain.from_iterable([[1, 2], [3, 4]])))


# -------------------------------------------------------------
# 14) GOTCHAS
# -------------------------------------------------------------
print("\n--- 14) GOTCHAS ---")
print("1. iterators are ONE-SHOT — list() them if you need two passes")
print("2. zip/map/filter are lazy in Py3 — print(map(...)) shows an object")
print("   ", map(str, [1]))
print("3. len() does NOT work on an iterator:")
try:
    len(iter([1, 2]))
except TypeError as e:
    print("   ", "TypeError:", e)
print("4. no indexing either:")
try:
    iter([1, 2])[0]
except TypeError as e:
    print("   ", "TypeError:", e)
print("5. mutating a list while iterating it -> skipped items / RuntimeError")
print("6. an infinite iterator without islice will hang forever")


# -------------------------------------------------------------
# 15) CHEAT SHEET
# -------------------------------------------------------------
#   iterable   __iter__            list, tuple, str, dict, set, range, file
#   iterator   __iter__+__next__   the thing that actually yields values
#   iter(x)    get an iterator     |  next(it, default)  pull one safely
#   StopIteration                  the signal that ends every for loop
#   class      __iter__/__next__   full control
#   generator  yield               the same thing in 3 lines
#   itertools  count cycle repeat islice chain zip_longest product
#              permutations combinations groupby accumulate tee compress
#              starmap takewhile dropwhile
print("\n--- 15) DONE ---")
print("iterator type ->", type(iter([])).__name__)
print("gen type      ->", type(x for x in []).__name__)
