# JavaScript — Data Types

Every value is either a **primitive** (simple, copied by value) or a **reference/object**
(collections, copied by address). `typeof` tells you which type a value is.

```text
        PRIMITIVES (7)                    REFERENCE (objects)
        copied by VALUE                   copied by REFERENCE
              \                                /
   string,number,boolean ─\    DATA TYPES ───/ object, array, function
   null,undefined,         \               /
   symbol,bigint            \             /
                            ►  every value ◄
                            /  has a type   \
   typeof tells you ───────/                 \──── dynamic typing:
   the type                                        a variable holds any type
```

---

## The 7 primitive types

| Type | Example | Meaning |
|------|---------|---------|
| `string` | `"hello"` | text |
| `number` | `42`, `3.14` | **all numbers** (int + float together) |
| `boolean` | `true` / `false` | yes / no |
| `undefined` | `undefined` | declared, no value yet (JS sets it) |
| `null` | `null` | intentional "nothing" (you set it) |
| `symbol` | `Symbol("id")` | unique identifier (advanced) |
| `bigint` | `123n` | integers bigger than `number` can hold |

## Reference types (objects)

| Type | Example |
|------|---------|
| `object` | `{ name: "Akshay" }` |
| `array` | `[1, 2, 3]` |
| `function` | `function () {}` |

---

## `typeof`

```js
typeof "hi"          // "string"
typeof 42            // "number"
typeof true          // "boolean"
typeof undefined     // "undefined"
typeof {}            // "object"
typeof [1,2]         // "object"     ← arrays report as object!
typeof function(){}  // "function"
typeof null          // "object"     ← historic BUG (see below)
```

---

## Dynamic typing

A variable can hold **any** type, and switch:

```js
let thing = "text";   // string
thing = 42;           // now a number — totally legal
```

---

## Primitive vs Reference ★ (critical)

```text
PRIMITIVE — copied by VALUE          REFERENCE — copied by ADDRESS
   let a = 1;                            let o1 = {n: 1};
   let b = a;   → b is a COPY            let o2 = o1;  → o2 points to SAME object
   b = 2;                                o2.n = 9;
   a is still 1 ✅                       o1.n is now 9 too ⚠️
```

```js
let a = 1, b = a;  b = 2;
console.log(a);            // 1  (independent copy)

let o1 = {n: 1}, o2 = o1;  o2.n = 9;
console.log(o1.n);         // 9  (same object — shared reference)
```

> Primitives copy the **value**; objects copy the **address** (both names point to one object).

---

## Gotcha 1 — `typeof null === "object"`

A 25-year-old bug, kept for backward compatibility.

```js
typeof null   // "object"   ← wrong, but never fixed
```

## Gotcha 2 — `null` vs `undefined`

| | `undefined` | `null` |
|---|------------|--------|
| Meaning | not assigned yet (JS sets it) | intentionally empty (you set it) |
| `typeof` | `"undefined"` | `"object"` (the bug) |
| `null == undefined` | **true** (loose) | |
| `null === undefined` | **false** (strict) | |

---

## Gotcha 3 — Truthy & Falsy ★

Every value is truthy or falsy in a boolean context. Decided by a **fixed list**, NOT by "looks empty."

```text
   THE 8 FALSY VALUES (the whole list)
   false   0   -0   0n   ""   null   undefined   NaN

   EVERYTHING ELSE → TRUTHY
   including:  []   {}   "0"   "false"   function(){}   42
```

```js
if ("")        { } // skipped (falsy)
if (0)         { } // skipped (falsy)
if (undefined) { } // skipped (falsy)
if ([])        { } // RUNS — objects are always truthy 😮
if ({})        { } // RUNS — objects are always truthy
if ("0")       { } // RUNS — non-empty string
```

**Why `[]`/`{}` are truthy:** they're **objects**, and *all objects are truthy* — empty or not.
Only primitives can be falsy.

### Real bug this causes
```js
let arr = [];
if (arr)            // ❌ always true (truthy) — wrong emptiness check
if (arr.length > 0) // ✅ correct way to test "has items"
```

---

## Key takeaways

- **7 primitives** + **objects** (object/array/function).
- `number` = all numbers; no separate int/float.
- `typeof` arrays/null → `"object"` (array is object; null is a bug).
- Primitives copy by **value**, objects by **reference**.
- `null` = intentional empty; `undefined` = not assigned.
- **8 falsy values**; `[]` and `{}` are **truthy** → use `.length` to check empty arrays.

---

### Interview angle
- ★ "Primitive vs reference / pass-by-value vs reference?" → primitives copy value, objects share a reference.
- ★ "What are the falsy values?" → `false, 0, -0, 0n, "", null, undefined, NaN` (and `[]`/`{}` are truthy).
- "`typeof null`?" → `"object"` (historic bug).
- "`null` vs `undefined`?" → intentional-empty vs not-assigned; `==` equal, `===` not.
