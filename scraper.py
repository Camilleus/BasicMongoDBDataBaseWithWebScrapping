import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    quotes_url = "/page/1"
    all_quotes = []

    while quotes_url:
        response = requests.get(base_url + quotes_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')

        for quote, author in zip(quotes, authors):
            quote_text = quote.get_text()
            author_name = author.get_text()

            all_quotes.append({"quote": quote_text, "author": author_name})

        next_button = soup.find('li', class_='next')
        quotes_url = next_button.a['href'] if next_button else None
        
    return all_quotes

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()