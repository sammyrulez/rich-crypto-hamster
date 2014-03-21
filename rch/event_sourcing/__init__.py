import django.dispatch
from django.dispatch import receiver

command_executed = django.dispatch.Signal(providing_args=["command", "payload"])


@receiver(command_executed)
def default_qcrs_callback(sender, **kwargs):
    print("Store to event store")
    print("denormalize")
