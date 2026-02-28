from sqlalchemy.orm import Session
from models.user import User
from datetime import datetime

# Repo Layer (DB Access only)
def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(
        User.id == user_id,
    ).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

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

def update_user(db: Session, user: User):
    db.commit()
    db.refresh(user)
    return user

def soft_delete_user(db: Session, user: User):
    user.is_deleted = True
    user.deleted_at = datetime.utcnow()
    db.commit()

def list_users_query(db: Session):
    return db.query(User).filter(User.is_deleted == False)