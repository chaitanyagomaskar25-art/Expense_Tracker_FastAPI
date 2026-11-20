import streamlit as st
from config.settings import CATEGORIES, STATUSES
from services.api_client import get_expenses, update_expense, delete_expense, APIError
from components.ui import page_header, expense_dataframe
from utils.formatters import safe_date


def render_expenses():
    page_header("TRANSACTION HISTORY", "All expenses", "Search, review, update, or remove a transaction.")
    c1, c2, c3 = st.columns([1, 1, 1])
    category = c1.selectbox("Category", ["All"] + CATEGORIES)
    min_amount = c2.number_input("Min amount", min_value=0.0, value=0.0)
    max_amount = c3.number_input("Max amount (0 = no limit)", min_value=0.0, value=0.0)
    try:
        expenses = get_expenses(
            category=category,
            min_amount=min_amount if min_amount > 0 else None,
            max_amount=max_amount if max_amount > 0 else None,
            limit=100, offset=0,
        )
    except APIError as error:
        st.error(str(error))
        return

    st.markdown(f'<div class="results-count">{len(expenses)} transaction(s) found</div>', unsafe_allow_html=True)
    expense_dataframe(expenses)

    if not expenses:
        return

    st.divider()
    st.markdown("### Manage a transaction")
    labels = {f"{x.get('title')} · {x.get('id')}": x for x in expenses}
    selected = st.selectbox("Select expense", list(labels.keys()))
    item = labels[selected]
    user = item.get("user") or {}

    edit_tab, delete_tab = st.tabs(["✏️ Edit", "🗑️ Delete"])
    with edit_tab:
        with st.form("edit_expense"):
            a, b = st.columns(2)
            name = a.text_input("Name", value=user.get("name", ""))
            email = b.text_input("Email", value=user.get("email", ""))
            title = a.text_input("Title", value=item.get("title", ""))
            amount = b.number_input("Amount (₹)", min_value=0.01, value=max(float(item.get("amount") or 0.01), 0.01))
            cat = item.get("category")
            category_value = a.selectbox("Category", CATEGORIES, index=CATEGORIES.index(cat) if cat in CATEGORIES else 0)
            stat = item.get("status", "Pending")
            status_value = b.selectbox("Status", STATUSES, index=STATUSES.index(stat) if stat in STATUSES else 0)
            expense_date = st.date_input("Date", value=safe_date(item.get("date")))
            notes = st.text_area("Notes", value=item.get("notes") or "", max_chars=500)
            paid = st.checkbox("Paid", value=bool(item.get("paid", False)))
            save = st.form_submit_button("Save changes", type="primary")
        if save:
            if not name.strip() or not email.strip() or not title.strip():
                st.warning("Name, email and title are required.")
            else:
                payload = {
                    "user": {"name": name.strip(), "email": email.strip()},
                    "title": title.strip(),
                    "amount": amount,
                    "category": category_value,
                    "status": status_value,
                    "date": expense_date.isoformat(),
                    "notes": notes.strip() or None,
                    "paid": paid,
                }
                try:
                    result = update_expense(item["id"], payload)
                    st.success(result.get("message", "Expense updated."))
                    st.rerun()
                except APIError as error:
                    st.error(str(error))

    with delete_tab:
        st.warning(f"Delete **{item.get('title')}** ({item.get('id')})? This action cannot be undone.")
        confirm = st.checkbox("I understand this expense will be permanently deleted.", key="confirm_delete")
        if st.button("Delete this expense", type="primary", disabled=not confirm):
            try:
                result = delete_expense(item["id"])
                st.success(result.get("message", "Expense deleted."))
                st.rerun()
            except APIError as error:
                st.error(str(error))
