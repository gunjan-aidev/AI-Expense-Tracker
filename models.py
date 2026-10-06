from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


ALLOWED_CATEGORIES = {
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Healthcare",
    "Travel",
    "Education",
    "Other",
}


class ExpenseCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255
    )
    amount: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    expense_date: date


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    category: str
    expense_date: date


class CategorySummary(BaseModel):
    category: str
    expense_count: int
    total_amount: Decimal


class ExpenseSummary(BaseModel):
    expense_count: int
    total_amount: Decimal
    categories: list[CategorySummary]


class AIExpenseCategory(BaseModel):
    category: Literal[
        "Food",
        "Transport",
        "Shopping",
        "Entertainment",
        "Bills",
        "Healthcare",
        "Travel",
        "Education",
        "Other",
    ]
