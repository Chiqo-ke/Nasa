# auth.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import UserDB
import os
import secrets

# Security settings
SECRET_KEY = "your-secret-key"  # Change this in production
REFRESH_SECRET_KEY = "your-refresh-secret-key"  # Separate key for refresh tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token blacklist
revoked_tokens = set()

# Utility functions
def generate_wallet_address():
    """Generate a unique wallet address."""
    return f"0x{secrets.token_hex(20)}"

def get_password_hash(password: str) -> str:
    """Generate password hash using bcrypt."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_user(db: Session, office_name: str):
    """Get user from database."""
    return db.query(UserDB).filter(UserDB.office_name == office_name).first()

def authenticate_user(db: Session, office_name: str, password: str):
    """Authenticate user."""
    user = get_user(db, office_name)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create refresh token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user from access token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token in revoked_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        office_name: str = payload.get("sub")
        if office_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(db, office_name=office_name)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_from_refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Get current user from refresh token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if refresh_token in revoked_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        office_name: str = payload.get("sub")
        if office_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = get_user(db, office_name=office_name)
    if user is None:
        raise credentials_exception
    return user

def log_user_activity(office_name: str, activity: str):
    """Log user activity."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open(f"{log_dir}/user_logs.txt", "a") as f:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        f.write(f"{timestamp} - {office_name}: {activity}\n")