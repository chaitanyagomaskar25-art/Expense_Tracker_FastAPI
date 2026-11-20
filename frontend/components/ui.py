import streamlit as st
import pandas as pd
from utils.formatters import money


def page_header(eyebrow, title, subtitle):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div><h1 class="page-title">{title}</h1><p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)


def metric_card(label, value, helper, symbol):
    st.markdown(
        f'<div class="metric-card"><div class="metric-top"><span>{label}</span>'
        f'<span class="metric-icon">{symbol}</span></div>'
        f'<div class="metric-value">{value}</div><div class="metric-helper">{helper}</div></div>',
        unsafe_allow_html=True,
    )


def expense_dataframe(expenses):
    if not expenses:
        st.info("No expenses found yet. Add your first expense to get started.")
        return
    rows = []
    for item in expenses:
        user = item.get("user") or {}
        rows.append({
            "Expense": item.get("title", ""),
            "Name": user.get("name", ""),
            "Amount": money(item.get("amount")),
            "Category": item.get("category", ""),
            "Status": item.get("status", "Pending"),
            "Date": item.get("date", ""),
            "Paid": "Yes" if item.get("paid") else "No",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
