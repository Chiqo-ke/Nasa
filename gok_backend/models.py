# models.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Define the Base for SQLAlchemy models
Base = declarative_base()

# SQLAlchemy Model for Database
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    office_name = Column(String(255), unique=True, index=True)
    wallet_address = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

# Report Model for suspicious activity reporting
class ReportDB(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(100))  # 'tax_payment' or 'citizen_portal'
    reported_by = Column(String(255))  # Email or name of reporter
    subject = Column(String(255))
    description = Column(Text)
    transaction_hash = Column(String(255), nullable=True)  # Optional reference
    status = Column(String(50), default="pending")  # pending, reviewed, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_by = Column(String(255), nullable=True)
    admin_notes = Column(Text, nullable=True)