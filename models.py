from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, BooleanField, ValidationError
import re

class CleanMixin:
    def clean(self):
        raise NotImplementedError("Clean method must be implemented in subclasses.")

class Author(Document, CleanMixin):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

    def clean(self):
        super().clean()
        if self.born_date and self.born_date > datetime.utcnow():
            raise ValidationError("Born date cannot be in the future.")

class Quote(Document, CleanMixin):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

class Contact(Document, CleanMixin):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent_email = BooleanField(default=False)
    phone_number = StringField()
    preferred_method = StringField(choices=["email", "sms"])

    meta = {
        'indexes': [
            {'fields': ['email'], 'unique': True},
        ],
    }

    def clean(self):
        super().clean()
        if self.phone_number and not re.match(r'^\+\d{1,3}-\d{1,14}$', self.phone_number):
            raise ValidationError("Invalid phone number format.")
