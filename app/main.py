
from fastapi import FastAPI

from app.routes import expenses, reports


app = FastAPI(
    title="Expense Tracker API",
    description="API for managing personal expenses",
    version="1.0.0"
)

# Register routers

app.include_router(expenses.router)
app.include_router(reports.router)


@app.get("/")
def home():
    return {
        "message": "Expense Tracker API is running"
    }
