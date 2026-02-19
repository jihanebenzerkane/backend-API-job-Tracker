from pydantic import BaseModel

# -------- USERS --------
class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# -------- APPLICATIONS --------
class ApplicationCreate(BaseModel):
    user_id: int
    company: str
    position: str

class ApplicationOut(BaseModel):
    id: int
    user_id: int
    company: str
    position: str
    status: str

    class Config:
        orm_mode = True
