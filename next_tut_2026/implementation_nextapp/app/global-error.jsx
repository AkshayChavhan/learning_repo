"use client";

// Catches errors thrown by the ROOT layout only. Must render its own <html> and <body>.
export default function GlobalError({ error, retry }) {
  return (
    <html lang="en">
      <body>
        <h1>App crashed</h1>
        <p>{error.message}</p>
        <button onClick={() => retry()}>Try again</button>
      </body>
    </html>
  );
}
