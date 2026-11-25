# 07: Loading UI

> Notes: [02_special_files.md](../../notes/02_special_files.md) — "`loading.jsx`: show while the page loads"

## Concept

`loading.jsx` shows a fallback while a route segment's page is loading. Next wraps the page in a **Suspense boundary** using this file. The fallback is shown first, then the page replaces it.

`loading.jsx` sits **inside** its folder's layout, and wraps `page.jsx` and everything below it. It does **not** wrap the layout in the same folder.

## What was built

`app/posts/loading.jsx`:

```jsx
export default function Loading() {
  return <p>Loading posts...</p>;
}
```

`app/posts/page.jsx` waits 1.5 s on purpose so the fallback is visible:

```jsx
export default async function PostsPage() {
  await wait(1500);
  const posts = await getPosts();
  // ...
}
```

## See it working

1. Click **Posts** in the header. You see "Loading posts..." for about 1.5 s, then the list.
2. Curl check: `curl localhost:3000/posts` contains `Loading posts` (the fallback is in the first HTML).

## Gotchas

- A **layout** that waits on data does **not** show `loading.jsx` in its own folder. It blocks navigation instead. Move the wait into `page.jsx`, or wrap it in its own `<Suspense>`.
- `loading.jsx` takes no props.
- With `cacheComponents: true`, the uncached wait must sit under a Suspense boundary, or the build fails. `loading.jsx` provides it.
