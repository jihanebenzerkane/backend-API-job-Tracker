from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from . import models, crud, database, schemas

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Job/Internship Application Tracker")

# ---------- DB Dependency ----------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Role Dependency ----------
def get_role(x_role: str = Header(...)):
    if x_role not in ["student", "recruiter"]:
        raise HTTPException(status_code=400, detail="Invalid role. Use 'student' or 'recruiter'.")
    return x_role

# ---------- ROOT ----------
@app.get("/")
def read_root():
    return {"message": "API is working!"}

# ---------- USERS ----------
@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.name, user.email)

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user

@app.get("/users", response_model=list[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

# ---------- APPLICATIONS ----------
@app.post("/applications/", response_model=schemas.ApplicationOut)
def create_application(app: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, app.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {app.user_id} not found")
    return crud.create_application(db, app.user_id, app.company, app.position)

@app.get("/applications/", response_model=list[schemas.ApplicationOut])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), role: str = Depends(get_role)):
    if role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can access all applications")
    return crud.get_applications(db, skip=skip, limit=limit)

@app.get("/applications/{app_id}", response_model=schemas.ApplicationOut)
def read_application(app_id: int, db: Session = Depends(get_db), role: str = Depends(get_role)):
    app_obj = crud.get_application(db, app_id)
    if not app_obj:
        raise HTTPException(status_code=404, detail=f"Application with id {app_id} not found")
    if role != "recruiter" and app_obj.user_id != 1:  # assuming student id=1, adjust for multi-user logic
        raise HTTPException(status_code=403, detail="Students can only access their own applications")
    return app_obj
