from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect
from models import Author, Quote
import json


def read_data_from_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def save_authors_and_quotes(authors_data, quotes_data):
    for author_data in authors_data:
        author = Author(**author_data)
        author.save()

    for quote_data in quotes_data:
        author_fullname = quote_data["author"]
        author = Author.objects(fullname=author_fullname).first()
        quote_data["author"] = author
        quote = Quote(**quote_data)
        quote.save()


def main():
    uri = "mongodb+srv://CamilleusRex:c47UaZGmGSlIR5PB@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"
    
    with connect(uri):
        authors_data = read_data_from_json("authors.json")
        quotes_data = read_data_from_json("quotes.json")
        
        save_authors_and_quotes(authors_data, quotes_data)


if __name__ == "__main__":
    main()
