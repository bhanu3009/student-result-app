from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, students, subjects, results

app = FastAPI(title="Student Result Management API")

# 1. CORS Configuration - This tells the backend to trust your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (perfect for local development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Register all of our API routes
app.include_router(users.router)
app.include_router(students.router)
app.include_router(subjects.router)
app.include_router(results.router)

@app.get("/")
def root():
    return {"message": "API is live and running!"}