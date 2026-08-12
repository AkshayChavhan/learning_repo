"""
tut00.3 — Basic types & literals.

Run from the repo root:
    python3 "python_tut_2026/python_basics/00c_basic_types.py"

Built-in types you'll use constantly: int, float, bool, str, None.
Predict each output before running.
"""

# ─────────────────────────────────────────────────────────────
# 1. int — arbitrary precision. No 32/64-bit limit.
# ─────────────────────────────────────────────────────────────
print("─── 1. int ───")
big = 2 ** 200
print("2**200 has", len(str(big)), "digits")
print("starts with:", str(big)[:20], "...")

# Bases
print("hex 0xff       =", 0xff)        # 255
print("octal 0o377    =", 0o377)       # 255
print("binary 0b1111  =", 0b1111)      # 15
print("with underscores: 1_000_000 =", 1_000_000)


# ─────────────────────────────────────────────────────────────
# 2. float — IEEE-754, with all the usual gotchas.
# ─────────────────────────────────────────────────────────────
print("\n─── 2. float ───")
print("0.1 + 0.2       =", 0.1 + 0.2)             # 0.30000000000000004
print("0.1 + 0.2 == 0.3?", 0.1 + 0.2 == 0.3)      # False

import math
print("isclose check  :", math.isclose(0.1 + 0.2, 0.3))  # True

inf = float("inf")
nan = float("nan")
print("inf > 10**100  :", inf > 10**100)          # True
print("nan == nan     :", nan == nan)             # False — yes really
print("math.isnan(nan):", math.isnan(nan))        # True


# ─────────────────────────────────────────────────────────────
# 3. Division: / is true division, // is floor, % is modulo.
# ─────────────────────────────────────────────────────────────
print("\n─── 3. Division operators ───")
print("7 / 2  =", 7 / 2)      # 3.5    (always float)
print("7 // 2 =", 7 // 2)     # 3
print("7 % 2  =", 7 % 2)      # 1
print("2 ** 10=", 2 ** 10)    # 1024

# Floor rounds toward negative infinity, not toward zero:
print("-7 // 2 =", -7 // 2)   # -4 (not -3)


# ─────────────────────────────────────────────────────────────
# 4. bool is a subtype of int. True == 1, False == 0.
# ─────────────────────────────────────────────────────────────
print("\n─── 4. bool is int ───")
print("True + True       =", True + True)             # 2
print("isinstance(True, int):", isinstance(True, int))  # True
print("sum([T,F,T,T,F])  =", sum([True, False, True, True, False]))  # 3


# ─────────────────────────────────────────────────────────────
# 5. Truthiness — what counts as "falsy".
# ─────────────────────────────────────────────────────────────
print("\n─── 5. Truthiness ───")
falsy_values = [False, None, 0, 0.0, "", [], {}, (), set()]
for v in falsy_values:
    print(f"  bool({v!r:>8}) = {bool(v)}")

# Common surprise: "False" the string is truthy
print('  bool("False") =', bool("False"))     # True
print('  bool([0])     =', bool([0]))         # True — list has one item


# ─────────────────────────────────────────────────────────────
# 6. None — the one and only sentinel.
# ─────────────────────────────────────────────────────────────
print("\n─── 6. None ───")
def no_return():
    pass            # implicit return None

result = no_return()
print("result is None:", result is None)      # True
print("type(None)    :", type(None).__name__) # NoneType

# Idiom: check None with `is`, not `==`
x = None
# Correct:
if x is None:
    print("x is None — using `is`")


# ─────────────────────────────────────────────────────────────
# 7. Type conversions — constructors are the type names.
# ─────────────────────────────────────────────────────────────
print("\n─── 7. Conversions ───")
print('int("42")     =', int("42"))
print('int("ff", 16) =', int("ff", 16))    # 255 — parse hex string
print("int(3.9)      =", int(3.9))         # 3 — truncates, doesn't round
print("int(-3.9)     =", int(-3.9))        # -3 — truncates toward zero
print("round(3.5)    =", round(3.5))       # 4 — banker's rounding (to even)
print("round(2.5)    =", round(2.5))       # 2 — also banker's rounding!
print('float("3.14") =', float("3.14"))
print("str(42)       =", str(42))
print('list("abc")   =', list("abc"))


# ─────────────────────────────────────────────────────────────
# 8. type() vs isinstance() — when each one is right.
# ─────────────────────────────────────────────────────────────
print("\n─── 8. type() vs isinstance() ───")
print("type(True) is int       :", type(True) is int)        # False (it's bool)
print("isinstance(True, int)    :", isinstance(True, int))    # True

# Test against multiple types in one call
def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)

print("is_number(5)    :", is_number(5))      # True
print("is_number(3.14) :", is_number(3.14))   # True
print("is_number(True) :", is_number(True))   # False — we exclude bool
print("is_number('5')  :", is_number("5"))    # False


# ─────────────────────────────────────────────────────────────
# 9. Conversion failures — what error do you get?
# ─────────────────────────────────────────────────────────────
print("\n─── 9. Common conversion errors ───")
for src in ["42", "3.9", "hello", ""]:
    try:
        print(f"int({src!r}) = {int(src)}")
    except ValueError as e:
        print(f"int({src!r}) → ValueError: {e}")


# ─────────────────────────────────────────────────────────────
# 10. Quick reference of useful conversions
# ─────────────────────────────────────────────────────────────
print("\n─── 10. bool(value) quick reference ───")
samples = [0, 1, -1, 0.0, "", "x", [], [0], None, {}]
for s in samples:
    print(f"  bool({s!r:>6}) = {bool(s)}")
