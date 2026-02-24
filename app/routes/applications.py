from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/", response_model=schemas.ApplicationOut, status_code=201)
def create_application(
    app_data: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create an application — must be logged in."""
    user = crud.get_user(db, app_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_application(
        db,
        user_id=app_data.user_id,
        company=app_data.company,
        position=app_data.position,
        status=app_data.status or "pending"
    )


@router.get("/", response_model=List[schemas.ApplicationOut])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_applications(db, skip, limit)


@router.get("/user/{user_id}", response_model=List[schemas.ApplicationOut])
def read_applications_by_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_applications_by_user(db, user_id)


@router.get("/{app_id}", response_model=schemas.ApplicationOut)
def read_application(app_id: int, db: Session = Depends(get_db)):
    application = crud.get_application(db, app_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.patch("/{app_id}", response_model=schemas.ApplicationOut)
def update_application(
    app_id: int,
    data: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update an application — must be logged in."""
    updated = crud.update_application(db, app_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated


@router.delete("/{app_id}", status_code=204)
def delete_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete an application — must be logged in."""
    deleted = crud.delete_application(db, app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
