# Student Analytics

Full-stack student analytics project with a FastAPI backend and a React frontend powered by Vite.

## Project structure

- `backend/` contains the Python 3.12 FastAPI service.
- `frontend/` contains the JavaScript React/Vite application.

## Start the backend

```bash
backend/.venv/bin/uvicorn app.main:app --app-dir backend --reload
```

The backend runs at `http://127.0.0.1:8000` and provides interactive API documentation at `/docs`.

## Start the frontend

```bash
cd frontend
npm install
npm run dev
```

The application is intentionally minimal and ready for future database, authentication, analytics, and UI work.
