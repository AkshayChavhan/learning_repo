import { cacheLife, cacheTag } from "next/cache";
import { getPosts } from "@/lib/posts";

// "use cache" caches the return value of an async function.
// cacheLife sets how long; cacheTag labels it so updateTag/revalidateTag can refresh it.
export async function getCachedPosts() {
  "use cache";
  cacheLife("max");
  cacheTag("posts");
  return getPosts();
}

// Time-based example: the stamp is generated once and reused for ~30 seconds.
export async function getStamp() {
  "use cache";
  cacheLife({ stale: 10, revalidate: 30, expire: 600 });
  return new Date().toISOString();
}
