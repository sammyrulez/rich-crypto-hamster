import django.dispatch
from django.dispatch import receiver

command_executed = django.dispatch.Signal(providing_args=["command", "payload"])

event_stored = django.dispatch.Signal(providing_args=["command", "payload"])

event_stored_fail = django.dispatch.Signal(providing_args=["command", "payload"])


@receiver(command_executed)
def event_sourcing_callback(sender, **kwargs):
    from event_sourcing import tasks
    tasks.store_event.delay(kwargs['command'], kwargs['payload'])
    print("event_sourcing_callback Command: %s" % kwargs['command'])
    print("event_sourcing_callback payload: %s" % kwargs['payload'])


class EventStorage(object):

    def store_event(self, event_data):
        raise NotImplemented()
