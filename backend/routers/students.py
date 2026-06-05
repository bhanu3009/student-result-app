from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection

router = APIRouter(prefix="/students", tags=["Students"])

# Define the exact data structure we expect from the frontend
class StudentCreate(BaseModel):
    name: str
    roll_no: str
    student_class: str  # Using 'student_class' because 'class' is a reserved word in Python

@router.post("/")
def add_student(student: StudentCreate):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 1. Security Check: Prevent duplicate roll numbers
            cursor.execute("SELECT * FROM students WHERE roll_no = %s", (student.roll_no,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="A student with this Roll Number already exists")
            
            # 2. Insert the new student using parameterized queries to prevent SQL Injection
            cursor.execute(
                "INSERT INTO students (name, roll_no, class) VALUES (%s, %s, %s)",
                (student.name, student.roll_no, student.student_class)
            )
            connection.commit()
            return {"message": f"Successfully added student: {student.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()

@router.get("/")
def get_all_students():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Retrieve all students from the vault
            cursor.execute("SELECT id, name, roll_no, class FROM students")
            students = cursor.fetchall()
            return {"students": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()