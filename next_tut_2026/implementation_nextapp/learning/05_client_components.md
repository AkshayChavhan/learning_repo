# 05: Client Components

> Notes: [01_nextjs.md](../../notes/01_nextjs.md) — "Server vs Client Components", "Where to put the `"use client"` line"

## Concept

Add `"use client"` as the **first line** of a file to make it a Client Component. It is then sent to the browser and **hydrated** (React attaches event handlers and state).

```text
Client Component ("use client")
   │  its JavaScript is sent to the browser and runs there (hydrates)
```

Rules from the notes:

- `"use client"` must be the first line, before imports.
- A `"use client"` file is a **boundary**: everything it imports also runs on the client.
- Server Components can render Client Components. Client Components **cannot import** Server Components directly; they receive them as `children` or props.
- Keep components on the server unless they need interactivity or browser APIs.

## What was built

`components/Counter.jsx`:

```jsx
"use client"; // first line

import { useState } from "react";

export default function Counter({ label }) {
  const [count, setCount] = useState(0);
  return (
    <button className="counter" onClick={() => setCount(count + 1)}>
      {label}: clicked {count} times
    </button>
  );
}
```

It is used in three places: `dashboard/layout.jsx`, `dashboard/settings/template.jsx`. (See [06](06_nested_layouts.md) and [11](11_template_vs_layout.md).)

## See it working

1. Open `/dashboard`.
2. Click "Layout counter (kept)" three times. It shows `clicked 3 times`.
3. Refresh the page: back to 0 (state is lost on a full reload, which is expected).

## Gotchas

| Mistake | Fix |
|---|---|
| `"use client"` below an import | Put it as the very first line |
| `useState` in a file with no `"use client"` | Add the directive |
| Adding `"use client"` to every file | Only where interactivity is needed |
