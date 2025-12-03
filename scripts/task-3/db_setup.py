# scripts/db_setup.py
import os
import psycopg2

DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB", "bank_reviews")
DB_USER = os.getenv("PG_USER", "review_user")
DB_PASS = os.getenv("PG_PASS", "review_pass")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS banks (
  bank_id SERIAL PRIMARY KEY,
  bank_name VARCHAR(200) UNIQUE NOT NULL,
  app_package VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id SERIAL PRIMARY KEY,
  bank_id INTEGER REFERENCES banks(bank_id) ON DELETE CASCADE,
  review_text TEXT NOT NULL,
  rating SMALLINT,
  review_date DATE,
  sentiment_label VARCHAR(32),
  sentiment_score FLOAT,
  theme VARCHAR(128),
  source VARCHAR(64),
  raw_id VARCHAR(255),
  ingestion_ts TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_reviews_bank_date ON reviews(bank_id, review_date);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label);
"""

DEFAULT_BANKS = [
    ("CBE", "com.cbe.mobilebanking"),
    ("BOA", "com.boa.boaMobileBanking"),
    ("Dashen", "com.dashen.mobilebanking")
]

def main():
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(SCHEMA_SQL)
    print("Schema created/verified.")
    for name, pkg in DEFAULT_BANKS:
        cur.execute("INSERT INTO banks (bank_name, app_package) VALUES (%s, %s) ON CONFLICT (bank_name) DO NOTHING;", (name, pkg))
    print("Banks ensured in table.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
