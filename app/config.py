
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

FILE_NAME = DATA_DIR / "expenses.csv"

FIELDS = [
    "id",
    "user",
    "title",
    "amount",
    "status",
    "category",
    "date",
    "notes",
    "paid"
]

JSON_FIELDS = ["user"]


# Create CSV if it doesn't exist
if not FILE_NAME.exists(): 
    import pandas as pd

    df = pd.DataFrame(columns=FIELDS)
    df.to_csv(FILE_NAME, index=False)
