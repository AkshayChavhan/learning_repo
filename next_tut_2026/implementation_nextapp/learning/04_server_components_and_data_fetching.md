# 04: Server Components and data fetching

> Notes: [01_nextjs.md](../../notes/01_nextjs.md) — "Server vs Client Components", "Data fetching in Server Components"

## Concept

Every component in the App Router is a **Server Component by default**.

| | Server Component (default) | Client Component |
|---|---|---|
| Runs on | Server only | Server (first HTML) + browser |
| Marked by | Nothing | `"use client"` |
| Can `await` data directly | ✅ | ❌ |
| Can use `useState`, `useEffect`, `onClick` | ❌ | ✅ |
| Sends its JS to the browser | ❌ | ✅ |

```text
Server pre-renders HTML → HTML sent to browser → (Client Components only) JS loads → hydration
```

## What was built

Data lives in `lib/posts.js` (a fake database):

```js
export async function getPosts() { return posts; }
export async function getPost(id) { return posts.find((post) => post.id === id) ?? null; }
```

Home page `app/page.jsx` awaits data directly, with **no `useEffect`**:

```jsx
export default async function Home() {
  const posts = await getPosts();
  return (
    <ul>
      {posts.slice(0, 2).map((post) => (
        <li key={post.id}><Link href={`/posts/${post.id}`}>{post.title}</Link></li>
      ))}
    </ul>
  );
}
```

The posts list at `app/posts/page.jsx` does the same, with an artificial `await wait(1500)` (see [07](07_loading.md)).

## See it working

- `/` shows two post titles. Each title is a link.
- View source: the post titles are already in the HTML. The fetch code is **not** in the browser bundle.

## Gotchas

- Do **not** put `useEffect` + `fetch` in a page when a Server Component can `await` the data.
- Server Components cannot use `useState` or `onClick`. Add `"use client"` only where needed (see [05](05_client_components.md)).
- Under this app's `cacheComponents: true` setting, uncached data that is read outside a `<Suspense>` boundary fails the build. `loading.jsx` provides that boundary for `/posts`.
