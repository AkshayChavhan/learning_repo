# 02: JSX

> **JSX** is a syntax that lets you write **HTML-like markup inside JavaScript**.
> It is **not HTML** and **not a string**. A compiler (Babel, or SWC in Next.js) turns it into plain JavaScript.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **JSX** | HTML-like syntax inside JavaScript, compiled before it runs |
| **Element** | A JSX expression, like `<h1>Hello</h1>`, that describes one piece of UI |
| **Expression** | Code that produces a value, usable inside `{ }` |
| **Fragment** | `<>...</>`, a wrapper that groups elements without adding a DOM node |
| **Compiler** | The tool (Babel, SWC) that turns JSX into JavaScript function calls |

---

## 🟢 Beginner

### What you write vs what runs

```jsx
// What you write
const element = <h1 className="title">Hello</h1>;
```

```javascript
// What runs after compilation
const element = React.createElement("h1", { className: "title" }, "Hello");
```

| Step | Code |
|---|---|
| **You write** | `<h1 className="title">Hello</h1>` |
| **Compiler outputs** | `React.createElement("h1", { className: "title" }, "Hello")` |
| **Result** | A plain JavaScript object describing the `<h1>` |

> Modern React compiles to `jsx()` from `react/jsx-runtime` instead of `createElement`. The idea is the same.

### Curly braces `{ }` = "put JavaScript here"

```jsx
const name = "Ravi";

<p>Hello, {name}!</p>       // Hello, Ravi!
<p>2 + 3 = {2 + 3}</p>      // 2 + 3 = 5
```

---

## 🟡 Intermediate

### Rule 1: Inside `{ }`, only expressions

An **expression** produces a value. A **statement** does not.

| | Works? | Why |
|---|---|---|
| `{isLoggedIn ? "Welcome" : "Log in"}` | ✅ | A ternary is an expression |
| `{isLoggedIn && <Dashboard />}` | ✅ | `&&` is an expression |
| `{if (isLoggedIn) "Welcome"}` | ❌ | An `if` is a statement |
| `{for (...) { }}` | ❌ | A loop is a statement |

**Fix for statement logic:** compute the value **above** the `return`.

```jsx
function Greeting({ isLoggedIn }) {
  let message;
  if (isLoggedIn) {
    message = "Welcome";
  } else {
    message = "Please log in";
  }

  return <p>{message}</p>;
}
```

### Rule 2: One root element

A component must return **one** root element. Use a wrapper or a **fragment**.

```jsx
// ❌ Two roots, not allowed
return (
  <h1>Title</h1>
  <p>Text</p>
);

// ✅ Fragment: one root, no extra DOM node
return (
  <>
    <h1>Title</h1>
    <p>Text</p>
  </>
);
```

| Option | Adds a DOM node? |
|---|---|
| `<div>...</div>` wrapper | ✅ Yes |
| `<>...</>` fragment | ❌ No |

### Rule 3: Attribute names change

HTML attributes mostly carry over, with a few changes:

| HTML | JSX | Why |
|---|---|---|
| `class` | `className` | `class` is a reserved word in JavaScript |
| `for` | `htmlFor` | `for` is a reserved word in JavaScript |
| `onclick` | `onClick` | JSX uses camelCase for event names |
| `style="color: red"` | `style={{ color: "red" }}` | `style` takes a JavaScript object |

```jsx
function Signup() {
  function handleClick() {
    console.log("clicked");
  }

  return (
    <>
      <label htmlFor="email">Email</label>
      <input id="email" className="input" />
      <button onClick={handleClick}>Sign up</button>
    </>
  );
}
```

> `onClick` takes a **function**, not a string. `onClick={handleClick}` is correct. `onClick="handleClick()"` is not.

---

## 🔴 Expert

### JSX is only syntax sugar

| You write | Compiled output |
|---|---|
| `<h1 className="t">Hi</h1>` | `React.createElement("h1", {className:"t"}, "Hi")` |
| `<Btn size="lg" />` | `React.createElement(Btn, {size:"lg"})` |
| `<>...</>` | `React.createElement(React.Fragment, ...)` |

- Each element becomes a call that returns a **plain object** (the React element).
- Capitalized names (`Btn`) are **components**. Lowercase names (`h1`) are **HTML tags**. This is why `<btn>` and `<Btn>` behave differently.

### What `$$typeof` does

Every React element object carries a special **`$$typeof` Symbol** that marks it as a real React element.

```text
Real React element  →  { $$typeof: <React symbol>, type: "h1", props: {...} }
Fake object (JSON)  →  { type: "h1", props: {...} }   ← no Symbol, so React rejects it
```

> JSON cannot hold a Symbol, so data from an API cannot pretend to be a React element. This is a security check against injected elements.

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| `class="box"` | `className="box"` |
| `{if (x) ...}` | Use `x ? ... : ...` or `x && ...` |
| Two sibling elements with no wrapper | Wrap them in `<>...</>` |
| `onClick={handleClick()}` (calls on render) | `onClick={handleClick}` (passes the function) |
| `style="color:red"` | `style={{ color: "red" }}` |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is JSX and what does it compile to? | HTML-like syntax inside JavaScript. The compiler turns each element into a `React.createElement` call (or `jsx()`), which returns a plain object. |
| What can go inside `{ }`? | Expressions only: variables, ternaries, `&&`, function calls. Statements like `if` and `for` go above the `return`. |
| Why one root element? | Each component returns one value. A fragment or wrapper gives React one root with the rest as children. |
| Main attribute differences from HTML? | `className` for `class`, `htmlFor` for `for`, camelCase events like `onClick`, and `style` as an object. The first two exist because `class` and `for` are reserved words in JavaScript. |

---

## ✅ Key Takeaways

- JSX **looks like HTML but compiles to JavaScript** function calls.
- Inside `{ }`: **expressions only**.
- **One root** per return: use a **fragment** `<>...</>` to avoid extra DOM nodes.
- Attributes: **`className`, `htmlFor`, `onClick`**, and `style={{ }}`.
