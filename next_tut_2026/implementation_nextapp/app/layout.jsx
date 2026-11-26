import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "Mini Blog - Next.js learning",
  description: "Covers the App Router notes: layouts, special files, routes and APIs.",
};

// Root layout: required. Must contain <html> and <body>. <main> lives here, so every page renders inside it.
// Alternative: multiple root layouts via route groups. See learning/03_root_layout_and_navigation.md.
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header>
          <strong>Mini Blog</strong>
          <nav>
            <Link href="/">Home</Link>
            <Link href="/posts">Posts</Link>
            <Link href="/about">About</Link>
            <Link href="/dashboard">Dashboard</Link>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
