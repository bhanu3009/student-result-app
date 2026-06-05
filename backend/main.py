from fastapi import FastAPI
from routers import users

app = FastAPI(title="Student Result Management API")

# Register the routes we just created
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API is live and running!"}