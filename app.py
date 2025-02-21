from flask import Flask, render_template
from news_scraper import fetch_news
from news_processor import process_news

app = Flask(__name__)

@app.route('/')
def index():
    news = fetch_news()
    processed_news = process_news(news)
    return render_template('index.html', news=processed_news)

if __name__ == '__main__':
    app.run(debug=True)