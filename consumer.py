import pika
import json
import logging
from mongoengine import connect
from models import Contact, Quote, Author
import redis
import re
from search_quotes import search_quotes, SearchContext, NameSearch, TagSearch, TagsSearch

class QueueHandler:
    def __init__(self, connection_params, queue_name, callback_function):
        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.callback_function = callback_function

    def start_consuming(self):
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback_function, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()

def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.fullname} at {contact.email}")
    contact.sent_email = True
    contact.save()

def handle_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        contact_id = message.get("contact_id")
        if contact_id:
            send_email(contact_id)
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        logging.exception("Exception details:")

if __name__ == "__main__":
    rabbitmq_connection_params = pika.ConnectionParameters('localhost')
    queue_handler = QueueHandler(rabbitmq_connection_params, 'contacts_queue', handle_message)

    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    with connect("mongodb+srv://CamilleusRex:c47UaZGmGSlIR5PB@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):
        try:
            queue_handler.start_consuming()
        except KeyboardInterrupt:
            pass
        finally:
            queue_handler.close_connection()
