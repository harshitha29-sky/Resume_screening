export type TokenResponse = {
  access_token: string;
  token_type: string;
};

export type User = {
  id: number;
  email: string;
  full_name: string | null;
  is_active: boolean;
};

export type DistributionItem = {
  label: string;
  count: number;
};

export type DashboardStats = {
  total_candidates: number;
  total_resumes: number;
  average_score: number;
  highest_score: number;
  lowest_score: number;
  top_candidate: string | null;
  skill_distribution: DistributionItem[];
  experience_distribution: DistributionItem[];
  score_distribution: DistributionItem[];
};

export type Candidate = {
  id: number;
  full_name: string;
  email: string | null;
  phone: string | null;
  skills: string[];
  education: string[];
  total_years_experience: number;
  overall_score: number | null;
  recommendation: string | null;
};

export type ScoreBreakdown = {
  overall_score: number;
  nlp_similarity: number;
  skill_match: number;
  experience_match: number;
  education_match: number;
  matching_skills: string[];
  missing_skills: string[];
  recommendation: string;
};

export type CandidateDetail = Candidate & {
  experience: string[];
  projects: string[];
  certifications: string[];
  raw_text: string | null;
  resume_url: string | null;
  score_breakdown: ScoreBreakdown | null;
  created_at: string;
};

export type RankingItem = {
  rank: number;
  candidate_id: number;
  candidate_name: string;
  overall_score: number;
  skill_match: number;
  experience_match: number;
  education_match: number;
  recommendation: string;
};

export type PaginatedCandidates = {
  items: Candidate[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};
