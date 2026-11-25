# 12: Parallel routes and `default.jsx`

> Notes: [02_special_files.md](../../notes/02_special_files.md) — "`default.jsx`: parallel-route fallback", "Parallel routes: what `@analytics` and `@team` mean"

## Concept

A **slot** is a folder starting with `@`. A layout can show several pages at once, each in its own area.

| Rule | Example |
|---|---|
| `@name` folders are **slots**, not URL segments | `app/dashboard/@stats/` does not add `/stats` |
| The name without `@` becomes a **prop** of the layout | `@stats` → `stats` prop |
| Each slot can have its own `page.jsx` | `app/dashboard/@stats/page.jsx` |
| If a slot has no page for the URL, `default.jsx` renders | `app/dashboard/@stats/default.jsx` |

## What was built

```text
app/dashboard/
├── layout.jsx           ← receives `children` and `stats`
├── page.jsx             ← /dashboard → children
├── @stats/
│   ├── page.jsx         ← /dashboard → stats prop
│   └── default.jsx      ← fallback when no stats page matches (e.g. /dashboard/settings)
└── settings/
    └── page.jsx         ← /dashboard/settings → children
```

`app/dashboard/layout.jsx`:

```jsx
export default function DashboardLayout({ children, stats }) {
  return (
    <section>
      <h1>Dashboard</h1>
      <Counter label="Layout counter (kept)" />
      {stats}
      {children}
    </section>
  );
}
```

`app/dashboard/@stats/page.jsx` is a Server Component that awaits data:

```jsx
export default async function Stats() {
  const posts = await getPosts();
  return <p>Stats: {posts.length} posts in total</p>;
}
```

## See it working

| Action | Expected |
|---|---|
| Open `/dashboard` | "Stats: 3 posts in total" shown under the counter |
| Click **Settings** (soft navigation) | The Stats line stays visible (the slot keeps its last state) |
| Hard refresh `/dashboard/settings` | The slot shows `default.jsx`: "Stats are only shown on the overview." |

## Gotchas

- Without a `default.jsx`, a slot can fail on a **hard** refresh with an error. Add one for each slot.
- `children` is an implicit slot too. The notes say it needs a `default.jsx` in some cases. This app's `children` always matches (`/dashboard` and `/dashboard/settings` both have pages), so none was added.
- Slots are only useful when the layout receives them as props.
