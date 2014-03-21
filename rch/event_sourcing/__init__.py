import django.dispatch
from django.dispatch import receiver
from event_sourcing import tasks

command_executed = django.dispatch.Signal(providing_args=["command", "payload"])


@receiver(command_executed)
def default_qcrs_callback(sender, **kwargs):
    tasks.store_event.delay(kwargs['command'],kwargs['payload'])
    print("Command: %s" % kwargs['command'])
    print("payload: %s" % kwargs['payload'])
    print("Store to event store")
    print("denormalize")





