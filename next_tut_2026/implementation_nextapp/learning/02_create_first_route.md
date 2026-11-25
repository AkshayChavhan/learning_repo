# 02: Create the first route

> Notes: [01_nextjs.md](../../notes/01_nextjs.md) — "Folders are routes"

## Concept

In the App Router, **the folder structure inside `app/` is the routing**.

| Rule | Example |
|---|---|
| A folder becomes a URL segment | `app/about/` → `/about` |
| A `page` file renders that URL | `app/about/page.jsx` |
| `app/page.jsx` is the home URL | `/` |

## What was built

```text
app/
├── page.jsx           →  /
└── about/
    └── page.jsx       →  /about
```

`app/about/page.jsx`:

```jsx
export default function About() {
  return (
    <>
      <h1>About</h1>
      <p>This app is a small playground for the App Router.</p>
    </>
  );
}
```

`app/page.jsx` (home) is an async Server Component. It is covered in [04](04_server_components_and_data_fetching.md).

## See it working

| URL | Expected |
|---|---|
| `/` | Home heading "Home" |
| `/about` | Heading "About" |
| `/nope` | "Not Found" page (see [10](10_not_found.md)) |

## Gotchas

- A folder **without** `page.jsx` is not a route. `app/posts/` alone gives 404 for `/posts`.
- `page.jsx` must be inside the folder. `app/about.jsx` does **not** create `/about`.
- In the notes, the file is called `page.jsx`. Next also accepts `page.js`; this app uses `.jsx` to match the notes.
