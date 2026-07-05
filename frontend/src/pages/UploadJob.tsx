import { FormEvent, useState } from "react";
import { FileText } from "lucide-react";
import { Toast } from "../components/Toast";
import { uploadJobDescription } from "../services/resumeAgent";

export function UploadJob() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);
  const [result, setResult] = useState<any>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!file) return;
    setLoading(true);
    try {
      const response = await uploadJobDescription(file);
      setResult(response);
      setToast({ message: "Job description uploaded and parsed.", type: "success" });
    } catch {
      setToast({ message: "Upload failed. Use PDF, DOCX, or TXT under 10 MB.", type: "error" });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6 pb-16">
      <Toast message={toast?.message ?? null} type={toast?.type ?? "success"} />
      <div>
        <h1 className="page-title">Upload Job Description</h1>
        <p className="page-subtitle">Only one job description remains active for scoring.</p>
      </div>
      <form onSubmit={handleSubmit} className="panel space-y-4">
        <label className="dropzone">
          <FileText className="h-8 w-8 text-cyan-600" />
          <span className="font-medium">{file ? file.name : "Choose PDF, DOCX, or TXT"}</span>
          <input className="hidden" type="file" accept=".pdf,.docx,.txt" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
        </label>
        <button className="primary-button" disabled={!file || loading}>
          {loading ? "Uploading..." : "Upload Job Description"}
        </button>
      </form>
      {result && (
        <section className="panel">
          <h2 className="section-title">Parsed Job Description</h2>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <Info label="Required Skills" values={result.required_skills} />
            <Info label="Preferred Skills" values={result.preferred_skills} />
            <Info label="Education" values={result.education} />
            <Info label="Keywords" values={result.keywords} />
          </div>
        </section>
      )}
    </div>
  );
}

function Info({ label, values }: { label: string; values: string[] }) {
  return (
    <div>
      <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{label}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        {values.length ? values.map((value) => <span className="pill" key={value}>{value}</span>) : <span className="text-sm text-slate-400">None found</span>}
      </div>
    </div>
  );
}
