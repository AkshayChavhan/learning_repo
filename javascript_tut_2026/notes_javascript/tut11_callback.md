# 🔁 Callbacks, Promises & Async/Await

### 🎯 Tut 11 · How JavaScript handles work that finishes *later*

---

## 🟢 Part 1 — Callbacks

> 📘 **DEFINITION: Callback**
> A **callback** is a function you **pass into another function**, so that the other
> function can **call it later**.

```javascript
function greet(name, callback) {
  console.log("Hello " + name);
  callback();
}

greet("Ravi", () => console.log("Bye!"));
```

`greet` takes two arguments: a name and a function. It prints the greeting, then calls the function you passed in. That passed-in function is the **callback**.

> 🔑 **KEY IDEA**
> The callback is just a **function**, passed as a **value**, and called by **someone else** at the **right time**.

> 🧭 **Pattern to remember**
> **You hand over a function → someone else calls it when they are ready.**

---

### 📌 Example 1 — Order of execution

`greet` prints **"Hello Ravi"** first, then calls the callback. So the callback runs **second**.

### 📌 Example 2 — `forEach` takes a callback

```javascript
const names = ["Ravi", "Asha"];
names.forEach(function (name) {
  console.log("Hi " + name);
});
```

The function we pass in is the **callback**. `forEach` calls it **two times**, once for Ravi and once for Asha.

### 📌 Example 3 — `setTimeout` takes a callback

```javascript
setTimeout(function () {
  console.log("One second passed");
}, 1000);
```

`setTimeout` waits **one second**, then runs the callback.

---

## 🟡 Part 2 — Callbacks can receive arguments

> 🔑 **KEY IDEA**
> A callback can **receive arguments** from the function that calls it.

### 📌 Example 4 — Passing a result to the callback

```javascript
function add(a, b, callback) {
  const sum = a + b;
  callback(sum);
}

add(2, 3, function (result) {
  console.log("The sum is " + result);
});
```

`add` calls the callback and gives it `sum`. Inside the callback, that value arrives as `result`.

### 📌 Example 5 — `map` passes each item to the callback

```javascript
const nums = [1, 2, 3];
const doubled = nums.map(function (n) {
  return n * 2;
});
console.log(doubled); // [2, 4, 6]
```

Each time, `map` passes **one number** into the callback as `n`.

### 📌 Example 6 — More than one argument (error-first)

```javascript
function fetchUser(id, callback) {
  const user = { id: id, name: "Ravi" };
  callback(null, user);
}

fetchUser(1, function (error, user) {
  if (error) {
    console.log("Something went wrong");
  } else {
    console.log("Found " + user.name);
  }
});
```

> 🟩 **COMMON PATTERN: Node.js error-first callback**
> The callback gets **two arguments**: an **`error`** and a **result**.
> The **first argument is the error**, if any.

---

## 🔴 Part 3 — Callback hell

> 🔥 **DEFINITION: Callback hell**
> Happens when callbacks are **nested inside other callbacks**, several levels deep.
> Each step waits for the one before it, so the code **shifts further to the right** and
> becomes **hard to read and debug**.

> ✅ **HOW TO AVOID IT**
> - 🔗 **Promises**: chain steps **flat**
> - ⏳ **async/await**: write steps like **normal sequential code**
> - 🧩 **Named functions**: split steps instead of nesting them

### 💥 The nested version

```javascript
getUser(1, function (err, user) {
  getOrders(user.id, function (err, orders) {
    getItems(orders[0].id, function (err, items) {
      console.log(items);
    });
  });
});
```

Each step waits for the one before it, so every new step adds **another level of indentation**. That's the **hell** part.

### ✨ The flat version with promises

```javascript
getUser(1)
  .then(user => getOrders(user.id))
  .then(orders => getItems(orders[0].id))
  .then(items => console.log(items));
```

> ✅ Same steps, **no nesting**.

---

## 🟣 Part 4 — Quiz

### ❓ Question 3 — Error-first convention

> **What is the error-first convention in callbacks, and why do Node.js developers use it?**
> *Answer in your own words, and I'll give you feedback.*

---

### ❓ Question 4 — Is a callback always asynchronous?

> **Answer in your own words, and give an example of one that runs synchronously and one that runs later.**

A callback is **not always asynchronous**. Whether it runs **now** or **later** depends on the
function that **receives** it.

| ⚡ Type | 🧰 Example | ⏱️ When the callback runs |
|---|---|---|
| 🟢 **Synchronous** | `map` | **Right away**, for each item, before the line finishes |
| 🔵 **Asynchronous** | `setTimeout` | **Later**, after the timer ends |

> 💡 The callback itself is just a function. **The receiving function decides when it runs.**

---

### ❓ Question 5 — How do callbacks relate to closures?

> **Answer in your own words, and give a short example if you can.**

```javascript
function setup() {
  let name = "Ravi";
  setTimeout(() => {
    console.log("Hello " + name);
  }, 1000);
}
setup();
```

- 🎯 The **arrow function is the callback**. It's passed to `setTimeout`, which calls it after one second.
- 🚪 By then, `setup` has **already finished** and left the call stack.
- 🔗 But the callback **still uses `name`**, so it keeps a link to that variable.

> 🧠 **That link is the closure.**
