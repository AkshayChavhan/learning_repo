# =============================================================
# PYTHON DECORATORS — wrap a function to add behaviour
# =============================================================
# A decorator is a function that TAKES a function and RETURNS a new one.
#
#     @my_decorator          is exactly the same as
#     def foo(): ...         foo = my_decorator(foo)
#
# Used for: logging, timing, caching, auth, retries, validation.
# =============================================================

import time
import functools


# -------------------------------------------------------------
# 1) THE TWO IDEAS YOU NEED FIRST
# -------------------------------------------------------------
print("--- 1) FOUNDATIONS ---")


# (a) Functions are objects — they can be passed and returned
def shout(text):
    return text.upper()


def run_it(fn, value):
    return fn(value)


print("fn as argument->", run_it(shout, "hi"))


# (b) A closure remembers the enclosing variables after the outer call ends
def make_prefixer(prefix):
    def inner(text):
        return prefix + text          # `prefix` survives after make_prefixer returns
    return inner


add_mr = make_prefixer("Mr. ")
print("closure       ->", add_mr("Akshay"))
print("remembered    ->", add_mr.__closure__[0].cell_contents)


# -------------------------------------------------------------
# 2) YOUR FIRST DECORATOR — the manual way
# -------------------------------------------------------------
print("\n--- 2) MANUAL ---")


def loud(fn):
    def wrapper():
        print("  >> before")
        result = fn()
        print("  >> after")
        return result
    return wrapper


def hello():
    print("  hello!")


hello = loud(hello)          # manual decoration
hello()


# -------------------------------------------------------------
# 3) THE @ SYNTAX — identical, just prettier
# -------------------------------------------------------------
print("\n--- 3) @ SYNTAX ---")


@loud
def bye():
    print("  bye!")


bye()
print("=> @loud is literally  bye = loud(bye)")


# -------------------------------------------------------------
# 4) HANDLING ANY SIGNATURE — *args / **kwargs
# -------------------------------------------------------------
print("\n--- 4) ANY SIGNATURE ---")


def logged(fn):
    def wrapper(*args, **kwargs):        # accepts ANY arguments
        print("  call %s(%s%s)" % (fn.__name__, args, kwargs or ""))
        result = fn(*args, **kwargs)     # forward them unchanged
        print("  -> returned", result)
        return result                    # NEVER forget to return the result
    return wrapper


@logged
def add(a, b, scale=1):
    return (a + b) * scale


add(2, 3, scale=10)


# -------------------------------------------------------------
# 5) functools.wraps — keep the original identity
# -------------------------------------------------------------
print("\n--- 5) functools.wraps ---")


def broken(fn):
    def wrapper(*a, **k):
        return fn(*a, **k)
    return wrapper


def fixed(fn):
    @functools.wraps(fn)                 # copies __name__, __doc__, __module__...
    def wrapper(*a, **k):
        return fn(*a, **k)
    return wrapper


@broken
def alpha():
    """Alpha docs."""


@fixed
def beta():
    """Beta docs."""


print("without wraps ->", alpha.__name__, "|", alpha.__doc__)   # 'wrapper' | None
print("with wraps    ->", beta.__name__, "|", beta.__doc__)     # 'beta' | 'Beta docs.'
print("original fn   ->", beta.__wrapped__.__name__)            # bonus: the real one
print("=> ALWAYS use @functools.wraps in real code")


# -------------------------------------------------------------
# 6) DECORATOR WITH ARGUMENTS — three nested levels
# -------------------------------------------------------------
print("\n--- 6) DECORATOR ARGS ---")


def repeat(times):                       # 1. takes the decorator's ARGUMENT
    def decorator(fn):                   # 2. takes the FUNCTION
        @functools.wraps(fn)
        def wrapper(*a, **k):            # 3. takes the CALL's arguments
            out = None
            for _ in range(times):
                out = fn(*a, **k)
            return out
        return wrapper
    return decorator


@repeat(times=3)
def ping():
    print("  ping", end="")


ping()
print()
print("=> @repeat(3) runs repeat(3) FIRST, then applies the result as decorator")


# -------------------------------------------------------------
# 7) STACKING DECORATORS — bottom-up
# -------------------------------------------------------------
print("\n--- 7) STACKING ---")


def tag_b(fn):
    @functools.wraps(fn)
    def wrapper():
        return "<b>" + fn() + "</b>"
    return wrapper


def tag_i(fn):
    @functools.wraps(fn)
    def wrapper():
        return "<i>" + fn() + "</i>"
    return wrapper


@tag_b          # applied SECOND -> ends up on the OUTSIDE
@tag_i          # applied FIRST  -> ends up closest to the function
def text():
    return "hi"


print("stacked       ->", text())         # <b><i>hi</i></b>
print("equivalent to -> tag_b(tag_i(text))")


# -------------------------------------------------------------
# 8) PRACTICAL DECORATORS
# -------------------------------------------------------------
print("\n--- 8) PRACTICAL ---")


def timer(fn):
    """Measure how long a call takes."""
    @functools.wraps(fn)
    def wrapper(*a, **k):
        start = time.perf_counter()
        result = fn(*a, **k)
        print("  %s took %.4f ms" % (fn.__name__, (time.perf_counter() - start) * 1000))
        return result
    return wrapper


@timer
def slow_sum(n):
    return sum(range(n))


slow_sum(200000)


def count_calls(fn):
    """Keep state ON the wrapper object."""
    @functools.wraps(fn)
    def wrapper(*a, **k):
        wrapper.calls += 1
        return fn(*a, **k)
    wrapper.calls = 0
    return wrapper


@count_calls
def tick():
    return "tick"


tick(); tick(); tick()
print("call counter  ->", tick.calls)     # 4


def validate_positive(fn):
    """Guard the inputs before running the real work."""
    @functools.wraps(fn)
    def wrapper(*a, **k):
        if any(isinstance(v, (int, float)) and v < 0 for v in a):
            raise ValueError("negative argument in %r" % (a,))
        return fn(*a, **k)
    return wrapper


@validate_positive
def sqrt_ish(n):
    return n ** 0.5


print("valid         ->", sqrt_ish(16))
try:
    sqrt_ish(-4)
except ValueError as e:
    print("invalid       -> ValueError:", e)


def retry(attempts=3):
    """Retry on exception — the classic network-call decorator."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*a, **k):
            for attempt in range(1, attempts + 1):
                try:
                    return fn(*a, **k)
                except Exception as exc:
                    print("  attempt %d failed (%s)" % (attempt, exc))
                    if attempt == attempts:
                        raise
        return wrapper
    return decorator


state = {"fails": 2}


@retry(attempts=3)
def flaky():
    if state["fails"] > 0:
        state["fails"] -= 1
        raise RuntimeError("boom")
    return "succeeded"


print("retry         ->", flaky())


# -------------------------------------------------------------
# 9) BUILT-IN DECORATORS
# -------------------------------------------------------------
print("\n--- 9) BUILT-INS ---")


@functools.lru_cache(maxsize=None)        # memoization, free of charge
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print("fib(60)       ->", fib(60))        # instant thanks to the cache
print("cache info    ->", fib.cache_info())
print("(3.9+ also has @functools.cache — same thing, no maxsize)")


class Circle:
    def __init__(self, r):
        self._r = r

    @property                              # call it like an attribute
    def area(self):
        return round(3.14159 * self._r ** 2, 2)

    @property
    def radius(self):
        return self._r

    @radius.setter                         # controlled assignment
    def radius(self, value):
        if value < 0:
            raise ValueError("radius must be >= 0")
        self._r = value

    @staticmethod                          # no self — just lives in the class
    def unit():
        return "cm"

    @classmethod                           # gets the CLASS, not the instance
    def from_diameter(cls, d):
        return cls(d / 2)


c = Circle(2)
print("@property     ->", c.area, Circle.unit())    # no parentheses on .area
c.radius = 3
print("@setter       ->", c.radius, c.area)
try:
    c.radius = -1
except ValueError as e:
    print("setter guard  -> ValueError:", e)
print("@classmethod  ->", Circle.from_diameter(10).radius)


# -------------------------------------------------------------
# 10) CLASS-BASED DECORATOR  (__call__)
# -------------------------------------------------------------
print("\n--- 10) CLASS DECORATOR ---")


class CountCalls:
    def __init__(self, fn):
        functools.update_wrapper(self, fn)
        self.fn = fn
        self.count = 0

    def __call__(self, *a, **k):           # makes the INSTANCE callable
        self.count += 1
        return "%s (call #%d)" % (self.fn(*a, **k), self.count)


@CountCalls
def hello_class():
    return "hello"


print("class deco    ->", hello_class())
print("class deco    ->", hello_class())
print("state on self ->", hello_class.count)


# -------------------------------------------------------------
# 11) GOTCHAS
# -------------------------------------------------------------
print("\n--- 11) GOTCHAS ---")


def forgot_return(fn):
    def wrapper(*a, **k):
        fn(*a, **k)                        # <- result thrown away!
    return wrapper


@forgot_return
def value():
    return 42


print("no return     ->", value())         # None — the #1 decorator bug

print("decoration is at DEFINITION time, not call time:")


def announce(fn):
    print("  decorating", fn.__name__, "<- printed while defining, not calling")
    return fn


@announce
def later():
    pass


print("=> also remember: @deco (no parens) vs @deco() (factory with parens)")


# -------------------------------------------------------------
# 12) CHEAT SHEET
# -------------------------------------------------------------
#   @deco             ->  fn = deco(fn)
#   def deco(fn):         def wrapper(*a, **k): ...; return wrapper
#   @functools.wraps(fn)  keep __name__ / __doc__
#   3 levels          ->  decorator WITH arguments
#   stacked           ->  bottom applied first, top wraps outermost
#   built-ins         ->  @property @staticmethod @classmethod @lru_cache
print("\n--- 12) DONE ---")
print("beta identity ->", beta.__name__)
print("fib cached    ->", fib.cache_info().hits, "hits")
