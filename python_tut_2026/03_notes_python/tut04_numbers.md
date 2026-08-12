# Python Numbers

Python has three numeric types: `int`, `float`, and `complex`.
The first two are the ones you'll use every day.

| Type      | Example       | What it is                       |
|-----------|---------------|----------------------------------|
| `int`     | `42`, `-7`    | Whole number, no size limit      |
| `float`   | `3.14`, `1e6` | Decimal number (64-bit double)   |
| `complex` | `2 + 3j`      | Complex number (rarely used)     |

---

## `int` — whole numbers

No upper limit on size.
Python grows the integer as needed.

```python
a = 42
b = -7
big = 2 ** 200

print(big)
```

Underscores make big numbers readable:

```python
salary = 1_500_000
print(salary)   # 1500000
```

Other number bases:

```python
print(0xff)    # 255  — hex
print(0o377)   # 255  — octal
print(0b1111)  # 15   — binary
```

---

## `float` — decimal numbers

Same precision as `double` in Java or C.
Roughly 15–17 significant digits.

```python
pi = 3.14
small = 1.5e-3   # 0.0015
big = 2.5e6      # 2500000.0
```

Special values:

```python
print(float("inf"))     # infinity
print(float("-inf"))    # negative infinity
print(float("nan"))     # not a number
```

`nan` never equals anything — not even itself:

```python
nan = float("nan")
print(nan == nan)   # False
```

Use `math.isnan` to test for it:

```python
import math
print(math.isnan(nan))   # True
```

---

## Arithmetic operators

```python
print(7 + 2)    # 9
print(7 - 2)    # 5
print(7 * 2)    # 14
print(7 / 2)    # 3.5   — true division, always float
print(7 // 2)   # 3     — floor division
print(7 % 2)    # 1     — modulo (remainder)
print(7 ** 2)   # 49    — power
```

### Two kinds of division

`/` always gives a float, even when both numbers are ints:

```python
print(10 / 2)   # 5.0   — not 5
```

`//` rounds **toward negative infinity**, not toward zero:

```python
print( 7 // 2)   #  3
print(-7 // 2)   # -4   — not -3
```

---

## Mixing int and float

If any operand is a float, the result is a float.

```python
print(2 + 3)      # 5
print(2 + 3.0)    # 5.0
print(2 * 0.5)    # 1.0
```

---

## The floating-point trap

Float math is **not always exact**.
This is a property of IEEE-754, not a Python bug.

```python
print(0.1 + 0.2)            # 0.30000000000000004
print(0.1 + 0.2 == 0.3)     # False
```

Compare floats safely with `math.isclose`:

```python
import math
print(math.isclose(0.1 + 0.2, 0.3))   # True
```

For money or exact decimal math, use `decimal`:

```python
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))   # 0.3
```

---

## Common conversions

The type name is the constructor.

```python
print(int("42"))       # 42
print(int(3.9))        # 3   — TRUNCATES, doesn't round
print(int(-3.9))       # -3  — truncates toward zero
print(float("3.14"))   # 3.14
print(float(5))        # 5.0
print(str(42))         # '42'
```

`int()` won't parse a string with a decimal point:

```python
# int("3.9")   # ValueError
print(int(float("3.9")))   # 3
```

---

## Rounding

`round()` uses **banker's rounding** (half-to-even).
This surprises most people.

```python
print(round(2.5))    # 2   — rounds to even
print(round(3.5))    # 4   — rounds to even
print(round(2.6))    # 3
print(round(2.4))    # 2
```

Round to a number of decimal places:

```python
print(round(3.14159, 2))   # 3.14
print(round(3.14159, 4))   # 3.1416
```

For traditional "always round half up", use the `decimal` module:

```python
from decimal import Decimal, ROUND_HALF_UP
print(Decimal("2.5").quantize(Decimal("1"), rounding=ROUND_HALF_UP))   # 3
```

---

## Useful number functions

```python
print(abs(-7))         # 7
print(min(3, 5, 1))    # 1
print(max(3, 5, 1))    # 5
print(sum([1, 2, 3]))  # 6
print(pow(2, 10))      # 1024
print(divmod(17, 5))   # (3, 2)  — quotient and remainder
```

---

## The `math` module

Standard library — has the math you'd expect.

```python
import math

print(math.pi)         # 3.141592653589793
print(math.sqrt(16))   # 4.0
print(math.floor(3.7)) # 3
print(math.ceil(3.2))  # 4
print(math.log(100, 10))   # 2.0
print(math.sin(math.pi / 2))  # 1.0
```

---

## Random numbers

```python
import random

print(random.random())          # 0.0 to 1.0 (float)
print(random.randint(1, 10))    # 1 to 10 (int, both ends included)
print(random.choice([1, 2, 3])) # random item from a list
```

For reproducible results, seed the generator:

```python
random.seed(42)
print(random.random())   # always the same value with seed 42
```

---

## Quick reference

```text
+    addition
-    subtraction
*    multiplication
/    true division   (always float)
//   floor division  (rounds toward -inf)
%    modulo (remainder)
**   power
```

```text
abs(x)        absolute value
round(x, n)   round (banker's rounding)
min(a, b, …)  smallest
max(a, b, …)  largest
sum(seq)      add up a list/tuple
divmod(a, b)  (a // b, a % b)
```
