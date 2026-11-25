// Route Handler: export functions named after HTTP methods.
export async function GET() {
  return Response.json({ message: "hello" });
}
