# scripts/task-3/load_reviews.py
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# ---------------- paths ----------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CANDIDATES = [
    os.path.join(ROOT, "data", "processed", "reviews_themes.csv"),
    os.path.join(ROOT, "data", "processed", "reviews_analysis.csv"),
    os.path.join(ROOT, "data", "processed", "reviews_sentiment.csv"),
    os.path.join(ROOT, "data", "clean", "clean_reviews.csv"),
    os.path.join(ROOT, "data", "raw_reviews.csv"),
]

CSV_PATH = None
for p in CANDIDATES:
    if os.path.exists(p):
        CSV_PATH = p
        break

if CSV_PATH is None:
    raise SystemExit("No input CSV found. Please run Task1/Task2 to generate data (checked processed/ and data/).")

print("Using CSV:", CSV_PATH)

# ---------------- DB config (env or defaults) ----------------
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB", "bank_reviews")
DB_USER = os.getenv("PG_USER", "review_user")
DB_PASS = os.getenv("PG_PASS", "review_pass")

# ---------------- load and normalize dataframe ----------------
df = pd.read_csv(CSV_PATH)
print("Loaded rows:", len(df))
print("Columns:", list(df.columns))

# Normalize column names: prefer 'review' then 'review_text'
if "review_text" in df.columns and "review" not in df.columns:
    df.rename(columns={"review_text": "review"}, inplace=True)

# Ensure required columns exist (fill missing with None)
for col in ["review", "rating", "date", "bank", "source", "sentiment_label", "sentiment_score", "theme"]:
    if col not in df.columns:
        df[col] = None

# If rating column exists but not integer, coerce
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").astype("Int64")

# Optionally shorten very long review_texts (not required)
# df["review"] = df["review"].astype(str).str.slice(0, 10000)

# ---------------- DB insertion ----------------
def load_dataframe_to_db(df, conn):
    with conn.cursor() as cur:
        # fetch existing banks
        cur.execute("SELECT bank_id, bank_name FROM banks;")
        rows = cur.fetchall()
        bank_map = {r[1]: r[0] for r in rows}

    records = []
    missing_banks = set()
    for _, r in df.iterrows():
        bank_name = r.get("bank") if pd.notna(r.get("bank")) else None
        if bank_name is None:
            # optional: skip rows without bank
            continue
        if bank_name not in bank_map:
            missing_banks.add(bank_name)
            # create bank entry
            with conn.cursor() as cur:
                cur.execute("INSERT INTO banks (bank_name) VALUES (%s) RETURNING bank_id;", (bank_name,))
                bank_id = cur.fetchone()[0]
                conn.commit()
                bank_map[bank_name] = bank_id
        bank_id = bank_map.get(bank_name)
        review_text = str(r.get("review")) if pd.notna(r.get("review")) else ""
        rating = int(r["rating"]) if pd.notna(r.get("rating")) else None
        review_date = r.get("date") if pd.notna(r.get("date")) else None
        sentiment_label = r.get("sentiment_label") if pd.notna(r.get("sentiment_label")) else None
        sentiment_score = float(r.get("sentiment_score")) if pd.notna(r.get("sentiment_score")) else None
        theme = r.get("theme") if pd.notna(r.get("theme")) else None
        source = r.get("source") if pd.notna(r.get("source")) else "google_play"
        # tuple order matches INSERT columns below
        records.append((bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, theme, source, None))

    if not records:
        print("No valid records to insert.")
        return 0

    with conn.cursor() as cur:
        sql = """
        INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, theme, source, raw_id)
        VALUES %s
        """
        execute_values(cur, sql, records, page_size=1000)
        conn.commit()

    return len(records)

def main():
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    try:
        inserted = load_dataframe_to_db(df, conn)
        print(f"Inserted {inserted} records.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
