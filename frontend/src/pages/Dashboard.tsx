import { Link } from "react-router-dom";
import { ArrowRight, Upload } from "lucide-react";
import { EmptyState } from "../components/EmptyState";
import { Metric } from "../components/Metric";
import { Spinner } from "../components/Spinner";
import { useAsync } from "../hooks/useAsync";
import { getDashboard, getRanking } from "../services/resumeAgent";

export function Dashboard() {
  const dashboard = useAsync(getDashboard, []);
  const ranking = useAsync(getRanking, []);

  if (dashboard.loading) {
    return <Spinner />;
  }

  if (!dashboard.data) {
    return <EmptyState title="Dashboard unavailable" message={dashboard.error ?? "Upload a job description and resumes to begin."} />;
  }

  return (
    <div className="space-y-6 pb-16">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Screening summary and top candidate signals.</p>
        </div>
        <Link className="primary-button inline-flex items-center gap-2" to="/upload-resumes">
          <Upload className="h-4 w-4" />
          Upload Resumes
        </Link>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Metric label="Total Candidates" value={dashboard.data.total_candidates} />
        <Metric label="Total Resumes" value={dashboard.data.total_resumes} />
        <Metric label="Average Score" value={`${dashboard.data.average_score}%`} />
        <Metric label="Top Candidate" value={dashboard.data.top_candidate ?? "None"} />
      </div>

      <section className="panel">
        <div className="flex items-center justify-between">
          <h2 className="section-title">Top Ranking</h2>
          <Link className="text-sm font-medium text-cyan-700 dark:text-cyan-300" to="/ranking">
            View all <ArrowRight className="inline h-4 w-4" />
          </Link>
        </div>
        {ranking.data && ranking.data.length > 0 ? (
          <div className="mt-4 overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Name</th>
                  <th>Score</th>
                  <th>Recommendation</th>
                </tr>
              </thead>
              <tbody>
                {ranking.data.slice(0, 5).map((item) => (
                  <tr key={item.candidate_id}>
                    <td>{item.rank}</td>
                    <td>{item.candidate_name}</td>
                    <td>{item.overall_score}%</td>
                    <td>{item.recommendation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState title="No rankings yet" message="Upload a job description and resumes to generate scores." />
        )}
      </section>
    </div>
  );
}
