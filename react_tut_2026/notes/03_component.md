# 03: Components

> A **component** is a **JavaScript function that returns JSX**, which describes what should appear on the screen.
> Components are the **building blocks** of every React app. You combine small components to build bigger ones.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Component** | A function that returns JSX |
| **Component name** | Must start with a **capital letter** (`Greeting`, not `greeting`) |
| **Render** | React calling the component function to get its JSX |
| **Composition** | Building bigger components out of smaller ones |
| **Props** | Inputs passed to a component (covered in the next note) |
| **State** | Data a component remembers between renders (covered later) |

---

## 🟢 Beginner

### Your first component

```jsx
function Greeting() {
  return <h1>Hello</h1>;
}
```

- `Greeting` is a **component**: a function that returns JSX.
- You use it like an HTML tag: `<Greeting />`.

### Use a component inside another

```jsx
function Greeting() {
  return <h1>Hello</h1>;
}

export default function App() {
  return (
    <div>
      <Greeting />
      <Greeting />
    </div>
  );
}
```

```text
Hello
Hello
```

> One component, used twice. Each `<Greeting />` runs the function and renders its own output.

### Capital letter rule

React uses the first letter to tell components from HTML tags.

| You write | React treats it as | Result |
|---|---|---|
| `<greeting />` | HTML tag (lowercase) | ❌ Unknown element, not your component |
| `<Greeting />` | Your component (capital) | ✅ Calls the `Greeting` function |
| `<h1>` | HTML tag | ✅ Built-in browser element |

---

## 🟡 Intermediate

### Components split the UI into pieces

Think of a page as a tree of components:

```text
App
├── Header
│   ├── Logo
│   └── NavMenu
├── Main
│   ├── Greeting
│   └── Card
└── Footer
```

| Benefit | Why it matters |
|---|---|
| **Reuse** | Write once, use many times |
| **Readability** | Each file describes one small piece |
| **Maintenance** | Change `Header` in one place, and every page using it updates |

### Naming and file layout

| Rule | Example |
|---|---|
| Name in **PascalCase** | `UserCard`, `NavMenu` |
| One main component per file (common practice) | `Greeting.jsx` exports `Greeting` |
| Use `export default` for the main component | `export default function Greeting() {}` |

### Components are just functions

Because they are functions, you can use normal JavaScript inside them:

```jsx
function Greeting() {
  const hour = 9;
  const text = hour < 12 ? "Good morning" : "Good afternoon";

  return <h1>{text}</h1>;
}
```

```text
Good morning
```

---

## 🔴 Expert

### What "rendering" a component means

| Step | What happens |
|---|---|
| 1 | React **calls** the component function |
| 2 | The function returns JSX |
| 3 | React turns that JSX into React elements (objects) |
| 4 | React **reconciles** and updates the real DOM |

> Rendering a component does **not** mean the browser redraws. It means React calls the function and gets a new description (see note 01).

### Pure components

A good component is a **pure function** for its inputs:

| Pure component | Impure component |
|---|---|
| Same inputs → same output | Output depends on hidden things (globals, random, time) |
| Does not change outside variables during render | Writes to variables or the DOM while rendering |
| Easy to test and predict | Causes bugs that are hard to trace |

```jsx
// Pure: same input always gives the same output
function Price({ amount }) {
  return <p>${amount}</p>;
}
```

> Side effects (fetching data, timers, DOM changes) belong in **effects** (`useEffect`), not in the component's body. This is covered in a later note.

### Component identity

- Defining a component **inside** another component creates a **new component type on every render**. React then unmounts and remounts it, which loses its state.

```jsx
// ❌ Bad: Inner is recreated on every render, so its state resets
function Parent() {
  function Inner() {
    return <p>Inside</p>;
  }
  return <Inner />;
}

// ✅ Good: define it at the top level
function Inner() {
  return <p>Inside</p>;
}

function Parent() {
  return <Inner />;
}
```

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| `<greeting />` (lowercase) | Use `<Greeting />` |
| Component returns nothing (`undefined`) | Return JSX or `null` |
| Two sibling elements returned with no wrapper | Wrap in `<>...</>` (see note 02) |
| Defining components inside other components | Move them to the top level |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is a component? | A function that returns JSX. It is the basic building block of React UIs. |
| Why must component names start with a capital letter? | React uses the capital letter to tell components from HTML tags. |
| What is composition? | Building bigger components by using smaller ones inside them. |
| Why should components be pure? | The same inputs give the same output, which makes behavior predictable and rendering safe to repeat. |

---

## ✅ Key Takeaways

- A **component** = a **function** that **returns JSX**.
- Name it with a **capital letter**, and use it as a tag: `<Greeting />`.
- Build pages by **composing** small components into a tree.
- Keep components **pure**. Put side effects in effects.
