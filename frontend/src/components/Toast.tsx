export function Toast({ message, type }: { message: string | null; type: "success" | "error" }) {
  if (!message) return null;
  return (
    <div
      className={`fixed right-4 top-4 z-50 rounded-md px-4 py-3 text-sm font-medium text-white shadow-lg ${
        type === "success" ? "bg-emerald-600" : "bg-rose-600"
      }`}
    >
      {message}
    </div>
  );
}
