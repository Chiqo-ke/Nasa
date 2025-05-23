from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import time
from models import UserDB
from schemas import User, Token, RefreshToken, Transaction
from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_current_user_from_refresh_token,
    log_user_activity,
    generate_wallet_address,
    get_password_hash,
    revoked_tokens,
    oauth2_scheme,
)
from blockchain import Blockchain
from database import get_db
from connections import active_connections

app = FastAPI()
router = APIRouter()

# Add this near the top of your file after creating the router
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Initialize blockchain
blockchain = Blockchain()

# Endpoints
@router.post("/register", response_model=dict)
async def register_user(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.office_name == user.office_name).first()
    if db_user: 
        raise HTTPException(status_code=400, detail="Office name already registered")

    # Generate wallet address
    wallet_address = generate_wallet_address()

    # Check if wallet address is unique
    db_user = db.query(UserDB).filter(UserDB.wallet_address == wallet_address).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Wallet address already exists")

    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        office_name=user.office_name,
        wallet_address=wallet_address,
        hashed_password=hashed_password
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        log_user_activity(user.office_name, "Registered new account")
        return {"message": "User registered successfully", "wallet_address": wallet_address}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ... (rest of the endpoints)

@router.post("/token", response_model=Token)
async def login_for_access_token(user: User, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.office_name, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect office name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.office_name}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": authenticated_user.office_name}, expires_delta=refresh_token_expires
    )

    log_user_activity(authenticated_user.office_name, "Logged in")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "wallet_address": authenticated_user.wallet_address,
        "office_name": authenticated_user.office_name
    }

@router.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token: RefreshToken, db: Session = Depends(get_db)):
    user = await get_current_user_from_refresh_token(refresh_token.refresh_token, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.office_name}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token.refresh_token,
        "wallet_address": user.wallet_address,
        "office_name": user.office_name
    }

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Check if the token has already been revoked
    if token in revoked_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has already been revoked"
        )

    # Add the token to the revoked tokens set
    revoked_tokens.add(token)

    return {"message": "Successfully logged out"}

 
@router.get("/balance/")
async def get_balance(current_user: UserDB = Depends(get_current_user)):
    balance = blockchain.calculate_wallet_balance(current_user.wallet_address)
    log_user_activity(current_user.office_name, f"Checked balance: {balance}")
    return {"balance": balance}

@router.post("/send/")
async def send_funds(
    transaction: Transaction,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Validate transaction amount
        if transaction.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be positive"
            )

        # Create blockchain transaction with enhanced details
        blockchain_transaction = {
            "sender": current_user.wallet_address,
            "recipient": transaction.recipient,
            "amount": float(transaction.amount),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "purpose": getattr(transaction, 'purpose', 'No purpose specified'),
            "approved_by": getattr(transaction, 'approved_by', 'Not specified'),
            "extra_info": getattr(transaction, 'extra_info', ''),
            "date": time.strftime("%Y-%m-%d", time.gmtime())
        }

        # Add transaction to blockchain
        if not blockchain.add_transaction(blockchain_transaction):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction validation failed"
            )

        # Mine the block
        try:
            await blockchain.mine_block(current_user.wallet_address, active_connections)
        except Exception as e:
            print(f"Mining error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to mine block: {str(e)}"
            )

        # Log the successful transaction with enhanced details
        log_message = (
            f"Sent {transaction.amount} to {transaction.recipient}\n"
            f"Purpose: {blockchain_transaction['purpose']}\n"
            f"Approved by: {blockchain_transaction['approved_by']}"
        )
        log_user_activity(current_user.office_name, log_message)

        return {
            "message": "Transaction successful",
            "transaction_details": blockchain_transaction
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Transaction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process transaction: {str(e)}"
        )

@router.get("/transactions/")
async def get_transactions(current_user: UserDB = Depends(get_current_user)):
    # Get transactions for the current user's wallet
    transactions = blockchain.get_transactions_for_wallet(current_user.wallet_address)
    return {"transactions": transactions}

@router.get("/transactions_all/")
async def get_all_transactions():
    """
    Get all transactions with complete details including optional fields.
    Returns a list of transactions with enhanced information.
    """
    transactions_all = []
    for block in blockchain.chain:
        for transaction in block.transactions:
            # Create detailed transaction object
            detailed_transaction = {
                "transaction_id": transaction.get("transaction_id", "N/A"),
                "sender": transaction.get("sender", "N/A"),
                "recipient": transaction.get("recipient", "N/A"),
                "amount": transaction.get("amount", 0.0),
                "timestamp": transaction.get("timestamp", "N/A"),
                "date": transaction.get("date", "N/A"),
                "purpose": transaction.get("purpose", "No purpose specified"),
                "approved_by": transaction.get("approved_by", "Not specified"),
                "extra_info": transaction.get("extra_info", ""),
                "block_id": block.block_id,
                "validator": block.validator
            }
            transactions_all.append(detailed_transaction)
    
    return {
        "transactions_all": transactions_all,
        "total_transactions": len(transactions_all)
    }

@router.get("/users/")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return {"users": [{"office_name": user.office_name, "wallet_address": user.wallet_address} for user in users]}

@router.get("/me/")
async def get_me(current_user: UserDB = Depends(get_current_user)):
    return {
        "office_name": current_user.office_name,
        "wallet_address": current_user.wallet_address
    }