import pika
import json
from mongoengine import connect
from models import Contact

def handle_email_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        contact_id = message.get("contact_id")
        if contact_id:
            with connect("mongodb+srv://CamilleusRex:c47UaZGmGSlIR5PB@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):
                contact = Contact.objects.get(id=contact_id)
                send_email(contact)
                mark_email_as_sent(contact)
    except Exception as e:
        print(f"Error processing email message: {e}")

def send_email(contact):
    # here goes the logic
    print(f"Sending email to {contact.fullname} at {contact.email}")

def mark_email_as_sent(contact):
    contact.sent_email = True
    contact.save()

if __name__ == "__main__":
    try:
        with connect("mongodb+srv://CamilleusRex:c47UaZGmGSlIR5PB@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='email_queue')

            channel.basic_consume(queue='email_queue', on_message_callback=handle_email_message, auto_ack=True)
            print(' [*] Waiting for email messages. To exit press CTRL+C')
            channel.start_consuming()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        connection.close()