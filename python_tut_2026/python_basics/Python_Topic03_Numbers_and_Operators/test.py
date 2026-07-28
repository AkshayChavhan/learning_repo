# =============================================================
# PYTHON NUMBERS & OPERATORS — every type, method and operator
# =============================================================
# Numbers are IMMUTABLE objects too.
# x += 1 does NOT edit x — it builds a new int and rebinds the name.
# =============================================================

import sys
import math
from decimal import Decimal, getcontext
from fractions import Fraction

a = 17          # int
b = 5           # int
f = 3.75        # float
c = 2 + 3j      # complex
flag = True     # bool  (bool IS a subclass of int)

print("a, b, f, c   ->", a, b, f, c)
print("types        ->", type(a), type(f), type(c), type(flag))
print("bool is int  ->", isinstance(True, int), "| True + True =", True + True)  # 2


# -------------------------------------------------------------
# 1) NUMBER LITERALS & CONVERSION
# -------------------------------------------------------------
print("\n--- 1) LITERALS & CONVERSION ---")
print("underscores   ->", 1_000_000)          # readability only
print("binary  0b    ->", 0b1011)             # 11
print("octal   0o    ->", 0o17)               # 15
print("hex     0x    ->", 0xFF)               # 255
print("sci notation  ->", 1.5e3, 2e-3)        # 1500.0  0.002

print("int('42')     ->", int("42"))
print("int('1011',2) ->", int("1011", 2))     # 11 — parse in any base
print("int(3.99)     ->", int(3.99))          # 3 — TRUNCATES toward zero
print("int(-3.99)    ->", int(-3.99))         # -3 — not -4!
print("float('3.5')  ->", float("3.5"))
print("bin/oct/hex   ->", bin(11), oct(15), hex(255))
print("complex(2,3)  ->", complex(2, 3))
print("big int       ->", 2 ** 100)           # ints are UNBOUNDED in Python


# -------------------------------------------------------------
# 2) ARITHMETIC OPERATORS
# -------------------------------------------------------------
print("\n--- 2) ARITHMETIC ---")
print("a + b         ->", a + b)              # 22
print("a - b         ->", a - b)              # 12
print("a * b         ->", a * b)              # 85
print("a / b         ->", a / b)              # 3.4   <- ALWAYS float
print("a // b        ->", a // b)             # 3     <- floor division
print("a % b         ->", a % b)              # 2     <- remainder
print("a ** b        ->", a ** b)             # 1419857
print("divmod(a, b)  ->", divmod(a, b))       # (3, 2) — // and % in one call

# The classic gotcha: // and % FLOOR toward -infinity (not toward zero)
print("-17 // 5      ->", -17 // 5)           # -4  (not -3)
print("-17 % 5       ->", -17 % 5)            # 3   (sign follows the DIVISOR)
print("17 % -5       ->", 17 % -5)            # -3
print("math.fmod     ->", math.fmod(-17, 5))  # -2.0 — C-style, sign follows dividend

print("float // float->", 7.5 // 2)           # 3.0 — float in, float out
print("modulo float  ->", 7.5 % 2)            # 1.5


# -------------------------------------------------------------
# 3) COMPARISON OPERATORS  (all return bool)
# -------------------------------------------------------------
print("\n--- 3) COMPARISON ---")
print("a == b        ->", a == b)             # False
print("a != b        ->", a != b)             # True
print("a >  b        ->", a > b)              # True
print("a <= b        ->", a <= b)             # False
print("chained       ->", 1 < b < 10)         # True — real math-style chaining
print("int == float  ->", 5 == 5.0)           # True — value equality across types
print("True == 1     ->", True == 1)          # True


# -------------------------------------------------------------
# 4) LOGICAL OPERATORS  (return an OPERAND, not always a bool)
# -------------------------------------------------------------
print("\n--- 4) LOGICAL ---")
print("True and False->", True and False)     # False
print("True or False ->", True or False)      # True
print("not True      ->", not True)           # False
print("0 or 'hi'     ->", 0 or "hi")          # 'hi'  <- returns the OPERAND
print("5 and 9       ->", 5 and 9)            # 9     <- last truthy value
print("default trick ->", None or "fallback") # 'fallback'


# Short-circuit: right side never evaluated if left decides the answer
def boom():
    print("   (boom ran!)")
    return True


print("short-circuit and:", False and boom())  # boom() NEVER runs
print("short-circuit or :", True or boom())    # boom() NEVER runs

# Falsy numbers: 0, 0.0, 0j  — everything else is truthy
print("falsy numbers ->", bool(0), bool(0.0), bool(0j), bool(-1), bool(0.0001))


# -------------------------------------------------------------
# 5) ASSIGNMENT OPERATORS
# -------------------------------------------------------------
print("\n--- 5) ASSIGNMENT ---")
n = 10
n += 3
print("n += 3        ->", n)   # 13
n -= 3
print("n -= 3        ->", n)   # 10
n *= 2
print("n *= 2        ->", n)   # 20
n /= 4
print("n /= 4        ->", n)   # 5.0  <- became a FLOAT
n //= 2
print("n //= 2       ->", n)   # 2.0
n **= 3
print("n **= 3       ->", n)   # 8.0
n %= 5
print("n %= 5        ->", n)   # 3.0

x = y = z = 0                            # chained assignment — all point to 0
p, q = 1, 2                              # tuple unpacking
p, q = q, p                              # swap — no temp variable needed
print("chained x,y,z ->", x, y, z)
print("swap p, q     ->", p, q)          # 2 1

# Walrus := assigns INSIDE an expression (Python 3.8+)
if (total := a + b) > 20:
    print("walrus total  ->", total)     # 22


# -------------------------------------------------------------
# 6) BITWISE OPERATORS  (work on the binary bits)
# -------------------------------------------------------------
print("\n--- 6) BITWISE ---")
m, k = 12, 10                            # 1100 and 1010
print("m, k in binary->", bin(m), bin(k))
print("m & k  AND    ->", m & k,  bin(m & k))   # 8  0b1000
print("m | k  OR     ->", m | k,  bin(m | k))   # 14 0b1110
print("m ^ k  XOR    ->", m ^ k,  bin(m ^ k))   # 6  0b110
print("~m     NOT    ->", ~m)                   # -13  (~x == -x-1)
print("m << 2 LSHIFT ->", m << 2)               # 48   (x * 2**2)
print("m >> 2 RSHIFT ->", m >> 2)               # 3    (x // 2**2)

# Common real uses
print("is even?      ->", (a & 1) == 0)         # False — cheapest even test
print("xor cancels   ->", 5 ^ 3 ^ 3)            # 5 — xor is its own inverse


# -------------------------------------------------------------
# 7) IDENTITY & MEMBERSHIP OPERATORS
# -------------------------------------------------------------
print("\n--- 7) IDENTITY & MEMBERSHIP ---")
i1, i2 = 256, 256
j1 = int("257")
j2 = int("257")
print("256 is 256    ->", i1 is i2)             # True  — small ints are CACHED
print("257 is 257    ->", j1 is j2)             # False — outside -5..256 cache
print("257 == 257    ->", j1 == j2)             # True  — ALWAYS compare with ==
print("in a range    ->", 5 in range(10))       # True
print("in a list     ->", 3 in [1, 2, 3])       # True


# -------------------------------------------------------------
# 8) INT METHODS
# -------------------------------------------------------------
print("\n--- 8) int METHODS ---")
print("(255).bit_length()  ->", (255).bit_length())        # 8 bits to hold it
print("(255).to_bytes()    ->", (255).to_bytes(2, "big"))  # b'\x00\xff'
print("int.from_bytes()    ->", int.from_bytes(b"\x00\xff", "big"))  # 255
print("(10).as_integer_ratio() ->", (10).as_integer_ratio())         # (10, 1)
print("(7).numerator/denom ->", (7).numerator, (7).denominator)      # 7 1
print("(7).real / .imag    ->", (7).real, (7).imag)                  # 7 0
print("(7).conjugate()     ->", (7).conjugate())                     # 7

if sys.version_info >= (3, 10):
    print("(255).bit_count()   ->", (255).bit_count())     # 8 set bits
else:
    print("(255).bit_count()   -> needs 3.10+ | 3.8 way:", bin(255).count("1"))


# -------------------------------------------------------------
# 9) FLOAT METHODS
# -------------------------------------------------------------
print("\n--- 9) float METHODS ---")
print("(3.0).is_integer()  ->", (3.0).is_integer())        # True
print("(3.75).is_integer() ->", f.is_integer())            # False
print("(3.75).hex()        ->", f.hex())                   # '0x1.e000000000000p+1'
print("float.fromhex()     ->", float.fromhex("0x1.e000000000000p+1"))   # 3.75
print("(3.75).as_integer_ratio() ->", f.as_integer_ratio())             # (15, 4)
print("(3.75).real/.imag   ->", f.real, f.imag)
print("(3.75).conjugate()  ->", f.conjugate())

# Special float values
print("inf / -inf / nan    ->", math.inf, -math.inf, math.nan)
print("nan == nan          ->", math.nan == math.nan)      # False! always
print("math.isnan()        ->", math.isnan(math.nan))      # True — the right test
print("math.isinf()        ->", math.isinf(math.inf))      # True
print("math.isfinite(1.0)  ->", math.isfinite(1.0))        # True


# -------------------------------------------------------------
# 10) COMPLEX METHODS
# -------------------------------------------------------------
print("\n--- 10) complex ---")
print("c             ->", c)                    # (2+3j)
print("c.real / c.imag ->", c.real, c.imag)     # 2.0 3.0
print("c.conjugate() ->", c.conjugate())        # (2-3j)
print("abs(c)        ->", abs(c))               # 3.605... = magnitude
print("c * c         ->", c * c)                # (-5+12j)


# -------------------------------------------------------------
# 11) BUILT-IN NUMBER FUNCTIONS
# -------------------------------------------------------------
print("\n--- 11) BUILT-INS ---")
print("abs(-7)       ->", abs(-7))
print("round(3.756,2)->", round(3.756, 2))      # 3.76
print("round(3.756)  ->", round(3.756))         # 4  — returns an int
print("pow(2, 10)    ->", pow(2, 10))           # 1024
print("pow(2,10,1000)->", pow(2, 10, 1000))     # 24 — modular pow, fast & huge-safe
print("min / max     ->", min(3, 9, 1), max(3, 9, 1))
print("sum([1,2,3])  ->", sum([1, 2, 3]))
print("sum(start=10) ->", sum([1, 2, 3], 10))   # 16

# BANKER'S ROUNDING — round() breaks .5 ties toward the EVEN number
print("round(0.5)    ->", round(0.5))           # 0  (not 1!)
print("round(1.5)    ->", round(1.5))           # 2
print("round(2.5)    ->", round(2.5))           # 2  (not 3!)


# -------------------------------------------------------------
# 12) math MODULE ESSENTIALS
# -------------------------------------------------------------
print("\n--- 12) math MODULE ---")
print("floor / ceil  ->", math.floor(3.7), math.ceil(3.2))     # 3 4
print("trunc(-3.7)   ->", math.trunc(-3.7))                    # -3 toward zero
print("floor(-3.7)   ->", math.floor(-3.7))                    # -4 toward -inf
print("sqrt(16)      ->", math.sqrt(16))                       # 4.0
print("isqrt(17)     ->", math.isqrt(17))                      # 4 — integer sqrt
print("pow(2,3)      ->", math.pow(2, 3))                      # 8.0 always float
print("fabs(-5)      ->", math.fabs(-5))                       # 5.0
print("gcd(12, 18)   ->", math.gcd(12, 18))                    # 6
print("factorial(5)  ->", math.factorial(5))                   # 120
print("comb(5,2)/perm->", math.comb(5, 2), math.perm(5, 2))    # 10 20
print("prod([1,2,3,4])->", math.prod([1, 2, 3, 4]))            # 24
print("log(8, 2)     ->", math.log(8, 2))                      # 3.0
print("log10 / log2  ->", math.log10(1000), math.log2(8))      # 3.0 3.0
print("exp(1)        ->", math.exp(1))                         # 2.718...
print("pi / e / tau  ->", math.pi, math.e, math.tau)
print("degrees(pi)   ->", math.degrees(math.pi))               # 180.0
print("radians(180)  ->", math.radians(180))                   # 3.14159...
print("sin/cos       ->", round(math.sin(math.pi / 2), 4), round(math.cos(0), 4))
print("hypot(3,4)    ->", math.hypot(3, 4))                    # 5.0
print("dist((0,0),(3,4)) ->", math.dist((0, 0), (3, 4)))       # 5.0

if sys.version_info >= (3, 9):
    print("lcm(4, 6)     ->", math.lcm(4, 6))                  # 12
else:
    print("lcm(4, 6)     -> needs 3.9+ | 3.8 way:", 4 * 6 // math.gcd(4, 6))


# -------------------------------------------------------------
# 13) FLOAT PRECISION — the #1 interview gotcha
# -------------------------------------------------------------
print("\n--- 13) FLOAT PRECISION ---")
print("0.1 + 0.2     ->", 0.1 + 0.2)                    # 0.30000000000000004
print("== 0.3        ->", 0.1 + 0.2 == 0.3)             # False !!
print("math.isclose  ->", math.isclose(0.1 + 0.2, 0.3))  # True — correct way
print("why           ->", format(0.1, ".20f"))          # 0.1 isn't exact in binary

# Fix 1: Decimal — exact decimal arithmetic (money, billing)
print("Decimal sum   ->", Decimal("0.1") + Decimal("0.2"))       # 0.3
print("Decimal == .3 ->", Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
print("float trap    ->", Decimal(0.1))                          # inherits the mess
getcontext().prec = 6
print("Decimal(1)/7  ->", Decimal(1) / Decimal(7))               # 0.142857

# Fix 2: Fraction — exact rational arithmetic
print("Fraction sum  ->", Fraction(1, 3) + Fraction(1, 6))       # 1/2
print("Fraction(0.75)->", Fraction(0.75))                        # 3/4
print("to float      ->", float(Fraction(1, 3)))                 # 0.333...


# -------------------------------------------------------------
# 14) OPERATOR PRECEDENCE  (high -> low)
# -------------------------------------------------------------
#  **   ->  unary - ~  ->  * / // %  ->  + -  ->  << >>  ->  &  ->  ^  ->  |
#  ->  comparisons / is / in  ->  not  ->  and  ->  or
print("\n--- 14) PRECEDENCE ---")
print("2 + 3 * 4     ->", 2 + 3 * 4)            # 14 — * before +
print("(2 + 3) * 4   ->", (2 + 3) * 4)          # 20 — parens win
print("2 ** 3 ** 2   ->", 2 ** 3 ** 2)          # 512 — ** is RIGHT associative
print("(2 ** 3) ** 2 ->", (2 ** 3) ** 2)        # 64
print("-2 ** 2       ->", -2 ** 2)              # -4 — ** binds tighter than unary -
print("(-2) ** 2     ->", (-2) ** 2)            # 4
print("1 + 2 > 2 and 1 ->", 1 + 2 > 2 and 1)    # arithmetic > compare > and


# -------------------------------------------------------------
# 15) FORMATTING NUMBERS FOR OUTPUT
# -------------------------------------------------------------
print("\n--- 15) NUMBER FORMATTING ---")
v = 1234567.8915
print("2 decimals    ->", f"{v:.2f}")           # 1234567.89
print("thousands sep ->", f"{v:,.2f}")          # 1,234,567.89
print("percent       ->", f"{0.8756:.1%}")      # 87.6%
print("padded int    ->", f"{42:05d}")          # 00042
print("aligned       ->", f"|{42:>8}|{42:^8}|{42:<8}|")
print("sci notation  ->", f"{v:.2e}")           # 1.23e+06
print("bin/oct/hex   ->", f"{255:b} {255:o} {255:x} {255:X}")
print("plus sign     ->", f"{42:+d} {-42:+d}")  # +42 -42


# -------------------------------------------------------------
# 16) IMMUTABILITY PROOF
# -------------------------------------------------------------
print("\n--- 16) IMMUTABLE ---")
orig = 10
copy_of = orig
orig += 5
print("orig / copy_of->", orig, copy_of)        # 15 10 — copy_of untouched
print("a still       ->", a)                    # 17 — nothing above changed it
