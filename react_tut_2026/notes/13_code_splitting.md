# 13: Code Splitting

> **Code splitting** breaks your JavaScript bundle into **smaller chunks** that load **only when needed**, instead of one big file up front.
> Result: a **faster first page load**.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Bundle** | The single JavaScript file a bundler creates from your app |
| **Chunk** | A separate JavaScript file, created by the bundler, that loads on demand |
| **Dynamic `import()`** | Loads a module at runtime. Returns a **Promise** of the module |
| **`React.lazy`** | Turns a dynamic import into a component that loads when first rendered |
| **`Suspense`** | Shows a `fallback` while a lazy component is loading |
| **Vendor chunk** | A chunk holding third-party libraries (like React), which change less often |

---

## 🟢 Beginner

### The idea

```text
Without splitting:   [ app.js — everything, 1 big file ]     → slow first load
With splitting:      [ app.js ]  + [ chart.js ] (only on click)  → fast first load
```

### Static vs dynamic import

| | Static `import` | Dynamic `import()` |
|---|---|---|
| Syntax | `import Chart from './chart.js'` | `import('./chart.js')` |
| When it loads | At startup, in the main bundle | When the line runs |
| Returns | The module | A **Promise** of the module |
| Creates a separate chunk? | ❌ No | ✅ Yes |

### Example: load a chart only on click

```js
button.addEventListener("click", async () => {
  const { drawChart } = await import("./chart.js");
  drawChart(container);
});
```

- Before the click, `chart.js` is **not downloaded**.
- After the first click, the browser fetches the chunk, resolves the Promise, and draws the chart.
- The chunk stays cached, so later clicks are instant.

> **Trade-off:** the first click waits for the download. Show a loading indicator.

---

## 🟡 Intermediate

### The three approaches

| Approach | What is split | Typical use |
|---|---|---|
| **1. Dynamic `import()`** | A single feature or module | Heavy feature triggered by the user (chart, editor, PDF viewer) |
| **2. Route-based `React.lazy`** | One component per page | Each page downloads its code on first visit |
| **3. Vendor chunks** | Third-party libraries | Libraries change rarely, so users keep them cached |

### 1. Dynamic import inside a React event handler

```jsx
function ChartButton() {
  const [Chart, setChart] = useState(null);

  async function handleClick() {
    const module = await import("./Chart");
    setChart(() => module.default);   // store the component
  }

  return (
    <>
      <button onClick={handleClick}>Show chart</button>
      {Chart && <Chart />}
    </>
  );
}
```

### 2. Route-based splitting with `React.lazy` and `Suspense`

```jsx
import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./Home";                              // always loaded

const Dashboard = lazy(() => import("./Dashboard"));   // loaded on first visit
const Reports = lazy(() => import("./Reports"));

export default function App() {
  return (
    <Suspense fallback={<p>Loading page...</p>}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Suspense>
  );
}
```

```text
Visit /            → downloads: main bundle only
Visit /dashboard   → downloads: dashboard chunk (shows "Loading page..." briefly)
```

**Rules for `React.lazy`:**

- The module must have a **default export**.
- A lazy component must be inside a **`Suspense`** boundary, or React throws an error.
- For a **named export**, map it to a default:

```jsx
const Chart = lazy(() =>
  import("./charts").then(module => ({ default: module.LineChart }))
);
```

### 3. Vendor splitting with `manualChunks` in Vite

```js
// vite.config.js
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          react: ["react", "react-dom"],   // React goes into its own chunk
        },
      },
    },
  },
});
```

```text
Before:  index-abc123.js   (React + your code together)
After:   react-f9e8d7.js   (React only, rarely changes)
         index-def456.js   (your code, changes often)
```

> **Why it helps:** when you change app code, only `index-*.js` changes. Users keep the cached `react-*.js`. This works best with **hashed file names**, which Vite adds by default.

---

## 🔴 Expert

### How the bundler decides where to split

```text
1. Read your code and follow every import
2. Build a dependency graph: which file uses which
3. Static import  →  same chunk as the importer
   Dynamic import()  →  stop here, create a NEW chunk
4. Split point = every dynamic import()
```

### The Promise can fail

A chunk request can fail (network drop, deploy that changed file names). Handle it, or the UI gets stuck.

| Failure | What to do |
|---|---|
| Network drops during a click-triggered import | `catch` the error, show a message, and offer a **retry** |
| Route chunk fails after a new deploy | Catch it with an **Error Boundary**, then reload the page |

```jsx
// Retry for a click-triggered import
async function loadChart() {
  try {
    const module = await import("./Chart");
    setChart(() => module.default);
  } catch (error) {
    setError("Couldn't load the chart. Try again.");
  }
}
```

> Route-level `lazy` failures are thrown to the nearest **Error Boundary**, not caught by `try/catch`. See the error boundary note.

### Preloading: fetch before the user needs it

Start the download early, for example on hover, so the click feels instant:

```jsx
const loadDashboard = () => import("./Dashboard");

<Link to="/dashboard" onMouseEnter={loadDashboard}>Dashboard</Link>
```

> The browser caches the module, so the later `lazy` import resolves at once.

### What to show while loading

| Good | Avoid |
|---|---|
| Spinner or "Loading chart..." near where content appears | A blank screen |
| Disable the button while loading | Letting double clicks start two requests |
| Keep the layout size stable | Content jumping when the chunk arrives |
| Retry option on failure | Leaving the user stuck |

### What is worth splitting

| Split | Don't split |
|---|---|
| Large, rarely used features (editors, charts, PDF tools) | Small components used on every page |
| Each route / page | Code needed for the first screen |
| Heavy third-party libraries used in one place | Tiny utilities (the extra request costs more than it saves) |

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| `React.lazy` without `Suspense` | Wrap lazy components in `<Suspense fallback={...}>` |
| Lazy-loading a component that is needed on first paint | Import it statically |
| Missing default export for `React.lazy` | Export default, or map the named export |
| No `catch` on the import | Handle failure with `try/catch` or an Error Boundary |
| Splitting tiny modules | Only split big or rarely used code |
| Using `import()` for everything | Use it at feature and route boundaries |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is code splitting? | Breaking the bundle into chunks that load only when needed, to speed up the first load. |
| What creates a separate chunk? | A dynamic `import()`. Static imports stay in the bundle of the file that imports them. |
| What does `import()` return? | A Promise that resolves to the module namespace object. |
| What does `React.lazy` need? | A dynamic import that resolves to a module with a default export, rendered inside `Suspense`. |
| What does `Suspense` do? | Shows its `fallback` while a lazy child is loading. |
| What is vendor splitting? | Putting third-party libraries in their own chunk, so app changes don't invalidate the cached library code. |
| What can go wrong? | The chunk request can fail. Handle it with `catch` or an Error Boundary. |

---

## ✅ Key Takeaways

- **Every dynamic `import()` is a split point.** Static imports stay in the main bundle.
- Use **route-based `React.lazy`** for pages, and **dynamic import** for heavy features.
- `React.lazy` needs a **default export** and a **`Suspense`** boundary.
- Handle **loading** and **failure** states, so users are never stuck.
- **Vendor chunks** keep libraries cached while your app code changes.
