import pandas as pd
import numpy as np
from app.config import FILE_NAME

def monthly_summary():
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        return {}

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df = df.dropna(subset=["date", "amount"])

    result = df.groupby(
        df["date"].dt.strftime("%Y-%m")
    )["amount"].apply(
        lambda values: np.sum(values.to_numpy())
    )

    return {
        month: float(amount)
        for month, amount in result.items()
    }


def category_report():

    df = pd.read_csv(FILE_NAME)

    if df.empty:
        return {}

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(subset=["amount", "category"])

    result = df.groupby("category")["amount"].apply(
        lambda values: np.sum(values.to_numpy())
    )

    return {
        category: float(amount)
        for category, amount in result.items()
    }


def overall_statistics():

    df = pd.read_csv(FILE_NAME)

    if df.empty:
        return {
            "total": 0,
            "average": 0,
            "highest": 0,
            "count": 0
        }

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    amounts = df["amount"].dropna().to_numpy()

    if amounts.size == 0:
        return {
            "total": 0,
            "average": 0,
            "highest": 0,
            "count": 0
        }

    return {
        "total": float(np.sum(amounts)),
        "average": float(np.mean(amounts)),
        "highest": float(np.max(amounts)),
        "count": int(np.size(amounts))
    }
