Sure, Akshay, here's the full list in the same style.

useState stores a value in a component, and changing it re-renders the component.

useEffect runs side effects after render, like fetching data or setting up a subscription.

useContext reads a value from the nearest context provider.

useReducer manages state through a reducer function and dispatched actions.

useRef holds a mutable value that doesn't cause a re-render, often used to reach a DOM element.

useMemo caches a computed value until its dependencies change.

useCallback caches a function reference until its dependencies change.

useLayoutEffect is like useEffect, but it runs before the browser paints.

useImperativeHandle controls what a parent can access through a ref.

useInsertionEffect runs style-injection code before the DOM is changed. It's mainly for library authors.

useId creates a unique, stable ID for accessibility attributes.

useTransition marks an update as low priority, so urgent updates stay responsive.

useDeferredValue lets a value update a little later, for smoother rendering.

useSyncExternalStore subscribes to an external store.

useDebugValue adds a label to a custom hook in React DevTools.

use reads a promise or a context during rendering, and it can be called inside conditions and loops.

useActionState tracks the state and result of a form action.

useOptimistic shows an expected value immediately while a real update is pending.

useFormStatus, from react-dom, gives a child component the pending state of its parent form.

Sure, Akshay. We'll go one at a time. The first is useState.

useState gives a component its own memory. You call it with an initial value, and it returns the current value and a setter function. When you call the setter, React re-renders the component with the new value.

```jsx
const [count, setCount] = useState(0);
```

Good. Next is useEffect. It runs side effects after the component renders, such as fetching data, setting up a timer, or subscribing to an event. You control when it runs with the dependency array, and you can return a cleanup function to undo what it started.

```jsx
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);
```

Good point, Akshay. With `useEffect`, you can map the component lifecycle like this.

Mount: an effect with an empty dependency array runs once, after the first render.

Update: an effect with dependencies runs again whenever one of those values changes. With no array, it runs after every render.

Unmount: the function you return from the effect runs as cleanup when the component is removed.

```jsx
useEffect(() => {
  console.log("mounted or updated");
  return () => console.log("cleanup on unmount or before next run");
}, [count]);
```

 Right, Akshay. Here's what each dependency array setting does.

No array at all: the effect runs after every render.

An empty array: the effect runs only once, after the first render, like mount.

An array with values: the effect runs after the first render, and again whenever any listed value changes, compared by reference.

One detail to remember: every value the effect uses from the component should be in the array. If you leave one out, the effect can use an outdated value.

useContext reads the value from the nearest provider of a context above the component. You don’t need to pass the value through props at each level.
The component re-renders whenever that provider’s value changes.

You're right, Akshay. Here's the full pattern, with the context created and provided.

```jsx
import { createContext, useContext } from "react";

const ThemeContext = createContext("light");

function Button() {
  const theme = useContext(ThemeContext);
  return ;
}

export default function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Button />
    
  );
}
```

`createContext` makes the context with a default value, "light". The provider in `App` supplies "dark" to everything inside it. `Button` reads that value with `useContext`, so it gets "dark" without any props.


useReducer manages state through a reducer function. You pass it the reducer and an initial value, and it returns the current state plus a dispatch function. You call dispatch with an action, and the reducer returns the next state.


You're right, Akshay. Here's the complete pattern, with the reducer defined.

```jsx
import { useReducer } from "react";

function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };
    case "reset":
      return { count: 0 };
    default:
      return state;
  }
}

export default function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <>
      {state.count}
      
      
    </>
  );
}
```

The reducer decides the next state based on the action type, and the component sends actions through dispatch.

Good. Next is useRef.

useRef returns a box with a single current property. Changing current doesn't re-render the component, so it's good for holding values you need across renders without triggering updates, most often a DOM element.

```jsx
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus();
```

Good point, Akshay. forwardRef lets a component receive a ref from its parent and pass it down to a DOM element inside.

Normally a ref can't be passed to a function component, because React keeps it separate from props. forwardRef wraps the component so it gets the ref as a second argument.

```jsx
import { forwardRef } from "react";

const FancyInput = forwardRef(function FancyInput(props, ref) {
  return <input ref={ref} {...props} />;
});

// in the parent
const inputRef = useRef(null);
<FancyInput ref={inputRef} />;
```

The parent's ref lands on the real input, so the parent can focus it.

Sure, Akshay. Here's how it fits together with useImperativeHandle.

Inside the child, you wrap the component in forwardRef, so it receives the parent's ref. Then useImperativeHandle decides what goes into that ref. Instead of the whole input, the parent gets only the methods you choose.

```jsx
const MyInput = forwardRef(function MyInput(props, ref) {
  const inputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
  }));

  return <input ref={inputRef} />;
});

// in the parent
const myRef = useRef(null);
<MyInput ref={myRef} />;
myRef.current.focus();
```

The parent calls `focus`, which runs the input's focus method inside the child. The parent never touches the input directly.


Good. Next is useMemo. It caches a computed value and only recalculates it when one of its dependencies changes. It's useful for expensive calculations.

```jsx
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items]);
```

Good. Next is useCallback. It caches a function reference, so the same function is passed on each render until its dependencies change. That matters when you pass a function to a memoized child.

```jsx
const handleClick = useCallback(() => console.log(count), [count]);
```

Good. Next is useLayoutEffect. It works like useEffect, but it runs synchronously after the DOM updates and before the browser paints. Use it when you need to measure or adjust the layout, so the user doesn't see a flicker.

```jsx
useLayoutEffect(() => {
  const height = boxRef.current.offsetHeight;
  console.log(height);
}, []);
```

Good. Next is useId. It generates a unique, stable ID for a component, which is useful for linking a label to an input, especially when the same component appears more than once.

```jsx
const id = useId();

<input id={id} />
```

The ID stays the same across renders, and it's unique on the page.

useTransition. It marks an update as low priority, so urgent updates, like typing, stay responsive while the slower one renders in the background.

Here's a search filter where typing stays smooth and a spinner shows during the slower update:

```jsx
import { useState, useTransition } from "react";

export default function Search({ items }) {
  const [query, setQuery] = useState("");
  const [filtered, setFiltered] = useState(items);
  const [isPending, startTransition] = useTransition();

  function handleChange(e) {
    setQuery(e.target.value);
    startTransition(() => {
      setFiltered(items.filter(item => item.includes(e.target.value)));
    });
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && Updating...}
      
        {filtered.map(item => {item})}
      
    </>
  );
}
```

The input updates immediately with `setQuery`, so typing feels instant. The filter list update is wrapped in `startTransition`, so React can delay it if needed. While it's pending, `isPending` is true and "Updating..." shows.

Good. Next is useDeferredValue. It gives you a copy of a value that can lag behind the latest one, so a slow render can use the older value while the new one catches up.

```jsx
const deferredQuery = useDeferredValue(query);
```

It's similar to useTransition, but it works on a value you already have, instead of wrapping an update.

Good. Next is useSyncExternalStore. It lets a component subscribe to data that lives outside React, like a browser API or a third-party store, and re-renders when that data changes.

```jsx
const width = useSyncExternalStore(subscribe, () => window.innerWidth);
```

You pass a subscribe function and a function that reads the current value.

Good. Next is useDebugValue. It adds a label to a custom hook in React DevTools, so you can see its state while debugging. It doesn't affect how the app behaves.

```jsx
useDebugValue(isOnline ? "Online" : "Offline");
```

Good. Next is `use`. It reads a promise or a context during rendering. Unlike other hooks, it can be called inside conditions and loops.

```jsx
const theme = use(ThemeContext);
```

Good question, Akshay. The main use is reading a promise. You pass it a promise, and the component suspends until it resolves, with a Suspense boundary showing a fallback.

```jsx
function Comments({ commentsPromise }) {
  const comments = use(commentsPromise);
  return {comments.map(c => {c.text})};
}
```

The other use is reading a context, the same way useContext does, but with the flexibility to call it conditionally.

```jsx
if (show) {
  const theme = use(ThemeContext);
}
```

Here's a full example. A name shows the new value immediately while the save is still running.

```jsx
import { useOptimistic, useState } from "react";

async function saveName(newName) {
  await new Promise(resolve => setTimeout(resolve, 1000));
}

export default function NameEditor() {
  const [name, setName] = useState("Ravi");
  const [optimisticName, setOptimisticName] = useOptimistic(name);

  async function handleSubmit(formData) {
    const newName = formData.get("name");
    setOptimisticName(newName);
    await saveName(newName);
    setName(newName);
  }

  return (
    
  );
}
```

When you submit, `setOptimisticName` shows the new name right away. The `saveName` call takes a second. Then `setName` stores the real value. Until then, the screen shows the optimistic value.

If the save failed and you never called `setName`, React would fall back to the real name.

Good, Akshay. Next is useFormStatus. It's from react-dom, and a child component inside a form can use it to read whether that form is currently submitting.

```jsx
import { useFormStatus } from "react-dom";

function SubmitButton() {
  const { pending } = useFormStatus();
  return ;
}
```

The button disables itself while the parent form is pending, without the form having to pass that down as a prop.

React tracks the form's submission. When a form with an `action` is submitted, React marks that form as pending until the action finishes. `useFormStatus` reads that state from the nearest parent form.

So the flow is: the user submits, React sets pending to true for that form, the action runs, and when it finishes, pending goes back to false. Any child component using `useFormStatus` re-renders with the new value.

Important point: `useFormStatus` only works in a component rendered inside the form, not in the component that owns the form.

No, Akshay, `useFormStatus` doesn't search for a form by itself. It connects through the React tree. When a component renders inside a `form`, React passes that form's status down to it.

In the example, `SubmitButton` is rendered inside the `form` element. So when you submit, React marks that form as pending, and `useFormStatus` in `SubmitButton` reads that state from the nearest parent form above it.

So the link comes from placement: the child has to sit inside the form, and it reads the nearest one.

Does that make sense?   


