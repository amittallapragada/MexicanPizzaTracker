from mongoengine import Document, StringField, ListField, DateTimeField, FloatField, IntField
from uuid import uuid4
from supported_restaurants import SUPPORTED_RESTAURANTS
import datetime

class Item(Document):
    id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    item_ids = ListField(StringField(), required=True)
    store = StringField(required = True, choices=SUPPORTED_RESTAURANTS.keys())
    icon = StringField(required = True)