# 09: useContext

> **Context** shares a value with **many components** without passing **props** through every level.
> A **Provider** supplies the value, and any child inside it reads it with **`useContext`**.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **`createContext(default)`** | Creates a context object. `default` is used only when no Provider is above the reader |
| **Provider** | `<Ctx.Provider value={...}>` supplies the value to everything inside it |
| **`useContext(Ctx)`** | Reads the nearest Provider's value. Works in any descendant |
| **Prop drilling** | Passing props through components that don't use them, just to reach a deep child |

---

## 🟢 Beginner

### The three parts

```text
1. createContext   →  create the context
2. Provider        →  supply a value to a part of the tree
3. useContext      →  read the value in any child
```

### Example: theme without props

```jsx
import { createContext, useContext } from "react";

const ThemeContext = createContext("light");   // 1. create

function Button() {
  const theme = useContext(ThemeContext);      // 3. read
  return <button className={theme}>Theme: {theme}</button>;
}

export default function App() {
  return (
    <ThemeContext.Provider value="dark">       {/* 2. supply */}
      <Button />
    </ThemeContext.Provider>
  );
}
```

```text
Theme: dark
```

- `Button` gets `"dark"` **without receiving a prop**.
- If `Button` were **outside** the Provider, it would get the default `"light"`.

---

## 🟡 Intermediate

### Prop drilling vs Context

| | Props | Context |
|---|---|---|
| Data passed through | Every level in between | Straight to the reader |
| Middle components | Must accept and forward it | Don't need to know about it |
| Good for | A few levels, explicit data flow | Shared app-wide values: theme, user, language |

```text
Props:    App → Layout → Sidebar → Menu → Item   (every level forwards `theme`)
Context:  App [Provider] ───────────────→ Item   (Item reads it directly)
```

### Reusable pattern: a custom hook

Wrap `useContext` in a hook, so readers get a clear error when they're outside the Provider:

```jsx
const ThemeContext = createContext(null);

export function useTheme() {
  const value = useContext(ThemeContext);
  if (value === null) {
    throw new Error("useTheme must be used inside ThemeProvider");
  }
  return value;
}
```

### What triggers re-renders

```text
Provider value changes (by Object.is)  →  EVERY component that calls useContext(Ctx) re-renders
                                           (even if it only uses part of the value)
```

| Value you pass | Re-renders readers when... |
|---|---|
| `value="dark"` (string) | Only when the string changes |
| `value={{ theme, user }}` (new object each render) | **Every** Provider render, because the object is new |

---

## 🔴 Expert

### Keep the value stable

Creating an object inside the Provider's render makes a new reference every time:

```jsx
// ❌ New object on every render → all consumers re-render
<ThemeContext.Provider value={{ theme, toggle }}>

// ✅ Memoize the object, so it only changes when its contents do
const value = useMemo(() => ({ theme, toggle }), [theme, toggle]);
<ThemeContext.Provider value={value}>
```

### Split unrelated data into separate contexts

```text
❌ One big context:  { theme, user, cart }   → cart update re-renders theme readers
✅ Separate:         ThemeContext, UserContext, CartContext
```

> A component that reads only `ThemeContext` won't re-render when `CartContext` changes.

### Context is not a state manager

- Context **transports** a value. It doesn't decide how the value changes.
- For complex updates, pair it with `useReducer` (or a library), and put the **dispatch** function in context. Dispatch identity is stable, so it doesn't cause re-renders by itself.

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Forgetting the Provider | Reader gets the default value silently. Use the custom hook to throw an error |
| New object in `value` every render | `useMemo` the value |
| One context for everything | Split by concern |
| Using context for fast-changing values (every keystroke) | Keep that state local, or pass it as a prop to the components that need it |
| Expecting `memo` on a child to block context updates | A consumer still re-renders when its context value changes |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is context for? | Sharing a value with many components without prop drilling. |
| What are the three parts? | `createContext`, a `Provider` that supplies `value`, and `useContext` to read it. |
| What does the default value in `createContext` do? | It's used only when there is no Provider above the reader. |
| What causes consumers to re-render? | A change to the Provider's `value` (compared with `Object.is`). Every consumer re-renders, even if it uses only part of the value. |
| How do you avoid unnecessary re-renders? | Keep the value stable with `useMemo`, and split unrelated data into separate contexts. |

---

## ✅ Key Takeaways

- Context = **shared value** without **prop drilling**.
- **Provider** supplies, **`useContext`** reads.
- Any change to the **value** re-renders **all consumers**. Keep the value **stable** and **small**.
- Split contexts by concern. Context carries values. It doesn't manage complex state by itself.
