from flask import Flask, render_template
from news_scraper import get_news
from news_processor import process_news

app = Flask(__name__)

@app.route('/')
def index():
    raw_news = get_news()
    
    if not raw_news:
        processed_news = []
    else:
        processed_news = [process_news(news) for news in raw_news if news]

    return render_template('index.html', news=processed_news)

if __name__ == '__main__':
    app.run(debug=True)
