from typing import Optional
from datetime import datetime, timedelta, timezone
import bcrypt

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from ..database import get_db
from ..schemas import TokenData, UserInDB
from ..models import User

SECRET_KEY = "8f0541d753e4f77f3f79a25dfa337819280ecf7d44b5c62f62f0b8b967c37968"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Grouping related routes
router = APIRouter()

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt for storage in the database.
    """
    pwd_bytes = password.encode('utf-8') # convert str to bytes
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if an input plain password matches a hashed password stored in DB.
    """
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password = plain_password_bytes, hashed_password = hashed_password_bytes)

def get_user(db: Session, username: str):
    """
    Retrieves a user from the database by username.
    """
    db_user = db.query(User).filter(User.username == username).first()
    return db_user # ORM object

# def get_user(db: Session, username: str) -> Optional[UserInDB]:
#     """
#     Retrieves a user from the database by username and converts to Pydantic model.
#     Returns None if user not found.
#     """
#     db_user = db.query(User).filter(User.username == username).first()
#     if db_user is None:
#         return None
    
#     # Convert SQLAlchemy ORM model to Pydantic model
#     return UserInDB(
#         username=db_user.username,
#         email=db_user.email,
#         hashed_password=db_user.hashed_password
#     )

def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticates a user by comparing input (username, password) to those stored in DB.
    """
    user = get_user(db, username)
    if not user: # no such user found
        return False
    if not verify_password(password, user.hashed_password): # incorrect password
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generates an access token using the provided data.

    :param data: The data to encode in the token, typically containing user-specific information like username
    :param expires_delta: The time delta for the token's expiration. Adds an expiration time to the token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    1. Verifies the JWT token by decoding it using jwt.decode.
    2. Extracts user information from the token payload.
    3. Retrieves the user object from DB.
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Step 1: Decode JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # payload = user data
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credential_exception
    
    # Step 2: Retrieve user from DB
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user

# TODO
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Checks if a user is active (disabled=True) before granting access to an endpoint.
    """
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user