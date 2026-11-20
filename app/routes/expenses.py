from fastapi import APIRouter, HTTPException, Path, Query
from typing import Annotated
from pydantic import ValidationError

from app.models import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseReplace,
    ExpenseListResponse,
    ExpenseDetailResponse,
    ExpenseMutationResponse,
    ExpenseCategory
)

from app.services import (
    read_expenses,
    create_expense,
    find_expense,
    save_updated_expense,
    remove_expense
)


router = APIRouter(prefix="/expenses", tags=["Expenses"])


# GET ALL EXPENSES

@router.get("", response_model=ExpenseListResponse)
def get_expenses(
    category: Annotated[
        ExpenseCategory | None,
        Query(description="Filter by category")
    ] = None,

    min_amount: Annotated[
        float | None,
        Query(ge=0)
    ] = None,

    max_amount: Annotated[
        float | None,
        Query(ge=0)
    ] = None,

    limit: Annotated[
        int,
        Query(ge=1, le=100)
    ] = 10,

    offset: Annotated[
        int,
        Query(ge=0)
    ] = 0
):

    expenses = read_expenses()

    if min_amount is not None and max_amount is not None:
        if min_amount > max_amount:
            raise HTTPException(
                status_code=400,
                detail="Minimum amount cannot exceed maximum amount"
            )

    if category is not None:
        expenses = [
            e for e in expenses
            if e["category"] == category.value
        ]

    if min_amount is not None:
        expenses = [
            e for e in expenses
            if float(e["amount"]) >= min_amount
        ]

    if max_amount is not None:
        expenses = [
            e for e in expenses
            if float(e["amount"]) <= max_amount
        ]

    expenses = expenses[offset:offset + limit]

    return {"expenses": expenses}


# CREATE EXPENSE

@router.post(
    "",
    response_model=ExpenseMutationResponse,
    status_code=201
)
def add_expense(expense: ExpenseCreate):

    new_expense = create_expense(expense)

    return {
        "message": "Expense created successfully",
        "data": new_expense
    }


# GET EXPENSE BY ID

@router.get(
    "/{expense_id}",
    response_model=ExpenseDetailResponse
)
def get_expense_by_id(
    expense_id: Annotated[str, Path(min_length=1)]
):

    expense = find_expense(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail=f"Expense with ID {expense_id} not found"
        )

    return {"data": expense}


# PATCH EXPENSE

@router.patch(
    "/{expense_id}",
    response_model=ExpenseMutationResponse
)
def update_expense_partially(
    expense_id: Annotated[str, Path(min_length=1)],
    updated_data: ExpenseUpdate
):

    expenses = read_expenses()

    old_expense = next(
        (e for e in expenses if e["id"] == expense_id),
        None
    )

    if old_expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    update_data = updated_data.model_dump(
        exclude_unset=True,
        mode="json"
    )

    merged_data = old_expense.copy()

    if "user" in update_data and update_data["user"] is not None:

        merged_data["user"] = {
            **merged_data["user"],
            **update_data["user"]
        }

        update_data.pop("user")

    merged_data.update(update_data)

    try:
        validated_expense = ExpenseCreate.model_validate(
            {
                key: value
                for key, value in merged_data.items()
                if key != "id"
            }
        )

    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail=exc.errors(include_context=False)
        )

    updated_expense = validated_expense.model_dump(mode="json")

    updated_expense["id"] = expense_id

    save_updated_expense(
        expenses,
        old_expense,
        updated_expense
    )

    return {
        "message": "Expense updated successfully",
        "data": updated_expense
    }


# PUT EXPENSE

@router.put(
    "/{expense_id}",
    response_model=ExpenseMutationResponse
)
def update_expense_completely(
    expense_id: Annotated[str, Path(min_length=1)],
    updated_data: ExpenseReplace
):

    expenses = read_expenses()

    old_expense = next(
        (e for e in expenses if e["id"] == expense_id),
        None
    )

    if old_expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    replacement = updated_data.model_dump(mode="json")

    replacement["id"] = expense_id

    save_updated_expense(
        expenses,
        old_expense,
        replacement
    )

    return {
        "message": "Expense replaced successfully",
        "data": replacement
    }


# DELETE EXPENSE

@router.delete(
    "/{expense_id}",
    response_model=ExpenseMutationResponse
)
def delete_expense(
    expense_id: Annotated[str, Path(min_length=1)]
):

    expense = find_expense(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    remove_expense(expense)

    return {
        "message": "Expense deleted successfully",
        "data": expense
    }
