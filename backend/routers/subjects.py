from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection

router = APIRouter(prefix="/subjects", tags=["Subjects"])

# The data we expect from the frontend
class SubjectCreate(BaseModel):
    name: str

@router.post("/")
def add_subject(subject: SubjectCreate):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 1. Check for duplicates
            cursor.execute("SELECT * FROM subjects WHERE name = %s", (subject.name,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="This subject already exists in the system")
            
            # 2. Insert the new subject
            cursor.execute(
                "INSERT INTO subjects (name) VALUES (%s)",
                (subject.name,)
            )
            connection.commit()
            return {"message": f"Successfully added subject: {subject.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()

@router.get("/")
def get_all_subjects():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM subjects")
            subjects = cursor.fetchall()
            return {"subjects": subjects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()