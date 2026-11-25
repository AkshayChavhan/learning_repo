# 15: Time-based caching

> Notes: [03_caching_revalidation.md](../../notes/03_caching_revalidation.md) — "The idea", "Time-based: `next.revalidate`"

## Concept

Caching keeps a stored copy of a result so later requests reuse it. **Time-based revalidation** reuses the copy for a set time, then refreshes it.

```text
t = 0s    request → computed, result cached
t = 30s   request → cached copy (no recompute)
t = 61s   request → stale → old copy served, refresh runs in background
t = 62s+  request → new copy
```

In this app (Next 16, `cacheComponents: true`) the cache is set with **`"use cache"` + `cacheLife`**, not with the `revalidate` route option from the notes (see [18](18_previous_model_and_notes_corrections.md)).

## What was built

`lib/cached.js`:

```js
import { cacheLife } from "next/cache";

export async function getStamp() {
  "use cache";
  cacheLife({ stale: 10, revalidate: 30, expire: 600 });
  return new Date().toISOString();
}
```

- `"use cache"` makes the return value cacheable. The function must be `async`.
- `cacheLife` sets three times: `stale` (client may reuse without asking), `revalidate` (after this, the server regenerates), `expire` (hard limit).
- `new Date()` inside the cached scope is what makes the value visible as "cached". Outside a cache scope, `Date` during prerender is not allowed with Cache Components.

`app/cache/page.jsx` renders it inside `<Suspense>`:

```jsx
async function CachedStamp() {
  const stamp = await getStamp();
  return <p>Generated at <code>{stamp}</code>. Refresh within 30s and it stays the same.</p>;
}
```

## See it working (checked with curl on `npm start`)

| Time | Request | Stamp shown |
|---|---|---|
| 09:05:12 | 1st | `09:05:12.814Z` (generated) |
| 09:05:12 → 09:06:18 | repeated | `09:05:12.814Z` (same, reused) |
| 09:06:18 | 1st after window | `09:05:12.814Z` (old copy served) |
| 09:06:18 | next request | `09:06:18.585Z` (regenerated) |

That is the stale-while-revalidate behaviour from the notes: the first request after the time limit gets the old copy, and the refresh runs in the background.

## Gotchas

- The notes' `next: { revalidate: 60 }` on a `fetch` still works (see [16](16_fetch_revalidate_vs_no_store.md)). For plain functions such as database queries, use `"use cache"` + `cacheLife`.
- `cacheLife` must be called inside the cache scope, not at module top level.
- Short lifetimes (`revalidate: 0`, `seconds` profile, or `expire` < 5 min) make the value a dynamic hole instead of a prerender. The `expire: 600` above is long enough to stay cached.
- A page-level shell can have its own revalidate window too: the build output showed `/cache` with `Revalidate 1m`, so the shell can lag the stamp.
