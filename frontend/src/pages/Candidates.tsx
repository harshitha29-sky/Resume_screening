import { Link } from "react-router-dom";
import { EmptyState } from "../components/EmptyState";
import { Spinner } from "../components/Spinner";
import { getCandidates } from "../services/resumeAgent";
import { useAsync } from "../hooks/useAsync";
import { useState } from "react";

export function Candidates() {
  const [query, setQuery] = useState({ search: "", min_score: "", sort_by: "score", sort_order: "desc", page: 1 });
  const { data, loading, error, refresh } = useAsync(
    () => getCandidates({ ...query, min_score: query.min_score ? Number(query.min_score) : undefined }),
    [query],
  );

  if (loading) return <Spinner />;

  return (
    <div className="space-y-6 pb-16">
      <div>
        <h1 className="page-title">Candidates</h1>
        <p className="page-subtitle">Search, filter, sort, and paginate candidate records.</p>
      </div>
      <section className="panel grid gap-3 md:grid-cols-5">
        <input className="field-input md:col-span-2" placeholder="Search candidates" value={query.search} onChange={(e) => setQuery({ ...query, search: e.target.value, page: 1 })} />
        <input className="field-input" placeholder="Min score" type="number" value={query.min_score} onChange={(e) => setQuery({ ...query, min_score: e.target.value, page: 1 })} />
        <select className="field-input" value={query.sort_by} onChange={(e) => setQuery({ ...query, sort_by: e.target.value })}>
          <option value="score">Score</option>
          <option value="name">Name</option>
          <option value="experience">Experience</option>
          <option value="education">Education</option>
        </select>
        <select className="field-input" value={query.sort_order} onChange={(e) => setQuery({ ...query, sort_order: e.target.value })}>
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </section>
      {!data?.items.length ? (
        <EmptyState title="No candidates" message={error ?? "Try changing filters or upload resumes."} />
      ) : (
        <section className="panel overflow-x-auto">
          <table className="data-table">
            <thead><tr><th>Name</th><th>Email</th><th>Experience</th><th>Score</th><th>Recommendation</th></tr></thead>
            <tbody>
              {data.items.map((candidate) => (
                <tr key={candidate.id}>
                  <td><Link className="font-medium text-cyan-700 dark:text-cyan-300" to={`/candidate/${candidate.id}`}>{candidate.full_name}</Link></td>
                  <td>{candidate.email ?? "None"}</td>
                  <td>{candidate.total_years_experience} years</td>
                  <td>{candidate.overall_score ?? 0}%</td>
                  <td>{candidate.recommendation ?? "Unscored"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="mt-4 flex items-center justify-between text-sm">
            <span>Page {data.page} of {data.total_pages}</span>
            <div className="flex gap-2">
              <button className="secondary-button" disabled={query.page <= 1} onClick={() => setQuery({ ...query, page: query.page - 1 })}>Previous</button>
              <button className="secondary-button" disabled={query.page >= data.total_pages} onClick={() => setQuery({ ...query, page: query.page + 1 })}>Next</button>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
