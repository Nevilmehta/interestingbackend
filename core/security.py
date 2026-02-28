from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from core.database import get_db
from repositories.user_repositories import get_user_by_id
import hashlib, secrets


# --------------------Config------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY= "7dc747d210b23118387735e063af5068"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 15

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# -------------------Password------------------
def _pre_hash(password:str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ---------------------JWT-----------------------
def create_access_token(data: dict, expires_delta: timedelta | None=None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid or expired token")

# -----------------Decode & Validate Token----------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(db, int(user_id))

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# -------------------refresh token helper---------------
def create_refresh_token():
    return secrets.token_urlsafe(64)

def hash_refresh_token(token: str) -> str:
    return pwd_context.hash(token)

def verify_refresh_token(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)