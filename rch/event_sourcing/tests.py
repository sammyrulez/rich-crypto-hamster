from django.dispatch import receiver
from django.test import TestCase
from event_sourcing import command_executed
from event_sourcing.tasks import store_event



@receiver(command_executed)
def flag_command( sender, **kwargs):
     sender.commandCalled = True

class SendCommandTest(TestCase):

    def setUp(self):
        self.commandCalled = False

    def test_send_command(self):
        command_executed.send(self,command="test",payload={'test':'value'})
        self.assertTrue(self.commandCalled)

class TaskTest(TestCase):

    def test_store_event(self):
        store_event("test",{'test':'value'})

