from typing import Optional
from datetime import datetime, timedelta, timezone
import bcrypt

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
# from passlib.context import CryptContext


# used in encrption and hashing algo
# $ openssl rand -hex 32
SECRET_KEY = "8f0541d753e4f77f3f79a25dfa337819280ecf7d44b5c62f62f0b8b967c37968"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = {
    "tim": {
        "username": "tim",
        "full_name": "Tim Ruscica",
        "email": "tim@gmail.com",
        "hashed_password": "$2b$12$jgJ6dvC0S/MvcUm.E3QboeCnoogbL8UcgibNr4s29W8dZjxthBfYC", # get_password_hash("tim1234")
        "disabled": False # False if signed in but the access token is not valid or expired
    }
}

# Define Data Models
class Token(BaseModel):
    access_token: str
    token_type: str

# data encoded by our token
class TokenData(BaseModel):
    username: Optional[str]= None

"""
Separation of Concerns & Security Best Practice: Keep sensitive data out of User class
- User class ONLY contains public data fields that are safe to share with other parts of the application or even with the client.
- UserInDB class extends the User class to include sensitive/private data fields.
"""
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# set up API user authentication
"""
pwd_context does 2 things: 1. use defined algo to hash passwords; 2. verify a given password against a stored one

Breakdown:
- CryptContext:
	•	A utility provided by the passlib library to manage password hashing.
	•	It standardizes the process of hashing and verifying passwords with various algorithms.
- schemes=["bcrypt"]:
	•	Specifies that the bcrypt hashing algorithm should be used.
	•	bcrypt is a secure, widely used hashing algorithm designed for password storage.
	•	It is slow and resistant to brute-force attacks, making it ideal for securing passwords.
- deprecated="auto":
	•	ensures that older or less secure hashing algorithms are marked as deprecated automatically if they were previously used in the application but are no longer listed in schemes.
	•	This is useful for applications upgrading from older hashing methods to newer, more secure ones.

Why Use It?
	•	To hash user passwords securely before storing them in a database.
	•	To verify user-provided passwords against stored hashed passwords during authentication.

NOTE: The use of passlib is abandoned in this code as it produces error: AttributeError: module 'bcrypt' has no attribute '__about__'. Directly use bcrypt instead.
Ref: https://github.com/pyca/bcrypt/issues/684
"""
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

"""
oauth2_scheme sets up an OAuth2 bearer token authentication scheme.

Breakdown:
- OAuth2PasswordBearer:
	•	A utility provided by FastAPI to implement OAuth2 authentication.
	•	It expects clients to send an access token in the Authorization header of HTTP requests.
- tokenUrl="token":
	•	Specifies the endpoint where clients can obtain the access token.
	•	In your case, this means the /token route in your FastAPI application will issue tokens when users provide valid credentials.

Why Use It?
	•	To protect endpoints that require authentication.
	•	FastAPI will use oauth2_scheme to automatically extract and validate the bearer token provided in requests.
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
Workflow:
1.	A client sends a request to the /token endpoint with credentials (username and password).
2.	The /token endpoint validates the credentials and generates a JWT (JSON Web Token).
3.	The client includes the JWT in the Authorization: Bearer <token> header for subsequent requests.
4.	oauth_2_scheme extracts the token and makes it available to your endpoint logic for verification and access control.
"""

# $ uvicorn tutorial_fastapi_auth:app --reload
app = FastAPI()


# utility functions to authenticate users and hash their passwords

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt for storage in the database.
    It is supposed to generate random hashes when re-run for the same password. 
    The affiliated salt is used to ensure the randomly generated hash matches the input password. 
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


def get_user(db, username: str):
    """
    Retrieves a user from the database by username.
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(db, username: str, password: str):
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
    给一个用户发放一个临时的有效身份(token), 后续该用户的任何请求都需要携带该身份才会被执行.
    用于用户登陆阶段, 如果用户成功登陆(用户名和密码都匹配正确), 则触发, 该登录用户获得一个临时的token, 用于后续的请求.

    :param data: The data to encode in the token, typically containing user-specific information like username
    :param expires_delta: The time delta for the token's expiration. Adds an expiration time to the token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # Combines the input data (including exp) into a JWT string using SECRET_KEY and signing algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""
- token: str = Depends(oauth2_scheme)
	•	Extracts the token from the Authorization header using the OAuth2PasswordBearer dependency.
	•	get_current_user()这个function会先触发依赖oauth2_scheme - 从/token endpoint接收请求, 并从请求的header中提取token

- Why async?
    •	Bc it depends on oauth2_scheme, which is async.

- Why separate Step 1 and Step 2?
	•	看上去好像多次一举, 为什么不直接使用payload中的username, 反而还要先搭载到TokenData?
    1. Separation of Concerns -> Decode JWT responsible ONLY for extracting raw data. DO NOT do anything further.
    2. Validation of Claims -> by creating a TokenData object, it implicitly validates the username field's type and value
    3. Decoupling -> By converting the payload into a TokenData object, you abstract away the JWT's internal structure and focus on the application-specific data you care about. If the JWT structure changes in the future (e.g., a different key is used instead of "sub"), you only need to update the part that maps the payload to TokenData, not the rest of your authentication logic.
    4. Encapsulation for Future Extensions -> TokenData model makes it easier to extend functionality later. e.g. you might add more fields to the TokenData model, such as scopes or roles, to handle more complex authorization logic.
"""
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    1. Verifies the JWT token by decoding it using jwt.decode.
    2. Extracts user information from the token payload.
    3. Retrieves the user object from a database or in-memory storage.

    jwt.decode() automatically checks if the current time is past the "exp" time. If the token is expired, it raises a JWTError.
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
    except JWTError:
        raise credential_exception
    
    # Step 2: Retrieve user from DB
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user # UserInDB object

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Checks if a user is active (disabled=True) before granting access to an endpoint.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

"""
This token route will be called when a user is signing in with their (username, password), and this function will return a Token object that we can use for whatever the duration the token is.

@app.post("/token"): Declares this function as an HTTP POST endpoint at the /token path.
response_model=Token: Specifies that the returned value should follow the Token Pydantic model.

OAuth2PasswordRequestForm: A built-in utility from FastAPI for OAuth2 password authentication. It extracts username and password from the application/x-www-form-urlencoded request body.
Depends(): Injects OAuth2PasswordRequestForm into the function. FastAPI automatically parses the form data from the request.

Workflow:
1. A user submits their username and password to /token using an HTTP POST request with application/x-www-form-urlencoded body.
2. The server validates the credentials using authenticate_user()
3. If authentication succeeds, the server generates a signed JWT (access token).
4. The server returns the access token to the client.
"""
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


## Sample routes that require authorization - need valid token to call
# The following both routes rely on get_current_active_user, which relies on get_current_user, which relies on oauth2_scheme, which relies on token through tokenUrl="token". This means that if we don't have a token, an exception will be raised saying unauthorized, and thus these 2 routes cannot be called.
# In real web flow, user will request a token from frontend, then they will save the token and use it to make any requests until the token expires. Then they will request a new token. 
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]
