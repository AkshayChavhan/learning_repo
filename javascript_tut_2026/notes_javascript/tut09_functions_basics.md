# JavaScript — Functions (Basics)

A **function** is a reusable block of code — **define once, run many times**.
(This is the basics layer; `this`, closures, `call/apply/bind` come in **Topic 12**.)

```text
        WAYS TO DEFINE              INPUTS / OUTPUT
        declaration, expression,    parameters → arguments
        arrow                       return value
              \                          /
               \      FUNCTIONS ─────────/
                \   (reusable blocks)   /
   DEFAULTS ─────►                 ◄───────── return
   default params  /              \           sends value back
   fn(a = 1)      /                \          (else undefined)
                 /                  \
        each call runs the body fresh
```

---

## Define & call

```js
function greet() {
  console.log("Hello!");
}
greet();   // call it
greet();   // run again
```
```text
Hello!
Hello!
```

---

## Parameters, arguments & return

```js
function add(a, b) {   // a, b = parameters
  return a + b;        // return = send a value back
}
let sum = add(3, 4);   // 3, 4 = arguments
console.log(sum);      // 7
```

```text
   add( 3, 4 )          ← arguments (actual values passed)
        │  │
   function add(a, b)    ← parameters (names in the definition)
        return a + b     ← return = the output
```

### Parameter vs argument ★ (common interview)

| Term | What it is | Where |
|------|-----------|-------|
| **Parameter** | placeholder name | function **definition** |
| **Argument** | real value | function **call** |

### `return` facts

- `return` sends a value back **and exits** the function immediately.
- No `return`? The function returns **`undefined`**.

```js
function noReturn() { let x = 5; }
console.log(noReturn());   // undefined
```

- Extra arguments are ignored; missing ones are `undefined`.

```js
function f(a, b) { return [a, b]; }
f(1, 2, 3);   // [1, 2]          (3 ignored)
f(1);         // [1, undefined]
```

---

## Three ways to define

```js
// 1. DECLARATION — hoisted (usable before its line)
function square(n) { return n * n; }

// 2. EXPRESSION — assigned to a variable, NOT hoisted
const cube = function (n) { return n * n * n; };

// 3. ARROW — shorter syntax (ES6)
const double = (n) => n * 2;
```

### Declaration vs expression ★ (hoisting)

| | Declaration | Expression |
|---|------------|------------|
| Syntax | `function f(){}` | `const f = function(){}` |
| **Hoisted?** | ✅ yes (call before defining) | ❌ no (TDZ, like `let`/`const`) |

```js
sayHi();                          // ✅ works — declaration hoisted
function sayHi() { console.log("hi"); }

sayBye();                         // ❌ ReferenceError — expression not hoisted
const sayBye = () => console.log("bye");
```

> Hoisting recap from **Topic 2**: declarations are moved to the top; `const`/expressions sit in the TDZ.

---

## Arrow functions = shorter syntax

For now, an arrow function is just a **shorter way to write a function**.

```text
   function (n) { return n * 2 }      →      (n) => n * 2
   └──── long form ────┘                      └─ arrow form ─┘
            same result, less typing
```

Syntax shortcuts:

```js
const double = n => n * 2;       // one param → parens optional; one expr → implicit return
const add    = (a, b) => a + b;  // multiple params → parens required
const greet  = () => "hi";       // no params → empty parens
const make   = () => ({ id: 1 });// returning an object → wrap in ( )
```

> 🚩 Arrow functions also handle the **`this`** keyword differently from regular functions —
> but that only makes sense after you learn `this`. **Covered in Topic 12.** For now: arrow = shorter syntax.

---

## Functions are values (first-class)

A function can be stored in a variable, put in an array, or passed around — just like a number or string.

```js
const ops = [add, square];
ops[0](2, 3);   // 5    (called add)
ops[1](4);      // 16   (called square)
```

> This is what makes callbacks and higher-order functions possible (Topic 12).

---

## Default parameters

A fallback value used when an argument is missing (`undefined`).

```js
function greet(name = "Guest") {
  return `Hello, ${name}`;
}
greet("Akshay");   // "Hello, Akshay"
greet();           // "Hello, Guest"
```

---

## Key takeaways

- **Parameter** = name in the definition; **argument** = value in the call.
- `return` sends a value back and exits; no return → `undefined`.
- **Declaration** is hoisted; **expression / arrow** is not.
- **Arrow** = shorter syntax (the `this` difference comes in Topic 12).
- Functions are **values** — store, pass, and return them.
- **Default parameters** fill in missing arguments.

---

### Interview angle
- ★ "Parameter vs argument?" → definition placeholder vs the actual value passed.
- ★ "Function declaration vs expression?" → declaration is hoisted; expression is not (TDZ).
- "What does a function return with no `return`?" → `undefined`.
- "What are first-class functions?" → functions treated as values (stored, passed, returned).
