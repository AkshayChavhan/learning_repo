# 13: Route handlers (API routes)

> Notes: [01_nextjs.md](../../notes/01_nextjs.md) — "API routes with `route.js`", "Dynamic routes"

## Concept

Create a `route.js` file in a folder and export functions named after HTTP methods. It answers requests with the Web `Response` API.

```text
GET /api/hello  →  {"message":"hello"}
```

Supported methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`.

> `route.js` and `page.jsx` cannot live in the same folder.

## What was built

| File | URL | Response |
|---|---|---|
| `app/api/hello/route.js` | `/api/hello` | `{"message":"hello"}` |
| `app/api/posts/route.js` | `/api/posts` | JSON list of all posts |
| `app/api/posts/[id]/route.js` | `/api/posts/1` | One post, or `404` JSON |

`app/api/posts/[id]/route.js`:

```js
export async function GET(request, { params }) {
  const { id } = await params;          // Promise in Next 15+
  const post = await getPost(id);

  if (!post) {
    return Response.json({ error: "Post not found" }, { status: 404 });
  }
  return Response.json(post);
}
```

## See it working

Verified with curl on the production build:

```text
GET /api/hello      200  {"message":"hello"}
GET /api/posts/1    200  {"id":"1","title":"What is Next.js?", ...}
GET /api/posts/999  404  {"error":"Post not found"}
```

The home page also links to these three URLs.

## Gotchas

- Use `<a href>` for API links, not `<Link>`, because a route handler is not a page.
- The file must be named exactly `route.js` (or `route.ts`). The notes use `route.js`, and this app does too.
- Reading the body: `await request.json()` inside `POST` if you add one.
