from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

def load_news():
    """Load news from JSON file"""
    try:
        with open('news_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    news = load_news()
    return render_template('index.html', news=news)

@app.route('/news')
def get_news():
    return jsonify(load_news())

if __name__ == "__main__":
    app.run(debug=True)
