import { getPost } from "@/lib/posts";

// Dynamic Route Handler: params is a Promise in Next 15+.
export async function GET(request, { params }) {
  const { id } = await params;
  const post = await getPost(id);

  if (!post) {
    return Response.json({ error: "Post not found" }, { status: 404 });
  }
  return Response.json(post);
}
