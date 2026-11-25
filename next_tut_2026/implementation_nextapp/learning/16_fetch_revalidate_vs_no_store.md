# 16: fetch: `revalidate` vs `no-store`

> Notes: [03_caching_revalidation.md](../../notes/03_caching_revalidation.md) — "Time-based: `next.revalidate`", "Caching behavior of `fetch`"

## 🟢 Concept

Topic 15 cached a **whole function** with `"use cache"`. This topic caches **one `fetch()` call** by passing an option to `fetch` itself (Server Components and Route Handlers only).

| Option | Behavior | Café analogy |
|---|---|---|
| `next: { revalidate: N }` | Reuse the response for N seconds, then refresh in the background (stale-while-revalidate) | Board rewritten every hour |
| `cache: "no-store"` | **Never** cache. Fetch on every request | Ask the chef fresh every time |
| `cache: "force-cache"` | Cache until cleared by tag or path ([17](17_on_demand_updateTag_revalidateTag_revalidatePath.md)) | Board stays until the manager wipes it |
| *(no option)* | Not cached (Next 15+) | Same as asking fresh |

### When to use which

| Data | Changes | Pick |
|---|---|---|
| Product title, description, blog posts | Rarely | `revalidate: 60` (or longer) |
| Stock count, live scores, a user's cart | Constantly, must be accurate | `no-store` |
| Changes only when an admin edits it | On edits | `force-cache` + clear on edit (17) |

### Topic 15 vs 16

| | `"use cache"` + `cacheLife` (15) | `fetch` options (16) |
|---|---|---|
| Caches | A whole function (DB, `fetch`, any code) | One `fetch` call |
| Timers | `stale`, `revalidate`, `expire` | `revalidate` only |
| Where | Server only | Server only |

## Where `fetch` runs matters

| Where `fetch` runs | `next.revalidate` works? | Where it's cached |
|---|---|---|
| Server Component / `route.js` | ✅ Yes | Server Data Cache |
| Client Component (browser) | ❌ Ignored | Browser HTTP cache only |

The browser's `fetch` doesn't know the `next` option, so it skips it. For client-side data, fetch in a Server Component and pass it down as props, or call your own `route.js`.

---

## 🟡 Practical example: details cached, stock live

```jsx
// app/products/[id]/page.jsx
import { Suspense } from "react";

async function ProductDetails({ params }) {
  const { id } = await params;

  // Details rarely change → reuse for 60s
  const detailsRes = await fetch(`https://dummyjson.com/products/${id}`, {
    next: { revalidate: 60 },
  });
  const product = await detailsRes.json();

  // Stock must be accurate → fresh every time
  const stockRes = await fetch(`https://dummyjson.com/products/${id}?select=stock`, {
    cache: "no-store",
  });
  const { stock } = await stockRes.json();

  return (
    <div>
      <h1>{product.title}</h1>
      <p>${product.price}</p>
      <p>In stock: {stock}</p>
      <small>
        Details from: {detailsRes.headers.get("date")}<br />
        Stock from: {stockRes.headers.get("date")}
      </small>
    </div>
  );
}

export default function Page({ params }) {
  return (
    <Suspense fallback={<p>Loading…</p>}>
      <ProductDetails params={params} />
    </Suspense>
  );
}
```

**The `Date` header trick:** every HTTP response has a `Date` header, set when the remote server created it. If it doesn't change → reused from cache. If it changes → new response.

| Time | Refresh | Details `Date` (`revalidate: 60`) | Stock `Date` (`no-store`) |
|---|---|---|---|
| 10:00:00 | 1st | 10:00:00 (fetched) | 10:00:00 (fetched) |
| 10:00:30 | 2nd | **10:00:00** (reused) | 10:00:30 (fetched) |
| 10:01:10 | 3rd | **10:00:00** (stale, served while refreshing) | 10:01:10 (fetched) |
| 10:01:15 | 4th | **10:01:10** (new copy) | 10:01:15 (fetched) |

Details: 2 fetches in 4 visits. Stock: 4 in 4, always live.

### Three rules you'll hit

| Rule | Why |
|---|---|
| Never combine `revalidate` and `no-store` in one call | They contradict each other. Next.js ignores them and warns in dev. |
| A `no-store` fetch must be inside `<Suspense>` (with `cacheComponents`) | It can't be baked in at build time, so that part becomes **dynamic** and needs a fallback. Without one, the **build fails**. |
| These options do nothing in a Client Component | The browser's `fetch` ignores `next` |

---

## 🔴 Expert

### Why "no option" stopped caching

| Version | `fetch()` with no option |
|---|---|
| Next 14 | **Cached forever** (like `force-cache`) |
| Next 15+ | **Not cached** |

People kept shipping old data without knowing it was cached, so Next.js switched to **opt-in caching**. That's why older tutorials behave differently.

### Request memoization vs Data Cache

If one render calls the **same `fetch` (same URL + same options)** more than once, only **one** network request is made.

```text
1 page render → 2 identical fetch calls in code → 1 network request
```

| | Memoization | Data Cache (`revalidate`) |
|---|---|---|
| Lasts | One render | Across requests, for N seconds |
| Shared between visitors | ❌ | ✅ |
| Purpose | No duplicate calls in one page | No API call on every visit |

> This app's demo fetches the **same URL with different options**, and the two `Date` values differed. Different options aren't merged.

### `fetch` inside `"use cache"`: the outer cache decides

```js
export async function getPrice(id) {
  "use cache";
  cacheLife({ revalidate: 30 });
  const res = await fetch(url);   // inner fetch
}
```

```text
"use cache" hit  → body skipped → inner fetch never runs
"use cache" miss → body runs    → inner fetch runs
```

Freshness comes from the **outer** `cacheLife`. Cache at **one** level, and don't rely on inner `fetch` options to control it.

### `tags`: the bridge to 17

```js
fetch(url, { next: { revalidate: 60, tags: ["todo"] } });
```

A tag labels the cached entry so you can clear it on demand ("clear everything tagged `todo`") without waiting for the timer.

---

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

## See it working (checked in the browser and with curl)

Observed in the Chrome tab at `/cache`:

| Action | `revalidate: 60` Date | `no-store` Date |
|---|---|---|
| First load | `09:06:18 GMT` | `10:06:23 GMT` |
| After a form submit (updateTag), more than 60s later | `10:06:23 GMT` | `10:06:44 GMT` |

The `revalidate` Date stayed the same while its 60-second window was open. Once the window passed, the next request refreshed it. The `no-store` Date changes on every request.

---

## ⚠️ Gotchas

- `revalidate` and `no-store` together are not allowed. Pick one.
- Route-level `export const revalidate = 60` from the notes is removed when `cacheComponents` is on (see [18](18_previous_model_and_notes_corrections.md)).
- A `no-store` fetch makes the component dynamic. Wrap it in `<Suspense>` (this app does) or the build fails.
- The browser `fetch` example from the notes (`"use client"` + `useEffect`) ignores `next`. This is documented, not demoed.

## 🎯 Interview quick answers

| Question | Short answer |
|---|---|
| `revalidate: 60` vs `no-store`? | Reuse for 60s (bg refresh) vs fetch every request |
| Is `fetch` cached by default? | Not in Next 15+. It was in Next 14. |
| Why must `no-store` be in `<Suspense>`? | It makes that part dynamic, so it needs a fallback at request time |
| `next.revalidate` in a Client Component? | Ignored. The browser's `fetch` doesn't know `next`. |
| Memoization vs Data Cache? | Memoization: duplicates in **one** render. Data Cache: reuse **across** requests. |
