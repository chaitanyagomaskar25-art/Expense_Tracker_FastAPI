import streamlit as st
import pandas as pd
from services.api_client import get_expenses, get_statistics, APIError
from components.ui import page_header, metric_card, expense_dataframe
from utils.formatters import money


def render_dashboard():
    page_header("OVERVIEW", "Your money, in focus.", "Track spending, understand patterns, and stay in control.")
    try:
        expenses = get_expenses(limit=100, offset=0)
        stats = get_statistics()
    except APIError as error:
        st.error(str(error))
        st.info("Start FastAPI with: python -m uvicorn app.main:app --reload")
        return

    total = stats.get("total", sum(float(x.get("amount") or 0) for x in expenses))
    average = stats.get("average", (total / len(expenses) if expenses else 0))
    highest = stats.get("highest", max([float(x.get("amount") or 0) for x in expenses], default=0))
    count = stats.get("count", len(expenses))

    cols = st.columns(4)
    values = [
        ("Total spent", money(total), "Across recorded expenses", "↗"),
        ("Average expense", money(average), "Average per transaction", "◉"),
        ("Largest expense", money(highest), "Your highest transaction", "⌁"),
        ("Transactions", str(count), "Recorded expenses", "▤"),
    ]
    for col, data in zip(cols, values):
        with col:
            metric_card(*data)

    st.markdown('<div class="section-heading">Spending overview</div>', unsafe_allow_html=True)
    left, right = st.columns([1.15, 1])
    df = pd.DataFrame(expenses)
    with left:
        st.markdown('<div class="chart-panel"><div class="panel-title">By category</div><div class="panel-subtitle">How your expenses are distributed</div>', unsafe_allow_html=True)
        if not df.empty and {"category", "amount"}.issubset(df.columns):
            chart = df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
            st.bar_chart(chart, x="category", y="amount", use_container_width=True)
        else:
            st.caption("Category chart will appear when expenses are available.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="chart-panel"><div class="panel-title">Monthly trend</div><div class="panel-subtitle">Spending over time</div>', unsafe_allow_html=True)
        if not df.empty and {"date", "amount"}.issubset(df.columns):
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            monthly = df.dropna(subset=["date"]).assign(month=lambda x: x["date"].dt.to_period("M").astype(str))
            monthly = monthly.groupby("month", as_index=False)["amount"].sum().sort_values("month")
            if not monthly.empty:
                st.line_chart(monthly, x="month", y="amount", use_container_width=True)
            else:
                st.caption("Add valid expense dates to see the monthly trend.")
        else:
            st.caption("Monthly trend will appear when expenses are available.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Latest activity</div>', unsafe_allow_html=True)
    expense_dataframe(expenses[:8])
