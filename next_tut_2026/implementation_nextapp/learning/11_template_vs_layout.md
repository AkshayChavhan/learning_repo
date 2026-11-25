# 11: Template vs layout

> Notes: [02_special_files.md](../../notes/02_special_files.md) — "`template.jsx`: like a layout, but re-mounts"

## Concept

| | `layout.jsx` | `template.jsx` |
|---|---|---|
| Re-mounts on navigation? | ❌ No, state is kept | ✅ Yes, state resets |
| Use for | Shared UI like headers and sidebars | Enter animations, per-page logging, forms that clear |

A template gets a **new key** for its segment. Its Client Component children are recreated when that segment changes. Navigation inside a deeper segment does **not** remount it.

Order: `layout` → `template` → `error` → `loading` → `not-found` → `page`.

## What was built

Both counters are the same `Counter` component:

| Counter | Where | Behavior |
|---|---|---|
| Layout counter | `app/dashboard/layout.jsx` | Kept when moving `/dashboard` ↔ `/dashboard/settings` |
| Template counter | `app/dashboard/settings/template.jsx` | Resets to 0 every time you navigate to `/dashboard/settings` |

`app/dashboard/settings/template.jsx`:

```jsx
import Counter from "@/components/Counter";

export default function SettingsTemplate({ children }) {
  return (
    <div>
      <Counter label="Template counter (resets)" />
      {children}
    </div>
  );
}
```

The template sits on the `settings` segment, not on `dashboard`. That is why it only resets on the Settings page. Had it been placed in `app/dashboard/template.jsx`, it would reset only when entering or leaving the whole dashboard.

## See it working

1. Open `/dashboard`. Click **Layout counter** 2 times. (The template counter only exists on Settings.)
2. Click **Settings**. Layout counter still shows **2**. Template counter starts at **0**.
3. Click the template counter 3 times, go to **Overview**, then back to **Settings**. It is **0** again. The layout counter is still 2.

## Gotchas

- A template is a Server Component by default, like a layout. Its state comes from Client Components inside it.
- Putting a template on the wrong segment is the common mistake: check which URL segment changes.
- `template` vs `layout` is about **state**, not about the HTML output. Both render `children`.
