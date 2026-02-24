from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ---------- USER ----------

class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str          # plain password — hashed before storage


class UserOut(UserBase):
    id: int

    model_config = {"from_attributes": True}


# ---------- APPLICATION ----------

class ApplicationBase(BaseModel):
    company: str
    position: str
    user_id: int
    status: Optional[str] = "pending"


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None


class ApplicationOut(ApplicationBase):
    id: int
    date_applied: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------- AUTH ----------

class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
