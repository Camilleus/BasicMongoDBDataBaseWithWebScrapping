# consumer_sms.py

import pika
import json
from mongoengine import connect
from models import Contact

def handle_sms_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        contact_id = message.get("contact_id")
        if contact_id:
            pass
    except Exception as e:
        print(f"Error processing SMS message: {e}")

if __name__ == "__main__":
    try:
        with connect("mongodb+srv://CamilleusRex:c47UaZGmGSlIR5PB@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='sms_queue')

            channel.basic_consume(queue='sms_queue', on_message_callback=handle_sms_message, auto_ack=True)
            print(' [*] Waiting for SMS messages. To exit press CTRL+C')
            channel.start_consuming()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        connection.close()
