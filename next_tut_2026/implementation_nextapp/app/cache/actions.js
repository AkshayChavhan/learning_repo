"use server"; // Server Actions: the only place updateTag() can be called

import { revalidatePath, updateTag } from "next/cache";
import { addPost } from "@/lib/posts";

// On-demand, read-your-own-writes: the next request sees the new post immediately.
export async function createPost(formData) {
  const title = formData.get("title")?.toString().trim();
  if (!title) return;

  addPost(title, "Added from the caching lab.");
  updateTag("posts");
}

// Refresh everything cached for this route.
export async function refreshPage() {
  revalidatePath("/cache");
}
