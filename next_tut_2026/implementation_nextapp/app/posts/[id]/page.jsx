import Link from "next/link";
import { notFound } from "next/navigation";
import { getPost } from "@/lib/posts";

// Dynamic route: [id] matches any value. params is a Promise in Next 15+.
export default async function PostPage({ params }) {
  const { id } = await params;

  // Demo: throw so error.jsx in this same folder catches it.
  if (id === "crash") {
    throw new Error("Demo crash: caught by posts/[id]/error.jsx");
  }

  const post = await getPost(id);
  if (!post) notFound(); // renders app/not-found.jsx

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.body}</p>
      <Link href="/posts">Back to posts</Link>
    </article>
  );
}
