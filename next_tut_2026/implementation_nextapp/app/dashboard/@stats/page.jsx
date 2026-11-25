import { getPosts } from "@/lib/posts";

// Parallel-route slot: @stats is NOT a URL segment. Its name becomes the `stats` prop.
export default async function Stats() {
  const posts = await getPosts();
  return <p>Stats: {posts.length} posts in total</p>;
}
