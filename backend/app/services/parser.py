import re
from dataclasses import dataclass

from app.services.document_reader import DocumentReader

COMMON_SKILLS = {
    "python",
    "fastapi",
    "django",
    "flask",
    "react",
    "typescript",
    "javascript",
    "sql",
    "sqlite",
    "postgresql",
    "mysql",
    "docker",
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "nlp",
    "pandas",
    "numpy",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "langchain",
    "git",
    "rest api",
    "graphql",
    "tailwind",
    "node",
}

SECTION_NAMES = {
    "education": ["education", "academic"],
    "experience": ["experience", "work history", "employment"],
    "projects": ["projects", "portfolio"],
    "certifications": ["certifications", "certificates"],
}


@dataclass
class ParsedResume:
    candidate_name: str
    email: str | None
    phone: str | None
    skills: list[str]
    education: list[str]
    experience: list[str]
    projects: list[str]
    certifications: list[str]
    total_years_experience: float
    raw_text: str


@dataclass
class ParsedJobDescription:
    title: str
    description: str
    required_skills: list[str]
    preferred_skills: list[str]
    required_experience: float
    education: list[str]
    keywords: list[str]


class ResumeParser:
    def __init__(self, reader: DocumentReader | None = None) -> None:
        self.reader = reader or DocumentReader()
        self.nlp = self._load_spacy()

    def parse_file(self, file_path: str) -> ParsedResume:
        text = self.reader.read_text(file_path)
        return self.parse_text(text)

    def parse_text(self, text: str) -> ParsedResume:
        cleaned_text = self._normalize(text)
        return ParsedResume(
            candidate_name=self._extract_name(cleaned_text),
            email=self._extract_email(cleaned_text),
            phone=self._extract_phone(cleaned_text),
            skills=self._extract_skills(cleaned_text),
            education=self._extract_section(cleaned_text, "education"),
            experience=self._extract_section(cleaned_text, "experience"),
            projects=self._extract_section(cleaned_text, "projects"),
            certifications=self._extract_section(cleaned_text, "certifications"),
            total_years_experience=self._extract_years(cleaned_text),
            raw_text=cleaned_text,
        )

    def _load_spacy(self):
        try:
            import spacy

            try:
                return spacy.load("en_core_web_sm")
            except OSError:
                return spacy.blank("en")
        except ImportError:
            return None

    def _normalize(self, text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text or "").strip()

    def _extract_name(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines[:8]:
            if "@" not in line and not re.search(r"\d{3}", line) and len(line.split()) <= 5:
                return line[:255]
        if self.nlp is not None:
            doc = self.nlp(text[:1000])
            for entity in getattr(doc, "ents", []):
                if entity.label_ == "PERSON":
                    return entity.text[:255]
        return "Unknown Candidate"

    def _extract_email(self, text: str) -> str | None:
        match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
        return match.group(0).lower() if match else None

    def _extract_phone(self, text: str) -> str | None:
        match = re.search(r"(\+?\d[\d\s().-]{8,}\d)", text)
        return match.group(1).strip() if match else None

    def _extract_skills(self, text: str) -> list[str]:
        lowered = text.lower()
        return sorted({skill for skill in COMMON_SKILLS if skill in lowered})

    def _extract_section(self, text: str, section: str) -> list[str]:
        aliases = SECTION_NAMES[section]
        lines = [line.strip(" -\t") for line in text.splitlines()]
        collected: list[str] = []
        capture = False
        for line in lines:
            lowered = line.lower().strip(":")
            if any(alias == lowered or lowered.startswith(alias + ":") for alias in aliases):
                capture = True
                continue
            if capture and lowered in {alias for group in SECTION_NAMES.values() for alias in group}:
                break
            if capture and line:
                collected.append(line)
            if len(collected) >= 8:
                break
        return collected

    def _extract_years(self, text: str) -> float:
        matches = re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)", text.lower())
        if not matches:
            return 0.0
        return max(float(value) for value in matches)


class JobDescriptionParser:
    def __init__(self, reader: DocumentReader | None = None) -> None:
        self.reader = reader or DocumentReader()

    def parse_file(self, file_path: str) -> ParsedJobDescription:
        text = self.reader.read_text(file_path)
        return self.parse_text(text)

    def parse_text(self, text: str) -> ParsedJobDescription:
        cleaned_text = re.sub(r"\n{3,}", "\n\n", text or "").strip()
        skills = self._extract_skills(cleaned_text)
        required = self._filter_contextual_skills(cleaned_text, skills, ["required", "must", "need"])
        preferred = self._filter_contextual_skills(cleaned_text, skills, ["preferred", "nice", "plus"])
        return ParsedJobDescription(
            title=self._extract_title(cleaned_text),
            description=cleaned_text,
            required_skills=required or skills,
            preferred_skills=preferred,
            required_experience=self._extract_required_experience(cleaned_text),
            education=self._extract_education(cleaned_text),
            keywords=self._extract_keywords(cleaned_text, skills),
        )

    def _extract_title(self, text: str) -> str:
        for line in text.splitlines()[:6]:
            line = line.strip()
            if line:
                return line[:255]
        return "Uploaded Job Description"

    def _extract_skills(self, text: str) -> list[str]:
        lowered = text.lower()
        return sorted({skill for skill in COMMON_SKILLS if skill in lowered})

    def _filter_contextual_skills(self, text: str, skills: list[str], cues: list[str]) -> list[str]:
        lowered = text.lower()
        selected = []
        for skill in skills:
            index = lowered.find(skill)
            window = lowered[max(0, index - 80) : index + 80] if index >= 0 else ""
            if any(cue in window for cue in cues):
                selected.append(skill)
        return selected

    def _extract_required_experience(self, text: str) -> float:
        matches = re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)", text.lower())
        return max((float(value) for value in matches), default=0.0)

    def _extract_education(self, text: str) -> list[str]:
        degrees = ["bachelor", "master", "phd", "degree", "computer science", "engineering"]
        lowered = text.lower()
        return [degree for degree in degrees if degree in lowered]

    def _extract_keywords(self, text: str, skills: list[str]) -> list[str]:
        words = re.findall(r"[A-Za-z][A-Za-z+#.-]{2,}", text.lower())
        stop_words = {"and", "the", "with", "for", "you", "are", "our", "will", "this", "that"}
        frequent = sorted({word for word in words if word not in stop_words and words.count(word) >= 2})
        return sorted(set(skills + frequent[:20]))
