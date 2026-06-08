# JavaScript — Conditionals

Conditionals **make decisions** — run different code based on truthy/falsy conditions.

```text
        if / else if / else          switch
        many true/false branches     match ONE value to cases
              \                          /
               \    CONDITIONALS ───────/
                \   (decide what       /
   TERNARY ──────►  code runs)    ◄───────── SHORT-CIRCUIT
   cond ? a : b   /                \          && || as guards
   one-line       /                 \
                 /                   \
        depends on TRUTHY/FALSY (Topic 3)
```

---

## `if` / `else if` / `else`

Checks **top to bottom, stops at the first truthy** condition.

```js
let score = 75;

if (score >= 90)      console.log("A");
else if (score >= 70) console.log("B");   // ← matches, stops here
else if (score >= 50) console.log("C");
else                  console.log("F");
```
```text
B
```

> Order matters — put the **most specific / highest** condition first.

---

## `switch`

Cleaner when comparing **one value** against many **exact** options.

```js
let day = "Mon";

switch (day) {
  case "Sat":
  case "Sun":
    console.log("Weekend");   // stacked cases share a block
    break;
  case "Mon":
    console.log("Monday blues");
    break;
  default:
    console.log("Weekday");
}
```
```text
Monday blues
```

**Two critical facts:**

| Fact | Detail |
|------|--------|
| **`break`** | stops the switch. Omit it → **fall-through** to next case (bug, unless intended) |
| **matches with `===`** | strict — `case "1"` will **not** match number `1` |

### Fall-through gotcha ★
```js
switch (1) {
  case 1: console.log("one");   // runs
  case 2: console.log("two");   // ALSO runs — no break above! 😱
          break;
}
```
```text
one
two
```

---

## Ternary `? :`

Compact `if/else` that **returns a value**.

```js
let msg = age >= 18 ? "Adult" : "Minor";
```

> Use ternary to **choose/return a value**; use `if` to **do actions**.
> Don't deeply nest ternaries — unreadable.

---

## Short-circuit as a guard

`&&` / `||` from Topic 4 double as mini-conditionals.

```js
user && console.log(user.name);   // run right side only if user is truthy
isLoggedIn && showDashboard();    // common conditional-render pattern
let name = input || "Guest";      // default if falsy
let port = input ?? 3000;         // default only if null/undefined
```

---

## When to use which ★

| Use | When |
|-----|------|
| `if / else if` | ranges / complex conditions (`x >= 70`), different variables |
| `switch` | one value vs many **exact** matches (`===`) |
| ternary | choosing/returning a **value** in one line |
| `&&` / `\|\|` / `??` | quick guards & defaults (no full `if`) |

**`switch(true)` trick** — ranges inside a switch:

```js
switch (true) {
  case score >= 90: console.log("A"); break;
  case score >= 70: console.log("B"); break;
  default:          console.log("F");
}
```

---

## Key takeaways

- `if/else if/else` → top-to-bottom, first truthy wins; order matters.
- `switch` → one value, **exact `===`** matches; **always `break`** (else fall-through).
- Ternary → returns a value; keep it shallow.
- `&&`/`||`/`??` → lightweight guards & defaults.

---

### Interview angle
- "Difference between `if-else` and `switch`?" → `if` for ranges/complex; `switch` for one value vs many exact (`===`) cases.
- "What is switch fall-through?" → missing `break` runs the next case too; useful for stacking cases, otherwise a bug.
- "Does `switch` coerce?" → No — it matches with **`===`** (`"1"` ≠ `1`).
