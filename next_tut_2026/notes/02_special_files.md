# 02: Layouts & Special Files

> A **layout** wraps a set of pages. It **stays mounted** while you navigate between those pages, so its state is kept.
> Special files like `loading`, `error`, `not-found`, and `template` handle the states around a page.

---

## 📌 Quick Reference

| File | One-line purpose |
|---|---|
| `layout.jsx` | Wraps pages and nested routes. Stays mounted across navigation |
| `page.jsx` | The UI for one URL |
| `loading.jsx` | Shows a fallback while the page is loading |
| `error.jsx` | Catches errors in the route and shows a fallback |
| `not-found.jsx` | Shows when a route doesn't exist, or when `notFound()` is called |
| `template.jsx` | Like a layout, but **re-mounts** on every navigation |
| `default.jsx` | Fallback for a parallel-route slot that has no matching page |

---

## 🟢 Beginner

### What a layout is

A layout is a file in a folder. It applies to every page in that folder and below.

```jsx
// app/layout.jsx  (root layout, required)

// Function name can be anything,children key fixed by nextjs.
export default function RootLayout({ children }) { 
  return (
    <html lang="en">
      <body>
        <header>My Site</header>
        <main>{children}</main>      {/* the current page renders here */}
      </body>
    </html>
  );
}
```

- `children` is the page for the current URL, `children` **prop key** Fixed by Next.js.
- The `<header>` stays on screen while you move between pages.

```text
app/layout.jsx        → wraps every page
app/about/page.jsx    → rendered inside <main> at /about
app/blog/page.jsx     → rendered inside <main> at /blog (header not re-mounted)
```

> **Why it matters:** the layout is not re-mounted on navigation, so anything it holds in state is kept.

---

## 🟡 Intermediate

### Nested layouts

Layouts stack. A page is wrapped by **every layout above it**, from the root down.

```text
app/
├── layout.jsx             ← wraps everything
└── dashboard/
    ├── layout.jsx         ← wraps only /dashboard pages
    └── settings/
        └── page.jsx       ← rendered inside BOTH layouts
```

```text
Output for /dashboard/settings:
  RootLayout
    └── DashboardLayout
          └── SettingsPage
```

> The **root layout** must include `<html>` and `<body>`. Nested layouts should not.

### `loading.jsx`: show while the page loads

```jsx
// app/dashboard/loading.jsx
export default function Loading() {
  return <p>Loading dashboard...</p>;
}
```

- Next.js wraps the page in a Suspense boundary using this file.
- It shows while the page's data is loading, then the page replaces it.

### `error.jsx`: catch errors in a route

```jsx
"use client";                         // error files must be Client Components

export default function Error({ error, reset }) {
  return (
    <div>
      <p>Something went wrong: {error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

| Prop | What it does |
|---|---|
| `error` | The error that was thrown |
| `reset` | Re-renders the segment, to try again |

### `not-found.jsx` and `notFound()`

```jsx
// app/posts/[id]/page.jsx
import { notFound } from "next/navigation";

export default async function Post({ params }) {
  const { id } = await params;
  const post = await getPost(id);
  if (!post) notFound();              // shows not-found.jsx
  return <h1>{post.title}</h1>;
}
```

```jsx
// app/not-found.jsx
export default function NotFound() {
  return <p>This page does not exist.</p>;
}
```

- Unknown URLs also show `not-found.jsx`.
- `notFound()` is called in a page or server code to trigger it on purpose.

### `template.jsx`: like a layout, but re-mounts

```jsx
// app/dashboard/template.jsx
export default function Template({ children }) {
  return <div>{children}</div>;
}
```

| | `layout` | `template` |
|---|---|---|
| Re-mounts on navigation? | ❌ No, state is kept | ✅ Yes, state resets |
| Use for | Shared UI like headers and sidebars | Things that should reset: enter animations, per-page logging, forms that clear |

### `default.jsx`: parallel-route fallback

Parallel routes render more than one page in named **slots** at once.

```text
app/
├── layout.jsx          ← receives @analytics and @team as props
├── @analytics/
│   ├── page.jsx
│   └── default.jsx     ← used when no analytics page matches the URL
└── @team/
    └── page.jsx
```

> `default.jsx` is the fallback for a slot that has no matching page. It is mainly used for parallel routes.

### Parallel routes: what `@analytics` and `@team` mean

A **slot** is a folder that starts with `@`. Slots let one layout show several pages at the same time, each in its own area.

| Rule | Example |
|---|---|
| `@name` folders are **slots**, not URL segments | `app/@team/` does not add `/team` to the URL |
| The name without `@` becomes a **prop** of the layout | `@team` → `team` prop |
| Each slot can have its own `page.jsx` | `app/@team/page.jsx` renders into the `team` prop |

```text
app/
├── layout.jsx          ← the shared frame, receives the slots as props
├── page.jsx            ← main content → the `children` prop
├── @analytics/
│   ├── page.jsx        ← the `analytics` prop
│   └── default.jsx     ← used when no analytics page matches the URL
└── @team/
    └── page.jsx        ← the `team` prop
```

```jsx
// app/layout.jsx
export default function Layout({ children, analytics, team }) {
  return (
    <>
      {children}      {/* app/page.jsx */}
      {analytics}     {/* app/@analytics/page.jsx */}
      {team}          {/* app/@team/page.jsx */}
    </>
  );
}
```

```text
URL /  →  main page + analytics panel + team panel, all on one screen
```

> If a slot has no page for the current URL, Next.js renders that slot's `default.jsx` instead. Without one, the slot can fail on a full page load.

---

## 🔴 Expert

### The file hierarchy inside one route

Next.js wraps each route segment in this order, from outer to inner:

```text
layout.jsx
  └── template.jsx
        └── error.jsx        (error boundary)
              └── loading.jsx  (Suspense boundary)
                    └── not-found.jsx
                          └── page.jsx
```

### Errors: a layout can't catch its own errors

An `error.jsx` catches errors from the **segment below it**, not from its own `layout.jsx`.

| Error comes from | Caught by |
|---|---|
| `page.jsx` in the same folder | `error.jsx` in that folder |
| `layout.jsx` in the same folder | `error.jsx` in the **parent** folder |
| Root `layout.jsx` | `global-error.jsx` (if you add one) |

> If a layout throws and no error file is above it, the whole app shows the error screen.

### Layouts don't re-render on navigation

```text
/dashboard/a  →  /dashboard/b
  DashboardLayout: kept mounted (not re-run for the change)
  Page: replaced with the new page
```

> This is why you can keep a sidebar's scroll position or open menu state across pages.

### Common Mistakes

| Mistake | Fix |
|---|---|
| Missing `{children}` in a layout | The page never renders. Always render `children` |
| `<html>` and `<body>` in a nested layout | Only the root layout includes them |
| `error.jsx` without `"use client"` | Error files must be Client Components |
| Expecting `error.jsx` to catch errors from the same folder's `layout.jsx` | Put the error file in the parent folder |
| Using `layout` when state should reset per page | Use `template` |
| Calling `notFound()` outside a route | Use it inside a page or server code |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is a layout? | A component that wraps pages and nested routes, and stays mounted during navigation. |
| Layout vs template? | A layout keeps its state. A template re-mounts and resets its state on every navigation. |
| What does `loading.jsx` do? | Shows a fallback while the page loads, using a Suspense boundary. |
| What does `error.jsx` do? | Catches errors in the route segment below it, and offers a `reset` function. It must be a Client Component. |
| When does `not-found.jsx` show? | When a URL doesn't match a route, or when `notFound()` is called. |
| What is `default.jsx` for? | The fallback for a parallel-route slot that has no matching page. |

---

## ✅ Key Takeaways

- **Layouts** wrap pages, nest by folder, and **keep their state** across navigation.
- Use `template` when a wrapper should reset on each navigation.
- `loading` and `error` handle the states around a page. `error` must be a Client Component.
- `not-found` handles unknown URLs and `notFound()` calls.
- A file's **error boundary** sits in the parent folder, not in the same folder as its layout.
