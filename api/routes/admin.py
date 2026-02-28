from fastapi import APIRouter, Depends
from core.dependencies import require_role
from core.roles import Roles

router = APIRouter()

@router.get("/dashboard")
def admin_dashboard(current_user = Depends(require_role(Roles.ADMIN))):
    return{
        "message": "Welcome Admin!",
        "admin_id": current_user.id
    }