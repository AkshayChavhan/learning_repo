# JavaScript — Operators

Operators **do things** with values: math, comparison, logic, assignment.

```text
        ARITHMETIC              COMPARISON
        + - * / % **            == === < > <= >=
              \                      /
               \    OPERATORS ──────/
                \   (do things     /
   ASSIGNMENT ───►  with values) ◄─────── LOGICAL
   = += -= *=     /                \       && || !
                 /                  \
        TERNARY /                    \ MODERN
        cond?a:b                      ?? ?.
```

---

## Arithmetic

| Op | Meaning | `5 _ 2` |
|----|---------|---------|
| `+` | add | `7` |
| `-` | subtract | `3` |
| `*` | multiply | `10` |
| `/` | divide | `2.5` |
| `%` | remainder (modulo) | `1` |
| `**` | power | `25` |

```js
10 % 3    // 1   (modulo — even check: n % 2 === 0)
2 ** 10   // 1024
```

## Assignment

```js
let x = 5;
x += 3;   // x = x + 3 → 8
x *= 2;   // 16
```
`=` `+=` `-=` `*=` `/=` `%=` `**=`

---

## Comparison: `==` vs `===` ★

| Operator | Name | Checks |
|----------|------|--------|
| `==` | loose | value **after coercion** |
| `===` | strict | value **AND type** (no coercion) |

```js
5 === 5     // true
5 === "5"   // false  (number vs string)
5 == "5"    // true   ← coerces "5" → 5 😬
0 == false  // true   ← coerces false → 0
```

> **Always use `===`.** Only deliberate use of `==`: `x == null` (matches `null` AND `undefined`).

---

## Logical & short-circuit

| Op | Name | true when |
|----|------|-----------|
| `&&` | AND | both truthy |
| `\|\|` | OR | at least one truthy |
| `!` | NOT | flips boolean |

`&&` / `||` **return a value** and stop early (short-circuit):

```js
true  || "x"   // true   (|| stops at first truthy)
false || "x"   // "x"    (returns the truthy side)
true  && "x"   // "x"    (&& returns last if all truthy)

let name = userName || "Guest";   // default value pattern
```

---

## Ternary (one-line if/else)

```js
let canVote = age >= 18 ? "yes" : "no";
```

---

## Type coercion gotchas ★

`+` with a string → **concatenation**. Every other math op → **convert to number**.

```js
1 + "2"    // "12"   (+ prefers strings → glue)
"5" - 2    // 3      (- forces numbers)
"5" * "2"  // 10     (* forces numbers)
true + 1   // 2      (true → 1)
```

> 🎯 Hook: **`+` is the only operator that prefers strings.** The rest coerce to numbers.

---

## `??` nullish coalescing vs `||`

| | `\|\|` falls back when… | `??` falls back when… |
|---|----------------------|----------------------|
| Triggers on | any **falsy** (`0`, `""`, `false`, `null`, `undefined`) | **only** `null` / `undefined` |

```js
0 || "default"   // "default"  ← 0 is falsy (often a bug!)
0 ?? "default"   // 0          ← ?? keeps 0
```

> Use `??` when `0`, `""`, or `false` are **valid** values you want to keep.

---

## `?.` optional chaining

Safely read nested props — returns `undefined` instead of crashing.
**`?.` guards the thing immediately to its LEFT.**

```js
let user = {};
user.address.city    // ❌ TypeError (reading .city on undefined)
user.address?.city   // ✅ undefined (?. stops before .city)
```

**Where to place it** — guard each value that *might* be null/undefined:

```text
   user  ?.  address  ?.  city
    └ guard if user    └ guard if address
      might be missing    might be missing
```

```js
let user = {};        // user exists → no ?. needed before address
user.address?.city    // ✅

let user2 = null;     // user2 might be missing → guard it
user2.address?.city   // ❌ crashes on user2 itself
user2?.address?.city  // ✅ guards user2 first
```

| Value | Could be null/undefined? | Guard it? |
|-------|--------------------------|-----------|
| `user = {}` | no | ❌ |
| `user = null` | yes | ✅ `user?.` |
| `user.address` | yes (key may be absent) | ✅ `address?.` |

> Works with methods `obj.fn?.()` and arrays `arr?.[0]` too. Don't over-spray it — it can hide real bugs.

---

## Operator precedence (order of evaluation)

Higher runs first (like math). Use `()` to be explicit and readable.

| Precedence | Operators |
|-----------|-----------|
| highest | `()` grouping, `?.` |
| | `**` |
| | `*` `/` `%` |
| | `+` `-` |
| | `<` `>` `<=` `>=` |
| | `==` `===` `!=` `!==` |
| | `&&` |
| | `\|\|` `??` |
| | `? :` ternary |
| lowest | `=` `+=` … assignment |

```js
2 + 3 * 4     // 14  (* before +)
(2 + 3) * 4   // 20  (() first)
```

---

## Key takeaways

- **`===` over `==`** — `==` coerces and causes bugs.
- **`+` prefers strings** (concatenation); other math ops coerce to numbers.
- `&&`/`||` **return values** and short-circuit (default-value pattern).
- **`??`** falls back only on `null`/`undefined`; **`||`** on any falsy.
- **`?.`** guards the value on its left; place it after anything that may be missing.

---

### Interview angle
- ★🔥 "`==` vs `===`?" → loose (coerces) vs strict (value + type); always prefer `===`.
- ★ "`??` vs `||`?" → `??` only triggers on `null`/`undefined`; `||` on any falsy (`0`, `""`).
- ★ "What does `?.` do / where to place it?" → safe nested access; guards the value to its left.
- 🧩 Predict: `1 + "2" + "2"` → `"122"`, `"5" - 2` → `3`, `true + 1` → `2`.
