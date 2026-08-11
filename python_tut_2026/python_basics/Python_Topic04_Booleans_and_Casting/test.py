# =============================================================
# PYTHON BOOLEANS & CASTING (type conversion)
# =============================================================
# bool has exactly TWO values: True / False  (capital first letter)
# Casting = turning one type into another: int() float() str() bool() ...
# =============================================================

t = True
f = False
print("t, f          ->", t, f)
print("type          ->", type(t))
print("bool IS an int->", isinstance(t, int), "| int(True):", int(True))


# -------------------------------------------------------------
# 1) WHERE BOOLEANS COME FROM
# -------------------------------------------------------------
print("\n--- 1) BOOLEAN SOURCES ---")
print("comparison    ->", 10 > 9)              # True
print("equality      ->", 10 == 9)             # False
print("membership    ->", "a" in "abc")        # True
print("identity      ->", None is None)        # True
print("isinstance    ->", isinstance(5, int))  # True
print("bool() call   ->", bool("hello"))       # True


# -------------------------------------------------------------
# 2) TRUTHY vs FALSY — what counts as False
# -------------------------------------------------------------
print("\n--- 2) TRUTHY / FALSY ---")
# THE COMPLETE FALSY LIST — everything else on earth is truthy:
#   False   None   0   0.0   0j   ""   []   ()   {}   set()   range(0)
falsy = [False, None, 0, 0.0, 0j, "", [], (), {}, set(), range(0)]
for item in falsy:
    print("  falsy ->", repr(item), "=>", bool(item))

truthy = [True, 1, -1, 0.1, "0", "False", [0], (0,), {"k": 0}, {0}, " "]
print("truthy check  ->", [bool(x) for x in truthy])   # all True

print('bool("False") ->', bool("False"))   # True! any non-empty string is truthy
print("bool('0')     ->", bool("0"))       # True! it's a non-empty string
print("bool([0])     ->", bool([0]))       # True! the list is not empty
print("bool(-1)      ->", bool(-1))        # True! only 0 is falsy


# -------------------------------------------------------------
# 3) USING TRUTHINESS IN CODE
# -------------------------------------------------------------
print("\n--- 3) TRUTHINESS IN USE ---")
name = ""
if not name:
    print("empty check   -> name is empty")     # pythonic; beats len(name) == 0

items = [1, 2]
print("pythonic if   ->", "has items" if items else "empty")

# CAREFUL: `if x:` and `if x is not None:` are NOT the same
value = 0
print("if value      ->", bool(value))              # False — 0 is falsy
print("is not None   ->", value is not None)        # True  — it EXISTS
# Use `is not None` when 0 / "" / [] are legitimate values


# -------------------------------------------------------------
# 4) BOOLEAN OPERATORS
# -------------------------------------------------------------
print("\n--- 4) OPERATORS ---")
print("and           ->", True and False)      # False — both must be True
print("or            ->", True or False)       # True  — at least one True
print("not           ->", not True)            # False — flips it

# and/or return an OPERAND, not necessarily a bool
print("'a' and 'b'   ->", "a" and "b")         # 'b' — last truthy
print("'' or 'x'     ->", "" or "x")           # 'x' — first truthy
print("0 and crash   ->", 0 and 1 / 0)         # 0 — short-circuits, no ZeroDivision

# any() / all() — booleans over a whole collection
print("any([0,0,1])  ->", any([0, 0, 1]))      # True  — at least one truthy
print("all([1,2,3])  ->", all([1, 2, 3]))      # True  — every item truthy
print("any([])       ->", any([]))             # False — empty has nothing true
print("all([])       ->", all([]))             # True! — vacuous truth, remember it


# -------------------------------------------------------------
# 5) BOOLEANS ARE INTEGERS (True == 1, False == 0)
# -------------------------------------------------------------
print("\n--- 5) BOOL AS INT ---")
print("True + True   ->", True + True)                 # 2
print("sum of bools  ->", sum([True, False, True]))    # 2 — counts the Trues
scores = [45, 82, 91, 30, 77]
print("count passing ->", sum(s >= 50 for s in scores))  # 3 — idiomatic counting
print("True == 1     ->", True == 1, "| False == 0:", False == 0)
one = int("1")                                         # dodge the literal-cache
print("True is 1     ->", True is one)                 # False — different objects
print("index with bool->", ["zero", "one"][True])      # 'one'


# =============================================================
# 6) CASTING — EXPLICIT TYPE CONVERSION
# =============================================================
print("\n--- 6) CASTING TO NUMBER ---")
print("int('42')     ->", int("42"))
print("int(3.99)     ->", int(3.99))            # 3 — truncates, never rounds
print("int(-3.99)    ->", int(-3.99))           # -3 — toward zero
print("int(True)     ->", int(True))            # 1
print("int('1010',2) ->", int("1010", 2))       # 10 — from binary
print("int(' 42 ')   ->", int(" 42 "))          # 42 — whitespace is stripped
print("float('3.5')  ->", float("3.5"))
print("float(7)      ->", float(7))             # 7.0
print("float('inf')  ->", float("inf"))
print("complex(2,3)  ->", complex(2, 3))
print("round vs int  ->", round(3.7), int(3.7))  # 4 vs 3


# -------------------------------------------------------------
# 7) CASTING ERRORS — and how to survive them
# -------------------------------------------------------------
print("\n--- 7) CASTING ERRORS ---")
for bad in ["abc", "3.5", "", "12a"]:
    try:
        int(bad)
    except ValueError as e:
        print("  int(%-6r) -> ValueError: %s" % (bad, e))

print("fix for '3.5' ->", int(float("3.5")))    # 3 — go via float first


def safe_int(text, default=0):
    """Convert if possible, otherwise fall back."""
    try:
        return int(text)
    except (ValueError, TypeError):
        return default


print("safe_int('42')->", safe_int("42"))
print("safe_int('ab')->", safe_int("ab"))       # 0
print("safe_int(None)->", safe_int(None))       # 0
print("isdigit guard ->", "42".isdigit(), "| '-42'.isdigit():", "-42".isdigit())


# -------------------------------------------------------------
# 8) CASTING TO STRING
# -------------------------------------------------------------
print("\n--- 8) CASTING TO str ---")
print("str(42)       ->", repr(str(42)))
print("str(3.5)      ->", repr(str(3.5)))
print("str(True)     ->", repr(str(True)))
print("str([1,2])    ->", repr(str([1, 2])))       # '[1, 2]'
print("str(None)     ->", repr(str(None)))         # 'None'
print("f-string      ->", f"Age: {29}")            # preferred everywhere
print("str vs repr   ->", str("hi"), repr("hi"))   # hi   'hi'
print("concat needs  ->", "Age: " + str(29))       # "Age: " + 29 -> TypeError


# -------------------------------------------------------------
# 9) CASTING TO bool
# -------------------------------------------------------------
print("\n--- 9) CASTING TO bool ---")
print("bool(1)/bool(0)->", bool(1), bool(0))
print("bool('')/bool('a')->", bool(""), bool("a"))
print("bool([])/bool([0])->", bool([]), bool([0]))
print("bool(None)    ->", bool(None))


def to_bool(text):
    """Real-world string -> bool (env vars, config files, CSV)."""
    return str(text).strip().lower() in {"true", "1", "yes", "y", "on"}


print("to_bool('Yes')->", to_bool("Yes"), "| to_bool('no'):", to_bool("no"))
print("naive trap    ->", bool("False"))     # True — why to_bool() exists


# -------------------------------------------------------------
# 10) CASTING BETWEEN COLLECTIONS
# -------------------------------------------------------------
print("\n--- 10) COLLECTION CASTS ---")
print("list('abc')   ->", list("abc"))
print("tuple([1,2])  ->", tuple([1, 2]))
print("set([1,1,2])  ->", set([1, 1, 2]))          # dedupes
print("list(set(..)) ->", list(set([3, 1, 3, 2])))  # dedupe, order NOT kept
print("dict(pairs)   ->", dict([("a", 1), ("b", 2)]))
print("dict(zip(..)) ->", dict(zip("ab", [1, 2])))
print("list(dict)    ->", list({"a": 1, "b": 2}))          # keys only
print("list(d.items())->", list({"a": 1}.items()))
print("str -> list -> str ->", "".join(list("abc")))
print("sorted() cast ->", sorted({3, 1, 2}))       # set -> sorted list


# -------------------------------------------------------------
# 11) CHARACTER & BYTE CASTS
# -------------------------------------------------------------
print("\n--- 11) chr / ord / bytes ---")
print("ord('A')      ->", ord("A"))                # 65
print("chr(65)       ->", chr(65))                 # 'A'
print("A-Z           ->", [chr(n) for n in range(65, 70)])
print("str -> bytes  ->", "hi".encode("utf-8"))
print("bytes -> str  ->", b"hi".decode("utf-8"))
print("bytes(list)   ->", bytes([104, 105]))       # b'hi'
print("list(bytes)   ->", list(b"hi"))             # [104, 105]


# -------------------------------------------------------------
# 12) IMPLICIT CONVERSION (Python does it for you)
# -------------------------------------------------------------
print("\n--- 12) IMPLICIT ---")
print("int + float   ->", 5 + 2.5, type(5 + 2.5))     # int promoted to float
print("bool + int    ->", True + 10)                  # 11
print("int + complex ->", 1 + 2j + 1)                 # promoted to complex
# print("str" + 1)  ->  TypeError: Python NEVER guesses across str/number
print("no str+int    -> TypeError (must cast explicitly)")
print("but str * int ->", "ab" * 3)                   # this one IS allowed


# -------------------------------------------------------------
# 13) CHECKING TYPES
# -------------------------------------------------------------
print("\n--- 13) TYPE CHECKS ---")
v = 42
print("type(v)       ->", type(v))
print("type(v) is int->", type(v) is int)
print("isinstance    ->", isinstance(v, int))          # preferred
print("isinstance tup->", isinstance(v, (int, float)))  # any of these
print("bool trap     ->", isinstance(True, int))       # True — bool subclasses int
print("strict int    ->", type(True) is int)           # False — use this if strict


# -------------------------------------------------------------
# 14) QUICK REFERENCE
# -------------------------------------------------------------
#   int(x)     -> integer   (truncates floats, parses digit strings)
#   float(x)   -> float
#   str(x)     -> string    (works on literally everything)
#   bool(x)    -> True/False (falsy list in section 2)
#   list/tuple/set(x) -> collections (x must be iterable)
#   dict(x)    -> from pairs or zip
#   chr/ord    -> char <-> code point
#   .encode()/.decode() -> str <-> bytes
print("\n--- 14) DONE ---")
print("bool is the only type with exactly 2 values:", [True, False])
