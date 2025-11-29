# preprocess.py
# This script cleans the raw reviews for analysis:
# removes empty reviews, duplicates, normalizes dates, and saves a clean CSV.

import pandas as pd
from dateutil import parser

# --- Step 1: Load raw reviews ---
df = pd.read_csv("../data/raw_reviews.csv")
print(f"Loaded {len(df)} raw reviews")

# --- Step 2: Remove empty reviews ---
# Some reviews may be blank or just whitespace
df['review'] = df['review'].astype(str).str.strip()   # strip leading/trailing spaces
df = df[df['review'].str.len() > 0]                  # keep only non-empty reviews

# --- Step 3: Normalize dates to YYYY-MM-DD ---
# Convert any datetime object or string to ISO date format
df['date'] = df['date'].apply(lambda x: parser.parse(str(x)).date().isoformat())

# --- Step 4: Remove duplicates ---
# Avoid counting the same review more than once
df.drop_duplicates(subset=['review', 'bank'], inplace=True)

# --- Step 5: Save cleaned reviews ---
df.to_csv("data/clean_reviews.csv", index=False)
print(f"Saved {len(df)} cleaned reviews to data/clean_reviews.csv")

# --- Step 6: Optional validation ---
print("Reviews per bank:")
print(df['bank'].value_counts())
missing_frac = df.isnull().sum().sum() / (df.shape[0]*df.shape[1])
print(f"Fraction of missing data: {missing_frac:.2%}")
