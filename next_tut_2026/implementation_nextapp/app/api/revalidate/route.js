import { revalidateTag } from "next/cache";

// Route Handler: revalidateTag works here (not updateTag).
// Demo only: no auth, so do not ship this as-is.
export async function POST(request) {
  const tag = new URL(request.url).searchParams.get("tag");
  if (!tag) {
    return Response.json({ error: "Pass ?tag=posts" }, { status: 400 });
  }

  // "max" = serve stale content while fresh data loads in the background.
  revalidateTag(tag, "max");
  return Response.json({ revalidated: tag });
}
