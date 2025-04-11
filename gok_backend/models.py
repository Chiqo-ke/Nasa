# models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Define the Base for SQLAlchemy models
Base = declarative_base()

# SQLAlchemy Model for Database
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    office_name = Column(String(255), unique=True, index=True)
    wallet_address = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))