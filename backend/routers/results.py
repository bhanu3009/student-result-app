from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection

router = APIRouter(prefix="/results", tags=["Results"])

class ResultCreate(BaseModel):
    student_id: int
    subject_id: int
    marks: int

def calculate_grade(marks: int) -> str:
    """Manual grading logic: A+, A, B, C, D, or F based on raw marks."""
    if marks >= 90: return 'A+'
    if marks >= 80: return 'A'
    if marks >= 70: return 'B'
    if marks >= 60: return 'C'
    if marks >= 50: return 'D'
    return 'F'

@router.post("/")
def add_result(result: ResultCreate):
    grade = calculate_grade(result.marks)
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 1. Security Check: Does this student actually exist?
            cursor.execute("SELECT id FROM students WHERE id = %s", (result.student_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Student not found in database")

            # 2. Security Check: Does this subject actually exist?
            cursor.execute("SELECT id FROM subjects WHERE id = %s", (result.subject_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Subject not found in database")

            # 3. Security Check: Prevent duplicate results for the same class
            cursor.execute("SELECT * FROM results WHERE student_id = %s AND subject_id = %s", 
                           (result.student_id, result.subject_id))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="This student already has a result for this subject")

            # 4. Insert the final mapped result
            cursor.execute(
                "INSERT INTO results (student_id, subject_id, marks, grade) VALUES (%s, %s, %s, %s)",
                (result.student_id, result.subject_id, result.marks, grade)
            )
            connection.commit()
            return {"message": "Result added successfully", "marks": result.marks, "grade": grade}
            
    except HTTPException:
        raise # Pass through our custom 404/400 errors cleanly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()

@router.get("/{student_id}")
def get_student_results(student_id: int):
    """Uses a SQL JOIN to pull the student's marks alongside the actual Subject Name."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT r.id, s.name as subject_name, r.marks, r.grade 
                FROM results r
                JOIN subjects s ON r.subject_id = s.id
                WHERE r.student_id = %s
            """
            cursor.execute(query, (student_id,))
            results = cursor.fetchall()
            return {"student_id": student_id, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()