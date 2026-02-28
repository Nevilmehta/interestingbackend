from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# create schema
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

# update schema
class UserUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

# Response schema
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        
# signup point
class SignupRequest(BaseModel):
    email: EmailStr
    name: str
    password: str