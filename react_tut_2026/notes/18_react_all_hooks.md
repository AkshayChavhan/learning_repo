# 18: All React Hooks

> **Hooks** let function components use React features: state, side effects, context, refs, performance tools, and more.
> Hooks **must be called at the top level** of a component or custom hook, never inside loops, conditions, or nested functions (except `use`).

---

## 📌 Quick Reference: all hooks at a glance

| Hook | Group | One-line purpose | Note |
|---|---|---|---|
| `useState` | State | Stores a value. Changing it re-renders | 04 |
| `useReducer` | State | Manages related state through a reducer and actions | 10 |
| `useEffect` | Effects | Runs side effects after render | 05 |
| `useLayoutEffect` | Effects | Like `useEffect`, but runs before the browser paints | this note |
| `useInsertionEffect` | Effects | Injects styles before layout. For library authors | this note |
| `useContext` | Context | Reads the nearest Provider's value | 09 |
| `useRef` | Refs | A mutable `{ current }` box that doesn't re-render | 07 |
| `useImperativeHandle` | Refs | Chooses what a parent sees through a ref | 07 |
| `useMemo` | Performance | Caches a computed value | 06 |
| `useCallback` | Performance | Caches a function reference | 06 |
| `useTransition` | Concurrent | Marks an update as low priority | this note |
| `useDeferredValue` | Concurrent | Lets a value lag behind for smoother rendering | this note |
| `useId` | Utility | Generates a unique, stable ID | this note |
| `useSyncExternalStore` | External data | Subscribes to data outside React | this note |
| `useDebugValue` | Debugging | Labels a custom hook in DevTools | this note |
| `use` | Async / context | Reads a promise or context. Can be conditional | this note |
| `useActionState` | Forms / actions | Tracks the state and result of an action | this note |
| `useOptimistic` | Forms / actions | Shows an expected value while an update is pending | this note |
| `useFormStatus` | Forms (`react-dom`) | Reads the pending state of the parent form | this note |

---

## 🟢 Beginner: the everyday hooks

### `useState`: a component's memory

```jsx
const [count, setCount] = useState(0);
// count = current value, setCount = changes it and re-renders
```

### `useEffect`: work after render

```jsx
useEffect(() => {
  document.title = `Count: ${count}`;
  return () => { /* cleanup */ };
}, [count]);
```

| Dependency array | When the effect runs |
|---|---|
| *(none)* | After every render |
| `[]` | Once, after the first render (mount) |
| `[a, b]` | After mount, and when `a` or `b` changes |

- The **returned function** is the cleanup. It runs before the next effect, and on unmount.

### `useContext`: read a shared value

```jsx
const ThemeContext = createContext("light");

function Button() {
  const theme = useContext(ThemeContext);      // "dark" below
  return <button className={theme}>Click</button>;
}

<ThemeContext.Provider value="dark">
  <Button />
</ThemeContext.Provider>
```

---

## 🟡 Intermediate: state, refs, and performance

### `useReducer`: state with actions

```jsx
function reducer(state, action) {
  switch (action.type) {
    case "increment": return { count: state.count + 1 };
    case "reset":     return { count: 0 };
    default:          return state;
  }
}

const [state, dispatch] = useReducer(reducer, { count: 0 });
dispatch({ type: "increment" });
```

### `useRef`: a box that doesn't re-render

```jsx
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus();
```

| Ref pattern | Purpose |
|---|---|
| `ref` on a DOM element | Access the element (focus, scroll, measure) |
| `forwardRef` | Receive a ref from the parent and pass it down |
| `useImperativeHandle` | Expose only chosen methods to the parent |

```jsx
const FancyInput = forwardRef(function FancyInput(props, ref) {
  return <input ref={ref} {...props} />;   // ref is the second argument
});

const MyInput = forwardRef(function MyInput(props, ref) {
  const inputRef = useRef(null);
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),  // parent only gets focus()
  }));
  return <input ref={inputRef} />;
});
```

### `useMemo` and `useCallback`: keep values stable

```jsx
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items]);
const handleClick = useCallback(() => console.log(count), [count]);
```

- `useMemo` caches a **value**. `useCallback` caches a **function**.
- Useful when passing values to a `memo` child or using them in an effect's dependencies.
- Details: see note 06.

---

## 🔴 Expert: layout, concurrency, external data, and forms

### `useLayoutEffect`: run before paint

```jsx
useLayoutEffect(() => {
  const height = boxRef.current.offsetHeight;   // measure
  // adjust layout here, before the user sees the frame
}, []);
```

| | `useEffect` | `useLayoutEffect` |
|---|---|---|
| Runs | After paint | After DOM update, **before** paint |
| Use for | Most side effects | Measuring or fixing layout without a flicker |

### `useInsertionEffect`: for CSS-in-JS libraries

Runs before layout effects, so a library can inject `<style>` rules before the DOM reads them. Application code rarely needs it. It can't access refs or state.

### `useId`: stable unique IDs

```jsx
function Field() {
  const id = useId();
  return (
    <>
      <label htmlFor={id}>Email</label>
      <input id={id} />
    </>
  );
}
```

- The same ID on the server and client, so it's safe for hydration.
- Use it for `id`, `htmlFor`, and ARIA attributes. Don't use it for list `key`s.

### `useTransition`: keep typing responsive

```jsx
import { useState, useTransition } from "react";

export default function Search({ items }) {
  const [query, setQuery] = useState("");
  const [filtered, setFiltered] = useState(items);
  const [isPending, startTransition] = useTransition();

  function handleChange(e) {
    const value = e.target.value;
    setQuery(value);                        // urgent: input updates now
    startTransition(() => {
      setFiltered(items.filter(item => item.includes(value)));  // low priority
    });
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <p>Updating...</p>}
      <ul>
        {filtered.map(item => <li key={item}>{item}</li>)}
      </ul>
    </>
  );
}
```

```text
Type "a" → input shows "a" immediately; list updates in the background
```

### `useDeferredValue`: lag a value behind

```jsx
const deferredQuery = useDeferredValue(query);
// use deferredQuery for the slow list; query for the input
```

| | `useTransition` | `useDeferredValue` |
|---|---|---|
| Works on | An update you wrap | A value you already have |
| Gives you | `isPending` and `startTransition` | A value that may be older |

### `useSyncExternalStore`: subscribe to outside data

```jsx
// Define subscribe OUTSIDE the component, so its identity is stable
function subscribe(callback) {
  window.addEventListener("resize", callback);
  return () => window.removeEventListener("resize", callback);
}

function WindowWidth() {
  const width = useSyncExternalStore(subscribe, () => window.innerWidth);
  return <p>Width: {width}</p>;
}
```

> Use it for browser APIs and external stores. Prefer normal state for data React owns.

### `useDebugValue`: label for DevTools

```jsx
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  // ... subscribe with an effect ...
  useDebugValue(isOnline ? "Online" : "Offline");   // shows in DevTools only
  return isOnline;
}
```

### `use`: read a promise or context, conditionally

```jsx
// Read a promise: suspends until it resolves (needs a Suspense boundary)
function Comments({ commentsPromise }) {
  const comments = use(commentsPromise);
  return <ul>{comments.map(c => <li key={c.id}>{c.text}</li>)}</ul>;
}

// Read a context inside a condition (useContext can't do this)
if (show) {
  const theme = use(ThemeContext);
}
```

> Create the promise **outside** the component (or cache it). Creating a new promise on every render causes an endless suspend loop.

### `useActionState`: track a form action's result

```jsx
import { useActionState } from "react";

async function submitName(prevState, formData) {
  const name = formData.get("name");
  return name ? { message: `Saved ${name}` } : { message: "Name required" };
}

function NameForm() {
  const [state, formAction, isPending] = useActionState(submitName, { message: "" });

  return (
    <form action={formAction}>
      <input name="name" />
      <button disabled={isPending}>Save</button>
      <p>{state.message}</p>
    </form>
  );
}
```

### `useOptimistic`: show the expected value first

```jsx
import { useOptimistic, useState } from "react";

async function saveName(newName) {
  await new Promise(resolve => setTimeout(resolve, 1000));   // fake slow save
}

export default function NameEditor() {
  const [name, setName] = useState("Ravi");
  const [optimisticName, setOptimisticName] = useOptimistic(name);

  async function handleSubmit(formData) {
    const newName = formData.get("name");
    setOptimisticName(newName);     // shows immediately
    await saveName(newName);
    setName(newName);               // store the real value
  }

  return (
    <form action={handleSubmit}>
      <p>Current: {optimisticName}</p>
      <input name="name" />
      <button>Save</button>
    </form>
  );
}
```

- The screen shows `optimisticName` while the save is pending.
- If the action fails before `setName`, React **reverts** to the real `name` once the action finishes.

### `useFormStatus`: the parent form's pending state

```jsx
import { useFormStatus } from "react-dom";

function SubmitButton() {
  const { pending } = useFormStatus();   // reads the nearest parent <form>
  return <button disabled={pending}>{pending ? "Saving..." : "Save"}</button>;
}

<form action={saveAction}>
  <input name="name" />
  <SubmitButton />                       {/* must be INSIDE the form */}
</form>
```

- The child must sit **inside** the `<form>`. It reads the status of the nearest form above it.
- It does **not** work in the component that renders the `<form>` itself.

---

## 🧭 Rules of Hooks

| Rule | Why |
|---|---|
| Call hooks at the **top level** | React relies on the same hooks running in the same order each render |
| Call hooks only in **components or custom hooks** | Hooks need React's render context |
| Custom hooks start with `use` | Lets linters check the rules |
| Exception: **`use`** can be conditional | It doesn't depend on call order the same way |

> Enable `eslint-plugin-react-hooks` to catch violations and missing dependencies.

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Calling a hook inside `if` or a loop | Move it to the top level |
| Missing dependency in `useEffect`, `useMemo`, `useCallback` | Add it, or use the lint rule |
| Creating a promise inside a component for `use` | Create it outside, or cache it |
| Defining `subscribe` inside the component for `useSyncExternalStore` | Define it outside |
| Using `useState` for values that should not re-render | Use `useRef` |
| Using `useRef` for values the screen shows | Use `useState` |
| Using `useFormStatus` in the form's own component | Put it in a child inside the form |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What are hooks? | Functions that let function components use state, effects, context, refs, and other React features. |
| Why must hooks be called at the top level? | React matches hook calls to their state by call order, so the order must stay the same each render. |
| `useEffect` vs `useLayoutEffect`? | `useEffect` runs after paint. `useLayoutEffect` runs before paint, for layout measurements. |
| `useMemo` vs `useCallback`? | `useMemo` caches a value. `useCallback` caches a function. |
| `useTransition` vs `useDeferredValue`? | `useTransition` wraps an update as low priority. `useDeferredValue` gives a lagging copy of a value. |
| What does `use` add? | It reads promises and context, and it can be called conditionally. |
| What does `useOptimistic` do? | It shows an expected value during a pending action, then reverts or updates to the real value. |
| What does `useFormStatus` need? | To be rendered inside the `<form>`. It reads the nearest parent form's status. |

---

## ✅ Key Takeaways

- Hooks fall into groups: **state**, **effects**, **context**, **refs**, **performance**, **concurrent**, **external data**, **forms**, and **debugging**.
- Start with `useState`, `useEffect`, `useContext`, `useRef`, `useMemo`, and `useCallback`. Learn the others when you need them.
- Always follow the **rules of hooks**, and keep dependency arrays complete.
