from django.dispatch import receiver
from django.test import TestCase
from pymongo import MongoClient
from event_sourcing import command_executed
from event_sourcing.mongodb_event_storage import SOURCED_EVENTS
from event_sourcing.tasks import store_event
from django.conf import settings
from bson.code import Code


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

    def test_map_reduce(self):
        store_event("withdraw", {'user': 'sam', 'amount': 10})
        store_event("withdraw", {'user': 'sam', 'amount': 5})
        store_event("deposit", {'user': 'sam', 'amount': 20})
        mapper_code = Code("""
               function () {
                    signed = this.payload.amount;
                    if(this.event == 'withdraw'){
                        signed = signed * -1;
                    }
                    emit(this.payload.user,signed);
               }
         """)
        reduce_code = Code("""
                function (key, values) {
                  var balance = 0;
                  for (var i = 0; i < values.length; i++) {
                    balance += values[i];
                  }
                  return balance;
                }
         """)
        result = self.collection.map_reduce(mapper_code, reduce_code, "balance_results")
        for k in result.find():
            print k


    def tearDown(self):
        self.collection.remove()
        for e in self.collection.find():
            print 'still', e

    def test_store_event(self):
        store_event("test", {'test': 'value'})
        self.assertTrue(self.collection.find({u'event': u'test'}))
        self.assertEquals(1, self.collection.find({'event': 'test'}).count())
