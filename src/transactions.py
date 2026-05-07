import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_PATH = os.path.join(BASE_DIR, "data", "cleaned_retail.csv")
TRANSACTIONS_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")

# Load cleaned data
df = pd.read_csv(CLEANED_PATH, encoding="ISO-8859-1")

# Group items by invoice into transactions
transactions = (
	df.groupby("InvoiceNo", as_index=False)["Description"]
	.agg(list)
	.rename(columns={"Description": "Items"})
)

print(transactions.head())

# Save transactions
transactions.to_csv(TRANSACTIONS_PATH, index=False)