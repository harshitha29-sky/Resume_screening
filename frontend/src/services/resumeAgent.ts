import { api } from "./api";
import type { CandidateDetail, DashboardStats, PaginatedCandidates, RankingItem } from "../types";

export type CandidateQuery = {
  search?: string;
  min_score?: number;
  max_score?: number;
  sort_by?: string;
  sort_order?: string;
  page?: number;
  page_size?: number;
};

export async function uploadResumes(files: File[]) {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  const { data } = await api.post("/upload/resumes", formData);
  return data;
}

export async function uploadJobDescription(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post("/upload/job-description", formData);
  return data;
}

export async function getCandidates(params: CandidateQuery): Promise<PaginatedCandidates> {
  const { data } = await api.get<PaginatedCandidates>("/candidates", { params });
  return data;
}

export async function getCandidate(id: string): Promise<CandidateDetail> {
  const { data } = await api.get<CandidateDetail>(`/candidate/${id}`);
  return data;
}

export async function getRanking(): Promise<RankingItem[]> {
  const { data } = await api.get<RankingItem[]>("/ranking");
  return data;
}

export async function getDashboard(): Promise<DashboardStats> {
  const { data } = await api.get<DashboardStats>("/dashboard");
  return data;
}

export async function downloadExport(type: "csv" | "json") {
  const response = await api.get(`/export/${type}`, { responseType: "blob" });
  const url = window.URL.createObjectURL(response.data);
  const link = document.createElement("a");
  link.href = url;
  link.download = `candidate-rankings.${type}`;
  link.click();
  window.URL.revokeObjectURL(url);
}
