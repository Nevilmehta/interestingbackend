from fastapi import Depends, HTTPException, status
from core.security import get_current_user
from core.roles import Roles
# from core.database import get_db
from sqlalchemy.orm import Session
from repositories.user_repositories import get_user_by_id

def require_role(require_role: str):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role != require_role:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail= "You don't have permission to access this resource"
            )
        return current_user
    return role_checker

def require_owner_or_admin(user_id: int, current_user = Depends(get_current_user)):

    # print("DEBUG:", current_user.id, current_user.__dict__)

    # admin can do anything
    if current_user.role == "admin":
        return current_user 
    
    # Owner check
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return current_user