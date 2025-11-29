# thematic_analysis.py
import pandas as pd
import spacy
import os

# Load sentiment-analyzed CSV
df = pd.read_csv("data/processed/reviews_sentiment.csv")

# Load small English model
nlp = spacy.load("en_core_web_sm")

# Preprocessing function
def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

df['clean_text'] = df['review'].map(preprocess)

# Simple rule-based theme assignment
def assign_theme(text):
    if any(word in text for word in ["login", "password", "forgot"]):
        return "Account Access Issues"
    elif any(word in text for word in ["slow", "crash", "lag"]):
        return "Transaction Performance"
    elif any(word in text for word in ["ui", "design", "navigation", "interface"]):
        return "User Interface & Experience"
    elif any(word in text for word in ["support", "help", "response"]):
        return "Customer Support"
    elif any(word in text for word in ["feature", "fingerprint", "notifications"]):
        return "Feature Requests"
    else:
        return "Other"

df['theme'] = df['clean_text'].map(assign_theme)

# Save final processed CSV
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/reviews_analysis.csv", index=False)

print(f"Thematic analysis complete. Themes assigned to {len(df)} reviews.")
print(df[['review', 'sentiment_label', 'theme']].head())
