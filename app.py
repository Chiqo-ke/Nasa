from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime, timedelta
import json
from gok import Blockchain, TransactionType

# Initialize FastAPI app
app = FastAPI(title="Government Blockchain API")

# Security configurations
SECRET_KEY = "your-secret-key-here"  # Change this to a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize blockchain
blockchain = Blockchain(save_file="blockchain.json")

# User database (replace with actual database in production)
users_db = {}

# Activity log file
ACTIVITY_LOG_FILE = "activity_log.json"

# Pydantic models
class User(BaseModel):
    username: str
    office_code: str
    full_name: str
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TransactionRequest(BaseModel):
    recipient_wallet: str
    amount: float
    transaction_type: str

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def log_activity(username: str, activity: str):
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "username": username,
        "activity": activity
    }
    try:
        with open(ACTIVITY_LOG_FILE, "r+") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=4)
    except FileNotFoundError:
        with open(ACTIVITY_LOG_FILE, "w") as f:
            json.dump([log_entry], f, indent=4)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# API endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    log_activity(user.username, "User logged in")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/balance")
async def get_balance(current_user: User = Depends(get_current_user)):
    balance = blockchain.calculate_wallet_balance(current_user.office_code)
    log_activity(current_user.username, f"Checked balance: {balance}")
    return {"office_code": current_user.office_code, "balance": balance}

@app.post("/transaction")
async def create_transaction(
    transaction: TransactionRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        # Create and validate transaction
        tx = {
            "sender": current_user.office_code,
            "recipient": transaction.recipient_wallet,
            "amount": transaction.amount,
            "type": transaction.transaction_type,
            "ministry_code": current_user.office_code
        }
        
        if not blockchain.add_transaction(tx):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction validation failed"
            )
            
        # Mine the transaction
        blockchain.mine_pending_transactions(
            ministry={"name": current_user.full_name},
            funding_sources={},
            expenditures={},
            remaining_budget=blockchain.calculate_wallet_balance(current_user.office_code),
            auditor_remarks=f"Transaction from {current_user.office_code}",
            smart_contract={}
        )
        
        log_activity(
            current_user.username,
            f"Created transaction: {transaction.amount} to {transaction.recipient_wallet}"
        )
        
        return {"status": "success", "message": "Transaction completed"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/transactions/history")
async def get_transaction_history(current_user: User = Depends(get_current_user)):
    transactions = []
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx["sender"] == current_user.office_code or tx["recipient"] == current_user.office_code:
                transactions.append({
                    "block_id": block.block_id,
                    "timestamp": block.timestamp,
                    **tx
                })
    
    log_activity(current_user.username, "Viewed transaction history")
    return transactions

# Admin endpoints (add appropriate admin-only authorization)
@app.post("/admin/register-user")
async def register_user(user: User, password: str):
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    users_db[user.username] = user_dict
    
    return {"status": "success", "message": "User registered successfully"}

@app.get("/admin/activity-log")
async def get_activity_log():
    try:
        with open(ACTIVITY_LOG_FILE, "r") as f:
            logs = json.load(f)
        return logs
    except FileNotFoundError:
        return []