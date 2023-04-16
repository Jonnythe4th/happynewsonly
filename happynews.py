import requests
from textblob import TextBlob
from operator import itemgetter

API_KEY = 'bbe04740bd0d4f44b7b766f825d059d3'
POLITICAL_KEYWORDS = ['politics', 'government', 'election', 'senate', 'congress', 'president', 'Ukraine', 'Biden', "Trump"]

def is_political(title, description):
    text = f"{title} {description}"
    text = text.lower()

    for keyword in POLITICAL_KEYWORDS:
        if keyword in text:
            return True

    return False

def get_happy_news():
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json()['articles']
        articles_with_sentiment = []

        for article in articles:
            if not is_political(article['title'], article['description']):
                sentiment = TextBlob(article['title']).sentiment.polarity
                if sentiment > 0:
                    articles_with_sentiment.append({
                        'title': article['title'],
                        'summary': article['description'],
                        'sentiment': sentiment
                    })

        top_five_happy_articles = sorted(articles_with_sentiment, key=itemgetter('sentiment'), reverse=True)[:5]

        for article in top_five_happy_articles:
            print(f"Title: {article['title']}")
            print(f"Summary: {article['summary']}")
            print('-' * 80)

if __name__ == "__main__":
    get_happy_news()