import streamlit as st
import pandas as pd
from services.api_client import get_expenses, get_statistics, APIError
from components.ui import page_header, metric_card
from utils.formatters import money


def render_reports():
    page_header("INSIGHTS", "Reports & analytics", "Understand where your money goes and how your spending changes.")
    try:
        expenses = get_expenses(limit=100, offset=0)
        stats = get_statistics()
    except APIError as error:
        st.error(str(error))
        return

    a, b, c = st.columns(3)
    with a: metric_card("Total spent", money(stats.get("total", 0)), "All transactions", "↗")
    with b: metric_card("Average", money(stats.get("average", 0)), "Per transaction", "◉")
    with c: metric_card("Transactions", str(stats.get("count", len(expenses))), "Total records", "▤")

    if not expenses:
        st.info("Add expenses to unlock your analytics.")
        return

    df = pd.DataFrame(expenses)
    if "amount" in df and "category" in df:
        st.markdown("### Category breakdown")
        category = df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
        l, r = st.columns(2)
        with l: st.bar_chart(category, x="category", y="amount")
        with r: st.dataframe(category, use_container_width=True, hide_index=True)

    if "date" in df and "amount" in df:
        st.markdown("### Monthly spending")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        if not df.empty:
            df["month"] = df["date"].dt.to_period("M").astype(str)
            monthly = df.groupby("month", as_index=False)["amount"].sum().sort_values("month")
            st.line_chart(monthly, x="month", y="amount")
