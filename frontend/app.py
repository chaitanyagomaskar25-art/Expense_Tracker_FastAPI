import streamlit as st
from config.settings import PAGE_TITLE, PAGE_ICON
from utils.styles import load_css
from components.sidebar import render_sidebar
from pages.dashboard import render_dashboard
from pages.add_expense import render_add_expense
from pages.expenses import render_expenses
from pages.reports import render_reports

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide", initial_sidebar_state="expanded")
load_css()

PAGES = {
    "Dashboard": ("⌂", render_dashboard),
    "Add Expense": ("＋", render_add_expense),
    "All Expenses": ("▤", render_expenses),
    "Reports & Analytics": ("▥", render_reports),
}

page = render_sidebar(PAGES)
PAGES[page][1]()
