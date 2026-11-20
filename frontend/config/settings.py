import os

API_BASE_URL = os.getenv("EXPENSE_API_URL", "https://expense-tracker-fastapi-m1ut.onrender.com").rstrip("/")
REQUEST_TIMEOUT = 10
PAGE_TITLE = "SpendWise | Expense Tracker"
PAGE_ICON = "💳"
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment"]
STATUSES = ["Pending", "Completed", "Failed"]
CURRENCY = "₹"
