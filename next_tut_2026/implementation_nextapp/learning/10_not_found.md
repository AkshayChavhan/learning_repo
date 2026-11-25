# 10: Not found

> Notes: [02_special_files.md](../../notes/02_special_files.md) — "`not-found.jsx` and `notFound()`"

## Concept

Two ways to show `not-found.jsx`:

1. **Unknown URL** that matches no route (for example `/nope`).
2. **Calling `notFound()`** from a page or server code on purpose (for example a missing post).

## What was built

`app/not-found.jsx` (global, because no folder has its own):

```jsx
import Link from "next/link";

export default function NotFound() {
  return (
    <>
      <h1>Not Found</h1>
      <p>This page or post does not exist.</p>
      <Link href="/">Return Home</Link>
    </>
  );
}
```

`app/posts/[id]/page.jsx` calls `notFound()`:

```jsx
import { notFound } from "next/navigation";
// ...
const post = await getPost(id);
if (!post) notFound();   // renders app/not-found.jsx
```

## See it working

| URL | Expected | HTTP status (checked with curl) |
|---|---|---|
| `/nope` | Not Found page | `404` |
| `/posts/999` | Not Found page inside the posts layout area | `200` |

`/posts/999` returns `200` because the page had already started streaming (it sits under `loading.jsx`). The docs say: before streaming starts, Next returns `404`; after it starts, the status stays `200` and the not-found UI is in the body. Both get `noindex`.

## Gotchas

- `notFound()` must be called inside a route segment or server code, not in a random helper on the client.
- `not-found.jsx` in a folder (for example `app/posts/not-found.jsx`) handles `notFound()` calls from that segment. This app has only the root one.
- The notes' example says "not-found shows when `notFound()` is called". The status code depends on whether streaming has started (see above).
