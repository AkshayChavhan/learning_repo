# 15: Time-based caching

> Notes: [03_caching_revalidation.md](../../notes/03_caching_revalidation.md) — "The idea", "Time-based: `next.revalidate`"

## 🟢 Concept

**The problem:** a page needs data that takes 2s to get (DB query, slow API). 1,000 visitors means the same 2s job runs 1,000 times, even though the data barely changes.

**Caching:** do the job **once**, save the result, and give everyone the saved copy.

```text
Without cache:  visitor → do the work (2s) → page      (every time)
With cache:     visitor → saved copy (instant) → page
```

**Time-based revalidation:** the copy is good for X seconds, then it gets refreshed.

### Stale-while-revalidate

When the timer runs out, the next visitor does **not** wait. They get the old copy, and the refresh runs in the background.

```text
t = 0s    request → computed, result cached
t = 30s   request → cached copy (no recompute)
t = 61s   request → stale → old copy served, refresh runs in background
t = 62s+  request → new copy
```

> One visitor sees slightly old data, but **nobody ever waits**.

### This app's method

This app runs Next 16 with `cacheComponents: true`, so caching uses **`"use cache"` + `cacheLife`**, not the `export const revalidate` route option from the notes (see [18](18_previous_model_and_notes_corrections.md)).

| Old model (notes) | New model (this app) |
|---|---|
| `export const revalidate = 60` | `"use cache"` + `cacheLife(...)` |
| Whole page/route | **One function** (more precise) |

---

## 🟡 The three `cacheLife` timers

There are **two caches**, and each timer controls one of them:

```text
  BROWSER                                SERVER
 ┌───────────────┐   asks if needed    ┌──────────────────┐
 │ browser copy  │ ──────────────────► │ server copy      │
 │ uses: stale   │ ◄────────────────── │ uses: revalidate │
 └───────────────┘                     │       expire     │
                                       └──────────────────┘
```

| Timer | Whose | Meaning | Café analogy |
|---|---|---|---|
| `stale` | **Browser** | Reuse its own copy without asking the server | You remember the menu, so you don't look at the board |
| `revalidate` | **Server** | After this, serve the old copy and refresh from the DB in the background | The chef rewrites the board while you read the old one |
| `expire` | **Server** | No requests for this long → copy **deleted**, next visitor **waits** | The café was closed all night, so the board is wiped |

Rule: `stale` ≤ `revalidate` ≤ `expire`. All are seconds since the copy was built.

```text
0s          10s                    30s                                   600s
├────────────┼──────────────────────┼─────────────────────────────────────┼──────────►
│  browser   │                      │                                     │
│  reuses    │  browser asks server │                                     │
│  its copy  │                      │                                     │
├────────────┴──────────────────────┼─────────────────────────────────────┼──────────
│  server: FRESH                    │  server: STALE                      │ EXPIRED
│  serve copy, no DB                │  serve old copy + DB call in bg     │ delete,
│                                   │  (visitor doesn't wait)             │ visitor WAITS
```

- `stale` only applies to **`<Link>` navigation**. F5 / refresh always asks the server.
- `revalidate` is **not** "the browser asks every 30s". The browser asks whenever. It's the server deciding whether its copy is fresh.
- `expire` only happens when **nobody** visits for a long time. Regular traffic keeps refreshing the copy first.

---

## 🟡 Practical example: `getPrice(productId)`

```js
// lib/products.js
import { cacheLife } from "next/cache";

export async function getPrice(productId) {
  "use cache";
  cacheLife({ stale: 10, revalidate: 30, expire: 600 });

  console.log(`📦 API called for product ${productId}`);

  const res = await fetch(`https://dummyjson.com/products/${productId}`);
  if (!res.ok) throw new Error("Could not load price");
  const product = await res.json();

  return {
    title: product.title,
    price: product.price,
    discount: product.discountPercentage,
    fetchedAt: new Date().toLocaleTimeString(),   // shows when the copy was built
  };
}
```

```jsx
// app/products/[id]/page.jsx
import { Suspense } from "react";
import { getPrice } from "@/lib/products";

async function ProductPrice({ params }) {
  const { id } = await params;
  const { title, price, discount, fetchedAt } = await getPrice(id);
  return (
    <div>
      <h1>{title}</h1>
      <p>Price: ${price} ({discount}% off)</p>
      <small>Price fetched at {fetchedAt}</small>
    </div>
  );
}

export default function Page({ params }) {
  return (
    <Suspense fallback={<p>Loading price…</p>}>
      <ProductPrice params={params} />
    </Suspense>
  );
}
```

| Time | Visit | Copy's age | Rule | API called? | Page shows |
|---|---|---|---|---|---|
| 10:00:00 | `/products/1` | none | first build | ✅ you wait | fetched at 10:00:00 |
| 10:00:20 | `/products/2` | none for "2" | first build | ✅ you wait | fetched at 10:00:20 |
| 10:00:25 | `/products/1` (F5) | 25s | fresh | ❌ | fetched at 10:00:00 |
| 10:00:45 | `/products/1` (F5) | 45s | stale → old copy + bg refresh | ✅ background | fetched at **10:00:00** |
| 10:00:46 | `/products/1` (F5) | 1s (new) | fresh | ❌ | fetched at **10:00:45** |
| 10:00:48 | `/products/2` (F5) | 28s | fresh (own timer) | ❌ | fetched at 10:00:20 |
| 10:20:00 | `/products/1` (F5) | > 600s | **expired** → deleted | ✅ you wait | fetched at 10:20:00 |

```text
10:00:00  📦 API called for product 1
10:00:20  📦 API called for product 2
10:00:45  📦 API called for product 1   ← background refresh
10:20:00  📦 API called for product 1   ← after expire
```

7 visits, 4 API calls.

### Why the log doesn't print every time

`"use cache"` caches the **whole function call**. On a hit, the body is **skipped**, so the `console.log` inside it never runs.

```text
getPrice("1") called → fresh saved result?
   YES → return saved result (body skipped, no log)
   NO  → run body (log prints, fetch runs) → save → return
```

> A log **outside** the cached function (e.g. in the component) prints on every request. That's an easy way to see the difference.

### Cache key: one copy per argument

```text
key = build ID + function (file + name) + arguments

getPrice + ("1")  → { title: "iPhone 9", ... }
getPrice + ("2")  → { title: "iPhone X", ... }
```

- Same arguments → same key, every time. IDs never mix.
- ⚠️ `getPrice("1")` and `getPrice(1)` are **different keys**. `params` gives strings, so keep the type consistent.

| A hit is not guaranteed when… | Why |
|---|---|
| Past `expire` | Entry deleted |
| New deploy | New build ID → new keys |
| Server restart | Default cache is in server memory |
| Memory full | Least-used entries dropped |
| Multiple servers | Each has its own memory cache (unless a shared cache handler is set up) |

### Can you see it in the browser?

| Cache | Lives in | Visible in DevTools? |
|---|---|---|
| `"use cache"` result | Server memory | ❌ Only its **output** (page / RSC response) |
| `stale` copy | Next.js router memory | ⚠️ Only as **no request** in the Network tab on `<Link>` navigation |

> Watch the server cache through the terminal log, `fetchedAt` on the page, or `NEXT_PRIVATE_DEBUG_CACHE=1 npm start` (an internal debug flag).

---

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
- `new Date()` inside the cached scope makes caching visible. Outside a cache scope, `Date` during prerender is not allowed with Cache Components. You must either cache it or make it dynamic inside `<Suspense>`.

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

That's stale-while-revalidate: the first request after the window gets the old copy, and the refresh runs in the background.

---

## ⚠️ Gotchas

- `fetch(..., { next: { revalidate: 60 } })` still works for **fetch calls** (see [16](16_fetch_revalidate_vs_no_store.md)). For other code (DB queries, calculations), use `"use cache"` + `cacheLife`.
- `cacheLife` must be called **inside** the cache scope, not at module top level.
- Short lifetimes (`revalidate: 0`, the `seconds` profile, or `expire` < 5 min) make the value a **dynamic hole** instead of a prerender. `expire: 600` is long enough to stay cached.
- The page shell has its own revalidate window: the build showed `/cache` with `Revalidate 1m`, so the shell can lag behind the stamp.
- Test caching with `npm run build && npm start`. `npm run dev` doesn't behave the same.
- Built-in presets instead of numbers: `cacheLife("seconds" | "minutes" | "hours" | "days" | "weeks" | "max")`.
