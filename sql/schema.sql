-- sql/schema.sql
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
