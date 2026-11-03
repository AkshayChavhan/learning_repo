# 07: useRef

> `useRef` gives you a **mutable box** `{ current: value }` that **persists across renders**.
> Changing `ref.current` **does not re-render** the component. Use refs for things that are **not on screen**: DOM access and behind-the-scenes values.

---

## 📌 Quick Reference

| Term                  | One-line definition                                                             |
| --------------------- | ------------------------------------------------------------------------------- |
| **Ref**               | An object `{ current }` that React keeps for the component's whole life         |
| `useRef(initial)`     | Creates the ref, with `current` starting as `initial`                           |
| `ref` **attribute**   | Connects a DOM element to a ref, so `ref.current` becomes that element          |
| `forwardRef`          | Lets a component pass a received ref down to a DOM element inside it            |
| `useImperativeHandle` | Chooses what the parent sees through a ref (for example, only a `focus` method) |

---

## 🟢 Beginner

### Basic example: focus an input

```jsx
import { useRef } from "react";

export default function Input() {
  const inputRef = useRef(null);

  return (
    <>
      <input ref={inputRef} />
      <button onClick={() => inputRef.current.focus()}>Focus</button>
    </>
  );
}
```

- `ref={inputRef}` connects the real `<input>` to `inputRef.current`.
- Clicking the button calls `focus()` on that input.

---

## 🟡 Intermediate

### State vs Ref

| | State (`useState`) | Ref (`useRef`) |
|---|---|---|
| Changing it re-renders? | ✅ Yes | ❌ No |
| Can be read during render? | ✅ Yes | ⚠️ Avoid (see Expert) |
| Use for | Anything shown on screen | DOM elements, timer IDs, previous values |

> **Rule of thumb:** if the value affects what's on screen, use **state**. If it's bookkeeping or direct DOM access, use a **ref**.

### Three main use cases

| Use case | Example |
|---|---|
| **1. Reach a DOM element** | Focus an input, scroll to a section, measure a size |
| **2. Keep a value across renders, no re-render** | A timer ID you need later to `clearInterval` |
| **3. Read the latest value inside callbacks** | Always read the newest value without recreating the callback |

### Example: store a timer ID

```jsx
import { useRef } from "react";

export default function Stopwatch() {
  const timerRef = useRef(null);

  function start() {
    timerRef.current = setInterval(() => console.log("tick"), 1000);
  }

  function stop() {
    clearInterval(timerRef.current); // same ID, from any render
  }

  return (
    <>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </>
  );
}
```

### Forwarding a ref: `forwardRef`

By default, a function component **does not** receive `ref` as a normal prop. `forwardRef` passes it through to a DOM element inside.

```jsx
import { forwardRef, useRef } from "react";

const FancyInput = forwardRef(function FancyInput(props, ref) {
  return <input ref={ref} className="fancy" {...props} />;
});

// Parent uses it
export default function Form() {
  const ref = useRef(null);

  return (
    <>
      <FancyInput ref={ref} />
      <button onClick={() => ref.current.focus()}>Focus</button>
    </>
  );
}
```

> **Note:** From **React 19**, `ref` is passed as a normal prop to function components, so `forwardRef` is often no longer needed. You will still see it in older code.

---

## 🔴 Expert

### Limit what the parent sees: `useImperativeHandle`

Instead of exposing the whole DOM element, the child exposes only the methods it chooses.

```jsx
import { forwardRef, useImperativeHandle, useRef } from "react";

const MyInput = forwardRef(function MyInput(props, ref) {
  const inputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
  }));

  return <input ref={inputRef} />;
});

// Parent: ref.current has ONLY focus()
// ref.current.focus();     ✅
// ref.current.value;       ❌ undefined (the input is hidden)
```

| Approach | Parent gets |
|---|---|
| `ref` directly on the DOM element | The full DOM element |
| `useImperativeHandle` | Only the methods you list |

### When is `ref.current` set?

```text
Render phase   →  ref.current is still the OLD value (or null on first render)
Commit phase   →  React attaches DOM elements to ref.current
After commit  →  safe to read ref.current (e.g., inside useEffect or event handlers)
```

> **Don't read or write** `ref.current` **during render**, except for lazy initialization. Renders should be predictable, and a ref can change without React knowing.

### Common Mistakes

| Mistake | Fix |
|---|---|
| Showing a ref's value on screen | Use **state**. Changing a ref doesn't re-render |
| `ref.current.focus()` during render | Do it in an event handler or `useEffect` (the element may not exist yet) |
| Passing `ref` to a function component on React 18 without `forwardRef` | Wrap it in `forwardRef`, or pass it under another prop name |
| Storing a value in a ref and expecting the UI to update | Use state for anything the screen shows |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is `useRef`? | Returns a mutable `{ current }` object that persists across renders and does not trigger re-renders when changed. |
| `useRef` vs `useState`? | State re-renders on change and is for what's on screen. A ref does not re-render and is for DOM access or internal values. |
| What is `forwardRef` for? | Passing a ref received by a component down to a DOM element inside it (needed in React 18; ref is a normal prop in React 19). |
| What is `useImperativeHandle` for? | Choosing what a parent can access through a ref, such as only a `focus` method. |
| When is `ref.current` available? | After the commit phase. It is `null` or stale during render. |

---

## ✅ Key Takeaways

- A **ref** = a box `{ current }` that **survives renders** and **doesn't re-render** on change.
- Use refs for **DOM access** and **internal values**. Use **state** for anything on screen.
- `forwardRef` passes a ref down (React 18). `useImperativeHandle` limits what a parent sees.
- Read `ref.current` **after** render, in handlers or effects.



Interview Round:-

Question 1: What is `useRef`, and how is it different from `useState`? Answer in your own words, and I'll give feedback.

`useRef` returns an object with a single `current` property. The key difference from `useState` is that changing `current` does not cause a re-render, while calling a state setter does.

a ref doesn’t prevent re-rendering in general. It just doesn’t cause one when you update `current`. Other state changes still re-render the component as usual.s



Question 2: What is `forwardRef` for, and why is it needed? Answer in your own words, and I'll give feedback.

`ref` isn’t passed as a normal prop, so a function component can’t receive it directly. `forwardRef` wraps the component so it gets the ref as its second argument.

One correction: the ref isn’t in props. It arrives as the second argument, separate from props. Also, when the component receives it, it usually attaches it to a DOM element inside, so the parent can reach that element.



Question 3: What does `useImperativeHandle` do, and why would you use it instead of passing the DOM element directly? Answer in your own words, and I'll give feedback.

`useImperativeHandle` controls what the parent can access through the ref.

To complete it, add why you’d do that instead of passing the DOM element. It hides the internal details, so the parent can only call the few methods you expose, like `focus`, and can’t change or reach everything else inside the child.
