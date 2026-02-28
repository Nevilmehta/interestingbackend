from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from core.dependencies import require_owner_or_admin
from core.tasks.email import send_welcome_email
from schemas.user import UserCreate, UserResponse, UserUpdate, SignupRequest
from services import user_services
from services.file_services import upload_user_avatar
from typing import Optional
from schemas.user import UserResponse

router = APIRouter()

# -------test protect a route-------------
@router.get("/me")
def read_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session=Depends(get_db)):
    return user_services.create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session=Depends(get_db), current_user = Depends(require_owner_or_admin)):
    try:
        return user_services.get_user(db, user_id)
    except ValueError: 
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/", response_model=list[UserResponse])
def list_users(
    limit: int =Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    email: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return user_services.list_users(
        db=db,
        limit=limit,
        offset=offset,
        email=email,
        is_active=is_active
    )

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user = Depends(require_owner_or_admin)):
    try:
        return user_services.update_user(db, user_id, user)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(require_owner_or_admin)):
    try: 
        user_services.delete_user(db, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")

# ---------file upload----------
@router.post("/{user_id}/avatar")
def upload_avatar(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(require_owner_or_admin)):
    return upload_user_avatar(db, user_id, file)

# ----------signpoint-------------
@router.post("/signup", response_model = UserResponse)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    try:
        user = user_services.signup_user(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # background_tasks.add_task(send_welcome_email, payload.email)
    send_welcome_email.delay(payload.email)
    return user