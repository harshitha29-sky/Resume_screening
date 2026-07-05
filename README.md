# Resume Screening Agent

Initial full-stack project structure for a Resume Screening Agent.

## Stack

- Backend: FastAPI with Python 3.12
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Database: SQLite with SQLAlchemy

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
