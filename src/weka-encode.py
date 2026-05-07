import ast
import os
from collections import Counter

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSACTIONS_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")
WEKA_READY_PATH = os.path.join(BASE_DIR, "data", "weka_ready.csv")

# Tune this threshold to limit the number of columns in Weka.
MIN_ITEM_FREQUENCY = 50

# Read transactions (Items column is stored as a stringified list).
df = pd.read_csv(TRANSACTIONS_PATH)

df["Items"] = df["Items"].apply(ast.literal_eval)

# Normalize item text to reduce accidental duplicates.
df["Items"] = df["Items"].apply(lambda items: [str(i).strip() for i in items])

# Keep only items that appear often enough.
all_items = [item for items in df["Items"] for item in items]
counts = Counter(all_items)
common_items = {item for item, count in counts.items() if count > MIN_ITEM_FREQUENCY}

df["Items"] = df["Items"].apply(lambda items: [i for i in items if i in common_items])

# Drop empty transactions after filtering.
df = df[df["Items"].map(len) > 0]

# One-hot encode for Weka.
mlb = MultiLabelBinarizer()
encoded = mlb.fit_transform(df["Items"])

# Ensure unique column names for Weka.
def make_unique(names):
	seen = {}
	unique = []
	for name in names:
		base = str(name)
		if base not in seen:
			seen[base] = 1
			unique.append(base)
			continue
		seen[base] += 1
		unique.append(f"{base}__{seen[base]}")
	return unique

weka_df = pd.DataFrame(encoded, columns=make_unique(mlb.classes_))
weka_df.to_csv(WEKA_READY_PATH, index=False)

print("Weka-ready shape:", weka_df.shape)
print("Saved:", WEKA_READY_PATH)
