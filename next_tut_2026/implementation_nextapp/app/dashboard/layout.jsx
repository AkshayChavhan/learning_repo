import Link from "next/link";
import Counter from "@/components/Counter";

// Dashboard layout. `stats` is a parallel-route slot (app/dashboard/@stats).
// `children` is the current page.
export default function DashboardLayout({ children, stats }) {
  return (
    <section>
      <h1>Dashboard</h1>
      <nav>
        <Link href="/dashboard">Overview</Link> | <Link href="/dashboard/settings">Settings</Link>
      </nav>

      {/* Layout state: this number is KEPT when you move between dashboard pages */}
      <Counter label="Layout counter (kept)" />

      {stats}
      {children}
    </section>
  );
}
