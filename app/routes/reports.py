
from fastapi import APIRouter

from app.models import StatisticsResponse

from app.analytics import (
    monthly_summary,
    category_report,
    overall_statistics
)


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly")
def get_monthly_report():
    return monthly_summary()


@router.get("/category")
def get_category_report():
    return category_report()


@router.get(
    "/statistics",
    response_model=StatisticsResponse
)
def get_statistics():
    return overall_statistics()
