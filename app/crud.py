from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hash_password, verify_password


# ---------- USERS ----------

def create_user(db: Session, name: str, email: str, password: str):
    db_user = models.User(
        name=name,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user


def authenticate_user(db: Session, email: str, password: str):
    """Return the user if credentials are valid, else None."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ---------- APPLICATIONS ----------

def create_application(db: Session, user_id: int, company: str, position: str, status: str = "pending"):
    db_app = models.Application(
        user_id=user_id,
        company=company,
        position=position,
        status=status
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def get_application(db: Session, app_id: int):
    return db.query(models.Application).filter(models.Application.id == app_id).first()


def get_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Application).offset(skip).limit(limit).all()


def get_applications_by_user(db: Session, user_id: int):
    return db.query(models.Application).filter(models.Application.user_id == user_id).all()


def update_application(db: Session, app_id: int, data: schemas.ApplicationUpdate):
    db_app = get_application(db, app_id)
    if not db_app:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_app, field, value)
    db.commit()
    db.refresh(db_app)
    return db_app


def delete_application(db: Session, app_id: int):
    db_app = get_application(db, app_id)
    if db_app:
        db.delete(db_app)
        db.commit()
    return db_app
