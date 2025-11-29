# scraping.py
# This script scrapes Google Play reviews for Ethiopian banks and saves raw data to CSV.

from google_play_scraper import reviews, Sort
import pandas as pd
import time

# --- Step 1: Define the apps to scrape ---
# We map bank names to their Google Play package names
APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

all_reviews = []  # list to store all scraped reviews

# --- Step 2: Scrape reviews for each bank ---
for bank_name, package in APPS.items():
    print(f"Fetching reviews for {bank_name}...")

    # Fetch up to 500 reviews sorted by newest
    # reviews() returns a list of dicts containing review content, rating, date, etc.
    bank_reviews, _ = reviews(
        package,
        count=500,         # number of reviews to fetch
        sort=Sort.NEWEST,  # get the latest reviews first
        lang='en',         # optional: only English reviews
        country='ET'       # optional: Ethiopian region
    )

    # --- Step 3: Process each review and append to list ---
    for r in bank_reviews:
        all_reviews.append({
            "review": r['content'],      # review text
            "rating": r['score'],        # star rating 1-5
            "date": r['at'],             # datetime object
            "bank": bank_name,           # bank name
            "source": "google_play"      # source info
        })

    # Polite pause between requests to avoid rate limiting
    time.sleep(1)

# --- Step 4: Save raw data to CSV ---

import os

# Ensure data folder exists
os.makedirs("../data", exist_ok=True)
df_raw = pd.DataFrame(all_reviews)        # convert list of dicts to DataFrame
df_raw.to_csv("data/raw_reviews.csv", index=False)  # save to data folder
print(f"Saved {len(df_raw)} raw reviews to data/raw_reviews.csv")
