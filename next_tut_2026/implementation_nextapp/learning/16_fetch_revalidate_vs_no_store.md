# 16: fetch: `revalidate` vs `no-store`

> Notes: [03_caching_revalidation.md](../../notes/03_caching_revalidation.md) — "Time-based: `next.revalidate`", "Caching behavior of `fetch`"

## Concept

`fetch` in a Server Component is where caching options matter most.

| Option | Behavior |
|---|---|
| `next: { revalidate: N }` | Cache the response for N seconds |
| `cache: "no-store"` | Never cache. Fetch on every request |
| `cache: "force-cache"` | Cache until revalidated by tag or path |
| *(no option)* | Not cached by default in Next 15+ |

Conflicting options such as `{ revalidate: 3600, cache: "no-store" }` are ignored, with a dev warning.

## Where `fetch` runs matters

| Where `fetch` runs | `next.revalidate` works? | Where it's cached |
|---|---|---|
| Server Component / `route.js` | ✅ Yes | Server Data Cache |
| Client Component (browser) | ❌ Ignored | Browser HTTP cache only |

The browser's `fetch` does not know the `next` option, so it skips it. For client-side data, fetch in a Server Component and pass it down as props, or call your own `route.js`.

## What was built

`app/cache/page.jsx` fetches the same URL two ways:

```jsx
async function RemoteFetches() {
  const url = "https://jsonplaceholder.typicode.com/todos/1";
  const cached = await fetch(url, { next: { revalidate: 60, tags: ["todo"] } });
  const fresh = await fetch(url, { cache: "no-store" });

  return (
    <ul>
      <li>next.revalidate 60 → response Date: <code>{cached.headers.get("date")}</code></li>
      <li>cache: "no-store" → response Date: <code>{fresh.headers.get("date")}</code></li>
    </ul>
  );
}
```

The `Date` header is the remote server's time when that response was made, so it shows whether a response was reused.

## See it working (checked in the browser and with curl)

Observed in the Chrome tab at `/cache`:

| Action | `revalidate: 60` Date | `no-store` Date |
|---|---|---|
| First load | `09:06:18 GMT` | `10:06:23 GMT` |
| After a form submit (updateTag), more than 60s later | `10:06:23 GMT` | `10:06:44 GMT` |

The `revalidate` Date stayed the same while its 60-second window was open. Once the window passed, the next request refreshed it. The `no-store` Date changes on every request.

## Gotchas

- `revalidate` and `no-store` together are not allowed. Pick one.
- Route-level `export const revalidate = 60` from the notes is removed when `cacheComponents` is on (see [18](18_previous_model_and_notes_corrections.md)).
- A `fetch` with `no-store` makes the component dynamic. Wrap it in `<Suspense>` (this app does) or the build fails.
- The browser `fetch` example from the notes (`"use client"` + `useEffect`) ignores `next`. This is documented, not demoed.
