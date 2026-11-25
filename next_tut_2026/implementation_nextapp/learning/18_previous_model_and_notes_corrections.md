# 18: Previous model and notes corrections

> Notes: [03_caching_revalidation.md](../../notes/03_caching_revalidation.md) — "Expert" section, "Opting out of caching", "Caching data that isn't a fetch"

This app has `cacheComponents: true`. Some parts of the notes describe the **previous caching model**, which Next 16 removes or replaces when Cache Components are on. The bundled docs are the source of truth:
`node_modules/next/dist/docs/01-app/02-guides/caching-without-cache-components.md`.

## What changed

| Notes say | Next 16 with `cacheComponents: true` | Used here |
|---|---|---|
| `export const revalidate = 60` on a page | Removed. Route-segment `revalidate`, `dynamic`, `dynamicParams`, `fetchCache` are gone | Not used |
| `export const dynamic = "force-dynamic"` | Removed. Use `cache: "no-store"` on fetch, or dynamic APIs | Not used |
| `unstable_cache(fn, [key], { revalidate, tags })` | Replaced by `"use cache"` + `cacheLife` + `cacheTag` | [15](15_time_based_caching.md), [17](17_on_demand_updateTag_revalidateTag_revalidatePath.md) |
| `revalidateTag("products")` (one argument) | Deprecated. Pass a profile: `revalidateTag("products", "max")` | Route Handler in [17](17_on_demand_updateTag_revalidateTag_revalidatePath.md) |
| `revalidatePath` / `revalidateTag` in Server Actions | `updateTag` is the read-your-own-writes choice; works only in Server Actions | [17](17_on_demand_updateTag_revalidateTag_revalidatePath.md) |
| `fetch` next.revalidate and tags | Still supported | [16](16_fetch_revalidate_vs_no_store.md) |
| Browser `fetch` with `next` option | Still ignored in the browser | Documented only |

## Things the notes got right

- Fetch is not cached by default in Next 15+. Check the option you need explicitly.
- `revalidatePath` / `revalidateTag` run in Server Actions or Route Handlers, not during render.
- The Client Component `fetch` + `next.revalidate` pitfall is still real.

## Note on "layers of caching"

The notes' three-layer table (Data Cache, Full Route Cache, Router Cache) is still a useful mental model. With Cache Components the route-level pieces are driven by `"use cache"` scopes and the shell prerender, not by the old route options. The build output in this app shows the effect: `/cache` is a partial prerender with its own `Revalidate 1m` window, separate from the 30s stamp inside it.

## Gotchas

- Copy caching examples from the bundled docs for this version, not from older tutorials.
- `"use cache"` needs `cacheLife` (the notes' recommendation). Without one, the `default` profile applies, which is less obvious at the call site.
