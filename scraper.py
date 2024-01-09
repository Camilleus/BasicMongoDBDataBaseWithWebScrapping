import requests
from bs4 import BeautifulSoup
import json
from typing import List, Any
from mongoengine import Document, StringField, connect, disconnect
from scraper_base import Quote, Author

class QuoteScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def scrape_quotes(self, page: int) -> List[dict[str, Any]]:
        quotes_url = f"/page/{page}"
        all_quotes = []

        while quotes_url:
            response = requests.get(self.base_url + quotes_url)
            response.raise_for_status() 

            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('span', class_='text')
            authors = soup.find_all('small', class_='author')

            for quote, author in zip(quotes, authors):
                quote_text, author_name = quote.get_text(), author.get_text()

                all_quotes.append({"quote": quote_text, "author": author_name})

            next_button = soup.find('li', class_='next')
            quotes_url = next_button.a['href'] if next_button else None

        return all_quotes


class DataSaver:
    @staticmethod
    def save_to_json(data: List[dict[str, Any]], filename: str):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)


class DatabaseUploader:
    @staticmethod
    def upload_to_mongodb(data: List[dict[str, Any]], connection_uri: str):
        with connect(connection_uri):
            for quote_info in data:
                author_name = quote_info["author"]
                quote_text = quote_info["quote"]

                author = Author.objects(name=author_name).first()
                if not author:
                    author = Author(name=author_name)
                    author.save()

                quote = Quote(quote=quote_text, author=author_name)
                quote.save()


if __name__ == "__main__":
    base_url = "http://quotes.toscrape.com"
    scraper = QuoteScraper(base_url)

    try:
        quotes_data = scraper.scrape_quotes(page=1)
        DataSaver.save_to_json(quotes_data, 'quotes.json')
        authors_data = list(set(quote['author'] for quote in quotes_data))
        DataSaver.save_to_json(authors_data, 'authors.json')
        DatabaseUploader.upload_to_mongodb(quotes_data, "mongodb+srv://CamilleusRex:c47UaZGmGSlIR5PB@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority")
    except requests.RequestException as e:
        print(f"Error during request: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        disconnect()
