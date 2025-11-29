# sentiment_analysis.py
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

# Create output folder if not exists
os.makedirs("data/processed", exist_ok=True)

# Load cleaned reviews from Task 1
df = pd.read_csv("data/clean_reviews.csv")

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.05:
        return 'Positive', score
    elif score <= -0.05:
        return 'Negative', score
    else:
        return 'Neutral', score

# Apply sentiment analysis
df['sentiment_label'], df['sentiment_score'] = zip(*df['review'].map(get_sentiment))

# Save intermediate CSV for thematic analysis
df.to_csv("data/processed/reviews_sentiment.csv", index=False)

print(f"Sentiment analysis complete. Processed {len(df)} reviews.")
print(df.head())
