import csv
import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.services.candidates import ranking
from app.utils.config import settings
from app.utils.files import ensure_directory, unique_export_name


def export_rankings_csv(db: Session) -> Path:
    export_dir = ensure_directory(Path(settings.export_root))
    path = export_dir / unique_export_name("candidate-rankings", ".csv")
    rows = ranking(db)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "rank",
                "candidate_id",
                "candidate_name",
                "overall_score",
                "skill_match",
                "experience_match",
                "education_match",
                "recommendation",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.model_dump())
    return path


def export_rankings_json(db: Session) -> Path:
    export_dir = ensure_directory(Path(settings.export_root))
    path = export_dir / unique_export_name("candidate-rankings", ".json")
    rows = [row.model_dump() for row in ranking(db)]
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return path
