import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileCheck } from "lucide-react";
import { login, register } from "../services/auth";
import { Toast } from "../components/Toast";

export function Login() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setToast(null);
    try {
      if (mode === "register") {
        await register(email, password, fullName);
      }
      const token = await login(email, password);
      localStorage.setItem("auth_token", token.access_token);
      navigate("/dashboard");
    } catch {
      setToast("Authentication failed. Check your details and try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-slate-100 px-4 dark:bg-slate-950">
      <Toast message={toast} type="error" />
      <section className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-md bg-cyan-600 text-white">
            <FileCheck className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-slate-950 dark:text-slate-50">Resume Screening Agent</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">Sign in to continue</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          {mode === "register" && (
            <label className="field-label">
              Full name
              <input className="field-input" value={fullName} onChange={(event) => setFullName(event.target.value)} />
            </label>
          )}
          <label className="field-label">
            Email
            <input className="field-input" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </label>
          <label className="field-label">
            Password
            <input
              className="field-input"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              minLength={mode === "register" ? 8 : 1}
              required
            />
          </label>
          <button className="primary-button w-full" disabled={loading}>
            {loading ? "Working..." : mode === "login" ? "Login" : "Create account"}
          </button>
        </form>

        <button className="mt-4 w-full text-sm text-cyan-700 dark:text-cyan-300" onClick={() => setMode(mode === "login" ? "register" : "login")}>
          {mode === "login" ? "Create a new account" : "Use an existing account"}
        </button>
      </section>
    </main>
  );
}
