# JavaScript — Numbers & Math

JS has **one** number type — IEEE-754 64-bit floats — used for both `42` and `3.14`.
For huge whole numbers there's a separate `BigInt` type.

```text
                  ┌──────────────────────────┐
                  │        NUMBERS           │
                  │  one 64-bit float type   │
                  │   (int + float merged)   │
                  └──────────────────────────┘
                            │
        ┌───────────┬───────┴───────┬──────────────┐
        ▼           ▼               ▼              ▼
     LITERALS    SPECIAL         CONVERT         MATH
   42  3.14      NaN             Number(s)       Math.round
   0xff 0b10     Infinity        parseInt(s,10)  Math.random
   1_000_000     -Infinity       +s   String(n)  Math.PI
                            │
                            ▼
                        BigInt    1n   BigInt(10)
                        (precise huge ints, no mixing)
```

---

## One number type ★

There is **no** `int` vs `float`. `42` and `3.14` are both `'number'`.

```js
typeof 42        // 'number'
typeof 3.14      // 'number'
typeof -0        // 'number'
42 === 42.0      // true
```

| Value | `typeof` |
|-------|----------|
| `42` | `'number'` |
| `3.14` | `'number'` |
| `NaN` | `'number'` |
| `Infinity` | `'number'` |
| `1n` | `'bigint'` |

---

## Numeric literals

| Form | Example | Value |
|------|---------|-------|
| decimal | `42` | 42 |
| float | `3.14` | 3.14 |
| underscore separator | `1_000_000` | 1000000 |
| hex | `0xff` | 255 |
| binary | `0b1010` | 10 |
| octal | `0o17` | 15 |
| scientific | `1.5e3` | 1500 |
| scientific (neg exp) | `2e-3` | 0.002 |

```js
1_000_000        // 1000000     — `_` is for readability, ignored
0xff             // 255         — hex
0b1010           // 10          — binary
0o17             // 15          — octal (modern syntax)
1.5e3            // 1500
2e-3             // 0.002
```

> Underscores are visual only. `1_000` is identical to `1000`.

---

## Floating-point gotcha ★

Numbers are IEEE-754 64-bit. Many decimals **cannot be represented exactly**.

```js
0.1 + 0.2                  // 0.30000000000000004
0.1 + 0.2 === 0.3          // false
```

Compare with a **tolerance** instead of `===`:

```js
const eq = (a, b) => Math.abs(a - b) < Number.EPSILON;
eq(0.1 + 0.2, 0.3)         // true
```

| Constant | Meaning |
|----------|---------|
| `Number.EPSILON` | smallest gap between 1 and the next float (~2.22e-16) |
| `Number.MAX_VALUE` | largest finite double |
| `Number.MIN_VALUE` | smallest positive non-zero double |

> Never use floats for **money**. Use cents as integers, or a decimal library.

---

## Integer safety ★

Only integers up to `2^53 - 1` are exact.

```js
Number.MAX_SAFE_INTEGER    // 9007199254740991   (2^53 - 1)
Number.MIN_SAFE_INTEGER    // -9007199254740991

Number.isSafeInteger(2 ** 53 - 1)  // true
Number.isSafeInteger(2 ** 53)      // false   ← beyond safe

2 ** 53 === 2 ** 53 + 1            // true (!) — precision lost
```

Beyond `MAX_SAFE_INTEGER`, consecutive integers **collapse** onto the same float.
Use `BigInt` for IDs, timestamps in nanoseconds, big counters.

---

## BigInt

Arbitrary-precision integers — suffix `n` or `BigInt(...)`.

```js
1n                       // BigInt literal
BigInt(10)               // 10n
typeof 1n                // 'bigint'

2n ** 64n                // 18446744073709551616n   — exact!
```

**You cannot mix BigInt with Number:**

```js
try {
  1n + 1;                // TypeError: Cannot mix BigInt and other types
} catch (e) {
  console.log(e.message);
}

1n + BigInt(1)           // 2n     ← convert first
Number(1n) + 1           // 2      ← or downcast (may lose precision)
```

| | Number | BigInt |
|---|--------|--------|
| precision | 53-bit ints | arbitrary |
| decimals | ✅ | ❌ ints only |
| `Math.*` | ✅ | ❌ |
| mix with each other | — | ❌ throws |

---

## `NaN` — Not a Number ★

`NaN` represents "invalid number result". It **is** a number.

```js
typeof NaN          // 'number'
0 / 0               // NaN
Number("abc")       // NaN
Math.sqrt(-1)       // NaN

NaN === NaN         // false   ← the famous gotcha
NaN !== NaN         // true
```

`NaN` is the **only** value not equal to itself. So to test for it:

```js
Number.isNaN(NaN)       // true     ← strict: only true NaN
Number.isNaN("abc")     // false    ← does NOT coerce

isNaN("abc")            // true     ← global isNaN COERCES first (bug-prone)
isNaN("abc") // → isNaN(Number("abc")) → isNaN(NaN) → true
```

> Use `Number.isNaN(x)` (strict). Avoid global `isNaN`.

---

## `Infinity` & `-Infinity`

Produced by overflow or divide-by-zero.

```js
1 / 0               //  Infinity
-1 / 0              // -Infinity
Math.pow(2, 1024)   //  Infinity   — overflows double

typeof Infinity     // 'number'

Number.isFinite(Infinity)   // false
Number.isFinite(42)         // true
Number.isFinite("42")       // false   ← strict, no coercion
isFinite("42")              // true    ← global coerces (avoid)
```

---

## String → number

| Way | `"42"` | `"42px"` | `"3.14"` | `""` | `"abc"` |
|-----|--------|----------|----------|------|---------|
| `Number(s)` | 42 | **NaN** | 3.14 | **0** | NaN |
| `parseInt(s, 10)` | 42 | **42** | 3 | NaN | NaN |
| `parseFloat(s)` | 42 | 42 | 3.14 | NaN | NaN |
| `+s` (unary) | 42 | NaN | 3.14 | 0 | NaN |

```js
Number("42")           // 42
Number("42px")         // NaN     — strict, all-or-nothing
Number("")             // 0       — surprising
Number(null)           // 0
Number(undefined)      // NaN
Number(true)           // 1

parseInt("42px", 10)   // 42      — lenient, reads digits then stops
parseInt("0.5", 10)    // 0       — int parser, stops at '.'
parseInt("08")         // 8       — but ALWAYS pass radix
parseFloat("3.14abc")  // 3.14

+"42"                  // 42      — concise idiom
+""                    // 0
+"abc"                 // NaN
```

### Always pass the radix to `parseInt` ★

`parseInt(string, radix)` takes a **second argument** — the **radix** (the number base to
parse in). `10` = normal decimal, `16` = hex, `2` = binary, `8` = octal.

```js
parseInt("10", 10)   // 10   — base 10 (decimal)
parseInt("10", 2)    // 2    — base 2  (binary  → 1×2 + 0 = 2)
parseInt("10", 16)   // 16   — base 16 (hex)
parseInt("ff", 16)   // 255  — hex
```

**Why always pass `10`:** if you omit the radix, JavaScript **guesses** the base from the
string's shape — and the guess can be wrong, giving silent bugs:

```js
parseInt("0x1f")     // 31   — saw "0x", guessed HEX (not what you wanted!)
parseInt("08")       // 8    — modern engines → 10; OLD engines guessed OCTAL → 0 😱
parseInt("08", 10)   // 8    — explicit base 10 → always correct, every engine
```

```text
   parseInt("08")            ← no radix → engine GUESSES → historically buggy
   parseInt("08", 10)        ← radix 10 → unambiguous → always 8  ✅
```

> **Rule: always write `parseInt(str, 10)`.** It removes the guessing, behaves identically
> on every engine, and many linters (ESLint `radix`) flag the missing argument.

---

## Number → string

```js
String(42)             // '42'
(42).toString()        // '42'
(255).toString(16)     // 'ff'        — hex
(10).toString(2)       // '1010'      — binary
(3.14159).toFixed(2)   // '3.14'      — RETURNS A STRING

`value: ${42}`         // 'value: 42' — template literal
"" + 42                // '42'        — concat trick
```

---

## Number instance methods

All of these **return strings**.

| Method | Example | Result |
|--------|---------|--------|
| `toFixed(n)` | `(3.14159).toFixed(2)` | `'3.14'` |
| `toPrecision(n)` | `(3.14159).toPrecision(3)` | `'3.14'` |
| `toString(radix)` | `(255).toString(16)` | `'ff'` |
| `toExponential(n)` | `(12345).toExponential(2)` | `'1.23e+4'` |

```js
(3.14159).toFixed(2)        // '3.14'   ← string!
typeof (3.14159).toFixed(2) // 'string'

+(3.14159).toFixed(2)       // 3.14     ← convert back with +
```

> Need a number? Wrap with `Number(...)` or unary `+`.

---

## `Number.*` static methods

**Coercing** = auto-converts the input to a number first, then checks (can mislead).
**Non-coercing** = does NOT convert; a wrong type just returns `false` (safe, predictable).

These `Number.*` methods are the modern **non-coercing** versions of the globals:

```js
isNaN("abc")          // true    ← coerces "abc" → NaN first, then checks (misleading)
Number.isNaN("abc")   // false   ← no conversion: "abc" isn't the NaN value

isFinite("42")        // true    ← coerces "42" → 42 first
Number.isFinite("42") // false   ← no conversion: "42" is a string, not a number
```

| Method | Use |
|--------|-----|
| `Number.isInteger(x)` | exact integer? |
| `Number.isFinite(x)` | finite number? (strict, no coerce) |
| `Number.isNaN(x)` | exactly `NaN`? (strict) |
| `Number.isSafeInteger(x)` | safe within 2^53? |
| `Number.parseInt(s, 10)` | same as global `parseInt` |
| `Number.parseFloat(s)` | same as global `parseFloat` |

```js
Number.isInteger(3)        // true
Number.isInteger(3.0)      // true   ← 3 and 3.0 are the same value
Number.isInteger(3.14)     // false
Number.isInteger("3")      // false  ← no coercion

Number.isFinite("42")      // false  vs  isFinite("42") → true
Number.isNaN("abc")        // false  vs  isNaN("abc")   → true
```

> Prefer `Number.isX` over the global `isX` — no surprise coercion.

---

## The `Math` object

A namespace of math functions and constants. **Not** a constructor — no `new Math`.

| Method | Does |
|--------|------|
| `Math.round(x)` | round half toward +∞ |
| `Math.floor(x)` | round toward -∞ |
| `Math.ceil(x)` | round toward +∞ |
| `Math.trunc(x)` | drop decimal (toward 0) |
| `Math.abs(x)` | absolute value |
| `Math.sign(x)` | -1, 0, or 1 |
| `Math.min(a, b, …)` | smallest |
| `Math.max(a, b, …)` | largest |
| `Math.pow(b, e)` | same as `b ** e` |
| `Math.sqrt(x)` | square root |
| `Math.cbrt(x)` | cube root |
| `Math.log(x)` | natural log |
| `Math.log2(x)` / `log10(x)` | other bases |
| `Math.exp(x)` | `e^x` |
| `Math.sin/cos/tan(x)` | trig (radians) |
| `Math.PI` | 3.141592… |
| `Math.E` | 2.718281… |

```js
Math.max(1, 5, 2)          // 5
Math.min(...[3, 1, 4])     // 1   ← spread an array
Math.abs(-7)               // 7
Math.sign(-7)              // -1
Math.sqrt(16)              // 4
Math.PI                    // 3.141592653589793
```

---

## `Math.random()` ★

Returns a float in `[0, 1)` — includes 0, excludes 1.

```js
Math.random()              // e.g. 0.7239...
```

**Random integer in `[min, max]` (inclusive both ends):**

```js
const randInt = (min, max) =>
  Math.floor(Math.random() * (max - min + 1)) + min;

// randInt(1, 6)   →  1, 2, 3, 4, 5, or 6
```

How it works:

```text
Math.random()              → [0, 1)
* (max - min + 1)          → [0, max-min+1)
Math.floor(...)            → int in {0, 1, …, max-min}
+ min                      → int in {min, …, max}
```

> `Math.random` is **not** cryptographically secure. For crypto use
> `crypto.getRandomValues` (browser) / `node:crypto`.

---

## Rounding differences ★

These four methods all "round" but behave differently — especially on negatives.

| `x` | `Math.round` | `Math.floor` | `Math.ceil` | `Math.trunc` |
|-----|--------------|--------------|-------------|--------------|
| `2.3` | 2 | 2 | 3 | 2 |
| `2.5` | **3** | 2 | 3 | 2 |
| `-2.3` | -2 | -3 | -2 | -2 |
| `-2.5` | **-2** | -3 | -2 | -2 |

```js
Math.round(2.5)    //  3   (half → toward +∞)
Math.round(-2.5)   // -2   (NOT -3 — same rule, +∞)
Math.floor(-2.5)   // -3   (toward -∞)
Math.ceil(-2.5)    // -2   (toward +∞)
Math.trunc(-2.5)   // -2   (drop decimal, toward 0)
```

> Mental model: `round` is **half-up-to-positive-infinity**.
> `floor` ≠ `trunc` for negatives.

---

## Bitwise quirks ★

Bitwise ops (`& | ^ ~ << >> >>>`) coerce to **32-bit signed int**.

```js
3.7  | 0           // 3        — | 0 truncates
~~3.7              // 3        — double bitwise-NOT, same trick
~~(-3.7)           // -3       — truncates toward 0 (like Math.trunc)

5 & 3              // 1        (0b101 & 0b011)
5 | 2              // 7
5 ^ 1              // 4
1 << 3             // 8        (1 * 2^3)
8 >> 1             // 4
-1 >>> 0           // 4294967295   — unsigned shift exposes 32-bit
```

> Don't use bitwise tricks on numbers bigger than `2^31 - 1` — they overflow into 32-bit.

---

## Pitfalls ★

| Pitfall | Demo | Why |
|---------|------|-----|
| Float precision | `0.1 + 0.2 === 0.30000000000000004` | IEEE-754 binary fractions |
| `NaN !== NaN` | `NaN === NaN // false` | NaN is "any invalid"; not one value |
| Global `isNaN` coerces | `isNaN("abc") // true` | coerces, then checks — use `Number.isNaN` |
| `parseInt` w/o radix | `parseInt("08")` ambiguous historically | always pass `10` |
| `parseInt("0.5") → 0` | int parser stops at `.` | use `parseFloat` or `Number` |
| `Number("")` is `0` | not `NaN`! | empty string coerces to 0 |
| `Number(null)` is `0` | but `Number(undefined)` is `NaN` | asymmetric |
| Beyond `MAX_SAFE_INTEGER` | `2**53 === 2**53 + 1` | use `BigInt` |
| Mix BigInt + Number | `1n + 1 // TypeError` | convert explicitly |
| `toFixed` returns string | `(1.5).toFixed(2) === "1.50"` | wrap with `+` or `Number` |
| `Math.round(-2.5)` | `-2`, not `-3` | half-to-+∞ rule |
| Floats for money | `0.1 + 0.2 ≠ 0.3` | use integer cents or decimal lib |

---

## Interview angle

- **★🔥 Why `0.1 + 0.2 !== 0.3`?** IEEE-754 64-bit can't represent `0.1` or `0.2` exactly; the rounded sum is `0.30000000000000004`. Compare with `Math.abs(a-b) < Number.EPSILON`.
- **★ Why `NaN !== NaN`?** IEEE-754 mandates: any comparison with `NaN` is false. So `===` can't detect it — use `Number.isNaN(x)`.
- **`==` vs `===` with numbers?** `==` coerces (`"5" == 5` → `true`); `===` doesn't. Always `===`.
- **Why is `parseInt("0.5")` `0`?** `parseInt` parses integers and stops at the `.`. Use `parseFloat` or `Number`.
- **When use BigInt?** IDs / counters beyond `2^53`, big-int crypto. Don't use for decimals — BigInt is integers only.
- **How to test "is integer" robustly?** `Number.isInteger(x)` — strict, no coercion, handles `NaN`/`Infinity` correctly.
- **`Math.round(-2.5)`?** `-2` — half-rounds to **positive** infinity, not away from zero.

---

## Quick reference

```text
TYPE             one 'number' (64-bit float) + 'bigint'
LITERALS         42  3.14  1_000_000  0xff  0b1010  0o17  1.5e3
SPECIAL          NaN  Infinity  -Infinity   (all typeof 'number')
EPSILON / SAFE   Number.EPSILON   Number.MAX_SAFE_INTEGER (2^53-1)
BIGINT           1n   BigInt(10)         (no mixing with Number)

STR → NUM        Number(s)    parseInt(s, 10)   parseFloat(s)   +s
NUM → STR        String(n)    n.toString()      n.toString(16)
                 n.toFixed(2)   n.toPrecision(3)   n.toExponential(2)

TEST             Number.isNaN     Number.isFinite
                 Number.isInteger Number.isSafeInteger

MATH             round  floor  ceil  trunc   abs  sign  min  max
                 pow  sqrt  cbrt  log  log2  log10  exp
                 sin  cos  tan       PI  E
RANDOM           Math.random()                    → [0, 1)
RANDOM INT       Math.floor(Math.random()*(max-min+1)) + min

BITWISE TRUNC    n | 0      ~~n      (32-bit signed, fast trunc)
TOLERANCE EQ     Math.abs(a-b) < Number.EPSILON
```
