from textblob import TextBlob

def process_news(news_list):
    processed = []
    
    for news in news_list:
        sentiment = TextBlob(news["summary"]).sentiment.polarity
        category = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        
        processed.append({
            "title": news["title"],
            "link": news["link"],
            "summary": news["summary"],
            "category": category
        })
    
    return processed
