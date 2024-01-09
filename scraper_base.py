from mongoengine import Document, StringField, connect, disconnect

class Quote(Document):
    quote = StringField(required=True)
    author = StringField(required=True)


class Author(Document):
    name = StringField(required=True)