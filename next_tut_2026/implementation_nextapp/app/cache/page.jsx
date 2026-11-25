import { Suspense } from "react";
import { getCachedPosts, getStamp } from "@/lib/cached";
import { createPost, refreshPage } from "./actions";

// 1. Time-based: a "use cache" value reused for ~30s, then regenerated.
async function CachedStamp() {
  const stamp = await getStamp();
  return (
    <p>
      Generated at <code>{stamp}</code>. Refresh within 30s and it stays the same.
    </p>
  );
}

// 2. fetch options: revalidate (cached 60s) vs no-store (never cached).
//    The Date header is the REMOTE server's time for the response.
async function RemoteFetches() {
  const url = "https://jsonplaceholder.typicode.com/todos/1";
  const cached = await fetch(url, { next: { revalidate: 60, tags: ["todo"] } });
  const fresh = await fetch(url, { cache: "no-store" });

  return (
    <ul>
      <li>next.revalidate 60 → response Date: <code>{cached.headers.get("date")}</code></li>
      <li>cache: "no-store" → response Date: <code>{fresh.headers.get("date")}</code></li>
    </ul>
  );
}

// 3. On-demand: updateTag from a Server Action after a write.
async function PostList() {
  const posts = await getCachedPosts();
  return (
    <>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
      <form action={createPost}>
        <input name="title" placeholder="New post title" required />{" "}
        <button type="submit">Add post (updateTag)</button>
      </form>
    </>
  );
}

export default function CacheLab() {
  return (
    <>
      <h1>Caching lab</h1>

      <h2>1. Time-based cache</h2>
      <Suspense fallback={<p>Loading stamp...</p>}>
        <CachedStamp />
      </Suspense>

      <h2>2. fetch: revalidate vs no-store</h2>
      <Suspense fallback={<p>Fetching...</p>}>
        <RemoteFetches />
      </Suspense>

      <h2>3. On-demand: updateTag</h2>
      <Suspense fallback={<p>Loading posts...</p>}>
        <PostList />
      </Suspense>

      <h2>4. On-demand: revalidatePath</h2>
      <form action={refreshPage}>
        <button type="submit">Revalidate /cache (revalidatePath)</button>
      </form>
      <p>
        Route Handler alternative: <code>POST /api/revalidate?tag=posts</code> calls{" "}
        <code>revalidateTag("posts", "max")</code>.
      </p>
    </>
  );
}
