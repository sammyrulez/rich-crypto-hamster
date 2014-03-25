from django.dispatch import receiver
from django.test import TestCase
from pymongo import MongoClient
from event_sourcing import command_executed
from event_sourcing.mongodb_event_storage import SOURCED_EVENTS
from event_sourcing.tasks import store_event
from django.conf import settings


@receiver(command_executed)
def flag_command(sender, **kwargs):
    sender.commandCalled = True

class SendCommandTest(TestCase):

    def setUp(self):
        self.commandCalled = False

    def test_send_command(self):
        command_executed.send(self, command="test", payload={'test': 'value'})
        self.assertTrue(self.commandCalled)


class TaskTest(TestCase):

    def setUp(self):
        self.client = MongoClient(settings.EVENT_SOURCING_MONGODB_URL)
        self.db = self.client[settings.EVENT_SOURCING_MONGODB_DBNAME]
        self.collection = self.db[SOURCED_EVENTS]

    def tearDown(self):
        self.collection.remove({'test': 'value'})
        for e in self.collection.find():
            print 'still', e

    def test_store_event(self):
        store_event("test", {'test': 'value'})
        self.assertTrue(self.collection.find( {'test': 'value'}))
        self.assertEquals(1,self.collection.find( {'test': 'value'}).count())





