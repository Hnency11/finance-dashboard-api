from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str # full name
    email: str 
    password: str # plain password for now
    role_id: UUID # assigned role ID


class UserUpdateAdmin(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[UUID] = None # new role
    is_active: Optional[bool] = None # enable/disable account


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role_id: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
