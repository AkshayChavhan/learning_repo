// Nested layout: wraps only /posts and /posts/[id]. Stays mounted while you move between posts.
export default function PostsLayout({ children }) {
  return (
    <section className="posts">
      <aside>
        <h2>Posts section</h2>
        <p>Nested layout: stays mounted when you switch posts.</p>
      </aside>
      <div>{children}</div>
    </section>
  );
}
