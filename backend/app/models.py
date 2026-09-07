from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)
    department: str = Field(min_length=1)
    semester: int = Field(ge=1)
    cgpa: float = Field(ge=0, le=10)


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=3)
    department: str | None = Field(default=None, min_length=1)
    semester: int | None = Field(default=None, ge=1)
    cgpa: float | None = Field(default=None, ge=0, le=10)


class StudentResponse(StudentCreate):
    id: str