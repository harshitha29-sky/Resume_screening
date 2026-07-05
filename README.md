# Resume Screening Agent

Full-stack AI resume screening application with FastAPI, React, SQLite, SQLAlchemy, JWT authentication, resume parsing, AI matching, rankings, analytics, and exports.

## Stack

- Backend: FastAPI with Python 3.12
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Database: SQLite with SQLAlchemy
- AI/NLP: pdfplumber, python-docx, spaCy, Sentence Transformers

## Features

- JWT registration, login, and protected routes
- Resume upload for PDF, DOCX, and TXT files
- Job description upload with one active job description
- Resume parsing for contact details, skills, education, experience, projects, certifications, and years of experience
- Job description parsing for required skills, preferred skills, required experience, education, and keywords
- AI matching with `all-MiniLM-L6-v2`
- Candidate rankings with recommendation labels
- Dashboard analytics and charts
- CSV and JSON exports
- Candidate search, filtering, sorting, pagination, preview, download, loading states, empty states, toast notifications, and dark mode

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

Core endpoints:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /upload/job-description`
- `POST /upload/resumes`
- `GET /candidates`
- `GET /candidate/{id}`
- `GET /ranking`
- `GET /dashboard`
- `GET /export/csv`
- `GET /export/json`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

## Run with Docker

```bash
docker compose up --build
```

## Notes

The backend is configured for Python 3.12. The local SQLite database is created automatically on startup for development. Alembic scaffolding is included for migration workflows.
