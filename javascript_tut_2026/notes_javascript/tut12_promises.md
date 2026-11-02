# 🤝 Promises

### 🎯 Tut 12 · A placeholder for a value that isn't ready yet

---

## 🟢 What is a promise?

> 📘 **DEFINITION: Promise**
> A **promise** is a **placeholder for a value that isn't ready yet**.

> 🧾 **MENTAL MODEL: The shop receipt**
> The shop hasn't handed you the item yet, but you have a **receipt** that says it's coming.

---

## 🟡 Promise states

A promise has **three states**:

| 🚦 State | 🗣️ Meaning | 🔒 Can it change? |
|---|---|---|
| ⏳ **Pending** | Waiting | ✅ Yes, it moves on |
| ✅ **Fulfilled** | It worked | ❌ **No, final** |
| ❌ **Rejected** | It failed | ❌ **No, final** |

> 🔑 **KEY RULE:** Once a promise is **fulfilled** or **rejected**, it **stays that way**.

---

## 🛠️ Creating a promise

A promise takes a function with **two parts**: `resolve` and `reject`.

```javascript
const p = new Promise((resolve, reject) => {
  resolve("it worked");
});
```

| 📞 Call | ➡️ Result |
|---|---|
| `resolve(value)` | ✅ **Fulfilled**, with the value you pass in |
| `reject(error)` | ❌ **Rejected**, with an error |

---

## 📥 Getting the value out

> 🎯 Use **`.then`** for **success** and **`.catch`** for **failure**.

```javascript
p.then(value => {
  console.log(value); // "it worked"
});
```

If the promise was rejected, `.catch` runs instead:

```javascript
p.catch(error => {
  console.log("Something failed");
});
```

---

## 🔗 Chaining

> 🧵 Each `.then` returns a **new promise**, so you can **line up steps one after another**,
> instead of **nesting** them.

```javascript
getUser(1)
  .then(user => getOrders(user.id))
  .then(orders => console.log(orders))
  .catch(error => console.log("Failed"));
```

- ⏭️ Each step **waits for the one before it**.
- 🛟 **One** `.catch` **at the end** handles an error from **any step**.

---

## 🧰 Promise combinators

### 📦 `Promise.all`: wait for **all**

> `Promise.all` takes a list of promises. It **waits until every one succeeds**. Then it gives
> you back **a single array**, with the results in the **same order** as the list.
>
> ⚠️ **If even one fails**, `Promise.all` **fails right away** with that error.

```javascript
const a = new Promise(resolve => setTimeout(() => resolve("A"), 1000));
const b = new Promise(resolve => setTimeout(() => resolve("B"), 500));

Promise.all([a, b]).then(results => {
  console.log(results); // ["A", "B"]
});
```

> 🧠 `b` finishes first, after **half a second**, but the results still come out in the
> **order you listed them**, `A` first, then `B`. The `.then` runs only after **both** are done,
> which is **one second** in.

---

### 🛡️ `Promise.allSettled`: wait for **all**, **never fails**

> It also waits for every promise, but it **never fails**. Instead, it gives you an array
> where **each entry** says whether that promise was **fulfilled** or **rejected**.

```javascript
const ok = Promise.resolve("done");
const bad = Promise.reject(new Error("oops"));

Promise.allSettled([ok, bad]).then(results => {
  console.log(results);
});
```

> 📋 The output has **one entry per promise**. The first has status `"fulfilled"` with its value,
> and the second has status `"rejected"` with its reason. **Nothing is thrown**, so you can
> see **every result**, good and bad.

---

### 🏁 `Promise.race`: the **first to finish** wins

> It takes a list of promises and settles with **whichever one finishes first**,
> whether it **succeeds or fails**.

```javascript
const slow = new Promise(resolve => setTimeout(() => resolve("slow"), 1000));
const fast = new Promise(resolve => setTimeout(() => resolve("fast"), 200));

Promise.race([slow, fast]).then(winner => {
  console.log(winner); // "fast"
});
```

> ⚡ The `fast` promise settles first, after **200 milliseconds**, so `race` resolves with its value.
> The slow one still finishes later, but `race` has **already moved on**.

---

### 🥇 `Promise.any`: the **first success** wins

> It takes a list of promises and resolves with the **first one that succeeds**.
> It **ignores failures**, unless **every** promise fails.

```javascript
const first = new Promise((_, reject) => setTimeout(() => reject("failed"), 100));
const second = new Promise(resolve => setTimeout(() => resolve("worked"), 300));

Promise.any([first, second]).then(value => {
  console.log(value); // "worked"
});
```

> 🙈 The first promise fails quickly, but `any` **skips it** and waits for the second, which succeeds.
> If **both** had failed, `any` would reject with an error that **groups all the failures** together.

---

### 🧪 `Promise.resolve` & `Promise.reject`: already settled

> These create a promise that is **already settled**, which is handy for **testing** or for
> **returning a value** from a function that doesn't need to wait.

```javascript
const done = Promise.resolve(42);
done.then(value => console.log(value)); // 42

const failed = Promise.reject(new Error("nope"));
failed.catch(error => console.log(error.message)); // "nope"
```

> ⏱️ **Nothing is pending here.** The value or error is ready right away, and `.then` or
> `.catch` picks it up.

---

## 📊 Quick comparison

| 🧰 Method | ⏳ Waits for | ✅ Resolves when | ❌ Fails when | 💻 Code sample (short) |
|---|---|---|---|---|
| 📦 `Promise.all` | **All** | **All** succeed | **Any one** fails | `Promise.all([a, b])` |
| 🛡️ `Promise.allSettled` | **All** | **All** finish (good or bad) | **Never** | `Promise.allSettled([ok, bad])` |
| 🏁 `Promise.race` | **First** | **First** settles | **First** settles with an error | `Promise.race([slow, fast])` |
| 🥇 `Promise.any` | **Until success** | **First** success | **All** fail | `Promise.any([first, second])` |

---

## 🧹 `.finally`: cleanup, always

> 🔁 `.finally` runs **once the promise settles**, whether it **succeeded or failed**.
> It's useful for **cleanup**, like hiding a loading spinner.

```javascript
fetchData()
  .then(data => console.log(data))
  .catch(error => console.log("Failed"))
  .finally(() => console.log("Done either way"));
```

> 🚫 `finally` **doesn't receive the value or the error**. It just runs at the end, and it
> **passes through** whatever the promise produced, so it **doesn't change the result**.

---

## 🎤 Interview round

> 🗣️ Answers below are in my own words. Feedback comes after each one.

### ❓ Question 1 — States and changing state

> **What are the three states of a promise, and can a settled promise change its state?**

✍️ **My answer:** Once a promise is settled, it can't change state again. If it's fulfilled, it
stays fulfilled. If it's rejected, it stays rejected. Calling `resolve` or `reject` a second time
does nothing.

---

### ❓ Question 2 — `.then` vs `.catch` vs `.finally`

> **What's the difference between `.then` and `.catch`, and what does `.finally` add?**

✍️ **My answer:** `.then` gets the resolved value, `.catch` gets the error when it's rejected, and
`.finally` is for cleanup.

🔧 **Two refinements:**
1. 🔁 `.finally` runs whether the promise succeeded or failed, and it **doesn't receive the value or the error**.
2. 🧵 "Promising" is the **object**, and "chaining" is what lets you **line up `.then` steps** one after another.

---

### ❓ Question 3 — `Promise.all` and failure

> **What does `Promise.all` do, and what happens if one of the promises fails?**

✍️ **My answer:** It waits for all promises to succeed, returns the results as an array, and
**rejects immediately** if any one of them fails.

---

### ❓ Question 4 — `Promise.all` vs `Promise.allSettled`

> **What's the difference between `Promise.all` and `Promise.allSettled`?**

✍️ **My answer:**

| 🧰 Method | 🧭 Behaviour |
|---|---|
| 📦 `Promise.all` | **Strict.** If any promise fails, it **rejects immediately** and stops reporting. It doesn't wait for the rest. |
| 🛡️ `Promise.allSettled` | Waits for **every** promise to finish. It **never rejects**. It returns an array where each entry says either `"fulfilled"` with its value, or `"rejected"` with its reason. |

> 🎯 **So the difference is:** `all` gives up at the **first failure**, while `allSettled` gives you a
> **full report** of every result, good and bad.

---

### ❓ Question 5 — When to use `race` or `any`

> **When would you choose `Promise.race` or `Promise.any` instead of `Promise.all`?**

✍️ **My answer:** `race` needs a small fix. It settles with whichever promise finishes first,
whether that's a success or a failure. So it's **not only about a success**. If the first one to
finish is a rejection, `race` **rejects too**.

📌 **The rule:**

| 🎯 Use this | ⏱️ When you care about |
|---|---|
| 🏁 `Promise.race` | **Speed**: whoever finishes first |
| 📦 `Promise.all` | **Every result**: all of them |
| 🥇 `Promise.any` | **One success**: the first that works |
