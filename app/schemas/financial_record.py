from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from app.models.financial_record import RecordType


class RecordCreate(BaseModel):
    amount: Decimal
    type: RecordType
    category: str
    date: datetime
    notes: Optional[str] = None


class RecordUpdate(BaseModel):
    amount: Optional[Decimal] = None
    type: Optional[RecordType] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None


class RecordResponse(BaseModel):
    id: UUID
    amount: Decimal
    type: RecordType
    category: str # simple label like 'Food'
    date: datetime
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    net_balance: Decimal # income minus expense


class CategorySummary(BaseModel):
    category: str
    amount: Decimal # total for this category


class MonthlySummary(BaseModel):
    month: str
    income: Decimal
    expense: Decimal
