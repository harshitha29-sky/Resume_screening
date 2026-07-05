import { FormEvent, useState } from "react";
import { Files } from "lucide-react";
import { Toast } from "../components/Toast";
import { uploadResumes } from "../services/resumeAgent";

export function UploadResumes() {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);
  const [result, setResult] = useState<any>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await uploadResumes(files);
      setResult(response);
      setToast({ message: `${response.uploaded_count} resumes uploaded and parsed.`, type: "success" });
    } catch {
      setToast({ message: "Upload failed. Check file count, size, type, or duplicate names.", type: "error" });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6 pb-16">
      <Toast message={toast?.message ?? null} type={toast?.type ?? "success"} />
      <div>
        <h1 className="page-title">Upload Resumes</h1>
        <p className="page-subtitle">Upload up to 20 PDF, DOCX, or TXT resumes at once.</p>
      </div>
      <form onSubmit={handleSubmit} className="panel space-y-4">
        <label className="dropzone">
          <Files className="h-8 w-8 text-cyan-600" />
          <span className="font-medium">{files.length ? `${files.length} files selected` : "Choose resume files"}</span>
          <input
            className="hidden"
            type="file"
            multiple
            accept=".pdf,.docx,.txt"
            onChange={(event) => setFiles(Array.from(event.target.files ?? []))}
          />
        </label>
        <button className="primary-button" disabled={!files.length || loading}>
          {loading ? "Uploading..." : "Upload Resumes"}
        </button>
      </form>
      {result && (
        <section className="panel">
          <h2 className="section-title">Upload Status</h2>
          <div className="mt-4 space-y-2">
            {result.uploads.map((upload: any) => (
              <div className="flex items-center justify-between rounded-md border border-slate-200 p-3 text-sm dark:border-slate-800" key={upload.id}>
                <span>{upload.filename}</span>
                <span className="pill">{upload.status}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
