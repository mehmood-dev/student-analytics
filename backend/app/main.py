from fastapi import FastAPI

from app.database import check_mongodb_connection
from app.students import router as students_router

app = FastAPI(
    title="Student Analytics API",
    description="Backend API for the student analytics project.",
    version="0.1.0",
)

app.include_router(students_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Student Analytics backend is running"}


@app.get("/health")
def read_health() -> dict[str, str]:
    mongodb_status = "ok" if check_mongodb_connection() else "unavailable"
    overall_status = "ok" if mongodb_status == "ok" else "degraded"

    return {
        "status": overall_status,
        "api": "ok",
        "mongodb": mongodb_status,
    }
