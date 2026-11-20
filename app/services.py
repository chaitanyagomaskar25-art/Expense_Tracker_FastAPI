import pandas as pd
from uuid import uuid4

from app.config import FILE_NAME, FIELDS
from app.utils import prepare_for_storage, prepare_for_response


def read_expenses():

    try:
        df = pd.read_csv(
            FILE_NAME,
            dtype={"id": str},
        )
        df = df.astype(object).where(pd.notna(df), None)
        expenses = df.to_dict(orient="records")

        return [prepare_for_response(expense) for expense in expenses]

    except pd.errors.EmptyDataError:
        return []


def write_expenses(expenses):

    storage_data = [prepare_for_storage(expense) for expense in expenses]

    df = pd.DataFrame(storage_data, columns=FIELDS)

    df.to_csv(FILE_NAME, index=False)


def create_expense(expense):

    expenses = read_expenses()

    new_expense = expense.model_dump(mode="json")

    new_expense["id"] = str(uuid4())

    expenses.append(new_expense)

    write_expenses(expenses)

    return new_expense


def find_expense(expense_id):

    expenses = read_expenses()

    return next((item for item in expenses if item["id"] == expense_id), None)


def save_updated_expense(expenses, old_expense, updated_expense):

    index = expenses.index(old_expense)

    expenses[index] = updated_expense

    write_expenses(expenses)

    return updated_expense


def remove_expense(expense):

    expenses = read_expenses()

    expenses.remove(expense)

    write_expenses(expenses)

    return expense
