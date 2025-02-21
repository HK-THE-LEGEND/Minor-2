import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def fetch_rss_news(url):
    """Fetch news from RSS feeds and save to JSON"""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        return [{'title': item.title.text, 'link': item.link.text} for item in items]
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

def fetch_static_news(url):
    """Fetch news from static websites (non-JS)"""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('a')[:10]
        return [{'title': a.get_text(strip=True), 'link': a['href']} for a in articles if a.get_text(strip=True)]
    except Exception as e:
        print(f"Error fetching static news: {e}")
        return []

def fetch_dynamic_news(url):
    """Fetch news from dynamic (JavaScript-rendered) websites"""
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        articles = soup.find_all('a')[:10]
        return [{'title': a.get_text(strip=True), 'link': a['href']} for a in articles if a.get_text(strip=True)]
    except Exception as e:
        print(f"Error fetching dynamic news: {e}")
        return []

def scrape_news():
    """Fetch news from multiple sources and save to a JSON file"""
    sources = {
        'rss': ['https://news.google.com/rss'],
        'static': ['https://www.bbc.com/news', 'https://www.thehindu.com/'],
        'dynamic': ['https://www.ndtv.com/']
    }
    
    all_news = []
    for category, urls in sources.items():
        for url in urls:
            if category == 'rss':
                all_news.extend(fetch_rss_news(url))
            elif category == 'static':
                all_news.extend(fetch_static_news(url))
            elif category == 'dynamic':
                all_news.extend(fetch_dynamic_news(url))
    
    with open("news_data.json", "w", encoding="utf-8") as file:
        json.dump(all_news, file)
    print("News data saved!")

if __name__ == "__main__":
    scrape_news()
