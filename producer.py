import pika
import json
import faker
from mongoengine import connect
from models import Contact
import redis


def generate_fake_contacts(num_contacts):
    fake = faker.Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = {
            "fullname": fake.name(),
            "email": fake.email(),
            "sent_email": False,
            "phone_number": fake.phone_number(),
            "preferred_method": fake.random_element(["email", "sms"]),
            "tags": [fake.word(), fake.word()]  # Przykładowe dodanie pola "tags"
        }
        contacts.append(contact)
    return contacts


def send_contacts_to_queue(contacts, channel, redis_client):
    for contact in contacts:
        contact_doc = Contact(**contact)
        contact_doc.save()


        message = {"contact_id": str(contact_doc.id)}
        channel.basic_publish(exchange='', routing_key='contacts_queue', body=json.dumps(message))


        name_key = f"name:{contact['fullname']}"
        if not redis_client.get(name_key):
            redis_client.setex(name_key, 300, json.dumps(contact))


        for tag in contact['tags']:
            tag_key = f"tag:{tag}"
            if not redis_client.get(tag_key):
                redis_client.setex(tag_key, 300, json.dumps(contact))


if __name__ == "__main__":
    try:
        with connect("mongodb+srv://CamilleusRex:c47UaZGmGSlIR5PB@pythonmongodbv1cluster0.na7ldv4.mongodb.net/?retryWrites=true&w=majority"):
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()


            channel.queue_declare(queue='contacts_queue')


            fake_contacts = generate_fake_contacts(10)


            redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
            send_contacts_to_queue(fake_contacts, channel, redis_client)
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    finally:
        connection.close()
