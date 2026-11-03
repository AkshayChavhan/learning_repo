# 05: useEffect

> **`useEffect`** runs code **after** a component renders. Use it for **side effects**: things that reach outside the component, like fetching data, timers, subscriptions, or changing the page title.
> Rendering should only **describe** the UI. Effects are where you **do** things.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Side effect** | Work that touches something outside the component (network, timers, DOM, subscriptions) |
| **Effect** | The function you pass to `useEffect`. It runs after render |
| **Dependency array** | The second argument. Tells React when to re-run the effect |
| **Cleanup** | A function returned from the effect. It stops whatever the effect started |

---

## 🟢 Beginner

### Basic syntax

```jsx
import { useEffect } from "react";

useEffect(() => {
  // runs after the component renders
}, []); // dependency array
```

### Example: a clock

```jsx
import { useEffect, useState } from "react";

function Clock() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id); // cleanup
  }, []);

  return <p>{time.toLocaleTimeString()}</p>;
}
```

```text
10:15:01
10:15:02   ← updates every second
10:15:03
```

- The effect starts a timer **once** (because the array is `[]`).
- The cleanup stops the timer when the component leaves the screen.

---

## 🟡 Intermediate

### The dependency array decides when the effect runs

| Dependency array | When the effect runs |
|---|---|
| `[]` (empty) | Once, after the first render |
| `[count]` | After the first render, and again **each time `count` changes** |
| *(left out)* | After **every** render (usually not what you want) |

```jsx
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]); // runs when count changes
```

> **Rule:** list every value the effect **reads** from the component (props, state) in the array. ESLint's `react-hooks/exhaustive-deps` rule checks this for you.

### Cleanup

The function you **return** from the effect runs:

- **before** the effect runs again (when a dependency changed), and
- **when the component unmounts** (is removed from the screen).

```jsx
useEffect(() => {
  const handler = () => console.log("resized");
  window.addEventListener("resize", handler);

  return () => window.removeEventListener("resize", handler); // cleanup
}, []);
```

> Without cleanup, the listener stays attached after the component is gone, which causes leaks and bugs.

### Common Mistake: infinite loop

```jsx
// ❌ No dependency array: runs after every render
useEffect(() => {
  setCount(count + 1);
});
```

**What happens:** `setCount` → re-render → effect runs → `setCount` → re-render → …

```text
render → effect → setCount → render → effect → setCount → …  (forever)
```

**Fix:** give the effect the array it needs, or don't update state there at all.

### Fetching data (with a cleanup guard)

```jsx
useEffect(() => {
  let ignore = false;

  fetch(`/api/users/${id}`)
    .then(res => res.json())
    .then(data => {
      if (!ignore) setUser(data);   // ignore stale responses
    });

  return () => { ignore = true; };
}, [id]);
```

> If `id` changes quickly, an older response could arrive last. The `ignore` flag stops it from overwriting newer data.

---

## 🔴 Expert

### When the effect runs

```text
Render (JSX computed)
   │
   ▼
Commit (DOM updated)
   │
   ▼
Browser paints the screen
   │
   ▼
useEffect runs  ← after paint, so it does not block the first view
```

| Hook | When it runs | Use when |
|---|---|---|
| `useEffect` | After paint | Most side effects: fetch, timers, subscriptions |
| `useLayoutEffect` | After DOM update, **before** paint | You must measure or change layout before the user sees it |

### Strict Mode runs effects twice (development only)

With `<StrictMode>`, React mounts, runs cleanup, and mounts again. This helps you find missing cleanups.

> If your effect shows a bug on the second run, the cleanup is probably missing or incomplete.

### Effects are not for derived values

```jsx
// ❌ Unnecessary effect and an extra render
const [fullName, setFullName] = useState("");
useEffect(() => setFullName(first + " " + last), [first, last]);

// ✅ Compute it during render
const fullName = first + " " + last;
```

> If a value can be calculated from props or state, calculate it during render. Don't store it in state through an effect.

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| No dependency array when it's needed | Add the array with every value the effect uses |
| Missing a dependency | Add it, or use the lint rule to find it |
| No cleanup for timers / listeners / subscriptions | Return a cleanup function |
| Setting state with no condition in an effect with no array | Add a dependency array, or set state only when a condition is met |
| Using an effect to compute a value from state | Compute it during render |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is `useEffect` for? | Running side effects after render, such as fetching data, timers, and subscriptions. |
| What does the dependency array do? | `[]` runs once. `[a, b]` re-runs when `a` or `b` changes. No array runs after every render. |
| When does cleanup run? | Before the effect re-runs, and when the component unmounts. |
| `useEffect` vs `useLayoutEffect`? | `useEffect` runs after paint. `useLayoutEffect` runs before paint, for layout-sensitive work. |
| Why can an effect cause an infinite loop? | If it sets state on every run, that causes a re-render, which runs the effect again. |

---

## ✅ Key Takeaways

- `useEffect` = **run side effects after render**.
- The **dependency array** controls when it runs. List everything the effect uses.
- Always **return a cleanup** for timers, listeners, and subscriptions.
- Don't use effects to compute values. **Compute during render.**
