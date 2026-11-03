# 04: State & Props

> **Props** are data a parent **passes down** to a child (read-only).
> **State** is data a component **owns** and changes with a **setter** (`useState`).
> Rule of thumb: **if the value comes from outside, it's a prop. If the component decides when it changes, it's state.**

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Props** | Read-only inputs a parent passes to a child, as attributes |
| **State** | Data a component owns and can change over time |
| **`useState`** | Hook that gives a component state. Returns `[value, setter]` |
| **Setter** | The function (`setCount`) that changes state and triggers a re-render |
| **Re-render** | React calling the component function again with the new values |

---

## 🟢 Beginner

### State: a value that can change

```jsx
import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

```text
Clicked 0 times   → click →   Clicked 1 times   → click →   Clicked 2 times
```

- `useState(0)` sets the **starting value** to `0`.
- `count` is the **current value**.
- `setCount` is the **only** way to change it. Calling it **re-renders** the component.

### Props: data passed from parent to child

```jsx
function Child({ message }) {
  return <p>{message}</p>;
}

function Parent() {
  return <Child message="Hello from parent" />;
}
```

```text
Hello from parent
```

- The parent writes `message="..."` as an **attribute**.
- The child reads it from its **props object**. Here it is destructured as `{ message }`.

---

## 🟡 Intermediate

### Props vs State

| | Props | State |
|---|---|---|
| Where it comes from | The **parent** | The **component itself** |
| Can the component change it? | ❌ No, read-only | ✅ Yes, with the setter |
| Changes cause | Parent re-renders with new values | Calling the setter |
| Typical use | Pass data and settings down | Track things that change over time (input text, toggles, counts) |

**Decision test:**

```text
Does the value come from outside?      → use a PROP
Does this component decide when it changes? → use STATE
```

### The setter does not update right away

```jsx
function handleClick() {
  setCount(count + 1);
  console.log(count); // still the OLD value
}
```

The new value shows up on the **next render**, not on the next line of code.

**If the new value depends on the old one, use the function form:**

```jsx
setCount(prev => prev + 1); // receives the latest value
```

> Calling `setCount(prev => prev + 1)` twice in a row adds 2. Calling `setCount(count + 1)` twice in one handler adds only 1.

### Changing state the wrong way

| ❌ Wrong | ✅ Right | Why |
|---|---|---|
| `count = count + 1` | `setCount(count + 1)` | Direct change doesn't tell React to re-render |
| `items.push(x)` | `setItems([...items, x])` | Mutating the same array means React may not notice |
| `user.name = "Ravi"` | `setUser({ ...user, name: "Ravi" })` | Create a new object, don't change the old one |

### Props are read-only

A child **must not** change its props. If it needs a change, it asks the parent through a **callback prop**:

```jsx
function Child({ onAdd }) {
  return <button onClick={onAdd}>Add</button>;
}

function Parent() {
  const [count, setCount] = useState(0);

  return (
    <>
      <p>{count}</p>
      <Child onAdd={() => setCount(count + 1)} />
    </>
  );
}
```

```text
Data flows DOWN:  Parent → Child (props)
Events flow UP:   Child → Parent (callback props)
```

---

## 🔴 Expert

### What happens when a setter is called

```text
setCount(...)  →  React schedules a re-render
              →  component function runs again → new JSX
              →  reconciliation (diff) → only changed nodes hit the real DOM
```

- Calling the setter is a **signal** to React. Without it, React doesn't know to update the screen.
- Multiple setter calls in one event are **batched** into a single re-render.

### Re-render cascade

| Event | What re-renders |
|---|---|
| A component's state changes | That component, and **all its children** by default |
| A parent's state changes | The parent, and its children that receive new JSX |
| A child's state changes | Only that child (its parent is not re-run) |

> Children re-render by default when the parent re-renders, even if their props didn't change. Tools like `React.memo` can skip this. Covered in the performance note.

### Why props must be read-only

- React compares **old** and **new** props to decide what to update.
- If a child mutates a prop, the parent does not know, and the UI can fall out of sync.
- Keeping data owned in **one place** (the parent or the component with state) keeps the app predictable.

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Reading state right after the setter | The value updates on the next render. Use the new value in the next render or use `prev =>` |
| Mutating state (`push`, `obj.x = ...`) | Create a new array or object and pass it to the setter |
| Changing a prop inside the child | Use a callback prop to ask the parent to change its state |
| Storing a value that can be calculated | Compute it from existing state or props instead |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is a component, compared to a plain function? | A function used as a JSX tag (`<Greeting />`) that React calls during rendering. Its name starts with a capital letter. |
| What are props, and why are they read-only? | Data passed from the parent. React relies on stable props to detect changes. If a child mutated them, the UI could go out of sync. |
| What is state, and how does it differ from props? | Data owned by the component, changed through its setter. Props come from outside. |
| What happens when you call the setter? | It updates the stored value and tells React to re-render. Changing state directly skips that signal. |
| How do you decide between props and state? | If the parent controls the value, use a prop. If the component decides when it changes, use state. |
| What happens to a child when the parent's state changes? | The parent re-renders, so the child re-renders too (unless memoized). Reconciliation updates only the changed DOM. |
| How do props flow? | Parent → child, as attributes. If the child needs a change, it calls a callback prop the parent passed in. |

---

## ✅ Key Takeaways

- **Props** = read-only, **from the parent**. **State** = owned, **changed by the setter**.
- Use the **setter**, never mutate state directly. Use `prev =>` when the new value depends on the old one.
- Data flows **down** through props. Events flow **up** through callback props.
- A re-render runs the component function again, and its children re-render by default.
