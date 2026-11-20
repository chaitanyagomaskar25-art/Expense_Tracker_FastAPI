import os

API_BASE_URL = os.getenv("EXPENSE_API_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 10
PAGE_TITLE = "SpendWise | Expense Tracker"
PAGE_ICON = "💳"
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment"]
STATUSES = ["Pending", "Completed", "Failed"]
CURRENCY = "₹"
