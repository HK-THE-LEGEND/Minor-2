from textblob import TextBlob

def process_news(news):
    if not isinstance(news, dict):
        print("Error: News data is not a dictionary:", news)
        return None

    summary = news.get("summary", "")  # Safely get the summary
    if not summary:
        print("Warning: No summary found in news data.")
        return None

    sentiment = TextBlob(summary).sentiment.polarity

    return {
        "title": news.get("title", "No Title"),
        "summary": summary,
        "sentiment": sentiment
    }
