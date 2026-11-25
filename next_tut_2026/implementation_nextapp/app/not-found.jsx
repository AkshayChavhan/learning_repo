import Link from "next/link";

// Shown for unknown URLs and when notFound() is called.
export default function NotFound() {
  return (
    <>
      <h1>Not Found</h1>
      <p>This page or post does not exist.</p>
      <Link href="/">Return Home</Link>
    </>
  );
}
