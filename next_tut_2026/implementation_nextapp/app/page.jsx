import Link from "next/link";
import { getPosts } from "@/lib/posts";

// Server Component (default): async + await, no useEffect needed.
export default async function Home() {
  const posts = await getPosts();

  return (
    <>
      <h1>Home</h1>
      <p>Latest posts (fetched on the server):</p>
      <ul>
        {posts.slice(0, 2).map((post) => (
          <li key={post.id}>
            <Link href={`/posts/${post.id}`}>{post.title}</Link>
          </li>
        ))}
      </ul>

      <h2>Route handlers (open in browser)</h2>
      <ul>
        <li><a href="/api/hello">/api/hello</a></li>
        <li><a href="/api/posts">/api/posts</a></li>
        <li><a href="/api/posts/1">/api/posts/1</a></li>
      </ul>
    </>
  );
}
