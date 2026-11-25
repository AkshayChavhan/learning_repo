"use client"; // error files must be Client Components

// Catches errors from page.jsx in this same folder. Next 16 passes `retry`
// (the older notes call it `reset`).
export default function PostError({ error, retry }) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={() => retry()}>Try again</button>
    </div>
  );
}
