from datetime import date

from fastapi import FastAPI, HTTPException, Query, status

from ai import categorize_expense
from crud import (
    create_expense as create_expense_db,
    delete_expense as delete_expense_db,
    get_expense_by_id as get_expense_by_id_db,
    get_expense_summary as get_expense_summary_db,
    get_expenses as get_expenses_db,
)
from models import (
    ALLOWED_CATEGORIES,
    CategorySummary,
    ExpenseCreate,
    ExpenseResponse,
    ExpenseSummary,
)


app = FastAPI(
    title="Smart Expense Tracker API",
    description="Expense tracking API with AI-powered expense categorization",
    version="1.0.0",
)


def row_to_expense(row):
    return {
        "id": row[0],
        "title": row[1],
        "amount": row[2],
        "category": row[3],
        "expense_date": row[4],
    }


def parse_month(month: str | None):
    if month is None:
        return None, None

    try:
        year, month_number = map(int, month.split("-"))

        if not 1 <= month_number <= 12:
            raise ValueError

        month_start = date(year, month_number, 1)

        if month_number == 12:
            month_end = date(year + 1, 1, 1)
        else:
            month_end = date(year, month_number + 1, 1)

        return month_start, month_end

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="month must be in YYYY-MM format",
        )


@app.get("/")
def home():
    return {"message": "Smart Expense Tracker API"}


@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense_endpoint(expense: ExpenseCreate):
    try:
        category = categorize_expense(expense.title)

        result = create_expense_db(
            expense.title,
            expense.amount,
            category,
            expense.expense_date,
        )

        return row_to_expense(result)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create expense",
        )


@app.get(
    "/expenses",
    response_model=list[ExpenseResponse],
)
def get_expenses_endpoint(
    category: str | None = Query(default=None, max_length=50),
    month: str | None = Query(
        default=None,
        pattern=r"^\d{4}-\d{2}$",
    ),
):
    if category and category not in ALLOWED_CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid expense category",
        )

    month_start, month_end = parse_month(month)

    try:
        expenses = get_expenses_db(
            category=category,
            month_start=month_start,
            month_end=month_end,
        )

        return [
            row_to_expense(expense)
            for expense in expenses
        ]

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve expenses",
        )


@app.get(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense_endpoint(expense_id: int):
    try:
        expense = get_expense_by_id_db(expense_id)

        if expense is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found",
            )

        return row_to_expense(expense)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve expense",
        )


@app.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense_endpoint(expense_id: int):
    try:
        deleted = delete_expense_db(expense_id)

        if deleted is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found",
            )

        return None

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete expense",
        )


@app.get(
    "/expenses/summary",
    response_model=ExpenseSummary,
)
def expense_summary_endpoint(
    month: str | None = Query(
        default=None,
        pattern=r"^\d{4}-\d{2}$",
    ),
):
    month_start, month_end = parse_month(month)

    try:
        total_row, category_rows = get_expense_summary_db(
            month_start=month_start,
            month_end=month_end,
        )

        return {
            "expense_count": total_row[0],
            "total_amount": total_row[1],
            "categories": [
                CategorySummary(
                    category=row[0],
                    expense_count=row[1],
                    total_amount=row[2],
                )
                for row in category_rows
            ],
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate expense summary",
        )