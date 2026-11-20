import requests
from config.settings import API_BASE_URL, REQUEST_TIMEOUT


class APIError(Exception):
    pass


def request(method: str, path: str, **kwargs):
    try:
        response = requests.request(
            method, f"{API_BASE_URL}{path}",
            timeout=REQUEST_TIMEOUT, **kwargs
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    except requests.exceptions.HTTPError as exc:
        response = exc.response
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise APIError(f"{response.status_code}: {detail}") from exc
    except requests.exceptions.RequestException as exc:
        raise APIError(
            f"Cannot connect to {API_BASE_URL}. Start the FastAPI server and try again."
        ) from exc


def get_expenses(category=None, min_amount=None, max_amount=None, limit=100, offset=0):
    params = {"limit": limit, "offset": offset}
    if category and category != "All":
        params["category"] = category
    if min_amount is not None:
        params["min_amount"] = min_amount
    if max_amount is not None:
        params["max_amount"] = max_amount
    return request("GET", "/expenses", params=params).get("expenses", [])


def create_expense(payload):
    return request("POST", "/expenses", json=payload)


def update_expense(expense_id, payload):
    return request("PATCH", f"/expenses/{expense_id}", json=payload)


def delete_expense(expense_id):
    return request("DELETE", f"/expenses/{expense_id}")


def get_statistics():
    return request("GET", "/reports/statistics")
