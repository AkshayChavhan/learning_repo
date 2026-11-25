# 03: Root layout and navigation

> Notes: [02_special_files.md](../../notes/02_special_files.md) — "What a layout is", "Nested layouts"

## Concept

A **layout** wraps pages and **stays mounted** while you navigate between pages inside it. The **root layout** (`app/layout.jsx`) is required and must include `<html>` and `<body>`.

```text
app/layout.jsx        → wraps every page
app/about/page.jsx    → rendered inside <main> at /about
app/posts/page.jsx    → rendered inside <main> at /posts (header NOT re-mounted)
```

`children` is the current page. Its prop name is fixed by Next.js.

## What was built

`app/layout.jsx`:

```jsx
import Link from "next/link";
import "./globals.css";

export const metadata = { title: "Mini Blog - Next.js learning", description: "..." };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header>
          <strong>Mini Blog</strong>
          <nav>
            <Link href="/">Home</Link>
            <Link href="/posts">Posts</Link>
            <Link href="/about">About</Link>
            <Link href="/dashboard">Dashboard</Link>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
```

- `<Link>` from `next/link` navigates **client-side** (no full page reload). The header stays on screen.
- `metadata` sets the page `<title>` and description.

## See it working

1. Open `/`, then click **Posts**. The header does not flash or reload.
2. The URL changes, `<main>` content changes.

## Gotchas

| Mistake | Fix |
|---|---|
| Missing `{children}` | The page never renders |
| `<html>`/`<body>` in a **nested** layout | Only the root layout has them |
| Using `<a href>` for internal pages | Full reload. Use `<Link>` |
