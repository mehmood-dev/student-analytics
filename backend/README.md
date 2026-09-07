# Backend

FastAPI backend for the student analytics project.

## Setup

The project uses Python 3.12 and a virtual environment at `backend/.venv`.

From the repository root:

```bash
backend/.venv/bin/python -m pip install -r backend/requirements.txt
```

## Run the API

From the repository root:

```bash
backend/.venv/bin/uvicorn app.main:app --app-dir backend --reload
```

The API is available at `http://127.0.0.1:8000`. The root endpoint returns a small health message, and interactive documentation is available at `/docs`.

This backend is intentionally minimal and can later be expanded with database, authentication, analytics, and other service modules.
