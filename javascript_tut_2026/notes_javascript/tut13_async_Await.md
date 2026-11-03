# ⏳ Async / Await

### 🎯 Tut 13 · Write async code that reads like normal, top-to-bottom code

---

## 🟢 Part 1 — `async` and `await`

> 📘 **DEFINITION: `async`**
> Put **`async` before a function**, and it **always returns a promise**.

> 📘 **DEFINITION: `await`**
> Inside an async function, **`await` pauses the function** until a promise **settles**, then gives you **its value**.

```javascript
async function getGreeting() {
  const value = await Promise.resolve("Hello");
  return value;
}

getGreeting().then(msg => console.log(msg)); // "Hello"
```

> 🔑 **KEY POINT**
> `getGreeting()` returns a **promise**, so you still use **`.then`** to read the result **from outside**.

---

## 🟡 Part 2 — Error handling with `try` / `catch`

> ⚠️ Since `await` can fail just like a promise, you **wrap it in `try` and `catch`**.

```javascript
async function loadUser() {
  try {
    const user = await fetchUser(1);
    console.log(user.name);
  } catch (error) {
    console.log("Could not load user");
  }
}
```

| 🔀 What happens | ➡️ Result |
|---|---|
| ✅ `fetchUser` **succeeds** | The code **keeps going normally** |
| ❌ `fetchUser` **rejects** | The code **jumps to the `catch` block**, just like a `.catch` would |

> 🧠 **WHY:** When a promise fails, `await` **throws an error**. That error **is the same as the rejection**.

> 🎯 The `await fetchUser(1)` line is **inside `try`**. If it fails, the `catch` block runs and prints
> `"Could not load user"`.

---

## 🔵 Part 3 — `await` pauses only its own function

> 🔑 **KEY POINT:** `await` only pauses the **function it's inside**, **not the whole program**.
> **Other code keeps running.**

```javascript
async function run() {
  console.log("start");
  await new Promise(resolve => setTimeout(resolve, 1000));
  console.log("after 1 second");
}

run();
console.log("outside");
```

### 📤 Output

```text
start
outside
after 1 second
```

> 🧭 `run` **paused**, but the **rest of the program didn't wait** for it.

---

## 🟣 Part 4 — One after another vs at the same time

### 🐢 Sequential: each `await` waits for the one before it

```javascript
const a = await fetchA(); // waits
const b = await fetchB(); // starts only after fetchA finishes
```

### 🚀 Parallel: start both, then wait together

> 💡 If the two tasks **don't depend on each other**, start both first, then wait for both
> together with **`Promise.all`**:

```javascript
const [a, b] = await Promise.all([fetchA(), fetchB()]);
```

> ⚡ This is usually **faster**, because **both run at the same time**.

---

## 🎤 Interview round

> 🗣️ Answers below are in my own words. Feedback comes after each one.

### ❓ Question 1 — What `async` and `await` do

> **What does the `async` keyword do to a function, and what does `await` do inside it?**

✍️ **My answer:** *(not written yet)*

---

### ❓ Question 2 — Error handling vs `.catch`

> **How do you handle errors in an async function, and how is that different from `.catch` on a promise?**

✍️ **My answer:** Wrap the awaited calls in `try`, and a rejection jumps to `catch`.

🔧 **Feedback — two fixes:**
1. 🎯 Only the **`await` calls** need to be inside `try`, not all the functions.
2. ⚡ A rejected promise **throws at the `await` line**, which is what sends control into the `catch` block.

📌 **The difference from `.catch`:**

| 🧰 Approach | 🧭 What it is |
|---|---|
| 🔗 `.catch` | A **method on the promise** |
| 🧱 `try` / `catch` | **Plain syntax** that works on **any awaited code** |

---

### ❓ Question 3 — `await` on a non-promise

> **What does `await` do to a value that isn't a promise, like `await 5`?**

✍️ **My answer:** `await` on a non-promise just gives you the value back, but it still **yields once**,
so the code after it runs as a **microtask**.

---

### ❓ Question 4 — Forgetting `await`

> **What happens if you forget to use `await` on a promise inside an async function?**

✍️ **My answer:** *Sure. Here's a function that fetches a user's name.*

```javascript
async function getName() {
  return "Ravi";
}

async function main() {
  const name = getName();      // forgot await
  console.log(name);           // Promise { 'Ravi' }
  console.log(name.toUpperCase()); // TypeError
}
```

> 🧩 `getName()` returns a **promise**, not the string. So `name` holds the **promise object**.
> When you try to use it like a string, the code **breaks**.

✅ **Fixed version:**

```javascript
async function main() {
  const name = await getName();
  console.log(name.toUpperCase()); // "RAVI"
}
```

---

### ❓ Question 5 — `await` inside a non-async function

> **Can you use `await` inside a regular function that isn't marked `async`?**

✍️ **My answer:** If you use it in a regular function, JavaScript **throws a syntax error** before the code even runs.

📌 **One detail to add:** the same rule applies at the **top level of a normal script**, where `await`
**isn't allowed**. Top-level `await` only works in **ES modules**.
