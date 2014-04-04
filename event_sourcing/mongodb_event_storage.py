from django.conf import settings
from event_sourcing import EventStorage, event_stored
from pymongo import MongoClient

SOURCED_EVENTS = 'sourced_events'


class MongoDbEventStorage(EventStorage):
    def __init__(self):
        self.client = MongoClient(settings.EVENT_SOURCING_MONGODB_URL)
        self.db = self.client[settings.EVENT_SOURCING_MONGODB_DBNAME]
        self.collection = self.db[SOURCED_EVENTS]

    def store_event(self, event_data):
        self.collection.insert(event_data)
        event_stored.send(self,event_data=event_data)


event_storage = MongoDbEventStorage()
