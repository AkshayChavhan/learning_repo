# Learning: App Router, step by step

This folder documents what was built in this app, one topic per file, in the order the
notes cover it. Each file says **what the concept is**, **which file implements it**,
**how to see it working**, and **gotchas**.

Source notes: [01_nextjs.md](../../notes/01_nextjs.md) and [02_special_files.md](../../notes/02_special_files.md).

## Topics

| # | Topic | Covers (from notes) | Main files |
|---|---|---|---|
| 01 | [Installation](01_installation_nextjs.md) | What Next.js is, setup, dev/build | `package.json`, `next.config.mjs` |
| 02 | [Create first route](02_create_first_route.md) | Folders are routes, `page` files | `app/page.jsx`, `app/about/page.jsx` |
| 03 | [Root layout and navigation](03_root_layout_and_navigation.md) | `layout`, `children`, `<html>`/`<body>` | `app/layout.jsx` |
| 04 | [Server components and data fetching](04_server_components_and_data_fetching.md) | Server Components, `async`/`await` | `app/page.jsx`, `app/posts/page.jsx`, `lib/posts.js` |
| 05 | [Client components](05_client_components.md) | `"use client"`, `useState`, hydration | `components/Counter.jsx` |
| 06 | [Nested layouts](06_nested_layouts.md) | Layouts stack and stay mounted | `app/posts/layout.jsx`, `app/dashboard/layout.jsx` |
| 07 | [Loading](07_loading.md) | `loading.jsx`, Suspense | `app/posts/loading.jsx` |
| 08 | [Dynamic routes](08_dynamic_routes.md) | `[id]`, `params` as a Promise | `app/posts/[id]/page.jsx` |
| 09 | [Error handling](09_error_handling.md) | `error.jsx`, `retry`, `global-error.jsx` | `app/posts/[id]/error.jsx`, `app/global-error.jsx` |
| 10 | [Not found](10_not_found.md) | `not-found.jsx`, `notFound()` | `app/not-found.jsx` |
| 11 | [Template vs layout](11_template_vs_layout.md) | `template.jsx`, state reset | `app/dashboard/settings/template.jsx` |
| 12 | [Parallel routes and default](12_parallel_routes_and_default.md) | `@slot`, `default.jsx` | `app/dashboard/@stats/*` |
| 13 | [Route handlers (API)](13_route_handlers_api.md) | `route.js`, HTTP-method exports | `app/api/**/route.js` |
| 14 | [Verification and gotchas](14_verification_and_gotchas.md) | Checklist, real test results, notes corrections | all |
| 15 | [Time-based caching](15_time_based_caching.md) | `"use cache"`, `cacheLife`, stale-while-revalidate | `lib/cached.js`, `app/cache/page.jsx` |
| 16 | [fetch: revalidate vs no-store](16_fetch_revalidate_vs_no_store.md) | `next.revalidate`, `cache: "no-store"`, client-side pitfall | `app/cache/page.jsx` |
| 17 | [On-demand revalidation](17_on_demand_updateTag_revalidateTag_revalidatePath.md) | `updateTag`, `revalidatePath`, `revalidateTag` | `app/cache/actions.js`, `app/api/revalidate/route.js` |
| 18 | [Previous model and notes corrections](18_previous_model_and_notes_corrections.md) | Route-segment `revalidate`, `unstable_cache`, deprecated signatures | all of the above |

## Run it

```bash
cd implementation_nextapp
npm install
npm run dev        # development, http://localhost:3000
# or
npm run build && npm start
```

## Route map

```text
/                      Home (server component, fetches posts)
/about                 static page
/posts                 list, with loading.jsx and nested layout
/posts/1               dynamic page
/posts/crash           throws on purpose -> error.jsx
/posts/999             missing post -> notFound() -> not-found.jsx
/dashboard             layout + @stats slot + layout counter
/dashboard/settings    template counter (resets) + layout counter (kept)
/cache                 caching lab: time-based, fetch options, updateTag, revalidatePath
/api/hello             route handler
/api/posts             route handler (list)
/api/posts/1           dynamic route handler
```
