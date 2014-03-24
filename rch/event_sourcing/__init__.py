import django.dispatch
from django.dispatch import receiver

command_executed = django.dispatch.Signal(providing_args=["command", "payload"])

event_stored = django.dispatch.Signal(providing_args=["command", "payload"])

event_stored_fail = django.dispatch.Signal(providing_args=["command", "payload"])

@receiver(command_executed)
def event_sourcing_callback(sender, **kwargs):
    from event_sourcing import tasks
    tasks.store_event.delay(kwargs['command'],kwargs['payload'])
    print("Command: %s" % kwargs['command'])
    print("payload: %s" % kwargs['payload'])
    print("Store to event store")
    print("denormalize")


class EventStorage(object):

    def store_event(self,event_data):
        raise NotImplemented()





