# 17: On-demand revalidation: `updateTag`, `revalidateTag`, `revalidatePath`

> Notes: [03_caching_revalidation.md](../../notes/03_caching_revalidation.md) — "On-demand: `revalidatePath` and `revalidateTag`"

## Concept

On-demand revalidation refreshes cached data right after a change, such as a form submit.

| Function | Refreshes | Where it can be called |
|---|---|---|
| `updateTag(tag)` | Everything with that tag, immediately (read-your-own-writes) | **Server Actions only** |
| `revalidateTag(tag, "max")` | Tagged data, stale-while-revalidate | Server Actions and Route Handlers |
| `revalidatePath("/cache")` | Everything cached for a path | Server Actions and Route Handlers |

Tags come from `cacheTag("posts")` inside a `"use cache"` scope, or from `fetch(url, { next: { tags: [...] } })`.

## What was built

Tagged cache, `lib/cached.js`:

```js
export async function getCachedPosts() {
  "use cache";
  cacheLife("max");
  cacheTag("posts");
  return getPosts();
}
```

**1. `updateTag` in a Server Action** — `app/cache/actions.js`:

```js
"use server";
import { updateTag } from "next/cache";

export async function createPost(formData) {
  const title = formData.get("title")?.toString().trim();
  if (!title) return;
  addPost(title, "Added from the caching lab.");
  updateTag("posts");          // next request sees the new post immediately
}
```

The form on `/cache` calls this action. In the browser, typing "Fresh from the browser" and submitting showed the new item in the list right away.

**2. `revalidatePath` in a Server Action** — same file:

```js
export async function refreshPage() {
  revalidatePath("/cache");
}
```

The "Revalidate /cache (revalidatePath)" button calls it.

**3. `revalidateTag` in a Route Handler** — `app/api/revalidate/route.js`:

```js
export async function POST(request) {
  const tag = new URL(request.url).searchParams.get("tag");
  if (!tag) return Response.json({ error: "Pass ?tag=posts" }, { status: 400 });
  revalidateTag(tag, "max");   // stale-while-revalidate
  return Response.json({ revalidated: tag });
}
```

## See it working

Checked with curl on `npm start`:

```text
POST /api/revalidate?tag=posts  → 200  {"revalidated":"posts"}
POST /api/revalidate            → 400  {"error":"Pass ?tag=posts"}
GET  /api/revalidate?tag=posts  → 405  (only POST is exported)
```

Checked in the browser: adding a post with `updateTag` showed the new item on the same request.

## Gotchas

- **`updateTag` cannot run in a Route Handler.** Use `revalidateTag` there.
- `revalidateTag(tag)` with one argument is deprecated. Always pass the second argument (`"max"` is recommended).
- The Route Handler above has **no auth**. It is a demo. Anyone who can reach it can flush the cache.
- The posts store is in memory. A restart resets it; the cache is not a database.
- Server Actions run on the server. Calling `revalidatePath` during render throws.
