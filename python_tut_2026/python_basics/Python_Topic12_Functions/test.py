# =============================================================
# PYTHON FUNCTIONS — def, arguments, scope, lambda
# =============================================================
#   def name(params):
#       """docstring"""
#       body
#       return value        <- without it, the function returns None
#
# Functions are OBJECTS: you can pass them around, store them, return them.
# =============================================================

import sys


# -------------------------------------------------------------
# 1) DEFINING & CALLING
# -------------------------------------------------------------
print("--- 1) BASICS ---")


def greet():
    """No parameters, no return."""
    print("  hello from greet()")


def add(a, b):
    """Two parameters, returns a value."""
    return a + b


greet()
print("add(2, 3)     ->", add(2, 3))
print("no return     ->", greet.__doc__ and add(1, 1))
print("returns None  ->", print("") is None)     # a function without return -> None


def no_return():
    a = 1                                        # computes, returns nothing


print("implicit None ->", no_return())           # None


# -------------------------------------------------------------
# 2) ARGUMENT TYPES
# -------------------------------------------------------------
print("\n--- 2) ARGUMENTS ---")


def profile(name, age, city="Pune", active=True):
    """name/age are REQUIRED (positional), city/active have DEFAULTS."""
    return "%s(%d) from %s active=%s" % (name, age, city, active)


print("positional    ->", profile("Akshay", 29))
print("keyword       ->", profile(age=29, name="Akshay"))       # order free
print("mixed         ->", profile("Riya", 25, active=False))
print("override defl ->", profile("Zoya", 41, "Goa"))

# Rule: positional args must come BEFORE keyword args
# profile(name="A", 29)  ->  SyntaxError

try:
    profile("Akshay")
except TypeError as e:
    print("missing arg   -> TypeError:", e)


# -------------------------------------------------------------
# 3) *args — collect extra POSITIONAL args into a TUPLE
# -------------------------------------------------------------
print("\n--- 3) *args ---")


def total(*args):
    return type(args).__name__, args, sum(args)


print("total(1,2,3)  ->", total(1, 2, 3))
print("total()       ->", total())                # empty tuple, no error


def tag(label, *values):
    return "%s: %s" % (label, list(values))


print("mixed w/ args ->", tag("nums", 1, 2, 3))
print("unpack a list ->", total(*[4, 5, 6]))      # * spreads the list


# -------------------------------------------------------------
# 4) **kwargs — collect extra KEYWORD args into a DICT
# -------------------------------------------------------------
print("\n--- 4) **kwargs ---")


def config(**kwargs):
    return type(kwargs).__name__, kwargs


print("config(a=1)   ->", config(a=1, b=2))
print("config()      ->", config())               # empty dict


def everything(req, *args, **kwargs):
    """THE canonical signature order: required, *args, **kwargs."""
    return {"req": req, "args": args, "kwargs": kwargs}


print("all together  ->", everything(1, 2, 3, x=10, y=20))
print("unpack a dict ->", config(**{"host": "local", "port": 80}))


# -------------------------------------------------------------
# 5) POSITIONAL-ONLY  /  and KEYWORD-ONLY  *   (3.8+)
# -------------------------------------------------------------
print("\n--- 5) / and * ---")


def strict(pos_only, /, normal, *, kw_only):
    """
    Everything BEFORE  /  -> positional only (cannot be passed by name)
    Everything AFTER   *  -> keyword only    (cannot be passed by position)
    """
    return pos_only, normal, kw_only


print("valid call    ->", strict(1, 2, kw_only=3))
print("normal by name->", strict(1, normal=2, kw_only=3))
try:
    strict(pos_only=1, normal=2, kw_only=3)
except TypeError as e:
    print("pos by name   -> TypeError:", e)
try:
    strict(1, 2, 3)
except TypeError as e:
    print("kw by position-> TypeError:", e)


# -------------------------------------------------------------
# 6) RETURN VALUES
# -------------------------------------------------------------
print("\n--- 6) RETURN ---")


def stats(values):
    """Returning several values is really returning a TUPLE."""
    return min(values), max(values), sum(values) / len(values)


lo, hi, avg = stats([4, 9, 2])
print("multi return  ->", lo, hi, round(avg, 2))
print("as a tuple    ->", stats([4, 9, 2]))


def early(n):
    """return exits IMMEDIATELY — nothing after it runs."""
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "positive"


print("early return  ->", [early(v) for v in (-1, 0, 5)])


def multiple_returns(n):
    return n * 2
    print("unreachable")                          # never executes


print("after return  ->", multiple_returns(5))


# -------------------------------------------------------------
# 7) SCOPE — LEGB (Local -> Enclosing -> Global -> Built-in)
# -------------------------------------------------------------
print("\n--- 7) SCOPE ---")
g = "global value"


def read_global():
    return g                                       # reading is always fine


def shadow():
    g = "local value"                              # NEW local, global untouched
    return g


print("read global   ->", read_global())
print("shadowing     ->", shadow(), "| global still:", g)


def write_global():
    global g                                       # explicit permission to rebind
    g = "changed"


write_global()
print("global keyword->", g)


def outer():
    count = 0

    def inner():
        nonlocal count                             # rebind the ENCLOSING variable
        count += 1
        return count

    inner()
    inner()
    return count


print("nonlocal      ->", outer())                 # 2


def unbound_demo():
    try:
        print(missing_var)
    except NameError as e:
        return "NameError: %s" % e


print("undefined     ->", unbound_demo())
print("builtins      ->", len("abc"), "<- len comes from the B in LEGB")


# -------------------------------------------------------------
# 8) MUTABLE DEFAULT ARGUMENT — the famous trap
# -------------------------------------------------------------
print("\n--- 8) MUTABLE DEFAULT ---")


def bad(item, store=[]):        # default is created ONCE, at def time, and REUSED
    store.append(item)
    return store


def good(item, store=None):     # the correct pattern
    if store is None:
        store = []
    store.append(item)
    return store


print("bad(1)        ->", bad(1))
print("bad(2)        ->", bad(2))          # [1, 2] — leaked from the previous call
print("bad(3)        ->", bad(3))          # [1, 2, 3]
print("good(1)       ->", good(1))
print("good(2)       ->", good(2))         # [2] — fresh every time
print("proof         ->", bad.__defaults__)   # the shared list lives on the function

# Same trap: default evaluated at DEFINITION time, not call time
def stamp(when=len("abc")):
    return when


print("default fixed ->", stamp())


# -------------------------------------------------------------
# 9) PASSING SEMANTICS — "pass by object reference"
# -------------------------------------------------------------
print("\n--- 9) PASSING ---")


def mutate(lst):
    lst.append(99)                # MUTATES the caller's list


def rebind(lst):
    lst = [0]                     # rebinds the LOCAL name only


def mutate_int(n):
    n += 1                        # ints are immutable -> caller never sees it


data = [1, 2]
mutate(data)
print("mutate list   ->", data)                   # [1, 2, 99] — changed!
rebind(data)
print("rebind list   ->", data)                   # unchanged
num = 5
mutate_int(num)
print("mutate int    ->", num)                    # 5 — unchanged
print("=> mutable args CAN be changed, immutable ones never")


# -------------------------------------------------------------
# 10) DOCSTRINGS, ANNOTATIONS & METADATA
# -------------------------------------------------------------
print("\n--- 10) METADATA ---")


def area(width: float, height: float = 1.0) -> float:
    """Return the area of a rectangle.

    Annotations are HINTS only — Python does not enforce them.
    """
    return width * height


print("call          ->", area(3, 4))
print("hints ignored ->", area("ab", 3))          # 'ababab' — no error!
print("__name__      ->", area.__name__)
print("__doc__       ->", area.__doc__.splitlines()[0])
print("__annotations__->", area.__annotations__)
print("__defaults__  ->", area.__defaults__)
print("arg count     ->", area.__code__.co_argcount)
print("arg names     ->", area.__code__.co_varnames[:2])


# -------------------------------------------------------------
# 11) LAMBDA — small anonymous functions
# -------------------------------------------------------------
print("\n--- 11) LAMBDA ---")
square = lambda x: x * x                  # one expression only, auto-returns
print("lambda        ->", square(5))
print("multi arg     ->", (lambda a, b: a + b)(2, 3))
print("with default  ->", (lambda a, b=10: a + b)(5))
print("immediately   ->", (lambda: "IIFE")())

people = [("riya", 25), ("amit", 30), ("zoya", 22)]
print("sort by age   ->", sorted(people, key=lambda p: p[1]))
print("map           ->", list(map(lambda n: n * 2, [1, 2, 3])))
print("filter        ->", list(filter(lambda n: n > 1, [1, 2, 3])))
print("max key       ->", max(people, key=lambda p: p[1]))
print("dict of fns   ->", {"sq": lambda n: n ** 2}["sq"](4))
# Use def when it needs a name, a docstring, or more than one expression


# -------------------------------------------------------------
# 12) FUNCTIONS ARE OBJECTS (first class)
# -------------------------------------------------------------
print("\n--- 12) FIRST CLASS ---")


def shout(text):
    return text.upper()


alias = shout                              # assign to a variable (no parens!)
print("aliased       ->", alias("hi"))
print("in a list     ->", [f("hi") for f in (shout, str.title)])
print("as an arg     ->", list(map(shout, ["a", "b"])))


def apply_twice(fn, value):                # higher-order: takes a function
    return fn(fn(value))


print("higher-order  ->", apply_twice(lambda n: n * 3, 2))    # 18


def make_multiplier(factor):               # returns a function (a CLOSURE)
    def multiply(n):
        return n * factor                  # remembers `factor` after outer exits
    return multiply


triple = make_multiplier(3)
print("closure       ->", triple(5))                          # 15
print("closure cell  ->", triple.__closure__[0].cell_contents)  # 3

# Attributes can be stuck onto a function object
shout.calls = 0
shout.calls += 1
print("fn attribute  ->", shout.calls)


# -------------------------------------------------------------
# 13) RECURSION (a function calling itself)
# -------------------------------------------------------------
print("\n--- 13) RECURSION ---")


def factorial(n):
    if n <= 1:              # BASE CASE — without it: infinite recursion
        return 1
    return n * factorial(n - 1)


print("factorial(5)  ->", factorial(5))
print("recursion cap ->", sys.getrecursionlimit())


# -------------------------------------------------------------
# 14) GOOD PRACTICE
# -------------------------------------------------------------
#   - one job per function, name it with a verb (get_user, calc_total)
#   - keep the parameter list short; use keyword args for clarity
#   - return values instead of printing them (callers decide what to do)
#   - never use a mutable default ([], {}) — use None
#   - guard clauses / early returns beat deep nesting
#   - add a docstring when the name alone isn't enough
print("\n--- 14) DONE ---")
print("callable?     ->", callable(add), callable(42))
print("dir sample    ->", [d for d in dir(add) if not d.startswith("__")][:4])
