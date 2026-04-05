from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.dependencies.db import get_db_session
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_role
from app.models.user import User
from app.services.users import UsersService
from app.schemas.user import UserResponse, UserCreate, UserUpdateAdmin


router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/", response_model=List[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["admin"]))
):
    """Admin: Show all user accounts."""
    return await UsersService.get_users(db)


@router.post("/", response_model=UserResponse)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["admin"]))
):
    """Admin: Manually create a user."""
    user = await UsersService.create_user(db, payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    return user


@router.patch("/{id}", response_model=UserResponse)
async def update_user(
    id: UUID,
    payload: UserUpdateAdmin,
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["admin"]))
):
    """Admin: Manage roles and active status."""
    updated_user = await UsersService.update_user(db, id, payload)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user
