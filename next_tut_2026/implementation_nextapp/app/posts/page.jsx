import Link from "next/link";
import { getPosts, wait } from "@/lib/posts";

export default async function PostsPage() {
  await wait(1500); // artificial delay so loading.jsx is visible
  const posts = await getPosts();

  return (
    <>
      <h1>All posts</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <Link href={`/posts/${post.id}`}>{post.title}</Link>
          </li>
        ))}
      </ul>
    </>
  );
}
