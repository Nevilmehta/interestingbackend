from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate, UserUpdate
from schemas.user import SignupRequest
from repositories import user_repositories
from core.security import hash_password
from core.roles import Roles

# service layer (Business logic)
def create_user(db: Session, user_data: UserCreate):
    user_dict = user_data.model_dump()
    password = user_dict.pop("password")

    user = User(**user_dict, hashed_password = hash_password(password), role = Roles.USER)
    return user_repositories.create_user(db, user)

def get_user(db: Session, user_id: int):
    user = user_repositories.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    return user

def list_users(
    db: Session,
    limit: int,
    offset: int,
    email: str | None = None,
    is_active: bool | None = None
):
    query = db.query(User).filter(User.is_deleted == False)

    if email:
        query = query.filter(User.email.ilike(f"%{email}"))

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    users = (
        query
        .order_by(User.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return users

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user(db, user_id)
    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    return user_repositories.update_user(db, user)

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    user_repositories.soft_delete_user(db, user)

def signup_user(db: Session, data: SignupRequest):
    user_data = data.model_dump()
    password = user_data.pop("password")

    if user_repositories.get_user_by_email(db, data.email):
        raise ValueError("Email already exists")

    user = User(**user_data, hashed_password = hash_password(password), role=Roles.USER, is_active=True)

    return user_repositories.create_user(db, user)