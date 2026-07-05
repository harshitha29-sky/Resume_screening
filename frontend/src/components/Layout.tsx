import { BarChart3, FileText, Home, Moon, Settings, Upload, UserSearch, Users } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const links = [
  { to: "/dashboard", label: "Dashboard", icon: Home },
  { to: "/upload-job", label: "Job Description", icon: FileText },
  { to: "/upload-resumes", label: "Resumes", icon: Upload },
  { to: "/candidates", label: "Candidates", icon: UserSearch },
  { to: "/ranking", label: "Ranking", icon: Users },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function Layout() {
  function toggleDarkMode() {
    document.documentElement.classList.toggle("dark");
    localStorage.setItem("theme", document.documentElement.classList.contains("dark") ? "dark" : "light");
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-950 dark:bg-slate-950 dark:text-slate-100">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900 lg:block">
        <div className="text-lg font-semibold">Resume Screening Agent</div>
        <nav className="mt-8 space-y-1">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-md px-3 py-2 text-sm ${
                  isActive
                    ? "bg-cyan-50 text-cyan-700 dark:bg-cyan-950 dark:text-cyan-200"
                    : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
                }`
              }
            >
              <Icon className="h-4 w-4" />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <header className="sticky top-0 z-20 flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3 dark:border-slate-800 dark:bg-slate-900 lg:ml-64">
        <div className="font-semibold lg:hidden">Resume Screening Agent</div>
        <div className="hidden text-sm text-slate-500 dark:text-slate-400 lg:block">AI candidate screening workspace</div>
        <div className="flex items-center gap-2">
          <button className="icon-button" onClick={toggleDarkMode} title="Toggle dark mode">
            <Moon className="h-4 w-4" />
          </button>
        </div>
      </header>
      <main className="p-4 lg:ml-64 lg:p-6">
        <Outlet />
      </main>
      <nav className="fixed bottom-0 left-0 right-0 z-20 grid grid-cols-5 border-t border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900 lg:hidden">
        {links.slice(0, 5).map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} className="flex flex-col items-center gap-1 px-2 py-2 text-[11px] text-slate-500">
            <Icon className="h-4 w-4" />
            {label.split(" ")[0]}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
