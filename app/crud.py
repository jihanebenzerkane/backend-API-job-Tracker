from sqlalchemy.orm import Session
from . import models

# -------- USERS --------
def create_user(db: Session, name: str, email: str):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# -------- APPLICATIONS --------
def create_application(db: Session, user_id: int, company: str, position: str):
    application = models.Application(user_id=user_id, company=company, position=position)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

def get_application(db: Session, app_id: int):
    return db.query(models.Application).filter(models.Application.id == app_id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Application).offset(skip).limit(limit).all()
