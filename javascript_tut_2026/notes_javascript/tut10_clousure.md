# 🔒 Closures

### 🎯 Tut 10 · How a function remembers the variables it was born with

---

## 🟢 What is a closure?

> 📘 **DEFINITION: Closure**
> A **closure** is when a function **remembers the variables** from the place where it was
> **created**, even **after that outer function has finished running**.

```javascript
function outer() {
  let message = "hello";
  return function inner() {
    console.log(message);
  };
}

const greet = outer();
greet(); // "hello"
```

`outer()` runs, creates `message`, and returns `inner`.

- ⚠️ Normally `message` would **disappear** once `outer` finishes.
- 🧠 But `inner` **still uses it**, so JavaScript **keeps it alive in the heap**.
- 🔒 That **kept-alive memory** is the **closure**.

> 🎒 **MENTAL MODEL: The backpack**
> Think of it as the function **carrying a backpack of variables** with it wherever it goes.

---

## 🟡 Key points

### 1️⃣ Closures capture variables, not values

> 🔑 A closure doesn't save a **copy of a value**. It keeps a **link to the variable itself**.
> So if that variable **changes later**, the closure **sees the new value**.

### 2️⃣ Closures give you private data

> 🛡️ The variable `count` in the example **can't be reached from outside**. You can only
> reach it through the functions the outer function **returns**.
> That's how you **hide data**.

### 3️⃣ Closures can use memory

> 📈 A closure keeps its variables **alive for as long as the closure exists**.
> If you hold on to **many closures**, or **big ones**, memory use can **grow**.

### 4️⃣ Loops with `var` are a trap

> 🪤 **GOTCHA:** If you create closures inside a loop that uses **`var`**, they **all share one
> variable**. That's why they **all print the final value**.
>
> ✅ Using **`let`** gives **each loop pass its own variable**.

---

## 🔴 A closure is NOT only for returned functions

> ❗ **IMPORTANT:** Any **inner function** that **uses a variable** from an **outer function** is a closure.

Here is an example. The outer function has a variable called `x`. Inside it, there is an
inner function. That inner function **uses `x`**.

| 🧩 Case | 🔁 Is it returned? | 🧹 What happens when the outer function finishes? |
|---|---|---|
| 🔸 **Inner function, not returned** | ❌ No | Nothing outside keeps it alive, so the inner function **goes away too** |
| 🔹 **Inner function, returned** | ✅ Yes | It **survives** (this is the counter case we looked at earlier) |

> 🧭 **So the returned case is just ONE type of closure.** It is **not the only type**.
