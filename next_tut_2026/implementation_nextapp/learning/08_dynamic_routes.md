# 08: Dynamic routes

> Notes: [01_nextjs.md](../../notes/01_nextjs.md) — "Dynamic routes"

## Concept

A folder name in **square brackets** matches any value in that URL position. The value comes in through `params`.

| Folder | URL | `params` |
|---|---|---|
| `app/posts/[id]/page.jsx` | `/posts/42` | `{ id: "42" }` |
| `app/posts/[id]/page.jsx` | `/posts/7` | `{ id: "7" }` |

> **Next 15+:** `params` is a **Promise**. Use `await params`. Older versions passed a plain object.

## What was built

`app/posts/[id]/page.jsx`:

```jsx
export default async function PostPage({ params }) {
  const { id } = await params;          // Promise in Next 15+
  const post = await getPost(id);
  if (!post) notFound();                // see 10
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.body}</p>
    </article>
  );
}
```

The same pattern is used in a route handler: `app/api/posts/[id]/route.js` (see [13](13_route_handlers_api.md)).

## See it working

| URL | Expected |
|---|---|
| `/posts/1` | "What is Next.js?" with its body |
| `/posts/3` | "Layouts stay mounted" |
| `/posts/999` | Not Found page (see [10](10_not_found.md)) |
| `/posts/crash` | Error page (see [09](09_error_handling.md)) |

## Gotchas

- Forgetting `await params` gives `undefined` or a Promise object, not the id.
- `[id]` is a single segment. `/posts/1/comments` needs its own folder.
- Route segments are strings. `"1"` is not the number `1`.
