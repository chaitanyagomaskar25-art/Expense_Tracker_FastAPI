
import json

from app.config import JSON_FIELDS


def prepare_for_storage(expense: dict) -> dict:
    expense = expense.copy()

    for field in JSON_FIELDS:
        expense[field] = json.dumps(expense[field])

    return expense 


def prepare_for_response(expense: dict) -> dict:
    expense = expense.copy()

    for field in JSON_FIELDS:
        value = expense.get(field)

        if isinstance(value, dict):
            continue

        if isinstance(value, str) and value.strip():
            try:
                expense[field] = json.loads(value)
            except json.JSONDecodeError:
                expense[field] = {}
        else:
            expense[field] = {}

    return expense