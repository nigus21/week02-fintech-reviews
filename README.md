# 📘 **Fintech Reviews – Data Scraping & Analysis**

**Week 02 – FAST TRACK CODE Program**

This project focuses on collecting user-generated reviews from Google Play and performing **sentiment analysis**, **theme extraction**, and **preliminary insights** for Ethiopian banking applications.
The workflow includes:

* Web scraping
* Data cleaning
* Sentiment analysis
* Thematic analysis
* Preparing outputs for the final report

---

## 🧩 **Project Structure**

```
week02-fintech-reviews/
│
├── data/
│   ├── raw_reviews.csv
│   ├── sentiment_output.csv
│   ├── thematic_output.csv
│
├── scripts/
│   ├── scrape_reviews.py
│   ├── sentiment_analysis.py
│   ├── thematic_analysis.py
│
└── README.md
```

---

# 📝 **Task 1 – Web Scraping**

### ✔ Goal

Scrape **user reviews**, **ratings**, **dates**, and **app source** from Google Play for selected Ethiopian banking apps.

### ✔ Tools Used

* `requests`
* `BeautifulSoup`
* `pandas`
* `time`

### ✔ Output

* **raw_reviews.csv** containing:
  | review | rating | date | bank | source |

### ✔ How to Run Scraper

```bash
python scripts/scrape_reviews.py
```

---

# 🧪 **Task 2 – Sentiment Analysis**

### ✔ Goal

Classify each review as **Positive**, **Neutral**, or **Negative** and generate a sentiment score.

### ✔ Tools Used

* `NLTK` + `VADER SentimentIntensityAnalyzer`
* `pandas`

### ✔ Output

* `sentiment_output.csv`

### ✔ Run Command

```bash
python scripts/sentiment_analysis.py
```

### ✔ Example Output

| review                      | sentiment_label | sentiment_score |
| --------------------------- | --------------- | --------------- |
| "good app"                  | Positive        | 0.44            |
| "why didn’t work this app?" | Neutral         | 0.00            |

---

# 🧵 **Task 3 – Thematic Analysis**

### ✔ Goal

Automatically classify reviews into broad themes such as:

* **UX/UI**
* **Performance Issues**
* **Login/Access Problems**
* **Customer Service**
* **New Feature Requests**
* **Other**

### ✔ Tools Used

* **spaCy** (keyword matching)
* `pandas`

### ✔ Output

* `thematic_output.csv`

### ✔ How to Run

```bash
python scripts/thematic_analysis.py
```

---

# 📊 **Early Insights (Interim Report Highlights)**

✔ Total reviews processed: **1267**
✔ Most common sentiment: **Positive**
✔ Many reviews fall into the **Other** category because users mix different languages (Afaan Oromo, Amharic, English).
✔ Future improvement: multilingual models (e.g., XLM-RoBERTa)

---

# 🚀 **Next Steps**

* Improve automatic theme detection
* Add visualizations (bar charts, word clouds)
* Clean multilingual reviews
* Prepare the final 4-page PDF report

