import Counter from "@/components/Counter";

// Template: like a layout, but gets a new key on every navigation to this segment,
// so its Client Component children reset their state.
export default function SettingsTemplate({ children }) {
  return (
    <div>
      <Counter label="Template counter (resets)" />
      {children}
    </div>
  );
}
