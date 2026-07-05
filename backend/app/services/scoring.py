from decimal import Decimal
from math import sqrt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.job_description import JobDescription
from app.models.resume_score import ResumeScore
from app.utils.config import settings
from app.utils.json_store import dumps, loads


def recommendation_for_score(score: float) -> str:
    if score > 85:
        return "Highly Recommended"
    if score >= 70:
        return "Recommended"
    if score >= 50:
        return "Consider"
    return "Not Recommended"


class ResumeMatcher:
    def __init__(self) -> None:
        self._model = None

    def score_candidate(
        self,
        db: Session,
        candidate: Candidate,
        job_description: JobDescription,
    ) -> ResumeScore:
        nlp_similarity = self._nlp_similarity(candidate.raw_text or "", job_description.description or "")
        skill_match, matching_skills, missing_skills = self._skill_match(candidate, job_description)
        experience_match = self._experience_match(candidate, job_description)
        education_match = self._education_match(candidate, job_description)
        overall = (0.5 * nlp_similarity) + (0.3 * skill_match) + (0.2 * experience_match)
        overall = round(overall, 2)

        existing = db.scalar(
            select(ResumeScore).where(
                ResumeScore.candidate_id == candidate.id,
                ResumeScore.job_description_id == job_description.id,
            )
        )
        score = existing or ResumeScore(
            candidate_id=candidate.id,
            job_description_id=job_description.id,
        )
        score.score = Decimal(str(overall))
        score.nlp_similarity = round(nlp_similarity, 2)
        score.skill_match = round(skill_match, 2)
        score.experience_match = round(experience_match, 2)
        score.education_match = round(education_match, 2)
        score.matching_skills = dumps(matching_skills)
        score.missing_skills = dumps(missing_skills)
        score.recommendation = recommendation_for_score(overall)
        score.summary = f"{score.recommendation} based on resume and job description match."

        if existing is None:
            db.add(score)
        db.commit()
        db.refresh(score)
        return score

    def score_all_for_active_job(self, db: Session) -> list[ResumeScore]:
        job = db.scalar(select(JobDescription).where(JobDescription.is_active.is_(True)))
        if job is None:
            return []
        candidates = db.scalars(select(Candidate)).all()
        return [self.score_candidate(db, candidate, job) for candidate in candidates]

    def _load_model(self):
        if self._model is not None:
            return self._model
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(settings.sentence_transformer_model)
        except Exception:
            self._model = False
        return self._model

    def _nlp_similarity(self, resume_text: str, job_text: str) -> float:
        if not resume_text or not job_text:
            return 0.0
        model = self._load_model()
        if model:
            embeddings = model.encode([resume_text, job_text])
            return max(0.0, min(100.0, self._cosine(embeddings[0], embeddings[1]) * 100))
        return self._token_similarity(resume_text, job_text)

    def _cosine(self, a, b) -> float:
        dot = sum(float(x) * float(y) for x, y in zip(a, b))
        norm_a = sqrt(sum(float(x) * float(x) for x in a))
        norm_b = sqrt(sum(float(y) * float(y) for y in b))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def _token_similarity(self, resume_text: str, job_text: str) -> float:
        resume_tokens = set(resume_text.lower().split())
        job_tokens = set(job_text.lower().split())
        if not resume_tokens or not job_tokens:
            return 0.0
        return len(resume_tokens & job_tokens) / len(job_tokens) * 100

    def _skill_match(self, candidate: Candidate, job: JobDescription) -> tuple[float, list[str], list[str]]:
        candidate_skills = set(loads(candidate.skills))
        required_skills = set(loads(job.required_skills))
        if not required_skills:
            return 100.0, sorted(candidate_skills), []
        matching = sorted(candidate_skills & required_skills)
        missing = sorted(required_skills - candidate_skills)
        return (len(matching) / len(required_skills) * 100), matching, missing

    def _experience_match(self, candidate: Candidate, job: JobDescription) -> float:
        required = job.required_experience or 0.0
        if required <= 0:
            return 100.0
        return min(100.0, ((candidate.total_years_experience or 0.0) / required) * 100)

    def _education_match(self, candidate: Candidate, job: JobDescription) -> float:
        required = set(loads(job.education))
        if not required:
            return 100.0
        candidate_education = " ".join(loads(candidate.education)).lower()
        matched = [item for item in required if item.lower() in candidate_education]
        return len(matched) / len(required) * 100
