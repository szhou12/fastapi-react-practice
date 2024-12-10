from typing import Optional
from pydantic import BaseModel

# Define Pydantic models

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# model that contains registration info
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# model that contains user's public info stored in DB
class UserResponse(BaseModel):
    username: str
    email: Optional[str] = None

# model that contains user's whole info stored in DB
class UserInDB(UserResponse):
    # private info
    hashed_password: str

