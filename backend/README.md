# Backend

FastAPI backend for the student analytics project.

## Setup

The project uses Python 3.12 and a virtual environment at `backend/.venv`.

From the repository root:

```bash
backend/.venv/bin/python -m pip install -r backend/requirements.txt
```

Set `MONGODB_URI` and `MONGODB_DATABASE` in `backend/.env`. The backend also recognizes the existing repository-root `.env` file. Use `.env.example` as a template; never commit a file containing real credentials.

## Run the API

From the repository root:

```bash
backend/.venv/bin/uvicorn app.main:app --app-dir backend --reload
```

The API is available at `http://127.0.0.1:8000`. The root endpoint returns a small health message, and interactive documentation is available at `/docs`.

The `/health` endpoint reports `api: "ok"` and checks MongoDB with a ping. It reports `mongodb: "ok"` when Atlas is reachable, or `mongodb: "unavailable"` with an overall `status` of `"degraded"` when configuration or connectivity is unavailable.

This backend is intentionally minimal and can later be expanded with database, authentication, analytics, and other service modules.
