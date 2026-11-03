# 06: useMemo & useCallback

> **`useMemo`** remembers a **value** between renders.
> **`useCallback`** remembers a **function** between renders.
> Both skip recreating something when its dependencies haven't changed. Use them to keep references **stable**, not to make every value faster.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Memoization** | Remembering a result between renders so React doesn't recompute or recreate it |
| **`useMemo(fn, deps)`** | Returns the **result** of `fn`. Re-runs `fn` only when `deps` change |
| **`useCallback(fn, deps)`** | Returns the **same function instance** until `deps` change |
| **Referential equality** | Two values are equal only if they are the **same reference** (`{} !== {}`) |
| **`memo(Component)`** | Skips a child's render if its props are shallowly equal |

---

## 🟢 Beginner

### Why this is needed

Every render runs the component function from the top. Anything created inside it is **new** every time, even if the contents are identical.

```jsx
function Parent() {
  const config = { id: 1 };       // new object on every render
  const onSelect = () => {};      // new function on every render
}
```

```text
Render 1:  config → object at address A      onSelect → function at address X
Render 2:  config → object at address B      onSelect → function at address Y
           A !== B                           X !== Y    (same contents, different references)
```

### `useMemo`: remember a value

```jsx
const total = useMemo(
  () => items.reduce((sum, item) => sum + item.price, 0),
  [items]
);
```

- The function runs **only when `items` changes**.
- On other renders, React returns the **saved result**.

### `useCallback`: remember a function

```jsx
const handleClick = useCallback(() => {
  console.log(count);
}, [count]);
```

- Returns the **same function** until `count` changes.

---

## 🟡 Intermediate

### The two hooks are related

```jsx
useCallback(fn, deps)  ===  useMemo(() => fn, deps)
```

| | `useMemo` | `useCallback` |
|---|---|---|
| Remembers | Any value (number, object, array, function result) | A function |
| Returns | The computed value | The function itself |
| Typical use | Expensive calculation, or a stable object/array | A function passed to a memoized child or used in an effect's dependencies |

### Why a child re-renders: and how `memo` stops it

```text
Parent re-renders
   │
   ▼
New props created (new object, new function)
   │
   ▼
memo(Child) compares props: references changed?  → YES → Child re-renders
                                                 → NO  → Child skipped
```

- **`memo`** does the skipping. It compares each prop with `===` (shallow comparison).
- **`useMemo` / `useCallback`** keep the references the same, so `memo` has something to skip.
- You need **both**. `memo` alone with new props does nothing. Hooks alone without `memo` also don't skip the child.

### Full example: a stable child

```jsx
import { useMemo, useCallback, memo, useState } from "react";

const Child = memo(function Child({ config, items, onSelect }) {
  console.log("Child rendered");
  return <p>{config.id} · {items.join(", ")}</p>;
});

export default function Parent() {
  const [count, setCount] = useState(0);

  const config = useMemo(() => ({ id: 1 }), []);
  const items = useMemo(() => ["a", "b"], []);
  const onSelect = useCallback((id) => console.log(id), []);

  return (
    <>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <Child config={config} items={items} onSelect={onSelect} />
    </>
  );
}
```

```text
Child rendered          ← first mount only
(click button → count changes → Parent re-renders)
(no "Child rendered" log, because all props kept the same references)
```

> Without the hooks, `config`, `items`, and `onSelect` would be new on every click, and `Child` would log again.

---

## 🔴 Expert

### Dependency arrays must be complete

```jsx
// ❌ Stale value: handleClick always sees the first count
const handleClick = useCallback(() => console.log(count), []);

// ✅ Include every value the function reads
const handleClick = useCallback(() => console.log(count), [count]);
```

> The `react-hooks/exhaustive-deps` lint rule catches missing dependencies.

### React may discard the cache

The React docs describe `useMemo` as a **performance hint**, not a guarantee. React may throw away a cached value and recompute it. Your code must still be correct if it recomputes.

### Memoization has a cost

| Cost | Why |
|---|---|
| Memory | React stores the cached value and dependencies |
| Comparison | React compares dependencies on every render |
| Complexity | More code and more dependency arrays to keep correct |

> If the value is cheap to compute and nothing depends on its reference, skip the hook.

### Newer React versions can do this automatically

The **React Compiler** can add memoization for you in supported setups. Learn the manual hooks first, because they explain what the compiler is doing.

---

## ⚠️ When NOT to use them

| Situation | Better choice |
|---|---|
| Simple value like `const x = a + 1` | Just compute it |
| Component re-renders rarely | Skip memoization |
| Child is **not** wrapped in `memo` | Stable props won't prevent a render |
| Preventing every render "just in case" | Measure first, then optimize |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| Why does a function or object in a component cause a child to re-render? | Each render creates new references. The child sees changed props, so it re-renders. |
| How does `memo` help? | `memo` compares props shallowly. If they're equal, it skips the render. |
| What is the difference between `useMemo` and `useCallback`? | `useMemo` caches any value. `useCallback` caches a function. `useCallback(fn, deps)` equals `useMemo(() => fn, deps)`. |
| When should you avoid them? | When the computation is cheap, the component rarely re-renders, or the child isn't memoized. Extra memoization has its own cost. |

---

## ✅ Key Takeaways

- **`useMemo`** = remember a **value**. **`useCallback`** = remember a **function**.
- They keep **references stable**. A **`memo`** child then skips its render.
- You need **both** `memo` and the hooks for the skip to happen.
- Include **every dependency**, and don't use them everywhere by default.
