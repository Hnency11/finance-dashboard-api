from uuid import UUID
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db_session
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_role
from app.models.user import User
from app.models.financial_record import RecordType
from app.services.records import RecordsService
from app.schemas.financial_record import RecordCreate, RecordUpdate, RecordResponse


router = APIRouter(prefix="/records", tags=["Records"])


@router.get("/", response_model=List[RecordResponse])
async def get_records(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user), # Base auth
    type: Optional[RecordType] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0
):
    """Fetch lists of records with simple filters."""
    return await RecordsService.get_records(
        db, record_type=type, category=category, 
        start_date=start_date, end_date=end_date, 
        limit=limit, offset=offset
    )


@router.post("/", response_model=RecordResponse)
async def create_record(
    payload: RecordCreate,
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["admin"]))
):
    """Admin-only: Create a new record."""
    return await RecordsService.create_record(db, payload, user.id)


@router.patch("/{id}", response_model=RecordResponse)
async def update_record(
    id: UUID,
    payload: RecordUpdate,
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["admin"]))
):
    """Admin-only: Update specific record fields."""
    record = await RecordsService.update_record(db, id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    return record


@router.delete("/{id}")
async def delete_record(
    id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["admin"]))
):
    """Admin-only: Soft delete a record."""
    deleted = await RecordsService.soft_delete_record(db, id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    return {"message": "Record deleted"}
