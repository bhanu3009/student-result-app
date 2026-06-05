from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import auth
from database import get_db_connection

router = APIRouter(prefix="/users", tags=["Users"])

# Pydantic models to validate incoming data
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
def register_user(user: UserCreate):
    # 1. Validate the role
    if user.role not in ['admin', 'student']:
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'student'")
        
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 2. Check if email already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email already registered")
                
            # 3. Hash the password and insert the user
            hashed_pwd = auth.get_password_hash(user.password)
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                (user.name, user.email, hashed_pwd, user.role)
            )
            connection.commit()
            return {"message": f"Successfully registered {user.role}: {user.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()

@router.post("/login")
def login_user(user: UserLogin):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 1. Find user by email
            cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            db_user = cursor.fetchone()
            
            # 2. Verify user exists AND password matches the hash
            if not db_user or not auth.verify_password(user.password, db_user['password']):
                raise HTTPException(status_code=401, detail="Invalid email or password")
                
            # 3. Generate the login token
            token = auth.create_access_token(data={"sub": db_user['email'], "role": db_user['role']})
            
            return {
                "access_token": token, 
                "token_type": "bearer", 
                "role": db_user['role'],
                "name": db_user['name']
            }
    finally:
        connection.close()