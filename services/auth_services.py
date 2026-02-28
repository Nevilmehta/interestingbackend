from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import verify_password, create_access_token, create_refresh_token, hash_refresh_token
from repositories.user_repositories import get_user_by_email

def authenticate_user(db:Session, email:str, password:str):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token()
    user.hashed_refresh_token = hash_refresh_token(refresh_token)

    db.commit()

    return{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }