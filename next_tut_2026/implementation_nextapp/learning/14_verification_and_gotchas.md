# 14: Verification and gotchas

Everything in notes 01 and 02, checked against this app.

## Checklist (notes → app)

| Note topic | Done | Where |
|---|---|---|
| Framework, App Router, Server/Client Component | ✅ | [04](04_server_components_and_data_fetching.md), [05](05_client_components.md) |
| Folders are routes, `page` files | ✅ | [02](02_create_first_route.md) |
| Dynamic segment `[id]`, `params` Promise | ✅ | [08](08_dynamic_routes.md) |
| `"use client"` boundary | ✅ | [05](05_client_components.md) |
| Async Server Component with `await` | ✅ | [04](04_server_components_and_data_fetching.md) |
| Route handler `route.js` | ✅ | [13](13_route_handlers_api.md) |
| Root layout, `children`, `<html>`/`<body>` | ✅ | [03](03_root_layout_and_navigation.md) |
| Nested layouts | ✅ | [06](06_nested_layouts.md) |
| `loading.jsx` | ✅ | [07](07_loading.md) |
| `error.jsx` | ✅ | [09](09_error_handling.md) |
| `global-error.jsx` (expert) | ✅ | [09](09_error_handling.md) |
| `not-found.jsx`, `notFound()` | ✅ | [10](10_not_found.md) |
| `template.jsx` | ✅ | [11](11_template_vs_layout.md) |
| Parallel routes `@slot`, `default.jsx` | ✅ | [12](12_parallel_routes_and_default.md) |

## Test results

Production build (`npm run build`): all routes compile.

```text
○ /   ○ /about   ○ /api/hello   ○ /api/posts   ○ /dashboard   ○ /dashboard/settings
◐ /posts   ◐ /posts/[id]   ƒ /api/posts/[id]
```

HTTP checks (`npm start`):

| URL | Status | Notes |
|---|---|---|
| `/`, `/about`, `/dashboard`, `/dashboard/settings` | 200 | |
| `/posts` | 200 | HTML contains "Loading posts" fallback, then list |
| `/posts/2` | 200 | |
| `/posts/999` | 200 | Not Found UI (streaming had started, see [10](10_not_found.md)) |
| `/posts/crash` | 200 | Error UI is rendered on the client; the server log shows the error with a digest |
| `/nope` | 404 | |
| `/api/posts/999` | 404 | JSON error |

Not verified in a browser: the visual error UI for `/posts/crash`, and the client-side counter reset/keep behaviour. Those are described from the code and Next's docs, so check them by clicking through the app.

## Corrections to the notes

| Notes say | Next 16 docs say | Where |
|---|---|---|
| `error.jsx` gets `{ error, reset }` | `{ error, retry }` | [09](09_error_handling.md) |

Source: `node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/error.md`.

## Gotchas collected

- `create-next-app` refuses to run in a folder with empty subfolders. Remove them first.
- Next 16 + `cacheComponents: true`: uncached data must sit under Suspense (`loading.jsx` or `<Suspense>`), or the build fails.
- Production hides server error messages. Use the server log and the `digest` id.
- A layout that throws is caught by the parent folder's `error.jsx`, not its own.
- Templates reset state on navigation to their own segment only, not to deeper ones.
- Parallel slots need a `default.jsx` or they can fail on hard refresh.
- Internal page links: `<Link>`. Route handlers: plain `<a>`.
