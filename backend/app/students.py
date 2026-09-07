from typing import Any

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError

from app.database import database
from app.models import StudentCreate, StudentResponse, StudentUpdate


router = APIRouter(prefix="/students", tags=["students"])


def _get_students_collection() -> Any:
    if database is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB is unavailable",
        )
    return database["students"]


def _parse_student_id(student_id: str) -> ObjectId:
    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID",
        )
    return ObjectId(student_id)


def _serialize_student(student: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"],
        "department": student["department"],
        "semester": student["semester"],
        "cgpa": student["cgpa"],
    }


def _check_database_error(error: PyMongoError) -> None:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="MongoDB is unavailable",
    ) from error


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate) -> dict[str, Any]:
    collection = _get_students_collection()
    student_data = student.dict()

    try:
        if collection.find_one({"email": student.email}) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A student with this email already exists",
            )
        result = collection.insert_one(student_data)
        created_student = collection.find_one({"_id": result.inserted_id})
    except HTTPException:
        raise
    except PyMongoError as error:
        _check_database_error(error)

    if created_student is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Student could not be created",
        )
    return _serialize_student(created_student)


@router.get("", response_model=list[StudentResponse])
def list_students() -> list[dict[str, Any]]:
    collection = _get_students_collection()
    try:
        return [_serialize_student(student) for student in collection.find()]
    except PyMongoError as error:
        _check_database_error(error)
    return []


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str) -> dict[str, Any]:
    collection = _get_students_collection()
    object_id = _parse_student_id(student_id)
    try:
        student = collection.find_one({"_id": object_id})
    except PyMongoError as error:
        _check_database_error(error)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return _serialize_student(student)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: str, student: StudentUpdate) -> dict[str, Any]:
    collection = _get_students_collection()
    object_id = _parse_student_id(student_id)
    update_data = student.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field is required",
        )

    try:
        if "email" in update_data:
            duplicate = collection.find_one(
                {"email": update_data["email"], "_id": {"$ne": object_id}}
            )
            if duplicate is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A student with this email already exists",
                )

        result = collection.update_one({"_id": object_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )
        updated_student = collection.find_one({"_id": object_id})
    except HTTPException:
        raise
    except PyMongoError as error:
        _check_database_error(error)

    if updated_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return _serialize_student(updated_student)


@router.delete("/{student_id}")
def delete_student(student_id: str) -> dict[str, str]:
    collection = _get_students_collection()
    object_id = _parse_student_id(student_id)
    try:
        result = collection.delete_one({"_id": object_id})
    except PyMongoError as error:
        _check_database_error(error)

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return {"message": "Student deleted", "id": student_id}