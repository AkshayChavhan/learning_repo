# JavaScript — Loops

Loops **repeat code** without rewriting it. Pick the loop by *what* you're repeating over.

```text
   for (let i=0; i<n; i++){}        for (const v of arr){}   ← values
   while (cond){}                   for (const k in obj){}   ← keys
   do {} while (cond)
        COUNT-BASED                  COLLECTION-BASED
              \                          /
               \      LOOPS  ───────────/
                \   (repeat code)      /
   CONTROL ──────►                ◄───────── WHEN TO USE
   break;         /                \         ┌─────────┬───────────┐
   continue;     /                  \        │ array   │ for...of  │
   outer: ...   /                    \       │ object  │ for...in  │
                                            │ count   │ for       │
                                            │ until   │ while     │
                                            └─────────┴───────────┘
```

---

## What is a label? (quick intro)

A **label** is a **name tag on a loop** — `name:` written before it. It is **not a function**,
so it's never "called." You define it with `name:` and refer to it via `break name` /
`continue name` to control **which** loop (handy for nested loops). Full detail in
[Labels](#labels-control-an-outer-loop) below.

```text
   outer: for (...) { ... }
   ▲────▲
   │    └─ the loop being labeled
   └─ the label = a name tag (any name + a colon)
```

---

## `for` loop

Repeat a known number of times — three parts: **init; condition; update**.

```js
for (let i = 0; i < 3; i++) {
  console.log(i);
}
```
```text
0
1
2
```

```text
   for (let i = 0;  i < 3;  i++)
            │         │       │
         ① start   ② check  ③ after each loop
         (once)    (each)   (each)
```

---

## `while` & `do...while`

```js
let n = 3;
while (n > 0) { console.log(n); n--; }   // ⚠️ must change n or infinite loop
```
```text
3
2
1
```

### Anatomy of `do...while`

```text
   do {
       ←──── ALL the action code goes HERE (the body)
   } while ( condition );
              ←──── ONLY the condition goes HERE
```

- **`do { ... }`** → the **body** = all your action code (the work that repeats)
- **`while ( ... )`** → just the **condition** = the true/false test deciding "loop again?"

```js
do {
  roll = Math.floor(Math.random() * 6) + 1;   // ← action code (body)
  console.log("Rolled:", roll);               // ← action code (body)
} while (roll !== 6);                          // ← ONLY the condition
```

### One important clarification

Regular `while` **also has a body** — the difference isn't "while has no body."
It's **WHERE the body sits relative to the condition.**

```text
   WHILE                          DO...WHILE
   ─────                          ──────────
   while (condition) {            do {
       action code                    action code     ← body comes FIRST
   }                              } while (condition); ← condition LAST
   ▲                                                ▲
   condition checked FIRST        condition checked AFTER body runs
```

Both have a body **and** a condition — the real difference is **order**:

| | Body location | Condition checked | Body runs at least once? |
|---|--------------|-------------------|--------------------------|
| `while` | after `while(cond)` | **before** body | ❌ No (could run 0 times) |
| `do...while` | inside `do {}`, before `while(cond)` | **after** body | ✅ **Yes** (always ≥ 1) |

### Side-by-side proof

```js
let x = 10;

// while: condition checked FIRST → x<5 is false → body NEVER runs
while (x < 5) {
  console.log("while body");   // ❌ never prints
}

// do...while: body runs FIRST, then checks → prints once, THEN sees false
do {
  console.log("do body");      // ✅ prints once
} while (x < 5);
```
```text
do body
```

> Use `for` when you know the count; `while` when you loop until some condition changes;
> **`do...while` when the body must execute at least once** (validation, menus, retries).

---

## `for...of` vs `for...in` ★ (classic interview)

| | `for...of` | `for...in` |
|---|-----------|------------|
| Iterates | **values** | **keys** (property names) |
| Use for | arrays, strings, Sets, Maps | objects |
| On an array gives | `10, 20, 30` (items) | `"0","1","2"` (string indexes!) |

```js
for (const fruit of ["apple", "banana"]) console.log(fruit);
// apple / banana   ← values

const user = { name: "Akshay", age: 25 };
for (const key in user) console.log(key, user[key]);
// name Akshay / age 25   ← keys
```

```js
const arr = [10, 20, 30];
for (const v of arr) console.log(v);   // 10 20 30    ← values ✅
for (const i in arr) console.log(i);   // "0" "1" "2" ← indexes as strings ⚠️
```

> 🎯 **`for...of` for arrays (values), `for...in` for objects (keys).** Don't use `for...in` on arrays.

---

## `break` & `continue`

| Keyword | Effect |
|---------|--------|
| `break` | exit the loop entirely |
| `continue` | skip to the next iteration |

```js
for (let i = 0; i < 5; i++) {
  if (i === 2) continue;   // skip 2
  if (i === 4) break;      // stop at 4
  console.log(i);
}
```
```text
0
1
3
```

---

## Labels (control an outer loop)

A **label** is a **name tag** on a loop (not a function — never "called"). You *define* it by
writing `name:` before a loop, and *refer* to it with `break name` / `continue name`.
By default `break`/`continue` only affect the **innermost** loop; a label lets you target an
**outer** one from inside a nested loop.

```js
outer: for (let i = 0; i < 3; i++) {     // outer loop, named "outer"
  for (let j = 0; j < 3; j++) {          // inner loop (no label)
    if (j === 1) continue outer;         // skip rest of inner → jump to next i
    console.log(i, j);
  }
}
```
```text
0 0
1 0
2 0
```

**Trace** of the run:

```text
i=0 → j=0 print "0 0"
      j=1 → continue outer → abandon inner, go to i=1
i=1 → j=0 print "1 0"
      j=1 → continue outer → go to i=2
i=2 → j=0 print "2 0"
      j=1 → continue outer → i becomes 3 → loop ends
```

| Statement | Effect |
|-----------|--------|
| `continue` | next iteration of **inner** loop |
| `break` | exit **inner** loop only |
| `continue outer` | next iteration of **outer** loop (skip rest of inner) |
| `break outer` | exit **outer** loop entirely (stops everything) |

> Without the label, plain `continue` would skip only to the next `j` (→ `0 0, 0 2, 1 0, …`).
> ⚠️ Labels are rarely needed — usually refactor (extract a function + `return`, or use a flag).
> They mostly appear in interview trivia and deeply-nested algorithms.

---

## Gotchas ★

| Gotcha | Detail |
|--------|--------|
| Infinite loop | forgetting to update the condition (`i++`, `n--`) |
| `for...in` on arrays | string indexes + may include inherited keys → avoid |
| `var` in loops | classic closure bug (Topic 12) — `let` fixes it |
| `forEach` can't break | array `.forEach` ignores `break`/early-exit — use `for...of` to exit early |

```js
for (const x of arr) { if (x > 1) break; }   // ✅ can stop early
arr.forEach(x => { if (x > 1) break; });     // ❌ SyntaxError — no break in forEach
```

> Array methods (`map`/`filter`/`reduce`/`forEach`) get their deep dive in Topic 10.

---

## Key takeaways

- `for` = known count; `while` = until a condition changes; `do...while` = run **≥ once**.
- **`for...of` → values** (arrays/strings/Sets/Maps); **`for...in` → keys** (objects).
- Don't use `for...in` on arrays (string indexes + inherited keys).
- `break` exits, `continue` skips; **labels** target outer loops.
- Need early exit? Use `for...of`, not `forEach`.

---

### Interview angle
- ★ "`for...of` vs `for...in`?" → values vs keys; of for arrays, in for objects.
- "Why avoid `for...in` on arrays?" → yields string indexes and can pick up inherited enumerable keys.
- "Can you `break` out of `forEach`?" → No; use a real loop (`for`/`for...of`) or `some`/`every`.
- "`while` vs `do...while`?" → `do...while` always executes the body once (post-check).
