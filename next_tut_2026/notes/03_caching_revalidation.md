# 03: Caching & Revalidation

> **Caching** keeps a **copy of a result** so you don't recompute or refetch it every time.
> **Revalidation** is how that copy gets **refreshed**: after a set time, or on demand after a change.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Cache** | A stored copy of a result that later requests reuse |
| **Data Cache** | Stores `fetch` results on the server, across requests |
| **Revalidation** | Replacing a cached copy with fresh data |
| **Time-based revalidation** | The cached copy is reused for N seconds, then refreshed |
| **On-demand revalidation** | Marking a cached copy stale right away, after a change |
| **Tag** | A label on cached data, so you can revalidate a group of it |

---

## 🟢 Beginner

### The idea

```text
Without cache:  request → fetch API → response      (every request calls the API)
With cache:     request → stored copy → response    (API called only when needed)
```

- In a **Server Component**, a `fetch` result can be stored on the server.
- The next request for the same data reads the stored copy.

### Two ways to refresh

| Type | When the data refreshes |
|---|---|
| **Time-based** | After N seconds |
| **On-demand** | Right after a change, such as a form submit |

---

## 🟡 Intermediate

### Time-based: `next.revalidate`

```jsx
// app/products/page.jsx  (Server Component)
export default async function Products() {
  const res = await fetch("https://api.example.com/products", {
    next: { revalidate: 60 },          // reuse for 60 seconds, then refetch
  });
  const products = await res.json();

  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

```text
t = 0s    request → API called, result cached
t = 30s   request → cached copy (no API call)
t = 61s   request → cache is stale → API called, cache refreshed
```

> The first request after the time limit gets the **old** copy, and the refresh runs in the background. This is "stale-while-revalidate".



The `next: { revalidate: 60 }` option has no effect in a Client Component.

```jsx
"use client";
useEffect(() => {
  fetch("/api/posts", { next: { revalidate: 60 } });  // ⚠️ "next" option is ignored
}, []);
```

| Where `fetch` runs | Which `fetch` | `revalidate: 60` works? | Where it's cached |
|---|---|---|---|
| Server Component / `route.js` | Next.js-extended `fetch` | ✅ Yes | **Server**, in the Next.js Data Cache |
| Client Component (browser) | The browser's own `fetch` | ❌ Ignored | Only the **browser HTTP cache**, if the response's `Cache-Control` headers allow it |

**Why:** revalidation belongs to Next.js's **server-side Data Cache**. The browser's `fetch` has never heard of the `next` option, so it just skips it.

**If you want 60s caching for client-side data:**

- Fetch in a **Server Component** and pass the data down as props. This is the usual approach.
- Or make the client call your own `route.js`, which fetches with `revalidate: 60` on the server.
- Or use a client library like **SWR** or **React Query** (for example `dedupingInterval` / `staleTime`), which cache in browser memory.



### Caching behavior of `fetch`

| Option | Behavior |
|---|---|
| `cache: "force-cache"` | Cache the result until revalidated |
| `cache: "no-store"` | Never cache. Fetch on every request |
| `next: { revalidate: N }` | Cache for N seconds |
| *(no option)* | Depends on your Next.js version (see Expert) |

```jsx
await fetch(url, { cache: "no-store" });        // always fresh
await fetch(url, { cache: "force-cache" });     // cached until revalidated
```

### On-demand: `revalidatePath` and `revalidateTag`

Refresh the cache right after a change, such as a form submit:

```jsx
// app/actions.js
"use server";

import { revalidatePath } from "next/cache";

export async function addProduct(formData) {
  await saveToDatabase(formData);
  revalidatePath("/products");        // the next /products request gets fresh data
}
```

| Function | What it refreshes |
|---|---|
| `revalidatePath("/products")` | Everything cached for that path |
| `revalidateTag("products")` | Every fetch tagged `products` |

Tag a fetch so you can revalidate it by name:

```jsx
const res = await fetch(url, { next: { tags: ["products"] } });
```

> `revalidatePath` and `revalidateTag` run in **Server Actions** or **Route Handlers**, not during render.

---

## 🔴 Expert

### Layers of caching

| Layer | What it stores | Where |
|---|---|---|
| **Data Cache** | `fetch` results | Server, persists across requests |
| **Full Route Cache** | Rendered HTML and RSC payload of static routes | Server, at build or revalidation |
| **Router Cache** | Pages the user has visited | Browser, for fast back/forward |

### Caching defaults changed between versions

- In **Next.js 14**, `fetch` was cached by default.
- In **Next.js 15** and later, `fetch` is **not cached** by default.
- Always check the docs for your version, and state `cache` or `next.revalidate` explicitly.

### Route-level revalidation

Set one value for a whole page, instead of on each `fetch`:

```jsx
// app/products/page.jsx
export const revalidate = 60;         // the page is cached and refreshed every 60 seconds
```

### Caching data that isn't a `fetch`

Wrap any async function (like a database query) with `unstable_cache`:

```jsx
import { unstable_cache } from "next/cache";

const getProducts = unstable_cache(
  async () => db.products.findMany(),
  ["products"],                        // cache key
  { revalidate: 60, tags: ["products"] }
);
```

> `unstable_cache` is the name in current releases. Check the docs for your version, since caching APIs are still changing.

### Opting out of caching

| Want | Use |
|---|---|
| Fresh data on each request | `cache: "no-store"` on `fetch` |
| Fresh data for a whole route | `export const dynamic = "force-dynamic"` |
| Cached until changed | `cache: "force-cache"`, plus `revalidatePath` or `revalidateTag` |

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Expecting `fetch` to be cached in Next.js 15+ without asking for it | Add `cache: "force-cache"` or `next: { revalidate }` |
| Calling `revalidatePath` during render | Call it in a Server Action or Route Handler |
| Setting a long `revalidate` for data that changes often | Use a short time, or revalidate on demand after changes |
| Expecting the update to show immediately after a time-based refresh | The first request after the time limit still gets the old copy |
| Caching user-specific data for everyone | Use `no-store`, or cache per user with a tag or key |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is caching in Next.js? | Storing a result, such as a `fetch` response, so later requests reuse it without calling the source again. |
| What is revalidation? | Replacing a cached copy with fresh data, either after a time limit or on demand. |
| Time-based vs on-demand? | Time-based refreshes after N seconds with `next: { revalidate }`. On-demand refreshes right after a change with `revalidatePath` or `revalidateTag`. |
| What does `no-store` do? | Skips the cache, so every request fetches fresh data. |
| What is the Data Cache? | The server-side store of `fetch` results, shared across requests. |
| Where do you call `revalidatePath`? | In a Server Action or Route Handler, not during render. |

---

## ✅ Key Takeaways

- **Cache** = reuse a stored result. **Revalidate** = refresh it.
- Use `next: { revalidate: N }` for data that can be a little stale.
- Use `revalidatePath` **/** `revalidateTag` after changes.
- Be explicit about caching: defaults **changed in Next.js 15**.
