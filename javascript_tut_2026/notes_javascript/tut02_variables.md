# JavaScript — Variables & Constants

A **variable** is a **named box** that holds a value. Three keywords create them:
**`let`**, **`const`**, **`var`**.

```text
              var (old)              const (modern)
                  \                      /
   function-scope ─\    DECLARING ──────/ can't reassign
   re-declarable    \   VARIABLES     /  block-scope
                     \               /
   a NAME ───────────►  stores a   ◄──────── a VALUE
                     /    value      \
   let (modern)     /                 \
   block-scope ────/                   \──── const = default,
   reassignable                              let = when value changes,
                                             var = avoid
```

---

## The basics

```js
let city = "Pune";       // can change later
const pi = 3.14159;      // CANNOT be reassigned
var old = "avoid this";  // old way — avoid

let age = 25;
age = 26;                // ✅ reassign a let
```

> **Default rule:** use **`const`**; switch to **`let`** only if the value must change; avoid **`var`**.

---

## var vs let vs const ★ (the #1 interview table)

| Feature | `var` | `let` | `const` |
|---------|-------|-------|---------|
| **Scope** | function | block `{}` | block `{}` |
| **Re-declare** (same scope) | ✅ | ❌ error | ❌ error |
| **Re-assign** | ✅ | ✅ | ❌ error |
| **Hoisting** | yes → `undefined` | yes → TDZ | yes → TDZ |
| **Use today?** | ❌ avoid | ✅ when changing | ✅ default |

```js
const x = 1;
x = 2;        // ❌ TypeError: Assignment to constant variable

let y = 1;
y = 2;        // ✅

var z = 1;
var z = 5;    // ✅ allowed (sloppy — bug source)
```

---

## `const` locks the BOX, not the CONTENTS ★ (classic gotcha)

`const` means the **variable can't be reassigned** — NOT that the value is frozen.
Objects/arrays can still be **mutated**.

```js
const user = { name: "Akshay" };
user.name = "Raj";    // ✅ allowed (mutating contents)
user = {};            // ❌ TypeError (reassigning the variable)
```
```text
{ name: "Raj" }
```

> To truly freeze contents → `Object.freeze()` (Topic 11).

---

## Scope — where a variable is visible

```js
function demo() {
  if (true) {
    var a = 1;    // function-scoped → leaks OUT of the if
    let b = 2;    // block-scoped → trapped in the if
  }
  console.log(a); // 1  ✅
  console.log(b); // ❌ ReferenceError
}
```

| | `var` | `let` / `const` |
|---|-------|-----------------|
| Lives in | whole function | the `{ }` block only |

---

## Naming rules

- Letters, digits, `_`, `$` — **can't start with a digit**
- Case-sensitive: `age` ≠ `Age`
- Can't use reserved words (`let`, `class`, `return`, …)
- Convention: **camelCase** (`firstName`, `totalPrice`)

---

## Hoisting (intro — full detail in Topic 13)

Declarations are conceptually "moved to the top"; the **value** is not.

```js
console.log(myVar);  // undefined   (var hoisted, value not)
var myVar = 5;

console.log(myLet);  // ❌ ReferenceError (TDZ)
let myLet = 5;
```

- **`var`** → hoisted and initialized to `undefined`.
- **`let` / `const`** → hoisted but **not initialized** → using them before their line throws
  (the **Temporal Dead Zone**).

---

## Key takeaways

- **`const` by default, `let` when it changes, avoid `var`.**
- `var` = function scope + re-declarable + hoists to `undefined` → bug-prone.
- `let`/`const` = block scope + TDZ → safer.
- `const` blocks **reassignment**, not **mutation** of objects/arrays.
- Use **camelCase**; names can't start with a digit.

---

### Interview angle
- ★ "Difference between `var`, `let`, `const`?" → use the table (scope, re-declare, re-assign, hoisting).
- ★ "Can you change a `const` object?" → **Yes** — `const` locks the binding, not the contents.
- "What's the TDZ?" → `let`/`const` exist but are unusable before their declaration line.
