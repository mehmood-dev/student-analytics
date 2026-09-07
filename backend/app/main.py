from fastapi import FastAPI

app = FastAPI(
    title="Student Analytics API",
    description="Backend API for the student analytics project.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Student Analytics backend is running"}
