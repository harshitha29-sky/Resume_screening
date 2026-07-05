import { Link, useParams } from "react-router-dom";
import { Download } from "lucide-react";
import { EmptyState } from "../components/EmptyState";
import { Spinner } from "../components/Spinner";
import { apiBaseUrl } from "../services/api";
import { getCandidate } from "../services/resumeAgent";
import { useAsync } from "../hooks/useAsync";

export function CandidateDetails() {
  const { id = "" } = useParams();
  const { data, loading, error } = useAsync(() => getCandidate(id), [id]);

  if (loading) return <Spinner />;
  if (!data) return <EmptyState title="Candidate not found" message={error ?? "The candidate record could not be loaded."} />;

  const resumeHref = data.resume_url ? `${apiBaseUrl}${data.resume_url}` : null;

  return (
    <div className="space-y-6 pb-16">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <h1 className="page-title">{data.full_name}</h1>
          <p className="page-subtitle">{data.email ?? "No email"} · {data.phone ?? "No phone"}</p>
        </div>
        {resumeHref && <a className="secondary-button" href={resumeHref}><Download className="h-4 w-4" /> Resume</a>}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
        <section className="panel">
          <h2 className="section-title">Resume Preview</h2>
          <div className="mt-4 max-h-[520px] overflow-auto rounded-md bg-slate-50 p-4 text-sm leading-6 text-slate-700 dark:bg-slate-950 dark:text-slate-300">
            {data.raw_text || "Preview unavailable for this resume."}
          </div>
        </section>
        <section className="panel space-y-4">
          <h2 className="section-title">Score Breakdown</h2>
          {data.score_breakdown ? (
            <>
              <div className="text-4xl font-semibold text-slate-950 dark:text-slate-50">{data.score_breakdown.overall_score}%</div>
              <p className="pill w-fit">{data.score_breakdown.recommendation}</p>
              <Score label="NLP Similarity" value={data.score_breakdown.nlp_similarity} />
              <Score label="Skill Match" value={data.score_breakdown.skill_match} />
              <Score label="Experience Match" value={data.score_breakdown.experience_match} />
              <Score label="Education Match" value={data.score_breakdown.education_match} />
            </>
          ) : (
            <p className="text-sm text-slate-500">No score available yet.</p>
          )}
        </section>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Info title="Skills" values={data.skills} />
        <Info title="Matching Skills" values={data.score_breakdown?.matching_skills ?? []} />
        <Info title="Missing Skills" values={data.score_breakdown?.missing_skills ?? []} />
        <Info title="Education" values={data.education} />
        <Info title="Experience" values={data.experience} />
        <Info title="Projects" values={data.projects} />
        <Info title="Certifications" values={data.certifications} />
      </div>
      <Link className="text-sm font-medium text-cyan-700 dark:text-cyan-300" to="/ranking">Back to ranking</Link>
    </div>
  );
}

function Score({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="mb-1 flex justify-between text-sm"><span>{label}</span><span>{value}%</span></div>
      <div className="h-2 rounded bg-slate-200 dark:bg-slate-800"><div className="h-2 rounded bg-cyan-600" style={{ width: `${Math.min(100, value)}%` }} /></div>
    </div>
  );
}

function Info({ title, values }: { title: string; values: string[] }) {
  return (
    <section className="panel">
      <h2 className="section-title">{title}</h2>
      <div className="mt-3 flex flex-wrap gap-2">
        {values.length ? values.map((value) => <span className="pill" key={value}>{value}</span>) : <span className="text-sm text-slate-400">None found</span>}
      </div>
    </section>
  );
}
