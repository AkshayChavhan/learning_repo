"use client"; // Client Component: needs useState and onClick

import { useState } from "react";

export default function Counter({ label }) {
  const [count, setCount] = useState(0);
  return (
    <button className="counter" onClick={() => setCount(count + 1)}>
      {label}: clicked {count} times
    </button>
  );
}
