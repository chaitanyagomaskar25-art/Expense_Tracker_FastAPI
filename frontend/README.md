# SpendWise — Streamlit Expense Tracker UI

## Folder structure

```text
frontend/
├── app.py
├── config/
│   └── settings.py
├── services/
│   └── api_client.py
├── pages/
│   ├── dashboard.py
│   ├── add_expense.py
│   ├── expenses.py
│   └── reports.py
├── components/
│   ├── sidebar.py
│   └── ui.py
├── utils/
│   ├── formatters.py
│   └── styles.py
├── assets/
│   └── style.css
└── requirements.txt
```

## Setup

From the project root, install:

```bash
pip install -r frontend/requirements.txt
```

Terminal 1 — start FastAPI:

```bash
python -m uvicorn app.main:app --reload
```

Terminal 2 — start Streamlit:

```bash
streamlit run frontend/app.py
```

Default API URL: `http://127.0.0.1:8000`

To change it, set `EXPENSE_API_URL` before launching Streamlit.

## Backend endpoints used

- `GET /expenses`
- `POST /expenses`
- `PATCH /expenses/{expense_id}`
- `DELETE /expenses/{expense_id}`
- `GET /reports/statistics`

Category and monthly charts are calculated from the expense list in the frontend, so the UI does not assume an undocumented response shape for those report endpoints.

Note: The list page requests up to 100 records because that is the API's documented maximum page size. Add pagination if you need to browse more than 100 records.
