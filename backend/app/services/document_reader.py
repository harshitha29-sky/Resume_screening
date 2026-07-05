from pathlib import Path

from fastapi import HTTPException, status


class DocumentReader:
    def read_text(self, file_path: str) -> str:
        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return self._read_pdf(path)
        if suffix == ".docx":
            return self._read_docx(path)
        if suffix == ".txt":
            return path.read_text(encoding="utf-8", errors="ignore")
        return ""

    def _read_pdf(self, path: Path) -> str:
        try:
            import pdfplumber
        except ImportError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PDF parsing dependency is not installed",
            ) from exc

        text_parts: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts).strip()

    def _read_docx(self, path: Path) -> str:
        try:
            from docx import Document
        except ImportError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="DOCX parsing dependency is not installed",
            ) from exc

        document = Document(path)
        return "\n".join(paragraph.text for paragraph in document.paragraphs).strip()
