from fastapi import FastAPI
from routers import users, students, subjects, results

app = FastAPI(title="Student Result Management API")

# Register all of our API routes
app.include_router(users.router)
app.include_router(students.router)
app.include_router(subjects.router)
app.include_router(results.router)

@app.get("/")
def root():
    return {"message": "API is live and running!"}