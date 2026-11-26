# 04: Data Fetching Strategies

> **Fetching in Server Components** is just `await` inside an `async` component: no `useState`, no `useEffect`, no loading state.
> **Caching** saves a result on the server so later requests skip the API. **Revalidation** refreshes it, by time or on demand.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Cache** | A saved result that later requests reuse instead of calling the source again |
| **Data Cache** | Server-side store for `fetch` results, shared across requests and users |
| **Revalidation** | Replacing a cached result with fresh data |
| **ISR** | Cache for N seconds, then refresh in the background (`revalidate: N`) |
| **SSG** | Cache at build time and serve it as a static page |
| **SSR** | Fetch on every request (`no-store`) |
| **Request memoization** | One render pass makes one real request for identical GET `fetch` calls |
| **Suspense streaming** | Sections of a page render as their data arrives, instead of waiting for all of it |

---

## 🟢 Beginner

### Why cache?

```text
WITHOUT cache:  1000 visitors → 1000 API calls   (slow, expensive)
WITH cache:     1000 visitors → 1 API call + 999 cache hits   (fast, cheap)
```

The cache lives on the **server**, so every user benefits. A browser cache only helps one person.

### Where can you fetch data?

| Location | Use it for |
|---|---|
| **Server Components** (default) | Reading data: `await` directly in the component |
| **Route Handlers** (`route.js`) | External APIs, webhooks |
| **Server Actions** | Writes: create, update, delete (form submits) |
| **Client Components** (`useEffect` or SWR) | User-specific or real-time data, after login |

### React vs Next.js

```jsx
// React (Client Component): state, effect, loading flag
const [products, setProducts] = useState([]);
const [loading, setLoading] = useState(true);
useEffect(() => {
  fetch("/api/products").then(r => r.json()).then(d => { setProducts(d); setLoading(false); });
}, []);

// Next.js (Server Component): just await
export default async function ProductsPage() {
  const res = await fetch("https://api.example.com/products");
  const products = await res.json();
  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

| | React (`useEffect`) | Next.js Server Component |
|---|---|---|
| Runs on | Browser | Server |
| Loading state | You write it | Not needed |
| HTML for search engines | Blank at first | Pre-rendered |

### The `fetch` cache options

Next.js extends the standard `fetch` with a `cache` option and a `next` option.

| Code | Strategy | Refetches when |
|---|---|---|
| `fetch(url, { cache: "force-cache" })` | SSG | Only on redeploy, or when revalidated |
| `fetch(url, { cache: "no-store" })` | SSR | Every request |
| `fetch(url, { next: { revalidate: 3600 } })` | ISR | Every 3600 seconds, refreshed in the background |
| `fetch(url, { next: { tags: ["products"] } })` | On-demand | When `revalidateTag("products")` runs |
| `fetch(url)` *(no option)* | Depends on version | See the version note below |

> **Version note:** in **Next.js 14**, `fetch` was cached by default. In **Next.js 15 and later**, a `fetch` with no cache option is **not cached** (it behaves like `no-store`). Add `cache: "force-cache"` to opt in.
> Source: [Next.js 15 upgrade guide](https://nextjs.org/docs/15/app/guides/upgrading/version-15), [Caching in Next.js (v15)](https://nextjs.org/docs/15/app/guides/caching)

### Real-world choices

| Data | Option | Why |
|---|---|---|
| About page, terms | `force-cache` | Never changes |
| Crop or stock prices | `revalidate: 3600` | Stale by up to an hour is fine |
| User's own dashboard | `no-store` | Different per user, always fresh |
| Admin-managed content | `tags` + `revalidateTag` | Refresh exactly when an admin edits it |

---

## 🟡 Intermediate

### Where the cache lives (Vercel)

A Lambda function is **stateless** and dies after each request, so the cache can't live inside it.

```text
Lambda A:  fetch → calls API → saves to Vercel Data Cache → dies
Lambda B:  fetch → Data Cache HIT → instant
SSG page:  full HTML saved to Edge CDN → Lambda not called at all
```

- **On Vercel:** the Data Cache is shared by all Lambdas, and the Edge CDN serves static HTML worldwide.
- **On your own server:** the cache is stored in `.next/cache/`. With several servers, use a shared cache handler such as Redis, so every server reads the same cache.

### Checking whether the cache is working

Look for the `x-nextjs-cache` response header in DevTools → Network:

| Value | Meaning |
|---|---|
| `HIT` | Served from cache |
| `MISS` | Fetched fresh from the source |
| `STALE` | Served from cache while refreshing in the background |
| `SKIP` | Cache not used (SSR or `no-store`) |

You can also time the call:

```js
const start = Date.now();
await fetch("https://api.example.com/products", { next: { revalidate: 30 } });
console.log(`Took: ${Date.now() - start}ms`);
// First call  → Took: 387ms  (MISS)
// Second call → Took: 2ms    (HIT)
```

### Sequential vs parallel fetching

Each `await` in a row waits for the one before it: a **waterfall**. `Promise.all` starts them together.

```js
// SEQUENTIAL: 200 + 300 + 250 = 750ms
const user    = await fetchUser();     // 200ms
const crops   = await fetchCrops();    // 300ms, waits for user
const weather = await fetchWeather();  // 250ms, waits for crops

// PARALLEL: max(200, 300, 250) = 300ms
const [user, crops, weather] = await Promise.all([
  fetchUser(),
  fetchCrops(),
  fetchWeather(),
]);
```

> **Rule:** if the requests don't depend on each other, use `Promise.all`.

### Request memoization

If `layout.jsx` and `page.jsx` both call the same URL during one render, Next.js makes **one** real request.

```jsx
// layout.jsx
const user = await fetch("/api/user").then(r => r.json());     // real request

// page.jsx (same render)
const user = await fetch("/api/user").then(r => r.json());     // reused, no request
```

| Applies to | Does not apply to |
|---|---|
| Identical GET `fetch` calls in one render pass | Different URLs or options |
| | Separate users or separate requests |
| | Prisma or other DB calls (they aren't `fetch`) |

### Caching Prisma or other DB queries

`fetch` caching doesn't cover Prisma. You have two choices:

**Option A: set the whole page** with route segment config.

```tsx
// app/dashboard/page.tsx
export const revalidate = 3600;           // ISR: refresh the page every hour
// or
export const dynamic = "force-dynamic";   // SSR: always fresh
```

| Setting | Strategy |
|---|---|
| `export const revalidate = false` | SSG (cache forever) |
| `export const revalidate = 0` | SSR (never cache) |
| `export const revalidate = 3600` | ISR (every hour) |
| `export const dynamic = "force-dynamic"` | Always SSR |
| `export const dynamic = "force-static"` | Always SSG |

**Option B: wrap the query** with `unstable_cache`.

```tsx
import { unstable_cache } from "next/cache";
import { db } from "@/lib/db";

const getCropStats = unstable_cache(
  async (region: string) =>
    db.crop.groupBy({ by: ["type"], where: { region }, _avg: { price: true } }),
  ["crop-stats"],                            // cache key
  { tags: ["crop-stats"], revalidate: 3600 } // tag + time
);
```

> `unstable_cache` is the name in current releases, but it's tied to the older caching model. Check your version's docs. See the note under **Newer Next.js** below.

### On-demand revalidation

Refresh the cache right after a change, instead of waiting for a timer.

```tsx
"use server";
import { revalidateTag, revalidatePath } from "next/cache";

export async function addProduct(formData: FormData) {
  await db.product.create({ data: { name: formData.get("name") as string } });
  revalidateTag("products");          // every fetch tagged "products", on any page
  revalidatePath("/products");        // the /products page itself
}
```

| Function | What it clears | Use when |
|---|---|---|
| `revalidateTag("products")` | Every fetch with that tag, across pages | The same data appears on many pages |
| `revalidatePath("/products")` | All data for one URL | You know exactly which page changed |

> Call these in a **Server Action** or **Route Handler**, not during render.

### Client-side fetching: SWR

Use client fetching only for user-specific data after login, or real-time updates. Prefer SWR over a hand-written `useEffect`, because SWR handles caching, retries, and refetching.

```tsx
"use client";
import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then(r => r.json());

function UserOrders() {
  const { data, error, isLoading } = useSWR("/api/my-orders", fetcher);
  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error!</p>;
  return <ul>{data.map(o => <li key={o.id}>{o.name}</li>)}</ul>;
}
```

---

## 🔴 Expert

### The four caching layers

| # | Layer | Where | Cleared by | Shared with |
|---|---|---|---|---|
| 1 | **Request memoization** | Lambda memory | End of the render | One request only |
| 2 | **Data Cache** | Server store | `revalidateTag` / `revalidatePath` | All users |
| 3 | **Full Route Cache** | CDN (HTML) | Revalidation | All users, worldwide |
| 4 | **Router Cache** | Browser memory | `router.refresh()` or a page reload | One user |

> **Router Cache timing changed in Next.js 15.** Dynamic pages are no longer kept in the browser by default (`staleTimes.dynamic` is 0). Static pages are kept for 5 minutes. To restore the old 30-second dynamic cache, set `experimental.staleTimes.dynamic` in `next.config`.
> Source: [staleTimes](https://nextjs.org/docs/15/app/api-reference/config/next-config-js/staleTimes), [Next.js 15 blog](https://nextjs.org/blog/next-15)

### Streaming with Suspense

Each `Suspense` boundary streams in on its own. A slow widget doesn't hold back the fast sections.

```tsx
import { Suspense } from "react";

export default function DashboardPage() {
  return (
    <>
      <h1>Dashboard</h1>                          {/* sent immediately */}
      <Suspense fallback={<p>Loading prices...</p>}>
        <CropPricesTable />                       {/* streams when its query finishes */}
      </Suspense>
      <Suspense fallback={<p>Loading weather...</p>}>
        <WeatherWidget />                         {/* streams independently */}
      </Suspense>
    </>
  );
}

async function CropPricesTable() {
  const crops = await db.crop.findMany();         // blocks only this section
  return <table>{/* rows */}</table>;
}

async function WeatherWidget() {
  const w = await fetch("https://api.weather.com", { cache: "no-store" }).then(r => r.json());
  return <div>Temp: {w.temp}°C</div>;
}
```

### Gotchas

| Gotcha | What happens | Fix |
|---|---|---|
| **Lowest `revalidate` wins for the whole route** | Two fetches with `3600` and `60` make the whole route refresh every 60 seconds | Put each fetch in its own async component inside its own `Suspense` boundary |
| **`cookies()`, `headers()`, `searchParams` opt the route into dynamic rendering** | Even `force-cache` fetches above that line stop being cached | Move the dynamic call into a leaf component |
| **Memoization is per request** | Users A and B don't share request memoization | Expected. It's only a within-render deduplication |
| **`revalidateTag` doesn't clear the browser's Router Cache** | A user may see stale data briefly | Call `router.refresh()` on the client after the Server Action |

> The "lowest value wins" rule is the documented behavior for the older caching model. The [Route Segment Config docs](https://nextjs.org/docs/15/app/api-reference/file-conventions/route-segment-config) and the [fetch reference](https://nextjs.org/docs/app/api-reference/functions/fetch) both describe it: a fetch with a lower `revalidate` than the route's default lowers the interval for the whole route.

---

## 🆕 Newer Next.js: Cache Components

The newer caching model is called **Cache Components**. Under it, `fetch` is uncached unless it runs inside a `use cache` scope, and route settings like `dynamic`, `revalidate`, and `fetchCache` are replaced by `use cache` and `cacheLife`. Everything above describes the Next.js 15 model. If you're on a newer version, check the [migration guide](https://nextjs.org/docs/app/guides/migrating-to-cache-components) before you copy any of these settings.

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Assuming `fetch` is cached by default in Next.js 15+ | Add `cache: "force-cache"` or `next: { revalidate }` |
| Awaiting independent fetches one after another | Use `Promise.all` |
| Caching a Prisma query with `fetch`-style options | Wrap it with `unstable_cache`, or set route config |
| Calling `revalidatePath` during render | Call it in a Server Action or Route Handler |
| A slow fetch and a fast fetch on one page share a short `revalidate` | Split them into separate Suspense boundaries |
| Caching per-user data for everyone | Use `no-store`, or cache per user with a key |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| Where is the Next.js data cache stored? | On the server. On Vercel it's a shared Data Cache, and full pages can be served from the Edge CDN. |
| Why can't the cache live inside a Lambda? | Lambdas are stateless and die after each request. |
| Sequential vs parallel fetching? | Sequential waits for each `await` in turn (sum of times). `Promise.all` runs them together (slowest one). |
| What is request memoization? | Identical GET `fetch` calls in one render pass make one real request. |
| `revalidateTag` vs `revalidatePath`? | `revalidateTag` clears every fetch with that tag across pages. `revalidatePath` clears one URL. |
| How do you cache a Prisma query? | `unstable_cache` with a key, tags, and a time, or route-level `revalidate`. |
| How many caching layers are there? | Four: request memoization, Data Cache, Full Route Cache, Router Cache. |
| How does Suspense help data fetching? | Each boundary streams in when its data arrives, so one slow fetch doesn't block the rest. |
| Why is `Promise.all` important? | It turns a waterfall into one wait for the slowest request. |

---

## ✅ Key Takeaways

- **Server Components** fetch with `await`. No hooks needed.
- Know the **cache options**: `force-cache`, `no-store`, `revalidate`, and `tags`. In **Next.js 15+**, `fetch` is not cached unless you opt in.
- Use **`Promise.all`** for independent requests.
- Use **Suspense** boundaries so slow data doesn't block fast data.
- Refresh with **`revalidateTag` / `revalidatePath`** in a Server Action, and call `router.refresh()` if the browser needs to update.

---

## 📚 Sources

- [Next.js 15 upgrade guide](https://nextjs.org/docs/15/app/guides/upgrading/version-15): `fetch` is no longer cached by default
- [Caching in Next.js (v15)](https://nextjs.org/docs/15/app/guides/caching): caching layers and defaults
- [staleTimes (v15)](https://nextjs.org/docs/15/app/api-reference/config/next-config-js/staleTimes): Router Cache durations
- [Next.js 15 blog](https://nextjs.org/blog/next-15): Router Cache default change
- [Route Segment Config (v15)](https://nextjs.org/docs/15/app/api-reference/file-conventions/route-segment-config): route-level `revalidate` and `dynamic`
- [fetch reference](https://nextjs.org/docs/app/api-reference/functions/fetch): per-fetch `revalidate` behavior
- [Migrating to Cache Components](https://nextjs.org/docs/app/guides/migrating-to-cache-components): the newer caching model
