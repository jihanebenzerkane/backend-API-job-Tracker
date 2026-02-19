from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# -------- USERS --------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer,primary_key=True, index=True)
    applications = relationship("Application", back_populates="user")

# -------- APPLICATIONS --------
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(String, default="Pending")

    user = relationship("User", back_populates="applications")
