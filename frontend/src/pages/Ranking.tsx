import { Link } from "react-router-dom";
import { Download } from "lucide-react";
import { EmptyState } from "../components/EmptyState";
import { Spinner } from "../components/Spinner";
import { useAsync } from "../hooks/useAsync";
import { downloadExport, getRanking } from "../services/resumeAgent";

export function Ranking() {
  const { data, loading, error } = useAsync(getRanking, []);

  if (loading) return <Spinner />;
  if (!data?.length) return <EmptyState title="No ranking data" message={error ?? "Scores will appear after uploading resumes and a job description."} />;

  return (
    <div className="space-y-6 pb-16">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <h1 className="page-title">Candidate Ranking</h1>
          <p className="page-subtitle">Candidates sorted by overall score.</p>
        </div>
        <div className="flex gap-2">
          <button className="secondary-button" onClick={() => void downloadExport("csv")}><Download className="h-4 w-4" /> CSV</button>
          <button className="secondary-button" onClick={() => void downloadExport("json")}><Download className="h-4 w-4" /> JSON</button>
        </div>
      </div>
      <section className="panel overflow-x-auto">
        <table className="data-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Candidate</th>
              <th>Overall</th>
              <th>Skills</th>
              <th>Experience</th>
              <th>Education</th>
              <th>Recommendation</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item.candidate_id}>
                <td>{item.rank}</td>
                <td><Link className="font-medium text-cyan-700 dark:text-cyan-300" to={`/candidate/${item.candidate_id}`}>{item.candidate_name}</Link></td>
                <td>{item.overall_score}%</td>
                <td>{item.skill_match}%</td>
                <td>{item.experience_match}%</td>
                <td>{item.education_match}%</td>
                <td>{item.recommendation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
