# 06: Nested layouts

> Notes: [02_special_files.md](../../notes/02_special_files.md) — "Nested layouts", "Layouts don't re-render on navigation"

## Concept

Layouts **stack**. A page is wrapped by every layout above it, from the root down.

```text
Output for /dashboard/settings:
  RootLayout
    └── DashboardLayout
          └── SettingsTemplate   (see 11)
                └── SettingsPage
```

Navigation inside a layout's segment **does not re-run** that layout. Its state survives.

## What was built

Two nested layouts:

| File | Wraps |
|---|---|
| `app/layout.jsx` | everything (see [03](03_root_layout_and_navigation.md)) |
| `app/posts/layout.jsx` | `/posts` and `/posts/[id]` |
| `app/dashboard/layout.jsx` | `/dashboard` and `/dashboard/settings` |

`app/posts/layout.jsx`:

```jsx
export default function PostsLayout({ children }) {
  return (
    <section className="posts">
      <aside>
        <h2>Posts section</h2>
        <p>Nested layout: stays mounted when you switch posts.</p>
      </aside>
      <div>{children}</div>
    </section>
  );
}
```

`app/dashboard/layout.jsx` also renders the parallel slot `stats` (see [12](12_parallel_routes_and_default.md)) and a `Counter`.

## See it working

1. Open `/posts`. The sidebar is on the left (wide screen) or top (phone).
2. Click a post. The sidebar **stays**; only the right-hand content changes.
3. Open `/dashboard`, click the layout counter 2 times, then open **Settings**. The count is still 2.

## Gotchas

- Nested layouts must **not** include `<html>` or `<body>`.
- Always render `{children}` in a layout, or the page never shows.
- A layout that throws is caught by the `error.jsx` in its **parent** folder (see [09](09_error_handling.md)).
