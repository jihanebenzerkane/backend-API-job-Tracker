from fastapi import FastAPI
from . import models, database
from .routes import users, applications, auth

app = FastAPI(
    title="Job Tracker API",
    description="Track your job and internship applications",
    version="1.0.0"
)

database.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(applications.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Job Tracker API is running"}