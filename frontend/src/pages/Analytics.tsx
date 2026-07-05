import type { ReactNode } from "react";
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { EmptyState } from "../components/EmptyState";
import { Metric } from "../components/Metric";
import { Spinner } from "../components/Spinner";
import { useAsync } from "../hooks/useAsync";
import { getDashboard } from "../services/resumeAgent";

const colors = ["#0891b2", "#16a34a", "#ca8a04", "#dc2626", "#7c3aed", "#475569"];

export function Analytics() {
  const { data, loading, error } = useAsync(getDashboard, []);

  if (loading) return <Spinner />;
  if (!data) return <EmptyState title="No analytics" message={error ?? "Analytics will appear when candidates are scored."} />;

  return (
    <div className="space-y-6 pb-16">
      <div>
        <h1 className="page-title">Analytics</h1>
        <p className="page-subtitle">Skill, experience, and score distributions.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <Metric label="Highest Score" value={`${data.highest_score}%`} />
        <Metric label="Lowest Score" value={`${data.lowest_score}%`} />
        <Metric label="Average Score" value={`${data.average_score}%`} />
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <ChartPanel title="Skill Distribution">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.skill_distribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="label" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#0891b2" />
            </BarChart>
          </ResponsiveContainer>
        </ChartPanel>
        <ChartPanel title="Experience Distribution">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={data.experience_distribution} dataKey="count" nameKey="label" outerRadius={100} label>
                {data.experience_distribution.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartPanel>
        <ChartPanel title="Candidate Score Distribution">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.score_distribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="label" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#16a34a" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </ChartPanel>
      </div>
    </div>
  );
}

function ChartPanel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="panel">
      <h2 className="section-title">{title}</h2>
      <div className="mt-4 h-[300px]">{children}</div>
    </section>
  );
}
