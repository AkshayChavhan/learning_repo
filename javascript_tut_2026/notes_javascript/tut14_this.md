# tut14: `this` keyword

> **Core idea:** `this` is decided by **how a function is called**, not by where it is written.
> The one exception is **arrow functions**.

---

## 📌 Quick Reference

| Call style            | Example                         | `this` is                                     |
| --------------------- | ------------------------------- | --------------------------------------------- |
| **Dot call** (method) | `user.sayName()`                | `user` (the object before the dot)            |
| **Plain call**        | `sayName()`                     | global object (sloppy) / `undefined` (strict) |
| `new` **call**        | `new Person()`                  | the brand-new empty object                    |
| **Explicit**          | `fn.call(obj)`, `apply`, `bind` | `obj`                                         |
| **Arrow function**    | `() => {}`                      | outer `this`, fixed when the arrow is created |

**Priority (highest wins):** `new` > `call / apply / bind` > dot call > plain call

---

## 🟢 Beginner

### 1. Dot call → `this` is the object

```javascript
const user = {
  name: "Ravi",
  sayName() {
    console.log(this.name);
  },
};

user.sayName(); // Ravi   → this = user
```

### 2. Plain call → no object, so `this` falls back

```javascript
function sayName() {
  console.log(this.name);
}

sayName(); // undefined  → sloppy mode: this = global object
```

> In **strict mode** (`"use strict"`), `this` is `undefined` here, so `this.name` throws a `TypeError`.

### 3. `new` → `this` is a new object

```javascript
function Person(name) {
  this.name = name;        // this = the new object
}

const p = new Person("Ravi");
console.log(p.name);       // Ravi
```

`new` creates an empty object, sets `this` to it, and returns it automatically.

### 4. `call`, `apply`, `bind` → you choose `this`

| Method | Runs now? | Arguments passed | Example |
|---|---|---|---|
| `call` | ✅ Yes | one by one | `greet.call(user, "Hello")` |
| `apply` | ✅ Yes | as an **array** | `greet.apply(user, ["Hello"])` |
| `bind` | ❌ No, returns a new function | one by one | `greet.bind(user, "Hello")` |

```javascript
function greet(greeting) {
  console.log(greeting + ", " + this.name);
}
const user = { name: "Ravi" };

greet.call(user, "Hello");     // Hello, Ravi
greet.apply(user, ["Hello"]);  // Hello, Ravi

const boundGreet = greet.bind(user, "Hello");
boundGreet();                  // Hello, Ravi
```

---

## 🟡 Intermediate

### Arrow functions: no `this` of their own

| Question | Regular function | Arrow function |
|---|---|---|
| Has its own `this`? | ✅ Yes | ❌ No |
| `this` decided by | how it is **called** | where it is **written** (lexical) |
| Can `call / apply / bind` change `this`? | ✅ Yes | ❌ No |
| Good as an object method? | ✅ Yes | ❌ Usually no |

**✅ Works: arrow inside a method**

```javascript
const user = {
  name: "Ravi",
  sayName() {
    const show = () => console.log(this.name); // takes this from sayName
    show();
  },
};

user.sayName(); // Ravi
```

**❌ Fails: arrow as the object property**

```javascript
const user = {
  name: "Ravi",
  sayName: () => console.log(this.name), // this = outer scope, NOT user
};

user.sayName(); // undefined
```

### ⚠️ Gotcha 1: Nested regular functions don't inherit `this`

```javascript
const user = {
  name: "Ravi",
  sayName() {
    function inner() {
      console.log(this.name);
    }
    inner(); // plain call → this is lost
  },
};

user.sayName(); // undefined
```

**Fix:** use an arrow function for `inner`, or `inner.call(this)`, or `.bind(this)`.

### ⚠️ Gotcha 2: Passing a method around loses `this`

```javascript
const user = { name: "Ravi", sayName() { console.log(this.name); } };

const f = user.sayName;
f(); // undefined → the dot is gone, so this is lost
```

This happens in **callbacks** and `setTimeout(user.sayName, 100)`.

**Fix:** `setTimeout(() => user.sayName(), 100)` or `user.sayName.bind(user)`.

---

## 🔴 Expert

| Topic                           | What really happens                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Strict mode**                 | Plain-call `this` is `undefined`, not the global object. This prevents accidental global writes. |
| **Top-level** `this`            | Node CommonJS: `module.exports` (`{}`). Browser script: `window`. ES module: `undefined`.        |
| `bind` **is permanent**         | The first `bind` wins. Later `bind` or `call` cannot change it.                                  |
| `new` **beats** `bind`          | `new` creates a fresh `this`, ignoring the bound one.                                            |
| **Arrows are not constructors** | `new (() => {})` throws `TypeError`. Arrows also have no `arguments`.                            |

```javascript
// bind is permanent: the first bind wins
function show() { console.log(this.name); }
const b = show.bind({ name: "A" }).bind({ name: "B" });
b(); // A

// new beats bind
function P() { this.x = 1; }
const BoundP = P.bind({ x: 99 });
console.log(new BoundP().x); // 1
```

---

## 🧭 Decision Flow

```text
Is the function an ARROW?  ──yes──►  this = outer scope (fixed, ignore call style)
          │ no
Called with `new`?        ──yes──►  this = new empty object
          │ no
Called with call/apply/bind? ─yes─► this = the object you passed
          │ no
Called with a dot (obj.fn())? ─yes─► this = obj (object before the dot)
          │ no
Plain call (fn())         ──────────►  this = global (sloppy) / undefined (strict)
```

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| How is `this` decided in a regular function? | By the call: dot → object on the left; plain → global or `undefined` (strict); `new` → the new object; `call/apply/bind` → the object you pass. |
| `call` vs `bind`? | Both set `this` first. `call` runs **now**; `bind` returns a function to run **later**. |
| `apply` vs `call`? | Same behavior. `apply` takes arguments as an **array**; `call` takes them one by one. |
| Method call vs plain call? | `user.f()` → `this` is `user`. `const g = user.f; g()` → `this` is lost. |
| `this` inside an arrow? | Taken from the enclosing scope when the arrow is created. `call/apply/bind` and the call style cannot change it. |

---

## ✅ Key Takeaways

- `this` depends on the **call**, not the **definition** (except arrows).
- Use **arrows** for callbacks inside methods. Use **regular functions** for object methods.
- When `this` goes missing, check **how** the function was called.
