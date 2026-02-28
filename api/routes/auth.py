from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.auth import LoginRequest, TokenResponse
from services.auth_services import authenticate_user
from core.database import get_db
from core.security import verify_refresh_token, create_access_token, get_current_user, hash_refresh_token
from models.user import User

router = APIRouter()

@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_user(db, data.username, data.password)

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.hashed_refresh_token.isnot(None)).first()

    if not user or not verify_refresh_token(refresh_token, user.hashed_refresh_token):
        raise HTTPException(status_code=401, detail="Invalid refresh Token")

    new_access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {"access_token": new_access_token}

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session= Depends(get_db)):
    current_user.hashed_refresh_token = None
    db.commit()
    return {"message": "Logged out"}