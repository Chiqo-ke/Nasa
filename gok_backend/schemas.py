# schemas.py

from pydantic import BaseModel

class User(BaseModel):
    office_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    wallet_address: str
    office_name: str

class RefreshToken(BaseModel):
    refresh_token: str

class Transaction(BaseModel):
    recipient: str
    amount: float