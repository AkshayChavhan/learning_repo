# 01: What is Next.js?

> **Next.js** is a **React framework**. It adds **routing**, **server rendering**, **data fetching**, and **API routes** on top of React, and it runs on **Node.js**.
> React gives you components. Next.js decides **where** those components run and **how** pages are delivered.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Framework** | React plus the tools to build a full app: routing, data, rendering, and APIs |
| **App Router** | Routing based on folders inside the `app/` directory (the current default) |
| **Server Component** | A component that runs **only on the server**. The default in the App Router |
| **Client Component** | A component that runs in the browser. Marked with `"use client"` at the top of the file |
| **Route segment** | A folder in `app/` that becomes part of a URL |
| **Dynamic segment** | A folder in square brackets, like `[id]`, that matches any value in that URL position |

---

## 🟢 Beginner

### The big idea

Components can run on the **server**, in the **browser**, or **both**. Next.js decides this for each component.

```text
Server Component  →  runs on the server, sends only HTML/result to the browser
Client Component  →  runs in the browser, handles clicks, state, and effects
```

### Folders are routes

In the App Router, the folder structure inside `app/` **is** the routing.

```text
app/
├── page.jsx              →  /
├── about/
│   └── page.jsx          →  /about
└── posts/
    └── [id]/
        └── page.jsx      →  /posts/42, /posts/7, ...
```

| Rule                                   | Example                                                  |
| -------------------------------------- | -------------------------------------------------------- |
| A folder becomes a URL segment         | `app/about/` → `/about`                                  |
| A `page` file renders that URL         | `app/about/page.jsx.` export default function About() {} |
| `[name]` in brackets matches any value | `app/posts/[id]/` → `/posts/anything`                    |

---

## 🟡 Intermediate

### Server vs Client Components

| | Server Component (default) | Client Component |
|---|---|---|
| Where it runs | Server | Browser |
| Marked by | Nothing | `"use client"` at the top of the file |
| Can use `useState`, `useEffect`, `onClick` | ❌ No | ✅ Yes |
| Can `await` data directly | ✅ Yes | ❌ No |
| Sends JavaScript to the browser | ❌ No | ✅ Yes |

```jsx
// app/counter/page.jsx  (Client Component)
"use client";

import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Clicked {count} times</button>;
}
```

> **Rule:** keep components on the server by default. Add `"use client"` only where you need interactivity or browser APIs.

### Data fetching in Server Components

A Server Component can be `async` and `await` the data directly. No `useEffect` is needed.

```jsx
// app/posts/page.jsx  (Server Component)
export default async function Posts() {
  const res = await fetch("https://api.example.com/posts");
  const posts = await res.json();

  return (
    <ul>
      {posts.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  );
}
```

- The `fetch` runs on the server.
- Only the **rendered result** is sent to the browser, not the fetch code.

### API routes with `route.js`

Create a `route.js` file in a folder, and export functions named after HTTP methods.

```javascript
// app/api/hello/route.js
export async function GET() {
  return Response.json({ message: "hello" });
}
```

```text
GET /api/hello  →  {"message":"hello"}
```

### Dynamic routes

Put a name in square brackets to create a dynamic segment. The value comes in through `params`.

```jsx
// app/posts/[id]/page.jsx
export default async function PostPage({ params }) {
  const { id } = await params;     // Next.js 15+: params is a Promise
  return <h1>Post {id}</h1>;
}
```

```text
/posts/42   →  Post 42
/posts/7    →  Post 7
```

> **Version note:** in Next.js 15 and later, `params` is a **Promise**, so you `await` it. In older versions, `params` was a plain object.

---

## 🔴 Expert

### Router comparison: App Router vs Pages Router

| Topic | App Router (`app/`) | Pages Router (`pages/`) |
|---|---|---|
| Route definition | Folder with a `page` file: `app/about/page.jsx` | One file per route: `pages/about.jsx` |
| Layouts | Nested `layout` files wrap child routes | A custom `_app` file wraps all pages |
| Default component type | **Server Components** | React components rendered on the server, then hydrated in the browser |
| Data fetching | `await` inside async Server Components | `getServerSideProps`, `getStaticProps`, and similar functions |
| API routes | `route.js` with HTTP-method exports | `pages/api/*.js` |
| Status | **Recommended** for new projects | Still supported, considered the older approach |

> **Correction to a common claim:** Pages Router components are not "client only". They are rendered on the server (or at build time), then the browser takes over (hydration).

### How rendering is decided

```text
Server Component (default)
   │  runs on the server → HTML + serialized data sent to browser
   ▼
Client Component ("use client")
   │  its JavaScript is sent to the browser and runs there (hydrates)
```

- A `"use client"` file is a **boundary**. Everything it imports also runs on the client.
- Server Components can render Client Components, but Client Components can't import Server Components directly. They can receive them as `children` or props.

### Where to put the `"use client"` line

```jsx
"use client";          // must be the first line, before imports

import { useState } from "react";
```

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Using `useState` in a Server Component | Add `"use client"` at the top of the file |
| `"use client"` below imports | Put it as the first line |
| Using `useEffect` to fetch data that a Server Component could fetch | `await` the fetch in an async Server Component |
| Forgetting that `params` is a Promise (Next.js 15+) | `const { id } = await params;` |
| Putting `page.jsx` directly in a folder that should be a route | Create a folder for each route segment |
| Adding `"use client"` to every file | Keep components on the server unless they need interactivity |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is Next.js? | A React framework for routing, server rendering, data fetching, and API routes. It runs on Node.js. |
| App Router vs Pages Router? | App Router uses folders in `app/` and Server Components by default. Pages Router uses files in `pages/` and is the older system. |
| What is a Server Component? | A component that runs only on the server. It can `await` data and sends no component code to the browser. |
| What does `"use client"` do? | Marks a file as a Client Component, which runs in the browser and can use state, effects, and event handlers. |
| How do you create an API route? | Add a `route.js` file and export functions named after HTTP methods, like `GET`. |
| How do dynamic routes work? | A bracketed folder name like `[id]` matches any value. The value is available in `params`. |

---

## ✅ Key Takeaways

- Next.js = **React + routing + server rendering + data + APIs**.
- In the **App Router**, folders are routes, `page` files render them, and components are **Server Components** by default.
- Add `"use client"` only where you need interactivity.
- Fetch data in **async Server Components** with `await`.
- In **Next.js 15+**, `params` is a Promise.
