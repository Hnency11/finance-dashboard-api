from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dependencies.db import get_db_session
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_role
from app.models.user import User
from app.services.records import RecordsService
from app.schemas.financial_record import SummaryResponse, CategorySummary, MonthlySummary, RecordResponse


router = APIRouter(prefix="/summary", tags=["Dashboard Summary"])


@router.get("/", response_model=SummaryResponse)
async def get_total_summary(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["analyst", "admin"]))
):
    """Get summarized totals (income vs expense)."""
    return await RecordsService.get_summary(db)


@router.get("/category", response_model=List[CategorySummary])
async def get_category_breakdown(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["analyst", "admin"]))
):
    """Get breakdown by category."""
    return await RecordsService.get_category_summary(db)


@router.get("/monthly", response_model=List[MonthlySummary])
async def get_monthly_trend(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["analyst", "admin"]))
):
    """Get monthly trends for the dashboard."""
    return await RecordsService.get_monthly_summary(db)


@router.get("/recent", response_model=List[RecordResponse])
async def get_recent_transactions(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_role(["viewer", "analyst", "admin"]))
):
    """Show the 5 most recent records."""
    return await RecordsService.get_records(db, limit=5)
