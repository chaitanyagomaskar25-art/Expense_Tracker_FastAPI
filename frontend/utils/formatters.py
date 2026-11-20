from datetime import date
from config.settings import CURRENCY


def money(value):
    try:
        return f"{CURRENCY}{float(value):,.2f}"
    except (TypeError, ValueError):
        return f"{CURRENCY}0.00"


def safe_date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return date.today()
