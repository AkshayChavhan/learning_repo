# 17: On-demand revalidation: `updateTag`, `revalidateTag`, `revalidatePath`

> Notes: [03_caching_revalidation.md](../../notes/03_caching_revalidation.md) — "On-demand: `revalidatePath` and `revalidateTag`"

## 🟢 Concept

**The problem with time-based caching:**

```text
10:00:00  Price cached: ₹999           (revalidate: 30)
10:00:05  Admin changes price to ₹799
10:00:05 → 10:00:35  customers still see ₹999  ❌
```

**On-demand revalidation:** cache for a long time, and refresh **exactly when the data changes**.

```text
Time-based:  "Refresh every 30s, whether anything changed or not"
On-demand:   "Refresh when something changed"
```

### Tags: labels on cache entries

```js
cacheTag("price-1");                              // inside a "use cache" function
fetch(url, { next: { tags: ["price-1"] } });      // on a fetch
```

Later, "refresh everything labelled `price-1`" affects only those entries.

### The three functions

| Function | Targets | What happens next | Can be called from |
|---|---|---|---|
| `updateTag(tag)` | A **tag** | Expires **now**. Next request **waits** for fresh data (read-your-own-writes) | **Server Actions only** |
| `revalidateTag(tag, "max")` | A **tag** | Marked **stale**. Next visitor gets the old copy, refresh runs in the background | Server Actions + Route Handlers |
| `revalidatePath(path)` | A **URL path** | Everything cached for that page is refreshed | Server Actions + Route Handlers |

| Function | Café analogy |
|---|---|
| `updateTag` | The chef changes the soup and rewrites the board **before the next customer looks** |
| `revalidateTag` | An "outdated" note goes on the board. The next customer reads the old one while it's rewritten. |
| `revalidatePath` | Wipe **everything on one wall** (the whole page) |

### `updateTag` or `revalidateTag`?

| Situation | Use | Why |
|---|---|---|
| **The user** just submitted a change and expects to see it | `updateTag` | They see their own change immediately |
| **Something outside** changed the data (CMS publish, webhook) | `revalidateTag` | Nobody is waiting on that request, so one old copy is fine and faster |

---

## 🟡 Practical example: admin changes a price

### 1. Cached function with a tag

```js
// lib/products.js
import { cacheLife, cacheTag } from "next/cache";

const prices = { "1": 999, "2": 1499 };   // pretend database (in memory)

export async function getPrice(id) {
  "use cache";
  cacheLife("max");           // very long life, no timer refresh
  cacheTag(`price-${id}`);    // label: price-1, price-2, ...

  console.log(`📦 DB read for product ${id}`);
  return { price: prices[id], readAt: new Date().toLocaleTimeString() };
}

export async function savePrice(id, price) {
  prices[id] = price;         // pretend DB write
}
```

> `cacheLife("max")` without a tag = the price **never** changes. The tag makes it refreshable.

### 2. Server Action: save, then refresh

A **Server Action** is a `"use server"` function. A `<form>` can call it directly, and it runs on the server.

```js
// app/products/[id]/actions.js
"use server";
import { updateTag } from "next/cache";
import { savePrice } from "@/lib/products";

export async function changePrice(formData) {
  const id = formData.get("id");
  const price = Number(formData.get("price"));

  await savePrice(id, price);   // 1. change the data
  updateTag(`price-${id}`);     // 2. drop only this product's cached price
}
```

### 3. Page

```jsx
// app/products/[id]/page.jsx
import { Suspense } from "react";
import { getPrice } from "@/lib/products";
import { changePrice } from "./actions";

async function Product({ params }) {
  const { id } = await params;
  const { price, readAt } = await getPrice(id);

  return (
    <div>
      <p>Price: ₹{price} <small>(read at {readAt})</small></p>
      <form action={changePrice}>
        <input type="hidden" name="id" value={id} />
        <input name="price" placeholder="New price" />
        <button>Save</button>
      </form>
    </div>
  );
}

export default function Page({ params }) {
  return (
    <Suspense fallback={<p>Loading…</p>}>
      <Product params={params} />
    </Suspense>
  );
}
```

| Time | Action | `price-1` cache | DB read? | Page shows |
|---|---|---|---|---|
| 10:00:00 | Open `/products/1` | empty → built | ✅ | ₹999 (read at 10:00:00) |
| 10:05:00 | Refresh | hit (`max`) | ❌ | ₹999 (read at 10:00:00) |
| 10:10:00 | Admin saves **799** | `updateTag` → **expired** | — | — |
| 10:10:00 | Page re-renders after the action | rebuilt | ✅ | **₹799** (read at 10:10:00) |
| 10:20:00 | Refresh | hit | ❌ | ₹799 (read at 10:10:00) |
| 10:20:00 | Open `/products/2` | `price-2` untouched | — | ₹1499 |

```text
10:00:00  📦 DB read for product 1
10:10:00  📦 DB read for product 1   ← only because updateTag cleared it
```

The DB is read **only when data changed**, and the admin sees the change **immediately**.

### The other two

**`revalidateTag` in a Route Handler** (e.g. a webhook from an external system):

```js
// app/api/price-changed/route.js
import { revalidateTag } from "next/cache";

export async function POST(request) {
  const { id } = await request.json();
  revalidateTag(`price-${id}`, "max");     // next visitor: old price once, then new
  return Response.json({ ok: true });
}
```

**`revalidatePath`**, to refresh a whole page:

```js
"use server";
import { revalidatePath } from "next/cache";

export async function refreshProductPage(id) {
  revalidatePath(`/products/${id}`);
}
```

### Recap

```text
Tag the cache   →  cacheTag("price-1")  /  fetch(..., { next: { tags: [...] } })
Data changes    →
   user's own edit   → updateTag        (Server Action, fresh immediately)
   external change   → revalidateTag    (Action or Route, stale-while-revalidate)
   whole page        → revalidatePath   (Action or Route)
```

---

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

---

## ⚠️ Gotchas

- **`updateTag` cannot run in a Route Handler.** Use `revalidateTag` there.
- `revalidateTag(tag)` with one argument is deprecated. Always pass the second argument (`"max"` is recommended).
- The Route Handler above has **no auth**. It's a demo: anyone who can reach it can flush the cache.
- The posts store is in memory. A restart resets it, and the cache is not a database.
- Server Actions run on the server. Calling `revalidatePath` during render throws.
