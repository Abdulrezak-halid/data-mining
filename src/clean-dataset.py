import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "online_retail.csv")
CLEANED_PATH = os.path.join(BASE_DIR, "data", "cleaned_retail.csv")
TRANSACTIONS_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")

# Load data (ISO-8859-1 handles common encoding issues in this dataset)
df = pd.read_csv(DATA_PATH, encoding="ISO-8859-1")
print("Before cleaning:", df.shape)

# Remove missing customers
df = df.dropna(subset=["CustomerID"])
2
# Remove returns or invalid quantities
df = df[df["Quantity"] > 0]

# Remove canceled invoices
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

print("After cleaning:", df.shape)

# Save cleaned dataset
df.to_csv(CLEANED_PATH, index=False)

# Build transactions: list of item descriptions per invoice
transactions = (
	df.groupby("InvoiceNo", as_index=False)["Description"]
	.agg(list)
	.rename(columns={"Description": "Items"})
)

# Save transactions dataset
transactions.to_csv(TRANSACTIONS_PATH, index=False)