import { Moon } from "lucide-react";

export function Settings() {
  function setTheme(theme: "light" | "dark") {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem("theme", theme);
  }

  return (
    <div className="space-y-6 pb-16">
      <div>
        <h1 className="page-title">Settings</h1>
        <p className="page-subtitle">Workspace preferences.</p>
      </div>
      <section className="panel">
        <div className="flex items-center gap-3">
          <Moon className="h-5 w-5 text-cyan-600" />
          <div>
            <h2 className="section-title">Appearance</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">Choose a display mode for this browser.</p>
          </div>
        </div>
        <div className="mt-4 flex gap-2">
          <button className="secondary-button" onClick={() => setTheme("light")}>Light</button>
          <button className="secondary-button" onClick={() => setTheme("dark")}>Dark</button>
        </div>
      </section>
    </div>
  );
}
