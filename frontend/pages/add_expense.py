import streamlit as st
from datetime import date
from config.settings import CATEGORIES, STATUSES
from services.api_client import create_expense, APIError
from components.ui import page_header


def render_add_expense():
    page_header("NEW TRANSACTION", "Add an expense", "Capture the details now. Keep your spending history accurate.")
    with st.container(border=True):
        with st.form("create_expense", clear_on_submit=True):
            st.markdown("#### Person and expense")
            c1, c2 = st.columns(2)
            name = c1.text_input("Full name *", placeholder="e.g. Alex Morgan")
            email = c2.text_input("Email address *", placeholder="alex@example.com")
            title = c1.text_input("Expense title *", placeholder="e.g. Weekly groceries")
            amount = c2.number_input("Amount (₹) *", min_value=0.01, step=50.0)
            category = c1.selectbox("Category", CATEGORIES)
            status = c2.selectbox("Status", STATUSES)
            expense_date = st.date_input("Date", value=date.today())
            notes = st.text_area("Notes", placeholder="Add a note (optional)", max_chars=500)
            paid = st.checkbox("This expense has been paid")
            submitted = st.form_submit_button("Save expense", type="primary", use_container_width=True)

    if submitted:
        if not name.strip() or not email.strip() or not title.strip():
            st.warning("Please complete all required fields.")
            return
        payload = {
            "user": {"name": name.strip(), "email": email.strip()},
            "title": title.strip(),
            "amount": amount,
            "category": category,
            "status": status,
            "date": expense_date.isoformat(),
            "notes": notes.strip() or None,
            "paid": paid,
        }
        try:
            result = create_expense(payload)
            st.success(result.get("message", "Expense saved successfully."))
            with st.expander("Created expense details"):
                st.json(result.get("data", {}))
        except APIError as error:
            st.error(str(error))
