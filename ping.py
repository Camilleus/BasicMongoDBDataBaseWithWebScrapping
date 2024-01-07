from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ServerSelectionTimeoutError
from abc import ABC, abstractmethod

class DatabaseConnector(ABC):
    @abstractmethod
    def ping_server(self):
        pass

class MongoDBConnector(DatabaseConnector):
    def __init__(self, uri):
        self.client = MongoClient(uri, server_api=ServerApi('1'))

    def ping_server(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except ServerSelectionTimeoutError:
            print("Connection timed out. Unable to connect to MongoDB.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    uri = "mongodb+srv://CamilleusRex:c47UaZGmGSlIR5PB@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"
    connector = MongoDBConnector(uri)
    connector.ping_server()
