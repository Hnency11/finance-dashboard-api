from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.orm import selectinload

from app.models.financial_record import FinancialRecord, RecordType
from app.schemas.financial_record import RecordCreate, RecordUpdate


class RecordsService:
    @staticmethod
    async def get_records(
        db: AsyncSession,
        record_type: Optional[RecordType] = None,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[FinancialRecord]:
        """Fetch records with optional filters."""
        query = select(FinancialRecord).where(FinancialRecord.is_deleted.is_(False))

        # apply filters if provided
        if record_type:
            query = query.where(FinancialRecord.type == record_type)
        if category:
            query = query.where(FinancialRecord.category == category)
        if start_date:
            query = query.where(FinancialRecord.date >= start_date)
        if end_date:
            query = query.where(FinancialRecord.date <= end_date)

        # sort by date and handle pagination
        query = query.order_by(FinancialRecord.date.desc()).limit(limit).offset(offset)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create_record(db: AsyncSession, payload: RecordCreate, user_id: UUID) -> FinancialRecord:
        """Create a new record."""
        record = FinancialRecord(
            **payload.model_dump(),
            user_id=user_id
        )
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    @staticmethod
    async def update_record(db: AsyncSession, record_id: UUID, payload: RecordUpdate) -> Optional[FinancialRecord]:
        """Update an existing record."""
        query = select(FinancialRecord).where(
            and_(FinancialRecord.id == record_id, FinancialRecord.is_deleted.is_(False))
        )
        result = await db.execute(query)
        record = result.scalars().first()

        if not record:
            return None

        # update fields only if provided in payload
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)

        await db.commit()
        await db.refresh(record)
        return record

    @staticmethod
    async def soft_delete_record(db: AsyncSession, record_id: UUID) -> bool:
        """Mark a record as deleted (soft delete)."""
        query = select(FinancialRecord).where(
            and_(FinancialRecord.id == record_id, FinancialRecord.is_deleted.is_(False))
        )
        result = await db.execute(query)
        record = result.scalars().first()

        if not record:
            return False

        record.is_deleted = True
        await db.commit()
        return True

    @staticmethod
    async def get_summary(db: AsyncSession):
        """Get totals for income and expenses."""
        # separate queries for totals
        income_query = select(func.sum(FinancialRecord.amount)).where(
            and_(FinancialRecord.type == RecordType.income, FinancialRecord.is_deleted.is_(False))
        )
        expense_query = select(func.sum(FinancialRecord.amount)).where(
            and_(FinancialRecord.type == RecordType.expense, FinancialRecord.is_deleted.is_(False))
        )

        income_res = await db.execute(income_query)
        expense_res = await db.execute(expense_query)

        total_income = income_res.scalar() or Decimal("0.00")
        total_expense = expense_res.scalar() or Decimal("0.00")

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": total_income - total_expense
        }

    @staticmethod
    async def get_category_summary(db: AsyncSession):
        """Get totals grouped by category."""
        query = select(
            FinancialRecord.category,
            func.sum(FinancialRecord.amount).label("total")
        ).where(
            FinancialRecord.is_deleted.is_(False)
        ).group_by(FinancialRecord.category)

        result = await db.execute(query)
        return [{"category": row[0], "amount": row[1]} for row in result.all()]

    @staticmethod
    async def get_monthly_summary(db: AsyncSession):
        """Get monthly income vs expense trends."""
        query = select(
            func.to_char(FinancialRecord.date, 'YYYY-MM').label('month'),
            func.sum(FinancialRecord.amount).filter(FinancialRecord.type == RecordType.income).label('income'),
            func.sum(FinancialRecord.amount).filter(FinancialRecord.type == RecordType.expense).label('expense')
        ).where(
            FinancialRecord.is_deleted.is_(False)
        ).group_by('month').order_by('month')

        result = await db.execute(query)
        return [
            {"month": row[0], "income": row[1] or Decimal("0.00"), "expense": row[2] or Decimal("0.00")}
            for row in result.all()
        ]
