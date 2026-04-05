from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdateAdmin


class UsersService:
    @staticmethod
    async def get_users(db: AsyncSession, limit: int = 100, offset: int = 0) -> List[User]:
        """List all users in the system."""
        query = select(User).options(selectinload(User.role)).limit(limit).offset(offset)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create_user(db: AsyncSession, payload: UserCreate) -> Optional[User]:
        """Create a new user profile."""
        # check if email is already taken
        query = select(User).where(User.email == payload.email)
        result = await db.execute(query)
        if result.scalars().first():
            return None

        user = User(
            **payload.model_dump()
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_user(db: AsyncSession, user_id: UUID, payload: UserUpdateAdmin) -> Optional[User]:
        """Update user role or status."""
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            return None

        # only update fields that were actually passed
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        return user
