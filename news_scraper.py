import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_rss_news(url):
    """Fetch news from RSS feeds"""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        news_list = []
        for item in items:
            title = item.title.text
            link = item.link.text
            news_list.append({'title': title, 'link': link})
        return news_list
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

def fetch_static_news(url):
    """Fetch news from static websites (non-JS)"""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('a')[:10]  # Adjust based on site structure
        news_list = []
        for article in articles:
            title = article.get_text(strip=True)
            link = article['href'] if 'http' in article['href'] else url + article['href']
            news_list.append({'title': title, 'link': link})
        return news_list
    except Exception as e:
        print(f"Error fetching static news: {e}")
        return []

def fetch_dynamic_news(url):
    """Fetch news from dynamic (JavaScript-rendered) websites"""
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--enable-unsafe-swiftshader')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        articles = soup.find_all('a')[:10]  # Adjust based on site structure
        news_list = []
        for article in articles:
            title = article.get_text(strip=True)
            link = article['href'] if 'http' in article['href'] else url + article['href']
            news_list.append({'title': title, 'link': link})
        return news_list
    except Exception as e:
        print(f"Error fetching dynamic news: {e}")
        return []

def get_news():
    """Fetch news from multiple sources"""
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
    
    return all_news

if __name__ == "__main__":
    news = get_news()
    for item in news:
        print(f"{item['title']}: {item['link']}")
