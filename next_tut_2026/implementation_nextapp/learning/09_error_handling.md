# 09: Error handling

> Notes: [02_special_files.md](../../notes/02_special_files.md) — "`error.jsx`: catch errors in a route", "Errors: a layout can't catch its own errors"

## Concept

`error.jsx` is a React **error boundary** for a route segment. It catches errors from the segment **below** it. It must be a Client Component (`"use client"`).

| Error comes from | Caught by |
|---|---|
| `page.jsx` in folder X | `error.jsx` in folder X |
| `layout.jsx` in folder X | `error.jsx` in the **parent** folder |
| Root `layout.jsx` | `global-error.jsx` |

> ⚠️ **Correction to the notes:** the notes show the prop as `reset`. In Next 16 the prop is **`retry`**, per the bundled docs at `node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/error.md`. Using `reset` gives an undefined function.

## What was built

`app/posts/[id]/error.jsx` catches errors thrown by `app/posts/[id]/page.jsx`:

```jsx
"use client";

export default function PostError({ error, retry }) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={() => retry()}>Try again</button>
    </div>
  );
}
```

`app/posts/[id]/page.jsx` throws on purpose:

```jsx
if (id === "crash") throw new Error("Demo crash: caught by posts/[id]/error.jsx");
```

`app/global-error.jsx` catches errors from the **root** layout. It must render its own `<html>` and `<body>`:

```jsx
"use client";
export default function GlobalError({ error, retry }) {
  return (
    <html lang="en">
      <body>
        <h1>App crashed</h1>
        <p>{error.message}</p>
        <button onClick={() => retry()}>Try again</button>
      </body>
    </html>
  );
}
```

## See it working

1. Open `/posts/crash`. The header stays, and the error UI replaces the post area.
2. Click **Try again**. It re-renders the segment (it will crash again, because the id is still `crash`).
3. Open `/posts/1` to confirm the rest of the app still works.

**Production note:** in `npm start`, Next hides the real message of server errors and shows a generic one. The server log shows the real error with a `digest` id. In `npm run dev` you see the full message.

## Gotchas

- Forgetting `"use client"` in `error.jsx`.
- Expecting `error.jsx` in the same folder to catch errors from that folder's `layout.jsx`. Put it in the parent folder.
- `global-error.jsx` is only for root-layout errors. Page errors go to the nearest `error.jsx`.
